# src/services/mantenimiento_service.py
import pandas as pd
import streamlit as st
from src.database.repositories.novedades_repository import NovedadesRepository

class MantenimientoService:
    def __init__(self, repository=None):
        self.repository = repository or NovedadesRepository()

    def add_mechanical_activity(self, df_master, movil_id, modified_moviles):
        """
        Adds a new mechanical activity row for the given vehicle, replicating vehicle-level checklist answers.
        """
        vehicle_rows = df_master[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == '')
        ]
        if vehicle_rows.empty:
            return df_master, False, "No active checklist found for this vehicle."
        
        last_row = vehicle_rows.iloc[-1]
        last_obs = str(last_row.get('Observaciones', '')).strip()
        if not last_obs:
            return df_master, False, "⚠️ ¡Debes seleccionar una Observación mecánica en la actividad actual antes de agregar otra!"
        
        # Check if there is already an empty mechanical activity slot
        empty_slot_idx = None
        for idx in vehicle_rows.index:
            det = str(df_master.at[idx, 'Detalles / Novedades']).strip()
            obs = str(df_master.at[idx, 'Observaciones']).strip()
            if not det and not obs:
                empty_slot_idx = idx
                break
                
        if empty_slot_idx is not None:
            return df_master, False, "ℹ️ Ya tienes un slot mecánico disponible."

        # Replicate values
        new_row = {
            'id': None,
            'Móvil': movil_id,
            'Nivel Aceite Motor (SI/NO)': last_row.get('Nivel Aceite Motor (SI/NO)', ''),
            'Nivel Aceite Motor (L)': last_row.get('Nivel Aceite Motor (L)', ''),
            'Nivel Refrigerante (SI/NO)': last_row.get('Nivel Refrigerante (SI/NO)', ''),
            'Nivel Refrigerante (L)': last_row.get('Nivel Refrigerante (L)', ''),
            'Nivel Aceite Hidráulico (SI/NO)': last_row.get('Nivel Aceite Hidráulico (SI/NO)', ''),
            'Nivel Aceite Hidráulico (L)': last_row.get('Nivel Aceite Hidráulico (L)', ''),
            'Nivel Limpiabrisas (SI/NO)': last_row.get('Nivel Limpiabrisas (SI/NO)', ''),
            'Nivel Limpiabrisas (L)': last_row.get('Nivel Limpiabrisas (L)', ''),
            'Inspección Ducto Admisión': last_row.get('Inspección Ducto Admisión', ''),
            'Drenar Tanques': last_row.get('Drenar Tanques', ''),
            'Observaciones Niveles': last_row.get('Observaciones Niveles', ''),
            'Revisión de Fugas': last_row.get('Revisión de Fugas', ''),
            'Separador de Humedad': last_row.get('Separador de Humedad', ''),
            'Inspección Embrague': last_row.get('Inspección Embrague', ''),
            'Inspección Palanca': last_row.get('Inspección Palanca', ''),
            'Inspección Ventilador': last_row.get('Inspección Ventilador', ''),
            'Inspección Suspensión': last_row.get('Inspección Suspensión', ''),
            'Inspección Frenos': last_row.get('Inspección Frenos', ''),
            'Inspección Dirección': last_row.get('Inspección Dirección', ''),
            'Elec. Luces': last_row.get('Elec. Luces', ''),
            'Elec. Tablero': last_row.get('Elec. Tablero', ''),
            'Elec. Rutero': last_row.get('Elec. Rutero', ''),
            'Elec. Arranque': last_row.get('Elec. Arranque', ''),
            'Elec. Puertas': last_row.get('Elec. Puertas', ''),
            'Elec. Baterías': last_row.get('Elec. Baterías', ''),
            'Detalles / Novedades': '',
            'Observaciones': '',
            'Detalles Eléctrico': '',
            'Observaciones Eléctrico': '',
            'Insumos / SAP': last_row.get('Insumos / SAP', ''),
            'Técnico': '',
            'Fecha Registro': '',
            'Tipo Novedad': last_row.get('Tipo Novedad', 'ALISTAMIENTO')
        }
        
        last_idx = vehicle_rows.index[-1]
        idx_pos = df_master.index.get_loc(last_idx)
        
        new_df = pd.concat([
            df_master.iloc[:idx_pos + 1],
            pd.DataFrame([new_row]),
            df_master.iloc[idx_pos + 1:]
        ]).reset_index(drop=True)
        
        modified_moviles.add(movil_id)
        return new_df, True, "Slot mecánico agregado correctamente."

    def add_electrical_activity(self, df_master, movil_id, modified_moviles):
        """
        Adds a new electrical activity row for the given vehicle, replicating vehicle-level checklist answers.
        """
        vehicle_rows = df_master[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == '')
        ]
        if vehicle_rows.empty:
            return df_master, False, "No active checklist found for this vehicle."
        
        last_row = vehicle_rows.iloc[-1]
        last_obs_elec = str(last_row.get('Observaciones Eléctrico', '')).strip()
        if not last_obs_elec:
            return df_master, False, "⚠️ ¡Debes seleccionar una Observación eléctrica en la actividad actual antes de agregar otra!"
        
        # Check if there is already an empty electrical activity slot
        empty_slot_idx = None
        for idx in vehicle_rows.index:
            det = str(df_master.at[idx, 'Detalles Eléctrico']).strip()
            obs = str(df_master.at[idx, 'Observaciones Eléctrico']).strip()
            if not det and not obs:
                empty_slot_idx = idx
                break
                
        if empty_slot_idx is not None:
            return df_master, False, "ℹ️ Ya tienes un slot eléctrico disponible."

        # Replicate values
        new_row = {
            'id': None,
            'Móvil': movil_id,
            'Nivel Aceite Motor (SI/NO)': last_row.get('Nivel Aceite Motor (SI/NO)', ''),
            'Nivel Aceite Motor (L)': last_row.get('Nivel Aceite Motor (L)', ''),
            'Nivel Refrigerante (SI/NO)': last_row.get('Nivel Refrigerante (SI/NO)', ''),
            'Nivel Refrigerante (L)': last_row.get('Nivel Refrigerante (L)', ''),
            'Nivel Aceite Hidráulico (SI/NO)': last_row.get('Nivel Aceite Hidráulico (SI/NO)', ''),
            'Nivel Aceite Hidráulico (L)': last_row.get('Nivel Aceite Hidráulico (L)', ''),
            'Nivel Limpiabrisas (SI/NO)': last_row.get('Nivel Limpiabrisas (SI/NO)', ''),
            'Nivel Limpiabrisas (L)': last_row.get('Nivel Limpiabrisas (L)', ''),
            'Inspección Ducto Admisión': last_row.get('Inspección Ducto Admisión', ''),
            'Drenar Tanques': last_row.get('Drenar Tanques', ''),
            'Observaciones Niveles': last_row.get('Observaciones Niveles', ''),
            'Revisión de Fugas': last_row.get('Revisión de Fugas', ''),
            'Separador de Humedad': last_row.get('Separador de Humedad', ''),
            'Inspección Embrague': last_row.get('Inspección Embrague', ''),
            'Inspección Palanca': last_row.get('Inspección Palanca', ''),
            'Inspección Ventilador': last_row.get('Inspección Ventilador', ''),
            'Inspección Suspensión': last_row.get('Inspección Suspensión', ''),
            'Inspección Frenos': last_row.get('Inspección Frenos', ''),
            'Inspección Dirección': last_row.get('Inspección Dirección', ''),
            'Elec. Luces': last_row.get('Elec. Luces', ''),
            'Elec. Tablero': last_row.get('Elec. Tablero', ''),
            'Elec. Rutero': last_row.get('Elec. Rutero', ''),
            'Elec. Arranque': last_row.get('Elec. Arranque', ''),
            'Elec. Puertas': last_row.get('Elec. Puertas', ''),
            'Elec. Baterías': last_row.get('Elec. Baterías', ''),
            'Detalles / Novedades': '',
            'Observaciones': '',
            'Detalles Eléctrico': '',
            'Observaciones Eléctrico': '',
            'Insumos / SAP': last_row.get('Insumos / SAP', ''),
            'Técnico': '',
            'Fecha Registro': '',
            'Tipo Novedad': last_row.get('Tipo Novedad', 'ALISTAMIENTO')
        }
        
        last_idx = vehicle_rows.index[-1]
        idx_pos = df_master.index.get_loc(last_idx)
        
        new_df = pd.concat([
            df_master.iloc[:idx_pos + 1],
            pd.DataFrame([new_row]),
            df_master.iloc[idx_pos + 1:]
        ]).reset_index(drop=True)
        
        modified_moviles.add(movil_id)
        return new_df, True, "Slot eléctrico agregado correctamente."

    def delete_mechanical_activity(self, df_master, index_df, modified_moviles, db_config):
        """
        Deletes a mechanical activity row and shifts subsequent mechanical activities up.
        Removes the empty final row if it's completely redundant, deleting it from database.
        """
        movil_id = df_master.at[index_df, 'Móvil']
        vehicle_rows = df_master[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == '')
        ]
        
        indices = list(vehicle_rows.index)
        pos = indices.index(index_df)
        
        # Shift mechanical fields up
        for k in range(pos, len(indices) - 1):
            df_master.at[indices[k], 'Detalles / Novedades'] = df_master.at[indices[k+1], 'Detalles / Novedades']
            df_master.at[indices[k], 'Observaciones'] = df_master.at[indices[k+1], 'Observaciones']
            
        df_master.at[indices[-1], 'Detalles / Novedades'] = ''
        df_master.at[indices[-1], 'Observaciones'] = ''
        
        # If there are multiple rows and the last one becomes empty, drop it
        if len(indices) > 1:
            last_idx = indices[-1]
            det_m = str(df_master.at[last_idx, 'Detalles / Novedades']).strip()
            obs_m = str(df_master.at[last_idx, 'Observaciones']).strip()
            det_e = str(df_master.at[last_idx, 'Detalles Eléctrico']).strip()
            obs_e = str(df_master.at[last_idx, 'Observaciones Eléctrico']).strip()
            
            if not det_m and not obs_m and not det_e and not obs_e:
                row_id = df_master.at[last_idx, 'id']
                if row_id is not None and pd.notnull(row_id) and str(row_id).strip() != "":
                    try:
                        self.repository.delete_record_by_id(
                            int(row_id),
                            host=db_config.get('host'),
                            user=db_config.get('user'),
                            password=db_config.get('password'),
                            db_name=db_config.get('db_name'),
                            port=db_config.get('port')
                        )
                    except Exception as e:
                        return df_master, False, f"Error al eliminar de la base de datos: {str(e)}"
                df_master = df_master.drop(last_idx).reset_index(drop=True)
                
        modified_moviles.add(movil_id)
        return df_master, True, "Actividad mecánica eliminada correctamente."

    def delete_electrical_activity(self, df_master, index_df, modified_moviles, db_config):
        """
        Deletes an electrical activity row and shifts subsequent electrical activities up.
        Removes the empty final row if it's completely redundant, deleting it from database.
        """
        movil_id = df_master.at[index_df, 'Móvil']
        vehicle_rows = df_master[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == '')
        ]
        
        indices = list(vehicle_rows.index)
        pos = indices.index(index_df)
        
        # Shift electrical fields up
        for k in range(pos, len(indices) - 1):
            df_master.at[indices[k], 'Detalles Eléctrico'] = df_master.at[indices[k+1], 'Detalles Eléctrico']
            df_master.at[indices[k], 'Observaciones Eléctrico'] = df_master.at[indices[k+1], 'Observaciones Eléctrico']
            
        df_master.at[indices[-1], 'Detalles Eléctrico'] = ''
        df_master.at[indices[-1], 'Observaciones Eléctrico'] = ''
        
        # If there are multiple rows and the last one becomes empty, drop it
        if len(indices) > 1:
            last_idx = indices[-1]
            det_m = str(df_master.at[last_idx, 'Detalles / Novedades']).strip()
            obs_m = str(df_master.at[last_idx, 'Observaciones']).strip()
            det_e = str(df_master.at[last_idx, 'Detalles Eléctrico']).strip()
            obs_e = str(df_master.at[last_idx, 'Observaciones Eléctrico']).strip()
            
            if not det_m and not obs_m and not det_e and not obs_e:
                row_id = df_master.at[last_idx, 'id']
                if row_id is not None and pd.notnull(row_id) and str(row_id).strip() != "":
                    try:
                        self.repository.delete_record_by_id(
                            int(row_id),
                            host=db_config.get('host'),
                            user=db_config.get('user'),
                            password=db_config.get('password'),
                            db_name=db_config.get('db_name'),
                            port=db_config.get('port')
                        )
                    except Exception as e:
                        return df_master, False, f"Error al eliminar de la base de datos: {str(e)}"
                df_master = df_master.drop(last_idx).reset_index(drop=True)
                
        modified_moviles.add(movil_id)
        return df_master, True, "Actividad eléctrica eliminada correctamente."

    @staticmethod
    def update_shared_vehicle_field(movil_id, col_name, new_val):
        """
        Updates a specific column value for all pending rows of a vehicle in st.session_state.df_master
        and synchronizes corresponding session state widget keys for both desktop and mobile views.
        """
        df_master = st.session_state.df_master
        df_master.loc[
            (df_master['Móvil'] == movil_id) &
            (df_master['Técnico'].astype(str).str.strip() == ''),
            col_name
        ] = new_val
        st.session_state.modified_moviles.add(movil_id)
        
        # Map column names to widget key prefixes
        col_to_prefix = {
            'Nivel Aceite Motor (SI/NO)': 'nivel_aceite_motor_sb',
            'Nivel Aceite Motor (L)': 'nivel_aceite_motor_cant_txt',
            'Nivel Refrigerante (SI/NO)': 'nivel_refrigerante_sb',
            'Nivel Refrigerante (L)': 'nivel_refrigerante_cant_txt',
            'Nivel Aceite Hidráulico (SI/NO)': 'nivel_aceite_hidraulico_sb',
            'Nivel Aceite Hidráulico (L)': 'nivel_aceite_hidraulico_cant_txt',
            'Nivel Limpiabrisas (SI/NO)': 'nivel_limpiabrisas_sb',
            'Nivel Limpiabrisas (L)': 'nivel_limpiabrisas_cant_txt',
            'Inspección Ducto Admisión': 'inspeccion_ducto_admision_sb',
            'Drenar Tanques': 'drenar_tanques_sb',
            'Revisión de Fugas': 'fuga_sb',
            'Separador de Humedad': 'separador_sb',
            'Inspección Embrague': 'embrague_sb',
            'Inspección Palanca': 'palanca_sb',
            'Inspección Ventilador': 'ventilador_sb',
            'Inspección Suspensión': 'suspension_sb',
            'Inspección Frenos': 'frenos_sb',
            'Inspección Dirección': 'direccion_sb',
            'Elec. Luces': 'luces_sb',
            'Elec. Tablero': 'tablero_sb',
            'Elec. Rutero': 'rutero_sb',
            'Elec. Arranque': 'arranque_sb',
            'Elec. Puertas': 'puertas_sb',
            'Elec. Baterías': 'baterias_sb',
            'Insumos / SAP': 'insumos_sb'
        }
        
        prefix = col_to_prefix.get(col_name)
        if prefix:
            indices = df_master[
                (df_master['Móvil'] == movil_id) &
                (df_master['Técnico'].astype(str).str.strip() == '')
            ].index
            for idx in indices:
                key_desk = f"{prefix}_{movil_id}_{idx}"
                key_mob = f"{prefix}_mobile_{movil_id}_{idx}"
                st.session_state[key_desk] = new_val
                st.session_state[key_mob] = new_val

    @staticmethod
    def on_checklist_field_change(movil_id, col_name, sb_key):
        """
        Callback triggered when a checklist field value changes.
        """
        new_val = st.session_state[sb_key]
        MantenimientoService.update_shared_vehicle_field(movil_id, col_name, new_val)
        
        si_no_to_cant = {
            'Nivel Aceite Motor (SI/NO)': ('Nivel Aceite Motor (L)', 'nivel_aceite_motor_cant_txt'),
            'Nivel Refrigerante (SI/NO)': ('Nivel Refrigerante (L)', 'nivel_refrigerante_cant_txt'),
            'Nivel Aceite Hidráulico (SI/NO)': ('Nivel Aceite Hidráulico (L)', 'nivel_aceite_hidraulico_cant_txt'),
            'Nivel Limpiabrisas (SI/NO)': ('Nivel Limpiabrisas (L)', 'nivel_limpiabrisas_cant_txt')
        }
        if col_name in si_no_to_cant:
            cant_col, cant_prefix = si_no_to_cant[col_name]
            if new_val in ["NO", ""]:
                new_cant_val = "N/A"
            else:
                df_master = st.session_state.df_master
                current_cant_series = df_master.loc[
                    (df_master['Móvil'] == movil_id) &
                    (df_master['Técnico'].astype(str).str.strip() == ''),
                    cant_col
                ].values
                if len(current_cant_series) > 0 and current_cant_series[0] == "N/A":
                    new_cant_val = ""
                else:
                    new_cant_val = current_cant_series[0] if len(current_cant_series) > 0 else ""
            
            MantenimientoService.update_shared_vehicle_field(movil_id, cant_col, new_cant_val)

    @staticmethod
    def on_insumos_change_callback(movil_id, col_name, sb_key):
        """
        Callback triggered when an SAP insumo entry changes.
        """
        chosen = st.session_state[sb_key]
        if chosen is not None:
            chosen = str(chosen).strip()
            if chosen.upper() in ["NO", "N/A"]:
                chosen = chosen.upper()
        else:
            chosen = ""
        MantenimientoService.update_shared_vehicle_field(movil_id, col_name, chosen)

    @staticmethod
    def on_observaciones_niveles_row_change(index_df, sb_key):
        """
        Callback triggered when levels observation selectbox changes.
        """
        new_val = st.session_state[sb_key]
        if new_val is None:
            new_val = ""
        else:
            new_val = str(new_val).strip()
        st.session_state.df_master.at[index_df, 'Observaciones Niveles'] = new_val
        movil_id = st.session_state.df_master.at[index_df, 'Móvil']
        st.session_state.modified_moviles.add(movil_id)

    @staticmethod
    def on_detalles_row_change(index_df, txt_key):
        """
        Callback triggered when mechanical details text input changes.
        """
        new_val = st.session_state[txt_key].strip()
        st.session_state.df_master.at[index_df, 'Detalles / Novedades'] = new_val
        movil_id = st.session_state.df_master.at[index_df, 'Móvil']
        st.session_state.modified_moviles.add(movil_id)

    @staticmethod
    def on_observaciones_row_change(index_df, sb_key):
        """
        Callback triggered when mechanical observation selectbox changes.
        """
        new_val = st.session_state[sb_key]
        if new_val is None:
            new_val = ""
        else:
            new_val = str(new_val).strip()
        st.session_state.df_master.at[index_df, 'Observaciones'] = new_val
        movil_id = st.session_state.df_master.at[index_df, 'Móvil']
        st.session_state.modified_moviles.add(movil_id)

    @staticmethod
    def on_detalles_elec_row_change(index_df, txt_key):
        """
        Callback triggered when electrical details text input changes.
        """
        new_val = st.session_state[txt_key].strip()
        st.session_state.df_master.at[index_df, 'Detalles Eléctrico'] = new_val
        movil_id = st.session_state.df_master.at[index_df, 'Móvil']
        st.session_state.modified_moviles.add(movil_id)

    @staticmethod
    def on_observaciones_elec_row_change(index_df, sb_key):
        """
        Callback triggered when electrical observation selectbox changes.
        """
        new_val = st.session_state[sb_key]
        if new_val is None:
            new_val = ""
        else:
            new_val = str(new_val).strip()
        st.session_state.df_master.at[index_df, 'Observaciones Eléctrico'] = new_val
        movil_id = st.session_state.df_master.at[index_df, 'Móvil']
        st.session_state.modified_moviles.add(movil_id)

