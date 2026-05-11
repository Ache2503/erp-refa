-- ==============================================
-- SCRIPT DE BASE DE DATOS: GESTION (CORREGIDO)
-- Versión: 2.0
-- Correcciones: Normalización de conductor, orden de tablas, índices, tipos de datos, pluralización.
-- ==============================================

DROP DATABASE IF EXISTS gestion;
CREATE DATABASE gestion;
USE gestion;

-- ========================================
-- 1. TABLAS MAESTRAS (SIN DEPENDENCIAS EXTERNAS FUERTES)
-- ========================================

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    rfc VARCHAR(13) UNIQUE,
    numero_seguridad_social VARCHAR(20) UNIQUE,
    cargo VARCHAR(50),
    estatus VARCHAR(20) DEFAULT 'activo' NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT (CURRENT_DATE)
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    direccion VARCHAR(200),
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    rfc VARCHAR(13) UNIQUE,
    estatus VARCHAR(20) DEFAULT 'activo' NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT (CURRENT_DATE)
);

CREATE TABLE tipos_almacen (
    id_tipo_almacen INT PRIMARY KEY AUTO_INCREMENT,
    nombre_tipo VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE categoria_padre (
    id_categoria_padre INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200)
);

CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    id_categoria_padre INT NULL, -- Permite NULL para categorías raíz
    FOREIGN KEY (id_categoria_padre) REFERENCES categoria_padre(id_categoria_padre),
    INDEX idx_categoria_padre (id_categoria_padre)
);

CREATE TABLE marcas (
    id_marca INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE unidades_medida (
    id_unidad_medida INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    abreviatura VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    email VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE tipo_vehiculo (
    id_tipo_vehiculo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- ========================================
-- 2. TABLAS DEPENDIENTES DE MAESTRAS (NIVEL 1)
-- ========================================

CREATE TABLE almacenes (
    id_almacen INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(200),
    id_empleado INT NOT NULL, -- Responsable
    id_tipo_almacen INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_tipo_almacen) REFERENCES tipos_almacen(id_tipo_almacen),
    INDEX idx_almacen_empleado (id_empleado),
    INDEX idx_almacen_tipo (id_tipo_almacen)
);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    id_categoria INT NOT NULL,
    id_marca INT NOT NULL,
    id_unidad_medida INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    estatus VARCHAR(20) DEFAULT 'activo' NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
    FOREIGN KEY (id_unidad_medida) REFERENCES unidades_medida(id_unidad_medida),
    INDEX idx_producto_categoria (id_categoria),
    INDEX idx_producto_marca (id_marca),
    INDEX idx_producto_um (id_unidad_medida)
);

CREATE TABLE proveedor_contacto (
    id_contacto INT PRIMARY KEY AUTO_INCREMENT,
    id_proveedor INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    INDEX idx_contacto_proveedor (id_proveedor)
);

CREATE TABLE vehiculo (
    id_vehiculo INT PRIMARY KEY AUTO_INCREMENT,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50),
    anio INT,
    numero_serie VARCHAR(50) UNIQUE,
    capacidad_carga DECIMAL(10,2),
    id_tipo_vehiculo INT NOT NULL,
    FOREIGN KEY (id_tipo_vehiculo) REFERENCES tipo_vehiculo(id_tipo_vehiculo),
    INDEX idx_vehiculo_tipo (id_tipo_vehiculo)
);

-- ========================================
-- 3. TABLA CONDUCTOR (REFACTORIZADA - SIN DUPLICAR DATOS DE EMPLEADO)
-- ========================================
CREATE TABLE conductores (
    id_conductor INT PRIMARY KEY AUTO_INCREMENT, 
    id_empleado INT NOT NULL, -- Clave primaria y foránea a la vez
    licencia_conducir VARCHAR(50) UNIQUE NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- ========================================
-- 4. INVENTARIO Y MOVIMIENTOS (NIVEL 2)
-- ========================================

CREATE TABLE productos_almacen (
    id_producto_almacen INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    id_almacen INT NOT NULL,
    stock INT DEFAULT 0 NOT NULL CHECK (stock >= 0),
    stock_minimo INT DEFAULT 0 NOT NULL,
    stock_maximo INT DEFAULT 0 NOT NULL,
    UNIQUE KEY uk_producto_almacen (id_producto, id_almacen),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_almacen) REFERENCES almacenes(id_almacen),
    INDEX idx_pa_producto (id_producto),
    INDEX idx_pa_almacen (id_almacen)
);

CREATE TABLE movimiento (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_movimiento VARCHAR(20) NOT NULL, -- 'ENTRADA', 'SALIDA', 'TRASLADO'
    id_usuario INT NOT NULL, -- Empleado que realiza el movimiento
    observaciones TEXT,
    FOREIGN KEY (id_usuario) REFERENCES empleados(id_empleado),
    INDEX idx_movimiento_usuario (id_usuario),
    INDEX idx_movimiento_fecha (fecha)
);

CREATE TABLE movimiento_detalle (
    id_movimiento_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_movimiento INT NOT NULL,
    id_producto INT NOT NULL,
    id_almacen INT NOT NULL,
    cantidad INT NOT NULL,
    -- Se recomienda añadir precio_unitario para valorizar el movimiento
    precio_unitario DECIMAL(10,2) NULL,
    FOREIGN KEY (id_movimiento) REFERENCES movimiento(id_movimiento) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_almacen) REFERENCES almacenes(id_almacen),
    INDEX idx_md_movimiento (id_movimiento),
    INDEX idx_md_producto (id_producto),
    INDEX idx_md_almacen (id_almacen)
);

-- ========================================
-- 5. COMPRAS
-- ========================================

CREATE TABLE compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    fecha_compra DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_proveedor INT NOT NULL,
    id_almacen INT NOT NULL, -- Almacén de destino de la mercancía
    id_empleado INT NOT NULL, -- Comprador
    tipo_comprobante VARCHAR(50),
    serie VARCHAR(20),
    numero VARCHAR(20),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    estatus VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_almacen) REFERENCES almacenes(id_almacen),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    INDEX idx_compra_proveedor (id_proveedor),
    INDEX idx_compra_almacen (id_almacen),
    INDEX idx_compra_empleado (id_empleado)
);

CREATE TABLE compra_detalle (
    id_compra_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    id_movimiento INT NOT NULL, -- Vincula con el movimiento de entrada generado
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_movimiento) REFERENCES movimiento(id_movimiento),
    INDEX idx_cd_compra (id_compra),
    INDEX idx_cd_producto (id_producto),
    INDEX idx_cd_movimiento (id_movimiento)
);

-- ========================================
-- 6. PEDIDOS (CLIENTES Y PROVEEDORES)
-- ========================================

CREATE TABLE pedidos_clientes (
    id_pedido_cliente INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    id_almacen INT NOT NULL, -- Almacén desde donde se despacha
    requiere_envio BOOLEAN DEFAULT FALSE,
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    impuesto DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    estatus VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_almacen) REFERENCES almacenes(id_almacen),
    INDEX idx_pc_cliente (id_cliente),
    INDEX idx_pc_empleado (id_empleado),
    INDEX idx_pc_almacen (id_almacen)
);

CREATE TABLE pedido_cliente_detalle (
    id_pedido_cliente_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido_cliente) REFERENCES pedidos_clientes(id_pedido_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    INDEX idx_pcd_pedido (id_pedido_cliente),
    INDEX idx_pcd_producto (id_producto)
);

CREATE TABLE pedidos_proveedores (
    id_pedido_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_proveedor INT NOT NULL,
    id_empleado INT NOT NULL,
    id_almacen INT NOT NULL, -- Almacén donde se recibirá
    subtotal DECIMAL(10,2) NOT NULL,
    impuesto DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    estatus VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_almacen) REFERENCES almacenes(id_almacen),
    INDEX idx_pp_proveedor (id_proveedor),
    INDEX idx_pp_empleado (id_empleado)
);

CREATE TABLE pedido_proveedor_detalle (
    id_pedido_proveedor_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido_proveedor INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_pedido_proveedor) REFERENCES pedidos_proveedores(id_pedido_proveedor) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- ========================================
-- 7. ENVÍOS Y LOGÍSTICA
-- ========================================

CREATE TABLE envios (
    id_envio INT PRIMARY KEY AUTO_INCREMENT,
    fecha_envio DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_pedido_cliente INT NOT NULL,
    id_vehiculo INT NOT NULL,
    id_empleado INT NOT NULL, -- Responsable del envío (no necesariamente el conductor)
    estatus VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (id_pedido_cliente) REFERENCES pedidos_clientes(id_pedido_cliente),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    UNIQUE KEY uk_envio_pedido (id_pedido_cliente), -- Un pedido puede tener un solo envío activo
    INDEX idx_envio_vehiculo (id_vehiculo)
);

CREATE TABLE envio_detalle (
    id_envio_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_envio INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_envio) REFERENCES envios(id_envio) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE ruta (
    id_ruta INT PRIMARY KEY AUTO_INCREMENT,
    origen VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    distancia DECIMAL(10,2),
    tiempo_estimado TIME
);

CREATE TABLE ruta_envio (
    id_ruta_envio INT PRIMARY KEY AUTO_INCREMENT,
    id_ruta INT NOT NULL,
    id_envio INT NOT NULL,
    FOREIGN KEY (id_ruta) REFERENCES ruta(id_ruta),
    FOREIGN KEY (id_envio) REFERENCES envios(id_envio) ON DELETE CASCADE,
    INDEX idx_re_ruta (id_ruta),
    INDEX idx_re_envio (id_envio)
);

CREATE TABLE mantenimiento_vehiculo (
    id_mantenimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_vehiculo INT NOT NULL,
    fecha_mantenimiento DATE NOT NULL,
    descripcion TEXT,
    costo DECIMAL(10,2),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo)
);

CREATE TABLE asignacion_transporte (
    id_asignacion INT PRIMARY KEY AUTO_INCREMENT,
    id_envio INT NOT NULL,
    id_conductor INT NOT NULL, -- Ahora referencia a conductores(id_empleado)
    fecha_asignacion DATE NOT NULL DEFAULT (CURRENT_DATE),
    FOREIGN KEY (id_envio) REFERENCES envios(id_envio),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_empleado),
    INDEX idx_at_conductor (id_conductor)
);

CREATE TABLE seguimiento_envio (
    id_seguimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_envio INT NOT NULL,
    fecha_seguimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ubicacion VARCHAR(100),
    estatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_envio) REFERENCES envios(id_envio) ON DELETE CASCADE,
    INDEX idx_se_envio (id_envio)
);

CREATE TABLE guia_remision (
    id_guia INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido_cliente INT NOT NULL,
    fecha_guia DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_vehiculo INT NOT NULL,
    id_conductor INT NOT NULL,
    estatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_pedido_cliente) REFERENCES pedidos_clientes(id_pedido_cliente),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_empleado),
    INDEX idx_gr_vehiculo (id_vehiculo),
    INDEX idx_gr_conductor (id_conductor)
);

CREATE TABLE guia_remision_detalle (
    id_guia_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_guia INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_guia) REFERENCES guia_remision(id_guia) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- ========================================
-- 8. DEVOLUCIONES
-- ========================================

CREATE TABLE devoluciones_clientes (
    id_devolucion INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido_cliente INT NOT NULL,
    fecha_devolucion DATE NOT NULL DEFAULT (CURRENT_DATE),
    motivo TEXT,
    estatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_pedido_cliente) REFERENCES pedidos_clientes(id_pedido_cliente)
);

CREATE TABLE devolucion_cliente_detalle (
    id_devolucion_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_devolucion INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_devolucion) REFERENCES devoluciones_clientes(id_devolucion) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE devoluciones_proveedores (
    id_devolucion INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido_proveedor INT NOT NULL,
    fecha_devolucion DATE NOT NULL DEFAULT (CURRENT_DATE),
    motivo TEXT,
    estatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_pedido_proveedor) REFERENCES pedidos_proveedores(id_pedido_proveedor)
);

CREATE TABLE devolucion_proveedor_detalle (
    id_devolucion_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_devolucion INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_devolucion) REFERENCES devoluciones_proveedores(id_devolucion) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- ========================================
-- 9. TRASLADOS INTERNOS
-- ========================================

CREATE TABLE traslados_internos (
    id_traslado INT PRIMARY KEY AUTO_INCREMENT,
    fecha_traslado DATE NOT NULL DEFAULT (CURRENT_DATE),
    id_almacen_origen INT NOT NULL,
    id_almacen_destino INT NOT NULL,
    id_empleado INT NOT NULL,
    estatus VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_almacen_origen) REFERENCES almacenes(id_almacen),
    FOREIGN KEY (id_almacen_destino) REFERENCES almacenes(id_almacen),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    CHECK (id_almacen_origen <> id_almacen_destino)
);

CREATE TABLE traslado_interno_detalle (
    id_traslado_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_traslado INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_traslado) REFERENCES traslados_internos(id_traslado) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- ========================================
-- 10. SEGURIDAD Y AUDITORÍA
-- ========================================

CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE permisos (
    id_permiso INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE rol_permiso (
    id_rol_permiso INT PRIMARY KEY AUTO_INCREMENT,
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id_permiso) ON DELETE CASCADE,
    UNIQUE KEY uk_rol_permiso (id_rol, id_permiso)
);

CREATE TABLE empleado_rol (
    id_empleado_rol INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol) ON DELETE CASCADE,
    UNIQUE KEY uk_empleado_rol (id_empleado, id_rol)
);

CREATE TABLE auditoria (
    id_auditoria INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    tabla VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT,
    FOREIGN KEY (id_usuario) REFERENCES empleados(id_empleado),
    INDEX idx_auditoria_usuario (id_usuario),
    INDEX idx_auditoria_fecha (fecha)
);

-- ========================================
-- 11. CONFIGURACIÓN Y UTILIDADES
-- ========================================

CREATE TABLE configuracion (
    id_configuracion INT PRIMARY KEY AUTO_INCREMENT,
    clave VARCHAR(50) UNIQUE NOT NULL,
    valor VARCHAR(200) NOT NULL,
    descripcion TEXT
);

CREATE TABLE backups (
    id_backup INT PRIMARY KEY AUTO_INCREMENT,
    fecha_backup DATETIME NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ruta_archivo VARCHAR(200) NOT NULL
);

CREATE TABLE restauraciones (
    id_restauracion INT PRIMARY KEY AUTO_INCREMENT,
    fecha_restauracion DATETIME NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ruta_archivo VARCHAR(200) NOT NULL
);