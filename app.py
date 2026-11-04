from flask import Flask, request, jsonify
import mysql.connector
import qrcode
import io
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Configuración de BD
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'salud_integral'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def generar_y_enviar_qr(email_paciente, id_turno, fecha_hora, medico_nombre):
    # Generar QR con los datos del turno
    qr_data = f"Turno ID: {id_turno} | Fecha: {fecha_hora} | Médico: {medico_nombre}"
    qr = qrcode.make(qr_data)
    
    # Aquí iría la lógica SMTP para enviar el correo con la imagen adjunta
    # y el botón/link de cancelación (ej: /api/turnos/cancelar/{id_turno})[cite: 1]
    print(f"Enviando QR al mail {email_paciente} con botón de cancelar...")

@app.route('/api/turnos/reservar', methods=['POST'])
def reservar_turno():
    data = request.get_json()
    id_turno = data.get('id_turno')
    id_paciente = data.get('id_paciente')
    
    if not id_turno or not id_paciente:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Obtener información del turno solicitado
        cursor.execute("SELECT id_medico, fecha_hora, estado FROM turnos WHERE id_turno = %s", (id_turno,))
        turno = cursor.fetchone()
        
        if not turno:
            return jsonify({"error": "Turno no encontrado"}), 404
        if turno['estado'] != 'disponible':
            return jsonify({"error": "El turno ya no está disponible"}), 409

        id_medico = turno['id_medico']
        fecha_hora_solicitada = turno['fecha_hora']

        # 2. Validación de negocio: Un paciente no puede tener dos turnos activos simultáneos con el mismo médico[cite: 1]
        query_simultaneos = """
            SELECT COUNT(*) AS turnos_activos 
            FROM turnos 
            WHERE id_paciente = %s 
              AND id_medico = %s 
              AND estado IN ('reservado', 'confirmado')
        """
        cursor.execute(query_simultaneos, (id_paciente, id_medico))
        activos = cursor.fetchone()['turnos_activos']
        
        if activos > 0:
            return jsonify({"error": "El paciente ya tiene un turno activo con este médico"}), 403

        # 3. Validación de negocio: Evitar superposición del médico[cite: 1]
        # Si las agendas se generan previamente (como en el script de carga), un 'id_turno' es único por franja.
        # Pero por seguridad, verificamos que el médico no tenga ya un turno reservado o confirmado en ese datetime.
        query_superposicion = """
            SELECT COUNT(*) AS superposiciones
            FROM turnos
            WHERE id_medico = %s
              AND fecha_hora = %s
              AND estado IN ('reservado', 'confirmado', 'atendido')
        """
        cursor.execute(query_superposicion, (id_medico, fecha_hora_solicitada))
        superposiciones = cursor.fetchone()['superposiciones']

        if superposiciones > 0:
            return jsonify({"error": "El médico ya tiene un turno asignado en este horario"}), 409

        # 4. Actualizar el estado del turno (SQL explícito, sin ORM)
        query_update = """
            UPDATE turnos 
            SET id_paciente = %s, estado = 'reservado' 
            WHERE id_turno = %s
        """
        cursor.execute(query_update, (id_paciente, id_turno))
        
        # 5. Obtener datos para el mail
        cursor.execute("SELECT email FROM pacientes WHERE id_paciente = %s", (id_paciente,))
        email_paciente = cursor.fetchone()['email']
        cursor.execute("SELECT nombre, apellido FROM medicos WHERE id_medico = %s", (id_medico,))
        medico = cursor.fetchone()
        nombre_medico = f"{medico['nombre']} {medico['apellido']}"
        
        conn.commit()

        # 6. Generar QR y enviar mail[cite: 1]
        generar_y_enviar_qr(email_paciente, id_turno, fecha_hora_solicitada, nombre_medico)

        return jsonify({"mensaje": "Turno reservado con éxito", "id_turno": id_turno}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)