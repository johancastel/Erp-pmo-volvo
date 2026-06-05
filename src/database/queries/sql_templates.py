# src/database/queries/sql_templates.py

CREATE_VEHICULOS_SQLITE = """
CREATE TABLE IF NOT EXISTS vehiculos (
    movil TEXT PRIMARY KEY,
    patio_predeterminado TEXT DEFAULT '',
    estado TEXT DEFAULT 'ACTIVO'
);
"""

CREATE_VEHICULOS_MYSQL = """
CREATE TABLE IF NOT EXISTS vehiculos (
    movil VARCHAR(50) PRIMARY KEY,
    patio_predeterminado VARCHAR(50) DEFAULT '',
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);
"""

CREATE_INSPECCIONES_SQLITE = """
CREATE TABLE IF NOT EXISTS inspecciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movil TEXT NOT NULL,
    patio TEXT NOT NULL,
    tecnico TEXT DEFAULT '',
    fecha_registro TEXT DEFAULT '',
    tipo_inspeccion TEXT DEFAULT 'COMBINADA',
    FOREIGN KEY (movil) REFERENCES vehiculos(movil)
);
"""

CREATE_INSPECCIONES_MYSQL = """
CREATE TABLE IF NOT EXISTS inspecciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movil VARCHAR(50) NOT NULL,
    patio VARCHAR(50) NOT NULL,
    tecnico VARCHAR(100) DEFAULT '',
    fecha_registro DATETIME,
    tipo_inspeccion VARCHAR(30) DEFAULT 'COMBINADA',
    FOREIGN KEY (movil) REFERENCES vehiculos(movil) ON DELETE RESTRICT
);
"""

CREATE_NIVELES_SQLITE = """
CREATE TABLE IF NOT EXISTS inspeccion_niveles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspeccion_id INTEGER UNIQUE NOT NULL,
    nivel_aceite_motor_si_no TEXT DEFAULT '',
    nivel_aceite_motor_cant TEXT DEFAULT '',
    nivel_refrigerante_si_no TEXT DEFAULT '',
    nivel_refrigerante_cant TEXT DEFAULT '',
    nivel_aceite_hidraulico_si_no TEXT DEFAULT '',
    nivel_aceite_hidraulico_cant TEXT DEFAULT '',
    nivel_limpiabrisas_si_no TEXT DEFAULT '',
    nivel_limpiabrisas_cant TEXT DEFAULT '',
    inspeccion_ducto_admision TEXT DEFAULT '',
    drenar_tanques TEXT DEFAULT '',
    observacion_niveles TEXT DEFAULT '',
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_NIVELES_MYSQL = """
CREATE TABLE IF NOT EXISTS inspeccion_niveles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inspeccion_id INT UNIQUE NOT NULL,
    nivel_aceite_motor_si_no VARCHAR(20) DEFAULT '',
    nivel_aceite_motor_cant VARCHAR(20) DEFAULT '',
    nivel_refrigerante_si_no VARCHAR(20) DEFAULT '',
    nivel_refrigerante_cant VARCHAR(20) DEFAULT '',
    nivel_aceite_hidraulico_si_no VARCHAR(20) DEFAULT '',
    nivel_aceite_hidraulico_cant VARCHAR(20) DEFAULT '',
    nivel_limpiabrisas_si_no VARCHAR(20) DEFAULT '',
    nivel_limpiabrisas_cant VARCHAR(20) DEFAULT '',
    inspeccion_ducto_admision VARCHAR(20) DEFAULT '',
    drenar_tanques VARCHAR(20) DEFAULT '',
    observacion_niveles TEXT,
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_MECANICA_SQLITE = """
CREATE TABLE IF NOT EXISTS inspeccion_mecanica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspeccion_id INTEGER NOT NULL,
    revision_fugas TEXT DEFAULT '',
    separador_humedad TEXT DEFAULT '',
    inspeccion_embrague TEXT DEFAULT '',
    inspeccion_palanca TEXT DEFAULT '',
    inspeccion_ventilador TEXT DEFAULT '',
    inspeccion_suspension TEXT DEFAULT '',
    inspeccion_frenos TEXT DEFAULT '',
    inspeccion_direccion TEXT DEFAULT '',
    detalles TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    insumos TEXT DEFAULT '',
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_MECANICA_MYSQL = """
CREATE TABLE IF NOT EXISTS inspeccion_mecanica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inspeccion_id INT NOT NULL,
    revision_fugas VARCHAR(20) DEFAULT '',
    separador_humedad VARCHAR(20) DEFAULT '',
    inspeccion_embrague VARCHAR(20) DEFAULT '',
    inspeccion_palanca VARCHAR(20) DEFAULT '',
    inspeccion_ventilador VARCHAR(20) DEFAULT '',
    inspeccion_suspension VARCHAR(20) DEFAULT '',
    inspeccion_frenos VARCHAR(20) DEFAULT '',
    inspeccion_direccion VARCHAR(20) DEFAULT '',
    detalles TEXT,
    observaciones TEXT,
    insumos TEXT,
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_ELECTRICA_SQLITE = """
CREATE TABLE IF NOT EXISTS inspeccion_electrica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspeccion_id INTEGER NOT NULL,
    elec_luces TEXT DEFAULT '',
    elec_tablero TEXT DEFAULT '',
    elec_rutero TEXT DEFAULT '',
    elec_arranque TEXT DEFAULT '',
    elec_puertas TEXT DEFAULT '',
    elec_baterias TEXT DEFAULT '',
    detalles_elec TEXT DEFAULT '',
    observaciones_elec TEXT DEFAULT '',
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_ELECTRICA_MYSQL = """
CREATE TABLE IF NOT EXISTS inspeccion_electrica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inspeccion_id INT NOT NULL,
    elec_luces VARCHAR(20) DEFAULT '',
    elec_tablero VARCHAR(20) DEFAULT '',
    elec_rutero VARCHAR(20) DEFAULT '',
    elec_arranque VARCHAR(20) DEFAULT '',
    elec_puertas VARCHAR(20) DEFAULT '',
    elec_baterias VARCHAR(20) DEFAULT '',
    detalles_elec TEXT,
    observaciones_elec TEXT,
    FOREIGN KEY (inspeccion_id) REFERENCES inspecciones(id) ON DELETE CASCADE
);
"""

CREATE_NOVEDADES_VOLVO_SQLITE = """
CREATE TABLE IF NOT EXISTS novedades_volvo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_novedad TEXT DEFAULT '',
    movil TEXT NOT NULL,
    chasis TEXT DEFAULT '',
    linea TEXT DEFAULT '',
    contrato TEXT DEFAULT '',
    fuente_informacion TEXT DEFAULT '',
    novedad TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    grupo_funcion TEXT DEFAULT '',
    criticidad TEXT DEFAULT '',
    dias INTEGER DEFAULT 0,
    estado TEXT DEFAULT '',
    fecha_correccion TEXT DEFAULT '',
    tecnico_correccion TEXT DEFAULT '',
    insumos_usados TEXT DEFAULT '',
    cantidad TEXT DEFAULT ''
);
"""

CREATE_NOVEDADES_VOLVO_MYSQL = """
CREATE TABLE IF NOT EXISTS novedades_volvo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_novedad DATE,
    movil VARCHAR(50) NOT NULL,
    chasis VARCHAR(100) DEFAULT '',
    linea VARCHAR(100) DEFAULT '',
    contrato VARCHAR(100) DEFAULT '',
    fuente_informacion VARCHAR(100) DEFAULT '',
    novedad TEXT,
    observaciones TEXT,
    grupo_funcion VARCHAR(100) DEFAULT '',
    criticidad VARCHAR(50) DEFAULT '',
    dias INT DEFAULT 0,
    estado VARCHAR(50) DEFAULT '',
    fecha_correccion DATE,
    tecnico_correccion VARCHAR(100) DEFAULT '',
    insumos_usados TEXT,
    cantidad VARCHAR(50) DEFAULT ''
);
"""

# Consolidated column names mapped to the application's unified schema
UNIFIED_COLS = [
    'id', 'Móvil',
    'Nivel Aceite Motor (SI/NO)', 'Nivel Aceite Motor (L)',
    'Nivel Refrigerante (SI/NO)', 'Nivel Refrigerante (L)',
    'Nivel Aceite Hidráulico (SI/NO)', 'Nivel Aceite Hidráulico (L)',
    'Nivel Limpiabrisas (SI/NO)', 'Nivel Limpiabrisas (L)',
    'Inspección Ducto Admisión', 'Drenar Tanques', 'Observaciones Niveles',
    'Revisión de Fugas', 'Separador de Humedad', 'Inspección Embrague',
    'Inspección Palanca', 'Inspección Ventilador', 'Inspección Suspensión',
    'Inspección Frenos', 'Inspección Dirección', 'Elec. Luces',
    'Elec. Tablero', 'Elec. Rutero', 'Elec. Arranque', 'Elec. Puertas',
    'Elec. Baterías', 'Detalles / Novedades', 'Observaciones', 'Detalles Eléctrico',
    'Observaciones Eléctrico', 'Insumos / SAP', 'Técnico', 'Fecha Registro', 'Tipo Novedad'
]
