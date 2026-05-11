-- ==============================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- Base de datos: GESTION
-- Versión: 2.0
-- Respetando claves foráneas y restricciones
-- ==============================================

USE gestion;

-- --------------------------------------------------
-- 1. TABLAS INDEPENDIENTES (MAESTRAS)
-- --------------------------------------------------

-- Empleados
INSERT INTO empleados (nombre, apellido, direccion, email, telefono, rfc, numero_seguridad_social, cargo, estatus) VALUES
('Carlos', 'Gómez', 'Av. Reforma 123, CDMX', 'carlos.gomez@empresa.com', '5551234567', 'GOCA800101HDF', 'SS123456789', 'Gerente de Logística', 'activo'),
('Ana', 'Martínez', 'Insurgentes 456, CDMX', 'ana.martinez@empresa.com', '5559876543', 'MAJA850202MDF', 'SS987654321', 'Almacenista', 'activo'),
('Luis', 'Pérez', 'Polanco 789, CDMX', 'luis.perez@empresa.com', '5554567890', 'PELU900303HDF', 'SS456123789', 'Vendedor', 'activo');

-- Clientes
INSERT INTO clientes (nombre, apellido, direccion, email, telefono, rfc, estatus) VALUES
('Juan', 'López', 'Calle 1 #202, Col. Centro, CDMX', 'juan.lopez@mail.com', '5551112233', 'LOJA750404HDF', 'activo'),
('María', 'Fernández', 'Av. Universidad 1500, CDMX', 'maria.fernandez@mail.com', '5552223344', 'FEMA860505MDF', 'activo');

-- Tipos de Almacén
INSERT INTO tipos_almacen (nombre_tipo, descripcion) VALUES
('Principal', 'Almacén central de la empresa'),
('Secundario', 'Almacén de distribución regional');

-- Categoría Padre
INSERT INTO categoria_padre (nombre, descripcion) VALUES
('Electrónica', 'Productos electrónicos y tecnológicos'),
('Ropa', 'Prendas de vestir y accesorios');

-- Categorías (hijas)
INSERT INTO categorias (nombre, descripcion, id_categoria_padre) VALUES
('Laptops', 'Computadoras portátiles', 1),
('Camisas', 'Camisas formales e informales', 2);

-- Marcas
INSERT INTO marcas (nombre, descripcion) VALUES
('Dell', 'Computadoras y accesorios'),
('Nike', 'Ropa deportiva y calzado');

-- Unidades de Medida
INSERT INTO unidades_medida (nombre, abreviatura) VALUES
('Pieza', 'pz'),
('Kilogramo', 'kg'),
('Litro', 'L');

-- Proveedores
INSERT INTO proveedores (nombre, direccion, email, telefono) VALUES
('ProveedorTech SA', 'Calle Tecnología 50, CDMX', 'ventas@proveedortech.com', '5558889900'),
('ModaGlobal', 'Av. Moda 200, GDL', 'contacto@modaglobal.com', '3331234567');

-- Tipo de Vehículo
INSERT INTO tipo_vehiculo (nombre, descripcion) VALUES
('Camión', 'Vehículo de carga pesada'),
('Furgoneta', 'Vehículo de reparto liviano');

-- --------------------------------------------------
-- 2. TABLAS DEPENDIENTES (NIVEL 1)
-- --------------------------------------------------

-- Almacenes
INSERT INTO almacenes (nombre, ubicacion, id_empleado, id_tipo_almacen) VALUES
('Almacén Norte', 'Av. Norte 100, CDMX', 2, 1),   -- Responsable: Ana Martínez
('Almacén Sur', 'Calzada Sur 200, CDMX', 2, 2);   -- Responsable: Ana Martínez

-- Productos
INSERT INTO productos (nombre, descripcion, codigo, id_categoria, id_marca, id_unidad_medida, precio, estatus) VALUES
('Laptop Dell Latitude 3420', 'Intel i5, 8GB RAM, 256GB SSD', 'LAT-3420-01', 1, 1, 1, 12500.00, 'activo'),
('Camisa Nike Dri-FIT', 'Camisa deportiva, manga corta', 'NIKE-CAM-01', 2, 2, 1, 850.00, 'activo');

-- Proveedor Contacto
INSERT INTO proveedor_contacto (id_proveedor, nombre, telefono, email) VALUES
(1, 'Roberto Díaz', '5558889901', 'roberto.diaz@proveedortech.com'),
(2, 'Laura Méndez', '3331234568', 'laura.mendez@modaglobal.com');

-- Vehículos
INSERT INTO vehiculo (placa, marca, modelo, anio, numero_serie, capacidad_carga, id_tipo_vehiculo) VALUES
('ABC-123', 'Ford', 'Transit', 2020, '1FTCR14X3HPA12345', 1500.00, 1),
('XYZ-789', 'Mercedes', 'Sprinter', 2022, 'WDB1234567890ABCD', 800.00, 2);

-- Conductores (relacionado con empleados)
INSERT INTO conductores (id_empleado, licencia_conducir) VALUES
(1, 'LIC-123456');   -- Carlos Gómez actúa como conductor

-- --------------------------------------------------
-- 3. INVENTARIO Y MOVIMIENTOS
-- --------------------------------------------------

-- Productos por Almacén (stock inicial)
INSERT INTO productos_almacen (id_producto, id_almacen, stock, stock_minimo, stock_maximo) VALUES
(1, 1, 50, 5, 200),
(1, 2, 20, 5, 100),
(2, 1, 100, 10, 300),
(2, 2, 30, 10, 150);

-- Movimientos (cabecera)
INSERT INTO movimiento (fecha, tipo_movimiento, id_usuario, observaciones) VALUES
('2025-01-10 10:30:00', 'ENTRADA', 2, 'Compra inicial a ProveedorTech'),
('2025-01-15 14:00:00', 'SALIDA', 3, 'Pedido cliente Juan López');

-- Movimiento Detalle (asociado a los movimientos)
INSERT INTO movimiento_detalle (id_movimiento, id_producto, id_almacen, cantidad, precio_unitario) VALUES
(1, 1, 1, 50, 12500.00),   -- Entrada de 50 laptops al almacén norte
(2, 2, 1, 10, 850.00);     -- Salida de 10 camisas del almacén norte

-- --------------------------------------------------
-- 4. COMPRAS
-- --------------------------------------------------

INSERT INTO compras (fecha_compra, id_proveedor, id_almacen, id_empleado, tipo_comprobante, serie, numero, subtotal, estatus) VALUES
('2025-01-10', 1, 1, 2, 'Factura', 'A', '001', 625000.00, 'completada');

INSERT INTO compra_detalle (id_compra, id_producto, id_movimiento, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 50, 12500.00, 625000.00);

-- --------------------------------------------------
-- 5. PEDIDOS DE CLIENTES
-- --------------------------------------------------

INSERT INTO pedidos_clientes (fecha, id_cliente, id_empleado, id_almacen, requiere_envio, subtotal, impuesto, total, estatus) VALUES
('2025-01-15', 1, 3, 1, TRUE, 8500.00, 1360.00, 9860.00, 'enviado');

INSERT INTO pedido_cliente_detalle (id_pedido_cliente, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 2, 10, 850.00, 8500.00);

-- --------------------------------------------------
-- 6. ENVÍOS Y LOGÍSTICA
-- --------------------------------------------------

INSERT INTO envios (fecha_envio, id_pedido_cliente, id_vehiculo, id_empleado, estatus) VALUES
('2025-01-16', 1, 2, 1, 'en_transito');

INSERT INTO envio_detalle (id_envio, id_producto, cantidad) VALUES
(1, 2, 10);

-- Rutas
INSERT INTO ruta (origen, destino, distancia, tiempo_estimado) VALUES
('Almacén Norte', 'Calle 1 #202, Col. Centro, CDMX', 15.5, '00:45:00');

INSERT INTO ruta_envio (id_ruta, id_envio) VALUES
(1, 1);

-- Mantenimiento Vehículo
INSERT INTO mantenimiento_vehiculo (id_vehiculo, fecha_mantenimiento, descripcion, costo) VALUES
(2, '2025-01-05', 'Cambio de aceite y filtros', 3500.00);

-- Asignación de Transporte
INSERT INTO asignacion_transporte (id_envio, id_conductor, fecha_asignacion) VALUES
(1, 1, '2025-01-15');  -- id_conductor hace referencia al id_empleado del conductor

-- Seguimiento de Envío
INSERT INTO seguimiento_envio (id_envio, fecha_seguimiento, ubicacion, estatus) VALUES
(1, '2025-01-16 08:00:00', 'Salida del almacén', 'en_transito'),
(1, '2025-01-16 10:30:00', 'Rumbo a destino', 'en_transito');

-- Guía de Remisión
INSERT INTO guia_remision (id_pedido_cliente, fecha_guia, id_vehiculo, id_conductor, estatus) VALUES
(1, '2025-01-16', 2, 1, 'emitida');

INSERT INTO guia_remision_detalle (id_guia, id_producto, cantidad) VALUES
(1, 2, 10);

-- --------------------------------------------------
-- 7. DEVOLUCIONES (opcional)
-- --------------------------------------------------

INSERT INTO devoluciones_clientes (id_pedido_cliente, fecha_devolucion, motivo, estatus) VALUES
(1, '2025-01-18', 'Producto defectuoso', 'en_proceso');

INSERT INTO devolucion_cliente_detalle (id_devolucion, id_producto, cantidad) VALUES
(1, 2, 2);

-- --------------------------------------------------
-- 8. TRASLADOS INTERNOS
-- --------------------------------------------------

INSERT INTO traslados_internos (fecha_traslado, id_almacen_origen, id_almacen_destino, id_empleado, estatus) VALUES
('2025-01-20', 1, 2, 2, 'completado');

INSERT INTO traslado_interno_detalle (id_traslado, id_producto, cantidad) VALUES
(1, 1, 10);

-- --------------------------------------------------
-- 9. SEGURIDAD Y ROLES
-- --------------------------------------------------

INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Almacenista', 'Gestión de inventarios'),
('Vendedor', 'Creación de pedidos');

INSERT INTO permisos (nombre, descripcion) VALUES
('productos.crear', 'Permite crear productos'),
('compras.aprobar', 'Permite aprobar compras'),
('envios.ver', 'Permite ver envíos');

INSERT INTO rol_permiso (id_rol, id_permiso) VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 3),
(3, 3);

INSERT INTO empleado_rol (id_empleado, id_rol) VALUES
(1, 1),   -- Carlos Gómez: Administrador
(2, 2),   -- Ana Martínez: Almacenista
(3, 3);   -- Luis Pérez: Vendedor

-- --------------------------------------------------
-- 10. CONFIGURACIÓN Y BACKUPS (datos mínimos)
-- --------------------------------------------------

INSERT INTO configuracion (clave, valor, descripcion) VALUES
('impuesto_default', '0.16', 'IVA estándar en México'),
('moneda', 'MXN', 'Moneda local');

INSERT INTO backups (fecha_backup, usuario, descripcion, ruta_archivo) VALUES
(NOW(), 'admin', 'Backup inicial de prueba', '/backups/gestion_20250101.sql');

INSERT INTO restauraciones (fecha_restauracion, usuario, descripcion, ruta_archivo) VALUES
(NOW(), 'admin', 'Restauración de datos de ejemplo', '/backups/gestion_20250101.sql');

-- --------------------------------------------------
-- Fin del script de datos
-- --------------------------------------------------