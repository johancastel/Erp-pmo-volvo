# src/database.py
import sqlite3
import pymysql
import os
import datetime
import pandas as pd
from src.config import PATIOS_CONFIG

_cached_db_type = None

def clear_db_type_cache():
    """
    Limpia la caché del tipo de base de datos activa para forzar una nueva verificación.
    """
    global _cached_db_type
    _cached_db_type = None

def get_db_connection(host, user, password, db_name, port):
    """
    Intenta conectarse a MySQL creando la base de datos si no existe. 
    Si falla o si ya se determinó previamente que se debe usar SQLite,
    retorna una conexión SQLite local para evitar retrasos de timeout de red.
    
    Returns:
        conn: Conexión a la base de datos (pymysql.Connection o sqlite3.Connection)
        db_type (str): "MySQL" o "SQLite"
    """
    global _cached_db_type
    
    # 1. Si ya se determinó que se debe usar SQLite, conectar directamente sin intentar MySQL
    if _cached_db_type == "SQLite":
        sqlite_path = os.path.join(os.getcwd(), "erp_pmo.db")
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        return conn, "SQLite"
        
    # 2. Si ya se determinó que MySQL funciona, intentar conectar directamente a la base de datos
    if _cached_db_type == "MySQL":
        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=int(port),
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=3
            )
            return conn, "MySQL"
        except Exception:
            # Si falla por alguna razón (ej. se apagó el servidor), cambiar a SQLite
            _cached_db_type = "SQLite"
            sqlite_path = os.path.join(os.getcwd(), "erp_pmo.db")
            conn = sqlite3.connect(sqlite_path)
            conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            return conn, "SQLite"

    # 3. Comprobación inicial (cuando _cached_db_type es None)
    try:
        # Primero conectar sin base de datos específica para asegurar su creación
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port),
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=3
        )
        # Crear la Base de Datos si no existe
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        
        # Seleccionar la Base de Datos
        conn.select_db(db_name)
        _cached_db_type = "MySQL"
        return conn, "MySQL"
    except Exception:
        # Fallback a SQLite local (erp_pmo.db)
        _cached_db_type = "SQLite"
        sqlite_path = os.path.join(os.getcwd(), "erp_pmo.db")
        conn = sqlite3.connect(sqlite_path)
        # Hace que las filas se retornen como diccionarios, igual que DictCursor en PyMySQL
        conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        return conn, "SQLite"

def init_db(host, user, password, db_name, port):
    """
    Inicializa la base de datos: crea la tabla y la puebla con la flota por patio.
    Compara la configuración actual (PATIOS_CONFIG) con los registros de la base de datos;
    si hay alguna discrepancia en el mapeo (patio, movil) o la tabla no existe, se recrea para sincronizar.
    """
    conn, db_type = get_db_connection(host, user, password, db_name, port)
    cursor = conn.cursor()
    
    fields_list = [
        'patio', 'movil',
        'nivel_aceite_motor_si_no', 'nivel_aceite_motor_cant',
        'nivel_refrigerante_si_no', 'nivel_refrigerante_cant',
        'nivel_aceite_hidraulico_si_no', 'nivel_aceite_hidraulico_cant',
        'nivel_limpiabrisas_si_no', 'nivel_limpiabrisas_cant',
        'inspeccion_ducto_admision', 'drenar_tanques', 'observacion_niveles',
        'revision_fugas', 'separador_humedad', 'inspeccion_embrague',
        'inspeccion_palanca', 'inspeccion_ventilador', 'inspeccion_suspension',
        'inspeccion_frenos', 'inspeccion_direccion', 'elec_luces',
        'elec_tablero', 'elec_rutero', 'elec_arranque', 'elec_puertas',
        'elec_baterias', 'detalles', 'observaciones', 'detalles_elec',
        'observaciones_elec', 'insumos', 'tecnico', 'fecha_registro'
    ]
    fields_str = ", ".join(fields_list)
    placeholders_mysql = ", ".join(["%s"] * len(fields_list))
    placeholders_sqlite = ", ".join(["?"] * len(fields_list))
    
    # 1. Obtener la flota configurada en memoria
    config_vehicles = {(patio, movil) for patio, moviles in PATIOS_CONFIG.items() for movil in moviles}
    
    # 2. Intentar leer la flota existente de la base de datos
    db_vehicles = set()
    table_exists = True
    try:
        cursor.execute("SELECT patio, movil FROM novedades_moviles")
        rows = cursor.fetchall()
        for row in rows:
            if isinstance(row, dict):
                db_vehicles.add((row['patio'], row['movil']))
            else:
                db_vehicles.add((row[0], row[1]))
    except Exception:
        table_exists = False

    # Verificar si tiene columna 'id' (para migración al nuevo esquema ID autoincremental)
    has_id = False
    if table_exists:
        try:
            cursor.execute("SELECT id FROM novedades_moviles LIMIT 1")
            cursor.fetchall()
            has_id = True
        except Exception:
            has_id = False
            
    if table_exists and not has_id:
        try:
            cursor.execute("DROP TABLE novedades_moviles")
            table_exists = False
            db_vehicles = set()
            conn.commit()
        except Exception:
            pass

    # Si la tabla ya existe, nos aseguramos de que tenga las columnas necesarias (migración/actualización de esquema)
    if table_exists:
        # Columnas mecánicas existentes
        mechanical_cols = [
            ("separador_humedad", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_embrague", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_palanca", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_ventilador", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_suspension", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_frenos", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_direccion", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("observaciones", "TEXT", "TEXT DEFAULT ''"),
            ("insumos", "TEXT", "TEXT DEFAULT ''")
        ]
        # Nuevas columnas eléctricas
        electrical_cols = [
            ("elec_luces", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("elec_tablero", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("elec_rutero", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("elec_arranque", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("elec_puertas", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("elec_baterias", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("detalles_elec", "TEXT", "TEXT DEFAULT ''"),
            ("observaciones_elec", "TEXT", "TEXT DEFAULT ''")
        ]
        # Nuevas columnas de niveles
        levels_cols = [
            ("nivel_aceite_motor_si_no", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_aceite_motor_cant", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_refrigerante_si_no", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_refrigerante_cant", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_aceite_hidraulico_si_no", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_aceite_hidraulico_cant", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_limpiabrisas_si_no", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("nivel_limpiabrisas_cant", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("inspeccion_ducto_admision", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("drenar_tanques", "VARCHAR(20) DEFAULT ''", "TEXT DEFAULT ''"),
            ("observacion_niveles", "TEXT", "TEXT DEFAULT ''")
        ]
        
        for col_name, mysql_type, sqlite_type in mechanical_cols + electrical_cols + levels_cols:
            try:
                if db_type == "MySQL":
                    cursor.execute(f"ALTER TABLE novedades_moviles ADD COLUMN {col_name} {mysql_type}")
                else:
                    cursor.execute(f"ALTER TABLE novedades_moviles ADD COLUMN {col_name} {sqlite_type}")
                conn.commit()
            except Exception:
                pass

    # 3. Si la tabla no existe, la creamos desde cero
    if not table_exists:
        # Crear tabla novedades_moviles con Clave Primaria autonumérica 'id'
        if db_type == "MySQL":
            cursor.execute("""
            CREATE TABLE novedades_moviles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patio VARCHAR(50),
                movil VARCHAR(50),
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
                revision_fugas VARCHAR(20) DEFAULT '',
                separador_humedad VARCHAR(20) DEFAULT '',
                inspeccion_embrague VARCHAR(20) DEFAULT '',
                inspeccion_palanca VARCHAR(20) DEFAULT '',
                inspeccion_ventilador VARCHAR(20) DEFAULT '',
                inspeccion_suspension VARCHAR(20) DEFAULT '',
                inspeccion_frenos VARCHAR(20) DEFAULT '',
                inspeccion_direccion VARCHAR(20) DEFAULT '',
                elec_luces VARCHAR(20) DEFAULT '',
                elec_tablero VARCHAR(20) DEFAULT '',
                elec_rutero VARCHAR(20) DEFAULT '',
                elec_arranque VARCHAR(20) DEFAULT '',
                elec_puertas VARCHAR(20) DEFAULT '',
                elec_baterias VARCHAR(20) DEFAULT '',
                detalles TEXT,
                observaciones TEXT,
                detalles_elec TEXT,
                observaciones_elec TEXT,
                insumos TEXT,
                tecnico VARCHAR(100),
                fecha_registro DATETIME
            )
            """)
        else:
            cursor.execute("""
            CREATE TABLE novedades_moviles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patio TEXT,
                movil TEXT,
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
                revision_fugas TEXT DEFAULT '',
                separador_humedad TEXT DEFAULT '',
                inspeccion_embrague TEXT DEFAULT '',
                inspeccion_palanca TEXT DEFAULT '',
                inspeccion_ventilador TEXT DEFAULT '',
                inspeccion_suspension TEXT DEFAULT '',
                inspeccion_frenos TEXT DEFAULT '',
                inspeccion_direccion TEXT DEFAULT '',
                elec_luces TEXT DEFAULT '',
                elec_tablero TEXT DEFAULT '',
                elec_rutero TEXT DEFAULT '',
                elec_arranque TEXT DEFAULT '',
                elec_puertas TEXT DEFAULT '',
                elec_baterias TEXT DEFAULT '',
                detalles TEXT,
                observaciones TEXT DEFAULT '',
                detalles_elec TEXT DEFAULT '',
                observaciones_elec TEXT DEFAULT '',
                insumos TEXT DEFAULT '',
                tecnico TEXT,
                fecha_registro TEXT
            )
            """)
        conn.commit()
        
        # Poblar con la configuración actual
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vehicles = []
        for patio_name, moviles_list in PATIOS_CONFIG.items():
            for movil_id in moviles_list:
                # 34 columns in total: patio, movil + 31 strings + now
                vehicles.append((patio_name, movil_id) + ("",) * 31 + (now,))
        
        if db_type == "MySQL":
            cursor.executemany(
                f"INSERT IGNORE INTO novedades_moviles ({fields_str}) VALUES ({placeholders_mysql})",
                vehicles
            )
        else:
            cursor.executemany(
                f"INSERT OR IGNORE INTO novedades_moviles ({fields_str}) VALUES ({placeholders_sqlite})",
                vehicles
            )
        conn.commit()
    else:
        # Si la tabla ya existe, hacemos un sync incremental si hay diferencias con la configuración
        if db_vehicles != config_vehicles:
            # 3.1. Insertar vehículos que están en la configuración pero no en la base de datos
            missing_vehicles = config_vehicles - db_vehicles
            if missing_vehicles:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                vehicles_to_add = []
                for patio_name, movil_id in missing_vehicles:
                    vehicles_to_add.append((patio_name, movil_id) + ("",) * 31 + (now,))
                
                if db_type == "MySQL":
                    cursor.executemany(
                        f"INSERT IGNORE INTO novedades_moviles ({fields_str}) VALUES ({placeholders_mysql})",
                        vehicles_to_add
                    )
                else:
                    cursor.executemany(
                        f"INSERT OR IGNORE INTO novedades_moviles ({fields_str}) VALUES ({placeholders_sqlite})",
                        vehicles_to_add
                    )
                conn.commit()
            
            # 3.2. Eliminar vehículos que están en la base de datos pero ya no en la configuración
            extra_vehicles = db_vehicles - config_vehicles
            if extra_vehicles:
                for patio_name, movil_id in extra_vehicles:
                    if db_type == "MySQL":
                        cursor.execute("DELETE FROM novedades_moviles WHERE patio=%s AND movil=%s", (patio_name, movil_id))
                    else:
                        cursor.execute("DELETE FROM novedades_moviles WHERE patio=? AND movil=?", (patio_name, movil_id))
                conn.commit()

        # Migrar valores 'Pendiente' existentes a '' para que se muestren vacíos por defecto
        try:
            cursor.execute("UPDATE novedades_moviles SET revision_fugas = '' WHERE revision_fugas = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET separador_humedad = '' WHERE separador_humedad = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_embrague = '' WHERE inspeccion_embrague = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_palanca = '' WHERE inspeccion_palanca = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_ventilador = '' WHERE inspeccion_ventilador = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_suspension = '' WHERE inspeccion_suspension = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_frenos = '' WHERE inspeccion_frenos = 'Pendiente'")
            cursor.execute("UPDATE novedades_moviles SET inspeccion_direccion = '' WHERE inspeccion_direccion = 'Pendiente'")
            conn.commit()
        except Exception:
            pass
        
    cursor.close()
    conn.close()

def load_patio_data(patio_name, host, user, password, db_name, port):
    """
    Carga los vehículos de un patio en un DataFrame, incluyendo el ID de base de datos.
    """
    conn, db_type = get_db_connection(host, user, password, db_name, port)
    cursor = conn.cursor()
    
    select_fields = (
        "id, movil, "
        "nivel_aceite_motor_si_no, nivel_aceite_motor_cant, "
        "nivel_refrigerante_si_no, nivel_refrigerante_cant, "
        "nivel_aceite_hidraulico_si_no, nivel_aceite_hidraulico_cant, "
        "nivel_limpiabrisas_si_no, nivel_limpiabrisas_cant, "
        "inspeccion_ducto_admision, drenar_tanques, observacion_niveles, "
        "revision_fugas, separador_humedad, inspeccion_embrague, "
        "inspeccion_palanca, inspeccion_ventilador, inspeccion_suspension, "
        "inspeccion_frenos, inspeccion_direccion, elec_luces, "
        "elec_tablero, elec_rutero, elec_arranque, elec_puertas, "
        "elec_baterias, detalles, observaciones, detalles_elec, "
        "observaciones_elec, insumos, tecnico, fecha_registro"
    )
    
    if db_type == "MySQL":
        cursor.execute(f"SELECT {select_fields} FROM novedades_moviles WHERE patio=%s ORDER BY movil ASC, id ASC", (patio_name,))
    else:
        cursor.execute(f"SELECT {select_fields} FROM novedades_moviles WHERE patio=? ORDER BY movil ASC, id ASC", (patio_name,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    df_data = pd.DataFrame(rows)
    cols = [
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
        'Observaciones Eléctrico', 'Insumos / SAP', 'Técnico', 'Fecha Registro'
    ]
    if df_data.empty:
        df_data = pd.DataFrame(columns=cols)
    else:
        df_data.columns = cols
        
    return df_data

def save_patio_changes(edits_to_apply, df_filtered, df_master, tecnico_name, patio_name, host, user, password, db_name, port):
    """
    Guarda los cambios de novedades hechos en la tabla editable st.data_editor.
    Actualiza tanto el DataFrame maestro como la base de datos activa.
    """
    db_conn, db_type = get_db_connection(host, user, password, db_name, port)
    db_cursor = db_conn.cursor()
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_count = 0
    
    for idx_str, col_changes in edits_to_apply.items():
        filtered_idx = int(idx_str)
        # Obtener el índice absoluto en el master dataframe a partir del índice relativo en el filtered dataframe
        master_idx = df_filtered.index[filtered_idx]
        
        # Aplicar cambios locales al master
        for col, val in col_changes.items():
            df_master.at[master_idx, col] = val
        
        # Actualizar metadatos de auditoría locales
        df_master.at[master_idx, 'Técnico'] = tecnico_name
        df_master.at[master_idx, 'Fecha Registro'] = now_str
        
        movil_id = df_master.at[master_idx, 'Móvil']
        
        # Columnas de niveles
        niv_mot_si_no = df_master.at[master_idx, 'Nivel Aceite Motor (SI/NO)']
        niv_mot_cant = df_master.at[master_idx, 'Nivel Aceite Motor (L)']
        niv_ref_si_no = df_master.at[master_idx, 'Nivel Refrigerante (SI/NO)']
        niv_ref_cant = df_master.at[master_idx, 'Nivel Refrigerante (L)']
        niv_hid_si_no = df_master.at[master_idx, 'Nivel Aceite Hidráulico (SI/NO)']
        niv_hid_cant = df_master.at[master_idx, 'Nivel Aceite Hidráulico (L)']
        niv_lim_si_no = df_master.at[master_idx, 'Nivel Limpiabrisas (SI/NO)']
        niv_lim_cant = df_master.at[master_idx, 'Nivel Limpiabrisas (L)']
        ins_ducto = df_master.at[master_idx, 'Inspección Ducto Admisión']
        drenar_t = df_master.at[master_idx, 'Drenar Tanques']
        obs_niv = df_master.at[master_idx, 'Observaciones Niveles']
        
        rev_val = df_master.at[master_idx, 'Revisión de Fugas']
        sep_val = df_master.at[master_idx, 'Separador de Humedad']
        emb_val = df_master.at[master_idx, 'Inspección Embrague']
        pal_val = df_master.at[master_idx, 'Inspección Palanca']
        vent_val = df_master.at[master_idx, 'Inspección Ventilador']
        susp_val = df_master.at[master_idx, 'Inspección Suspensión']
        frenos_val = df_master.at[master_idx, 'Inspección Frenos']
        direccion_val = df_master.at[master_idx, 'Inspección Dirección']
        
        # Columnas eléctricas
        luces_val = df_master.at[master_idx, 'Elec. Luces']
        tablero_val = df_master.at[master_idx, 'Elec. Tablero']
        rutero_val = df_master.at[master_idx, 'Elec. Rutero']
        arranque_val = df_master.at[master_idx, 'Elec. Arranque']
        puertas_val = df_master.at[master_idx, 'Elec. Puertas']
        baterias_val = df_master.at[master_idx, 'Elec. Baterías']
        
        det_val = df_master.at[master_idx, 'Detalles / Novedades']
        obs_val = df_master.at[master_idx, 'Observaciones']
        det_elec_val = df_master.at[master_idx, 'Detalles Eléctrico']
        obs_elec_val = df_master.at[master_idx, 'Observaciones Eléctrico']
        ins_val = df_master.at[master_idx, 'Insumos / SAP']
        
        # Guardar en base de datos
        if db_type == "MySQL":
            db_cursor.execute("""
                UPDATE novedades_moviles 
                SET nivel_aceite_motor_si_no = %s, nivel_aceite_motor_cant = %s, nivel_refrigerante_si_no = %s, nivel_refrigerante_cant = %s, nivel_aceite_hidraulico_si_no = %s, nivel_aceite_hidraulico_cant = %s, nivel_limpiabrisas_si_no = %s, nivel_limpiabrisas_cant = %s, inspeccion_ducto_admision = %s, drenar_tanques = %s, observacion_niveles = %s, revision_fugas = %s, separador_humedad = %s, inspeccion_embrague = %s, inspeccion_palanca = %s, inspeccion_ventilador = %s, inspeccion_suspension = %s, inspeccion_frenos = %s, inspeccion_direccion = %s, elec_luces = %s, elec_tablero = %s, elec_rutero = %s, elec_arranque = %s, elec_puertas = %s, elec_baterias = %s, detalles = %s, observaciones = %s, detalles_elec = %s, observaciones_elec = %s, insumos = %s, tecnico = %s, fecha_registro = %s 
                WHERE patio = %s AND movil = %s
            """, (niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str, patio_name, movil_id))
        else:
            db_cursor.execute("""
                UPDATE novedades_moviles 
                SET nivel_aceite_motor_si_no = ?, nivel_aceite_motor_cant = ?, nivel_refrigerante_si_no = ?, nivel_refrigerante_cant = ?, nivel_aceite_hidraulico_si_no = ?, nivel_aceite_hidraulico_cant = ?, nivel_limpiabrisas_si_no = ?, nivel_limpiabrisas_cant = ?, inspeccion_ducto_admision = ?, drenar_tanques = ?, observacion_niveles = ?, revision_fugas = ?, separador_humedad = ?, inspeccion_embrague = ?, inspeccion_palanca = ?, inspeccion_ventilador = ?, inspeccion_suspension = ?, inspeccion_frenos = ?, inspeccion_direccion = ?, elec_luces = ?, elec_tablero = ?, elec_rutero = ?, elec_arranque = ?, elec_puertas = ?, elec_baterias = ?, detalles = ?, observaciones = ?, detalles_elec = ?, observaciones_elec = ?, insumos = ?, tecnico = ?, fecha_registro = ? 
                WHERE patio = ? AND movil = ?
            """, (niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str, patio_name, movil_id))
        updated_count += 1
        
    db_conn.commit()
    db_cursor.close()
    db_conn.close()
    
    return updated_count

def save_patio_changes_custom(modified_moviles, df_master, tecnico_name, patio_name, host, user, password, db_name, port):
    """
    Guarda los cambios de novedades hechos en la cuadrícula personalizada.
    Actualiza tanto el DataFrame maestro como la base de datos activa para los móviles modificados.
    Soporta múltiples registros duplicados por móvil.
    """
    db_conn, db_type = get_db_connection(host, user, password, db_name, port)
    db_cursor = db_conn.cursor()
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_count = 0
    
    for movil_id in modified_moviles:
        row_mask = df_master['Móvil'] == movil_id
        for idx in df_master[row_mask].index:
            # Actualizar metadatos de auditoría locales
            df_master.at[idx, 'Técnico'] = tecnico_name
            df_master.at[idx, 'Fecha Registro'] = now_str
            
            row_id = df_master.at[idx, 'id']
            
            # Columnas de niveles
            niv_mot_si_no = df_master.at[idx, 'Nivel Aceite Motor (SI/NO)']
            niv_mot_cant = df_master.at[idx, 'Nivel Aceite Motor (L)']
            niv_ref_si_no = df_master.at[idx, 'Nivel Refrigerante (SI/NO)']
            niv_ref_cant = df_master.at[idx, 'Nivel Refrigerante (L)']
            niv_hid_si_no = df_master.at[idx, 'Nivel Aceite Hidráulico (SI/NO)']
            niv_hid_cant = df_master.at[idx, 'Nivel Aceite Hidráulico (L)']
            niv_lim_si_no = df_master.at[idx, 'Nivel Limpiabrisas (SI/NO)']
            niv_lim_cant = df_master.at[idx, 'Nivel Limpiabrisas (L)']
            ins_ducto = df_master.at[idx, 'Inspección Ducto Admisión']
            drenar_t = df_master.at[idx, 'Drenar Tanques']
            obs_niv = df_master.at[idx, 'Observaciones Niveles']
            
            rev_val = df_master.at[idx, 'Revisión de Fugas']
            sep_val = df_master.at[idx, 'Separador de Humedad']
            emb_val = df_master.at[idx, 'Inspección Embrague']
            pal_val = df_master.at[idx, 'Inspección Palanca']
            vent_val = df_master.at[idx, 'Inspección Ventilador']
            susp_val = df_master.at[idx, 'Inspección Suspensión']
            frenos_val = df_master.at[idx, 'Inspección Frenos']
            direccion_val = df_master.at[idx, 'Inspección Dirección']
            
            # Columnas eléctricas
            luces_val = df_master.at[idx, 'Elec. Luces']
            tablero_val = df_master.at[idx, 'Elec. Tablero']
            rutero_val = df_master.at[idx, 'Elec. Rutero']
            arranque_val = df_master.at[idx, 'Elec. Arranque']
            puertas_val = df_master.at[idx, 'Elec. Puertas']
            baterias_val = df_master.at[idx, 'Elec. Baterías']
            
            det_val = df_master.at[idx, 'Detalles / Novedades']
            obs_val = df_master.at[idx, 'Observaciones']
            det_elec_val = df_master.at[idx, 'Detalles Eléctrico']
            obs_elec_val = df_master.at[idx, 'Observaciones Eléctrico']
            ins_val = df_master.at[idx, 'Insumos / SAP']
            
            # Si tiene id, actualizar
            if row_id is not None and pd.notnull(row_id) and str(row_id).strip() != "":
                if db_type == "MySQL":
                    db_cursor.execute("""
                        UPDATE novedades_moviles 
                        SET nivel_aceite_motor_si_no = %s, nivel_aceite_motor_cant = %s, nivel_refrigerante_si_no = %s, nivel_refrigerante_cant = %s, nivel_aceite_hidraulico_si_no = %s, nivel_aceite_hidraulico_cant = %s, nivel_limpiabrisas_si_no = %s, nivel_limpiabrisas_cant = %s, inspeccion_ducto_admision = %s, drenar_tanques = %s, observacion_niveles = %s, revision_fugas = %s, separador_humedad = %s, inspeccion_embrague = %s, inspeccion_palanca = %s, inspeccion_ventilador = %s, inspeccion_suspension = %s, inspeccion_frenos = %s, inspeccion_direccion = %s, elec_luces = %s, elec_tablero = %s, elec_rutero = %s, elec_arranque = %s, elec_puertas = %s, elec_baterias = %s, detalles = %s, observaciones = %s, detalles_elec = %s, observaciones_elec = %s, insumos = %s, tecnico = %s, fecha_registro = %s 
                        WHERE id = %s
                    """, (niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str, int(row_id)))
                else:
                    db_cursor.execute("""
                        UPDATE novedades_moviles 
                        SET nivel_aceite_motor_si_no = ?, nivel_aceite_motor_cant = ?, nivel_refrigerante_si_no = ?, nivel_refrigerante_cant = ?, nivel_aceite_hidraulico_si_no = ?, nivel_aceite_hidraulico_cant = ?, nivel_limpiabrisas_si_no = ?, nivel_limpiabrisas_cant = ?, inspeccion_ducto_admision = ?, drenar_tanques = ?, observacion_niveles = ?, revision_fugas = ?, separador_humedad = ?, inspeccion_embrague = ?, inspeccion_palanca = ?, inspeccion_ventilador = ?, inspeccion_suspension = ?, inspeccion_frenos = ?, inspeccion_direccion = ?, elec_luces = ?, elec_tablero = ?, elec_rutero = ?, elec_arranque = ?, elec_puertas = ?, elec_baterias = ?, detalles = ?, observaciones = ?, detalles_elec = ?, observaciones_elec = ?, insumos = ?, tecnico = ?, fecha_registro = ? 
                        WHERE id = ?
                    """, (niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str, int(row_id)))
            else:
                # Si no tiene id, insertar
                insert_fields = [
                    'patio', 'movil',
                    'nivel_aceite_motor_si_no', 'nivel_aceite_motor_cant',
                    'nivel_refrigerante_si_no', 'nivel_refrigerante_cant',
                    'nivel_aceite_hidraulico_si_no', 'nivel_aceite_hidraulico_cant',
                    'nivel_limpiabrisas_si_no', 'nivel_limpiabrisas_cant',
                    'inspeccion_ducto_admision', 'drenar_tanques', 'observacion_niveles',
                    'revision_fugas', 'separador_humedad', 'inspeccion_embrague',
                    'inspeccion_palanca', 'inspeccion_ventilador', 'inspeccion_suspension',
                    'inspeccion_frenos', 'inspeccion_direccion', 'elec_luces',
                    'elec_tablero', 'elec_rutero', 'elec_arranque', 'elec_puertas',
                    'elec_baterias', 'detalles', 'observaciones', 'detalles_elec',
                    'observaciones_elec', 'insumos', 'tecnico', 'fecha_registro'
                ]
                ins_fields_str = ", ".join(insert_fields)
                ins_placeholders_mysql = ", ".join(["%s"] * len(insert_fields))
                ins_placeholders_sqlite = ", ".join(["?"] * len(insert_fields))
                
                if db_type == "MySQL":
                    db_cursor.execute(f"""
                        INSERT INTO novedades_moviles ({ins_fields_str}) 
                        VALUES ({ins_placeholders_mysql})
                    """, (patio_name, movil_id, niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str))
                    new_id = db_cursor.lastrowid
                else:
                    db_cursor.execute(f"""
                        INSERT INTO novedades_moviles ({ins_fields_str}) 
                        VALUES ({ins_placeholders_sqlite})
                    """, (patio_name, movil_id, niv_mot_si_no, niv_mot_cant, niv_ref_si_no, niv_ref_cant, niv_hid_si_no, niv_hid_cant, niv_lim_si_no, niv_lim_cant, ins_ducto, drenar_t, obs_niv, rev_val, sep_val, emb_val, pal_val, vent_val, susp_val, frenos_val, direccion_val, luces_val, tablero_val, rutero_val, arranque_val, puertas_val, baterias_val, det_val, obs_val, det_elec_val, obs_elec_val, ins_val, tecnico_name, now_str))
                    new_id = db_cursor.lastrowid
                df_master.at[idx, 'id'] = new_id
            
            updated_count += 1
            
            updated_count += 1
            
    db_conn.commit()
    db_cursor.close()
    db_conn.close()
    
    return updated_count

def load_all_data(host, user, password, db_name, port):
    """
    Carga todos los vehículos registrados de todos los patios en un DataFrame, incluyendo el ID de base de datos.
    """
    conn, db_type = get_db_connection(host, user, password, db_name, port)
    cursor = conn.cursor()
    
    select_fields = (
        "id, patio, movil, "
        "nivel_aceite_motor_si_no, nivel_aceite_motor_cant, "
        "nivel_refrigerante_si_no, nivel_refrigerante_cant, "
        "nivel_aceite_hidraulico_si_no, nivel_aceite_hidraulico_cant, "
        "nivel_limpiabrisas_si_no, nivel_limpiabrisas_cant, "
        "inspeccion_ducto_admision, drenar_tanques, observacion_niveles, "
        "revision_fugas, separador_humedad, inspeccion_embrague, "
        "inspeccion_palanca, inspeccion_ventilador, inspeccion_suspension, "
        "inspeccion_frenos, inspeccion_direccion, elec_luces, "
        "elec_tablero, elec_rutero, elec_arranque, elec_puertas, "
        "elec_baterias, detalles, observaciones, detalles_elec, "
        "observaciones_elec, insumos, tecnico, fecha_registro"
    )
    
    cursor.execute(f"SELECT {select_fields} FROM novedades_moviles ORDER BY patio ASC, movil ASC, id ASC")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    df_data = pd.DataFrame(rows)
    cols = [
        'id', 'Patio', 'Móvil',
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
        'Observaciones Eléctrico', 'Insumos / SAP', 'Técnico', 'Fecha Registro'
    ]
    if df_data.empty:
        df_data = pd.DataFrame(columns=cols)
    else:
        df_data.columns = cols
        
    return df_data
