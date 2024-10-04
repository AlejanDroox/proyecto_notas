USE notas;
-- Insertar datos de prueba en la tabla 'usuarios'
INSERT INTO usuarios (nombre_usuario, contrasena, correo) 
VALUES 
('brayan', 'amomimoto', 'brayn@xd.com'),
('ronald', 'pato_ronald', 'ronald@xd.com');

-- Insertar datos de prueba en la tabla 'categorias'
INSERT INTO categorias (nombre_categoria)
VALUES 
('Personal'),
('universidad');

-- Insertar datos de prueba en la tabla 'notas'
INSERT INTO notas (id_usuario, titulo, contenido, fecha_creacion, fecha_actualizacion)
VALUES 
(1, 'Briandar', 'brindar unas empanadas al grupo', NOW(), NOW()),
(2, 'proyecto api', 'Ayudar a Daniel', NOW(), NOW());

-- Relacionar notas con categorías en la tabla 'nota_categoria'
INSERT INTO nota_categoria (id_nota, id_categoria)
VALUES 
(1, 1), -- La primera nota está relacionada con la categoría 'Personal'
(2, 2); -- La segunda nota está relacionada con la categoría 'Trabajo'
