# src/ui/forms/electrical_form.py
import streamlit as st
import pandas as pd
from src.constants.choices import OBSERVACIONES_OPCIONES
from src.services.mantenimiento_service import MantenimientoService

def render_electrical_form(row, first_idx, row_data):
    """
    Renders the mobile vertical form for electrical checklist and activity inputs.
    """
    mantenimiento_service = MantenimientoService()
    
    st.markdown("<h4 style='color: #ffffff; margin-top:15px; margin-bottom: 5px; font-weight:700; font-size:18px;'>Alistamiento Eléctrico</h4>", unsafe_allow_html=True)
    with st.container(key="mobile_form_container_electric"):
        
        # 1. Elec. Luces
        current_val = row.get('Elec. Luces', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"luces_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar luces externas e internas, pito, limpiabrisas, desempañador, estacionarias",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Luces', sb_key)
        )

        # 2. Elec. Tablero
        current_val = row.get('Elec. Tablero', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"tablero_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar tablero de instrumentos y multiplexado (manómetros, gasómetro, testigos)",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Tablero', sb_key)
        )

        # 3. Elec. Rutero
        current_val = row.get('Elec. Rutero', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"rutero_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar rutero e informadores",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Rutero', sb_key)
        )

        # 4. Elec. Arranque
        current_val = row.get('Elec. Arranque', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"arranque_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar funcionamiento de arranque y alternador",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Arranque', sb_key)
        )

        # 5. Elec. Puertas
        current_val = row.get('Elec. Puertas', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"puertas_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar apertura y cierre de puertas exterior e interior",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Puertas', sb_key)
        )

        # 6. Elec. Baterías
        current_val = row.get('Elec. Baterías', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"baterias_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Verificar sujeción baterías y estado bornes",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Elec. Baterías', sb_key)
        )

        st.markdown("<h5 style='color: #ffffff; margin-top:20px; margin-bottom: 5px; font-weight:600;'>Actividades Adicionales y Observaciones Eléctricas</h5>", unsafe_allow_html=True)
        for idx_num, (index_df, vehicle_row) in enumerate(row_data.iterrows()):
            # Detalles Eléctrico selectbox (allow writing freely)
            current_detalles_elec = vehicle_row.get('Detalles Eléctrico', '')
            if current_detalles_elec is None:
                current_detalles_elec = ""
            else:
                current_detalles_elec = str(current_detalles_elec).strip()
                
            sb_options = ["", "N/A"]
            if current_detalles_elec and current_detalles_elec not in sb_options:
                sb_options.append(current_detalles_elec)
                
            try:
                sb_index = sb_options.index(current_detalles_elec)
            except ValueError:
                sb_index = 0
                
            sb_key_elec = f"detalles_sb_elec_mobile_{vehicle_row['Móvil']}_{index_df}"
            
            st.selectbox(
                f"Actividad eléctrica ejecutada #{idx_num + 1}",
                options=sb_options,
                index=sb_index,
                key=sb_key_elec,
                accept_new_options=True,
                placeholder="Escribe la actividad o selecciona...",
                on_change=MantenimientoService.on_detalles_elec_row_change,
                args=(index_df, sb_key_elec)
            )
            
            # Observaciones Eléctrico selectbox
            current_obs_elec = vehicle_row.get('Observaciones Eléctrico', '')
            if current_obs_elec is None:
                current_obs_elec = ""
            
            options = ["", "N/A"] + OBSERVACIONES_OPCIONES
            if current_obs_elec and current_obs_elec not in options:
                options.append(current_obs_elec)
                
            try:
                default_index = options.index(current_obs_elec)
            except ValueError:
                default_index = 0
                
            idx_val = None if current_obs_elec == "" else default_index
            sb_key_elec = f"observaciones_sb_elec_mobile_{vehicle_row['Móvil']}_{index_df}"
            
            st.selectbox(
                f"Observación eléctrica #{idx_num + 1}",
                options=options,
                index=idx_val,
                placeholder="Escribir N/A si no tiene novedad",
                key=sb_key_elec,
                on_change=MantenimientoService.on_observaciones_elec_row_change,
                args=(index_df, sb_key_elec)
            )
            
            # Delete button if more than 1 row exists
            if len(row_data) > 1:
                if st.button("❌ Eliminar esta Actividad Eléctrica", key=f"del_row_btn_mobile_elec_{vehicle_row['Móvil']}_{index_df}", use_container_width=True):
                    db_config = {
                        'host': st.session_state.db_host,
                        'user': st.session_state.db_user,
                        'password': st.session_state.db_password,
                        'db_name': st.session_state.db_name,
                        'port': st.session_state.db_port
                    }
                    new_df, success, msg = mantenimiento_service.delete_electrical_activity(
                        st.session_state.df_master, index_df, st.session_state.modified_moviles, db_config
                    )
                    if success:
                        st.session_state.df_master = new_df
                        st.rerun()
                    else:
                        st.error(msg)
            
            st.write("---")
            
        last_row_obs_elec = str(row_data.iloc[-1].get('Observaciones Eléctrico', '')).strip()
        btn_add_disabled_elec = not last_row_obs_elec
        if st.button("Agregar otra Actividad/ Observación", key=f"add_row_btn_mobile_elec_{row['Móvil']}", use_container_width=True, disabled=btn_add_disabled_elec):
            new_df, success, msg = mantenimiento_service.add_electrical_activity(
                st.session_state.df_master, row['Móvil'], st.session_state.modified_moviles
            )
            if success:
                st.session_state.df_master = new_df
                st.rerun()
            else:
                st.toast(msg)
