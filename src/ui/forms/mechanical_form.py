# src/ui/forms/mechanical_form.py
import streamlit as st
import pandas as pd
from src.constants.choices import OBSERVACIONES_OPCIONES
from src.services.mantenimiento_service import MantenimientoService

def render_mechanical_form(row, first_idx, row_data):
    """
    Renders the mobile vertical form for mechanical checklist and activity inputs.
    """
    mantenimiento_service = MantenimientoService()
    
    st.markdown("<h4 style='color: #ffffff; margin-top:15px; margin-bottom: 5px; font-weight:700; font-size:18px;'>Alistamiento Mecánico</h4>", unsafe_allow_html=True)
    with st.container(key="mobile_form_container"):
        
        # 1. Revisión de Fugas
        current_val = row.get('Revisión de Fugas', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"fuga_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Revisión de Fugas (Motor, Transmisión, Diferencial, Dirección)",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Revisión de Fugas', sb_key)
        )
        
        # 2. Separador de Humedad
        current_val = row.get('Separador de Humedad', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"separador_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Separador de Humedad del Combustible",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Separador de Humedad', sb_key)
        )
        
        # 3. Inspección Embrague
        current_val = row.get('Inspección Embrague', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"embrague_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección Sistema de Embrague - Líneas del Circuito y Pedal",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Embrague', sb_key)
        )
        
        # 4. Inspección Palanca
        current_val = row.get('Inspección Palanca', '')
        if current_val not in ["SI", "NO", "N/A"]:
            current_val = ""
        options = ["", "SI", "NO", "N/A"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"palanca_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección Función de Palanca de Velocidades, Guayas",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Palanca', sb_key)
        )
        
        # 5. Inspección Ventilador
        current_val = row.get('Inspección Ventilador', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"ventilador_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección Visual del Ventilador y Correas",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Ventilador', sb_key)
        )
        
        # 6. Inspección Suspensión
        current_val = row.get('Inspección Suspensión', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"suspension_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección Sistema de Suspensión Delantera-Trasera",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Suspensión', sb_key)
        )
        
        # 7. Inspección Frenos
        current_val = row.get('Inspección Frenos', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"frenos_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Frenos Revisión Bandas, Cubos, Tuberías y Conexiones",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Frenos', sb_key)
        )
        
        # 8. Inspección Dirección
        current_val = row.get('Inspección Dirección', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"direccion_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección Sistema de Dirección (Caja, Bomba y Terminales)",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Dirección', sb_key)
        )

        # 9. Insumos / SAP
        current_val = row.get('Insumos / SAP', '')
        if current_val is None:
            current_val = ''
        else:
            current_val = str(current_val).strip()
            
        sb_key = f"insumos_sb_mobile_{row['Móvil']}_{first_idx}"
        options = ["", "NO", "N/A"]
        if current_val and current_val not in options:
            options.append(current_val)
            
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
            
        st.selectbox(
            "Insumos Instalados Código SAP / Cantidad",
            options=options,
            index=default_index,
            key=sb_key,
            accept_new_options=True,
            placeholder="Escribe o selecciona...",
            on_change=MantenimientoService.on_insumos_change_callback,
            args=(row['Móvil'], 'Insumos / SAP', sb_key)
        )

        st.markdown("<h5 style='color: #ffffff; margin-top:20px; margin-bottom: 5px; font-weight:600;'>Actividades Adicionales y Observaciones Mecánicas</h5>", unsafe_allow_html=True)
        for idx_num, (index_df, vehicle_row) in enumerate(row_data.iterrows()):
            # Detalles / Novedades text input
            current_detalles = vehicle_row.get('Detalles / Novedades', '')
            if current_detalles is None:
                current_detalles = ""
            txt_key = f"detalles_txt_mobile_{vehicle_row['Móvil']}_{index_df}"
            
            st.text_input(
                f"Actividad mecánica ejecutada #{idx_num + 1}",
                value=current_detalles,
                key=txt_key,
                placeholder="Escribir N/A si no se realiza alguna actividad",
                on_change=MantenimientoService.on_detalles_row_change,
                args=(index_df, txt_key)
            )
            
            # Observaciones selectbox
            current_obs = vehicle_row.get('Observaciones', '')
            if current_obs is None:
                current_obs = ""
            
            options = ["", "N/A"] + OBSERVACIONES_OPCIONES
            if current_obs and current_obs not in options:
                options.append(current_obs)
                
            try:
                default_index = options.index(current_obs)
            except ValueError:
                default_index = 0
                
            idx_val = None if current_obs == "" else default_index
            sb_key = f"observaciones_sb_mobile_{vehicle_row['Móvil']}_{index_df}"
            
            st.selectbox(
                f"Observación mecánica #{idx_num + 1}",
                options=options,
                index=idx_val,
                placeholder="Escribir N/A si no tiene novedad",
                key=sb_key,
                on_change=MantenimientoService.on_observaciones_row_change,
                args=(index_df, sb_key)
            )
            
            # Delete button if more than 1 row exists
            if len(row_data) > 1:
                if st.button("❌ Eliminar esta Actividad Mecánica", key=f"del_row_btn_mobile_mec_{vehicle_row['Móvil']}_{index_df}", use_container_width=True):
                    db_config = {
                        'host': st.session_state.db_host,
                        'user': st.session_state.db_user,
                        'password': st.session_state.db_password,
                        'db_name': st.session_state.db_name,
                        'port': st.session_state.db_port
                    }
                    new_df, success, msg = mantenimiento_service.delete_mechanical_activity(
                        st.session_state.df_master, index_df, st.session_state.modified_moviles, db_config
                    )
                    if success:
                        st.session_state.df_master = new_df
                        st.rerun()
                    else:
                        st.error(msg)
            
            st.write("---")
            
        last_row_obs = str(row_data.iloc[-1].get('Observaciones', '')).strip()
        btn_add_disabled = not last_row_obs
        if st.button("➕ Agregar otra Actividad Mecánica", key=f"add_row_btn_mobile_mec_{row['Móvil']}", use_container_width=True, disabled=btn_add_disabled):
            new_df, success, msg = mantenimiento_service.add_mechanical_activity(
                st.session_state.df_master, row['Móvil'], st.session_state.modified_moviles
            )
            if success:
                st.session_state.df_master = new_df
                st.rerun()
            else:
                st.toast(msg)
