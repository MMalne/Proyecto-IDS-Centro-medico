CREATE DATABASE IF NOT EXISTS salud_integral;
USE salud_integral;

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(50)
);

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE turnos (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    id_medico INT NOT NULL,
    id_paciente INT DEFAULT NULL,
    fecha_hora DATETIME NOT NULL,
    estado ENUM('disponible', 'reservado', 'confirmado', 'atendido', 'cancelado', 'ausente') DEFAULT 'disponible',
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE SET NULL
);