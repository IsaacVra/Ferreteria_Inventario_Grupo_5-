-- ============================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- ============================================

USE ferreteria_db;

-- Insertar tipos de usuario
INSERT INTO TIPO_USUARIO (nombre_tipo, descripcion) VALUES
('Administrador', 'Acceso completo al sistema'),
('Gerente', 'Gestión general y reportes'),
('Jefe de Bodega', 'Control de inventario'),
('Comprador', 'Gestión de compras a proveedores'),
('Vendedor', 'Registro de ventas');

-- Insertar usuarios (contraseñas hasheadas con SHA256)
-- admin123 = 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
-- gerente123 = 698d51a19d8a121ce581499d7b701668d1794452d991f059878abcc4b6e0cda7
-- bodega123 = 5a0b7f8f5f6c9b1e8c3d2a6f7e9b2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0
-- ventas123 = 7c222fb2927d828af22f592134e8932480637c0d496e540a745c6e8e0b5fcf2f3

INSERT INTO USUARIO (cedula, nombres, apellidos, usuario_login, clave_hash, email, telefono, id_tipo_usuario) VALUES
('1712345678', 'Kenny', 'Chung Velastegui', 'kenny.admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'kenny@ferreteria.com', '09987654321', 1),
('1723456789', 'Isaac', 'Kalef Vera Villalba', 'isaac.manager', '698d51a19d8a121ce581499d7b701668d1794452d991f059878abcc4b6e0cda7', 'isaac@ferreteria.com', '09987654322', 2),
('1734567890', 'Valeria', 'Mero Zambrano', 'valeria.jefe', '5a0b7f8f5f6c9b1e8c3d2a6f7e9b2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0', 'valeria@ferreteria.com', '09987654323', 3),
('1745678901', 'Ana', 'Vendedor', 'ana.vendedor', '7c222fb2927d828af22f592134e8932480637c0d496e540a745c6e8e0b5fcf2f3', 'ana@ferreteria.com', '09987654324', 5);

-- Insertar categorías
INSERT INTO CATEGORIA (nombre_categoria, descripcion) VALUES
('Herramientas Manuales', 'Herramientas manuales para construcción y reparación'),
('Herramientas Eléctricas', 'Herramientas eléctricas y accesorios'),
('Material Eléctrico', 'Cables, interruptores y accesorios eléctricos'),
('Pinturas y Acabados', 'Pinturas, brochas y materiales de acabado'),
('Fontanería', 'Tuberías, grifería y accesorios de fontanería'),
('Construcción', 'Cementos, bloques y materiales de construcción'),
('Fijaciones', 'Tornillos, clavos y elementos de fijación'),
('Seguridad', 'Equipos de protección personal y seguridad');

-- Insertar proveedores
INSERT INTO PROVEEDOR (nombre_comercial, ruc, telefono, email, direccion) VALUES
('Distribuidora Nacional S.A.', '1790012345001', '022345678', 'contacto@distnacional.com', 'Av. Amazonas N45-123'),
('Herramientas del Ecuador', '1790023456002', '023456789', 'ventas@herramientas.ec', 'Calles 10 de Agosto y Venezuela'),
('Materiales de Construcción Cía. Ltda.', '1790034567003', '024567890', 'info@matconst.com', 'Av. Eloy Alfaro N12-34'),
('Electric Supply S.A.', '1790045678004', '025678901', 'sales@electricsupply.com', 'Av. 6 de Diciembre N34-56'),
('Pinturas Premium', '1790056789005', '026789012', 'contacto@pinturaspremium.com', 'Av. La Gasca N23-45');

-- Insertar productos
INSERT INTO PRODUCTO (codigo_producto, nombre_producto, descripcion, precio_compra_ref, precio_venta, stock_actual, stock_minimo, unidad_medida, id_categoria, id_proveedor) VALUES
('HM001', 'Martillo de Carpintero', 'Martillo de 16oz con mango de madera', 8.50, 12.75, 25, 10, 'UNIDAD', 1, 2),
('HM002', 'Juego de Destornilladores', 'Set de 6 destornilladores Phillips y plano', 15.00, 22.50, 15, 8, 'JUEGO', 1, 2),
('HM003', 'Llave Inglesa Adjustable', 'Llave inglesa 8-12mm', 12.00, 18.00, 20, 5, 'UNIDAD', 1, 2),
('HE001', 'Taladro Eléctrico 550W', 'Taladro con cable y velocidad variable', 45.00, 67.50, 8, 3, 'UNIDAD', 2, 1),
('HE002', 'Sierra Circular 7-1/4"', 'Sierra circular con disco incluido', 85.00, 127.50, 5, 2, 'UNIDAD', 2, 1),
('ME001', 'Cable Eléctrico 2.5mm', 'Cable THW 2.5mm x 100m', 35.00, 52.50, 12, 5, 'ROLLO', 3, 4),
('ME002', 'Interruptor Simple', 'Interruptor de pared tipo palanca', 3.50, 5.25, 50, 15, 'UNIDAD', 3, 4),
('ME003', 'Toma Corriente Universal', 'Toma de corriente doble universal', 4.20, 6.30, 40, 10, 'UNIDAD', 3, 4),
('PA001', 'Pintura Blanca Mate', 'Pintura látex blanca mate 1 galón', 18.00, 27.00, 18, 8, 'GALÓN', 4, 5),
('PA002', 'Brocha 2"', 'Brocha angular 2 pulgadas', 2.50, 3.75, 30, 12, 'UNIDAD', 4, 5),
('FO001', 'Tubo PVC 1/2"', 'Tubo PVC sanitario 1/2" x 3m', 6.80, 10.20, 25, 8, 'UNIDAD', 5, 3),
('FO002', 'Codo PVC 90° 1/2"', 'Codo PVC 90 grados 1/2"', 1.20, 1.80, 60, 20, 'UNIDAD', 5, 3),
('CO001', 'Cemento Portland', 'Cemento Portland 50kg', 7.50, 11.25, 40, 15, 'SACO', 6, 3),
('CO002', 'Bloque Hueco 15cm', 'Bloque de concreto 15x20x40cm', 0.80, 1.20, 200, 50, 'UNIDAD', 6, 3),
('FI001', 'Tornillo 3x1"', 'Tornillo para madera 3x1 pulgada', 0.05, 0.08, 500, 100, 'UNIDAD', 7, 2),
('FI002', 'Clavo 2"', 'Clavo común 2 pulgadas', 0.03, 0.05, 800, 200, 'UNIDAD', 7, 2),
('FI003', 'Arandela Plana #8', 'Arandela plana zincada #8', 0.02, 0.03, 1000, 300, 'UNIDAD', 7, 2),
('SE001', 'Casco de Seguridad', 'Casco de seguridad color amarillo', 8.00, 12.00, 15, 5, 'UNIDAD', 8, 1),
('SE002', 'Guantes de Cuero', 'Guantes de cuero para trabajo', 4.50, 6.75, 25, 10, 'PAR', 8, 1),
('SE003', 'Lentes de Seguridad', 'Lentes de seguridad antiimpacto', 3.20, 4.80, 20, 8, 'UNIDAD', 8, 1);

-- Insertar clientes
INSERT INTO CLIENTE (nombres, apellidos, identificacion, telefono, email, direccion) VALUES
('Juan', 'Pérez', '1710001234', '0991234567', 'juan.perez@email.com', 'Calle 1 y Avenida 2'),
('María', 'García', '1720005678', '0992345678', 'maria.garcia@email.com', 'Calle 3 y Avenida 4'),
('Carlos', 'Rodríguez', '1730009012', '0993456789', 'carlos.rodriguez@email.com', 'Calle 5 y Avenida 6'),
('Ana', 'Martínez', '1740003456', '0994567890', 'ana.martinez@email.com', 'Calle 7 y Avenida 8'),
('Luis', 'Hernández', '1750007890', '0995678901', 'luis.hernandez@email.com', 'Calle 9 y Avenida 10');

-- Insertar algunas ventas de ejemplo
INSERT INTO VENTA (fecha_hora, total, estado, tipo_comprobante, numero_comprobante, id_cliente, id_usuario) VALUES
('2024-01-15 10:30:00', 45.50, 'COMPLETADA', 'FACTURA', 'F001-001', 1, 4),
('2024-01-15 14:20:00', 127.80, 'COMPLETADA', 'BOLETA', 'B001-001', 2, 4),
('2024-01-16 09:15:00', 23.40, 'COMPLETADA', 'FACTURA', 'F001-002', 3, 4),
('2024-01-16 16:45:00', 89.90, 'COMPLETADA', 'BOLETA', 'B001-002', 4, 4),
('2024-01-17 11:30:00', 156.75, 'COMPLETADA', 'FACTURA', 'F001-003', 5, 4);

-- Insertar detalles de ventas
INSERT INTO DETALLE_VENTA (cantidad, precio_unitario, id_venta, id_producto) VALUES
(1, 12.75, 1, 1),  -- Martillo
(2, 5.25, 1, 7),   -- Interruptores
(1, 67.50, 2, 4),  -- Taladro
(1, 27.00, 2, 9),  -- Pintura
(2, 1.80, 3, 11),  -- Codos PVC
(1, 18.00, 3, 3),  -- Llave inglesa
(1, 127.50, 4, 5), -- Sierra circular
(1, 11.25, 5, 13), -- Cemento
(1, 27.00, 5, 9),  -- Pintura
(1, 12.00, 5, 18); -- Casco

-- Actualizar stock de productos según las ventas
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 1;
UPDATE PRODUCTO SET stock_actual = stock_actual - 2 WHERE id_producto = 7;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 4;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 9;
UPDATE PRODUCTO SET stock_actual = stock_actual - 2 WHERE id_producto = 11;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 3;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 5;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 13;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 9;
UPDATE PRODUCTO SET stock_actual = stock_actual - 1 WHERE id_producto = 18;
