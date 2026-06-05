# src/services/cache_service.py
import streamlit as st

class CacheService:
    @staticmethod
    def initialize_state(defaults=None):
        """
        Initializes default values in st.session_state if they do not exist.
        """
        if defaults is None:
            defaults = {}
        for key, val in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = val

    @staticmethod
    def get(key, default=None):
        """
        Retrieves a value from st.session_state safely.
        """
        return st.session_state.get(key, default)

    @staticmethod
    def set(key, value):
        """
        Sets a value in st.session_state.
        """
        st.session_state[key] = value

    @staticmethod
    def delete(key):
        """
        Deletes a value from st.session_state if it exists.
        """
        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def clear_checklist_widget_state():
        """
        Clears dynamic widget values for checklists (selectbox, input keys) from session state.
        This prevents stale inputs when switching buses or patios.
        """
        prefixes = [
            'nivel_aceite_motor_sb', 'nivel_aceite_motor_cant_txt',
            'nivel_refrigerante_sb', 'nivel_refrigerante_cant_txt',
            'nivel_aceite_hidraulico_sb', 'nivel_aceite_hidraulico_cant_txt',
            'nivel_limpiabrisas_sb', 'nivel_limpiabrisas_cant_txt',
            'inspeccion_ducto_admision_sb', 'drenar_tanques_sb',
            'observaciones_niveles_sb',
            'fuga_sb', 'separador_sb', 'embrague_sb', 'palanca_sb', 
            'ventilador_sb', 'suspension_sb', 'frenos_sb', 'direccion_sb', 
            'luces_sb', 'tablero_sb', 'rutero_sb', 'arranque_sb', 
            'puertas_sb', 'baterias_sb',
            'insumos_sb', 'detalles_txt', 'observaciones_sb',
            'detalles_txt_elec', 'observaciones_sb_elec'
        ]
        keys_to_delete = []
        for key in list(st.session_state.keys()):
            for prefix in prefixes:
                if key.startswith(prefix):
                    keys_to_delete.append(key)
                    break
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
