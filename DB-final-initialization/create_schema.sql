-- Script de creación del esquema de base de datos para Fredys Food
-- Ejecutar antes de usar main.py para generar datos

-- Crear la base de datos (ejecutar como superusuario)
-- CREATE DATABASE final_project;

-- Usar la base de datos final_project
-- \c final_project;

-- Eliminar tablas si existen (en orden inverso de dependencias)
DROP TABLE IF EXISTS Cubre CASCADE;
DROP TABLE IF EXISTS Vive CASCADE;
DROP TABLE IF EXISTS Hace CASCADE;
DROP TABLE IF EXISTS Tiene CASCADE;
DROP TABLE IF EXISTS Pedido CASCADE;
DROP TABLE IF EXISTS ZonaEntrega CASCADE;
DROP TABLE IF EXISTS Pertenece CASCADE;
DROP TABLE IF EXISTS Plato CASCADE;
DROP TABLE IF EXISTS Menu CASCADE;
DROP TABLE IF EXISTS Administrador CASCADE;
DROP TABLE IF EXISTS Repartidor CASCADE;
DROP TABLE IF EXISTS Trabajador CASCADE;
DROP TABLE IF EXISTS Cliente CASCADE;
DROP TABLE IF EXISTS Usuario CASCADE;

-- Crear tablas en orden de dependencias

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    apellido VARCHAR(25) NOT NULL,
    numero_telef VARCHAR(30) NOT NULL
);

CREATE TABLE Cliente (
    id_usuario INTEGER PRIMARY KEY,
    empresa VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Trabajador (
    id_usuario INTEGER PRIMARY KEY,
    nro_telef_emergencia VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Repartidor (
    id_usuario INTEGER PRIMARY KEY,
    FOREIGN KEY (id_usuario) REFERENCES Trabajador(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Administrador (
    id_usuario INTEGER PRIMARY KEY,
    correo VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Trabajador(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Menu (
    id_menu SERIAL PRIMARY KEY,
    id_administrador INTEGER NOT NULL,
    variacion VARCHAR(50),
    fecha DATE NOT NULL,
    FOREIGN KEY (id_administrador) REFERENCES Administrador(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Plato (
    id_plato SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    foto VARCHAR(200),
    tipo VARCHAR(30),
    categoria VARCHAR(30),
    codigo_info_nutricional VARCHAR(36) NOT NULL,
    precio DECIMAL(10,2) DEFAULT 15.99
);

CREATE TABLE Pertenece (
    id_menu INTEGER,
    id_plato INTEGER,
    PRIMARY KEY (id_menu, id_plato),
    FOREIGN KEY (id_menu) REFERENCES Menu(id_menu) ON DELETE CASCADE,
    FOREIGN KEY (id_plato) REFERENCES Plato(id_plato) ON DELETE CASCADE
);

CREATE TABLE ZonaEntrega (
    nombre VARCHAR(50) PRIMARY KEY,
    costo DECIMAL(5,2) NOT NULL
);

CREATE TABLE Pedido (
    id_pedido SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('Pendiente', 'En preparación', 'En reparto', 'Entregado', 'Cancelado')),
    hora_salida TIME,
    hora_entrega TIME,
    hora_entrega_estimada TIME,
    direccion_exacta VARCHAR(200) NOT NULL,
    zona_entrega VARCHAR(50) NOT NULL,
    FOREIGN KEY (zona_entrega) REFERENCES ZonaEntrega(nombre) ON DELETE CASCADE
);

CREATE TABLE Tiene (
    id_pedido INTEGER,
    id_menu INTEGER,
    PRIMARY KEY (id_pedido, id_menu),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_menu) REFERENCES Menu(id_menu) ON DELETE CASCADE
);

CREATE TABLE Hace (
    id_pedido INTEGER,
    id_usuario INTEGER,
    calificacion INTEGER CHECK (calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    PRIMARY KEY (id_pedido, id_usuario),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Vive (
    zona_entrega VARCHAR(50),
    id_usuario INTEGER,
    PRIMARY KEY (zona_entrega, id_usuario),
    FOREIGN KEY (zona_entrega) REFERENCES ZonaEntrega(nombre) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE Cubre (
    zona_entrega VARCHAR(50),
    id_usuario INTEGER,
    PRIMARY KEY (zona_entrega, id_usuario),
    FOREIGN KEY (zona_entrega) REFERENCES ZonaEntrega(nombre) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Repartidor(id_usuario) ON DELETE CASCADE
);

-- Crear índices básicos para mejorar el rendimiento general
CREATE INDEX idx_pedido_fecha ON Pedido(fecha);
CREATE INDEX idx_pedido_estado ON Pedido(estado);
CREATE INDEX idx_usuario_nombre ON Usuario(nombre, apellido);

-- Mensaje de confirmación
SELECT 'Esquema creado exitosamente' as status;
