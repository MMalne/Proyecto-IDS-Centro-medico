INSERT INTO pacientes (nombre, apellido, dni, email, telefono) VALUES
('Juan', 'Pérez', '30123456', 'juan.perez@email.com', '1122334455'),
('María', 'Gómez', '31987654', 'maria.gomez@email.com', '1155667788'),
('Carlos', 'López', '29456789', 'carlos.lopez@email.com', '1199887766');

INSERT INTO medicos (nombre, apellido, especialidad, matricula, email) VALUES
('Ana', 'Martínez', 'Clínica Médica', 'MN112233', 'ana.martinez@saludintegral.com'),
('Luis', 'Fernández', 'Cardiología', 'MN445566', 'luis.fernandez@saludintegral.com'),
('Laura', 'Díaz', 'Pediatría', 'MN778899', 'laura.diaz@saludintegral.com');

INSERT INTO turnos (id_medico, id_paciente, fecha_hora, estado) VALUES
(1, NULL, '2026-11-10 09:00:00', 'disponible'),
(1, 1, '2026-11-10 09:30:00', 'reservado'),
(1, NULL, '2026-11-10 10:00:00', 'disponible'),
(2, 2, '2026-11-11 14:00:00', 'reservado'),
(2, NULL, '2026-11-11 14:30:00', 'disponible'),
(3, 3, '2026-11-12 10:00:00', 'reservado');