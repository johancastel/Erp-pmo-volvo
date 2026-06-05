# src/ui/forms/levels_form.py
import streamlit as st
from src.constants.choices import OBSERVACIONES_OPCIONES
from src.services.mantenimiento_service import MantenimientoService

def render_levels_form(row, first_idx, row_data):
    """
    Renders the mobile vertical form for fluid levels check.
    """
    st.markdown("<h4 style='color: #ffffff; margin-top:15px; margin-bottom: 5px; font-weight:700; font-size:18px;'>Niveles</h4>", unsafe_allow_html=True)
    with st.container(key="mobile_form_container_levels"):
        
        # 1. Nivel Aceite Motor (SI/NO)
        current_val = row.get('Nivel Aceite Motor (SI/NO)', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"nivel_aceite_motor_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Nivel de aceite motor",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Aceite Motor (SI/NO)', sb_key)
        )
        
        # Cant Aceite Motor (L)
        mot_si_no = row.get('Nivel Aceite Motor (SI/NO)', '')
        mot_cant = row.get('Nivel Aceite Motor (L)', '')
        if mot_si_no != "SI":
            mot_cant_options = ["N/A"]
            default_index = 0
            disabled_cant = True
        else:
            mot_cant_options = ["", "0", "1", "2", "3", "4", "5"]
            mot_cant_str = ""
            if mot_cant is not None and str(mot_cant).strip() != "" and str(mot_cant).lower().strip() != "nan":
                mot_cant_str = str(mot_cant).strip()
            if mot_cant_str == "N/A":
                mot_cant_str = ""
            if mot_cant_str and mot_cant_str not in mot_cant_options:
                mot_cant_options.append(mot_cant_str)
            try:
                default_index = mot_cant_options.index(mot_cant_str)
            except ValueError:
                default_index = 0
            disabled_cant = False
            
        sb_cant_key = f"nivel_aceite_motor_cant_txt_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Cantidad de aceite motor (L)",
            options=mot_cant_options,
            index=default_index,
            key=sb_cant_key,
            disabled=disabled_cant,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Aceite Motor (L)', sb_cant_key)
        )
        
        # 2. Nivel Refrigerante (SI/NO)
        current_val = row.get('Nivel Refrigerante (SI/NO)', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"nivel_refrigerante_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Nivel de refrigerante",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Refrigerante (SI/NO)', sb_key)
        )
        
        # Cant Refrigerante (L)
        ref_si_no = row.get('Nivel Refrigerante (SI/NO)', '')
        ref_cant = row.get('Nivel Refrigerante (L)', '')
        if ref_si_no != "SI":
            ref_cant_options = ["N/A"]
            default_index = 0
            disabled_cant = True
        else:
            ref_cant_options = ["", "0", "1", "2", "3", "4", "5"]
            ref_cant_str = ""
            if ref_cant is not None and str(ref_cant).strip() != "" and str(ref_cant).lower().strip() != "nan":
                ref_cant_str = str(ref_cant).strip()
            if ref_cant_str == "N/A":
                ref_cant_str = ""
            if ref_cant_str and ref_cant_str not in ref_cant_options:
                ref_cant_options.append(ref_cant_str)
            try:
                default_index = ref_cant_options.index(ref_cant_str)
            except ValueError:
                default_index = 0
            disabled_cant = False
            
        sb_cant_key = f"nivel_refrigerante_cant_txt_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Cantidad de refrigerante (L)",
            options=ref_cant_options,
            index=default_index,
            key=sb_cant_key,
            disabled=disabled_cant,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Refrigerante (L)', sb_cant_key)
        )
        
        # 3. Nivel Aceite Hidráulico (SI/NO)
        current_val = row.get('Nivel Aceite Hidráulico (SI/NO)', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"nivel_aceite_hidraulico_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Nivel de aceite hidráulico",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Aceite Hidráulico (SI/NO)', sb_key)
        )
        
        # Cant Aceite Hidráulico (L)
        hid_si_no = row.get('Nivel Aceite Hidráulico (SI/NO)', '')
        hid_cant = row.get('Nivel Aceite Hidráulico (L)', '')
        if hid_si_no != "SI":
            hid_cant_options = ["N/A"]
            default_index = 0
            disabled_cant = True
        else:
            hid_cant_options = ["", "0", "1", "2", "3", "4", "5"]
            hid_cant_str = ""
            if hid_cant is not None and str(hid_cant).strip() != "" and str(hid_cant).lower().strip() != "nan":
                hid_cant_str = str(hid_cant).strip()
            if hid_cant_str == "N/A":
                hid_cant_str = ""
            if hid_cant_str and hid_cant_str not in hid_cant_options:
                hid_cant_options.append(hid_cant_str)
            try:
                default_index = hid_cant_options.index(hid_cant_str)
            except ValueError:
                default_index = 0
            disabled_cant = False
            
        sb_cant_key = f"nivel_aceite_hidraulico_cant_txt_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Cantidad de aceite hidráulico (L)",
            options=hid_cant_options,
            index=default_index,
            key=sb_cant_key,
            disabled=disabled_cant,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Aceite Hidráulico (L)', sb_cant_key)
        )
        
        # 4. Nivel Limpiabrisas (SI/NO)
        current_val = row.get('Nivel Limpiabrisas (SI/NO)', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"nivel_limpiabrisas_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Nivel de limpiabrisas",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Limpiabrisas (SI/NO)', sb_key)
        )
        
        # Cant Limpiabrisas (L)
        lim_si_no = row.get('Nivel Limpiabrisas (SI/NO)', '')
        lim_cant = row.get('Nivel Limpiabrisas (L)', '')
        if lim_si_no != "SI":
            lim_cant_options = ["N/A"]
            default_index = 0
            disabled_cant = True
        else:
            lim_cant_options = ["", "0", "1", "2", "3", "4", "5"]
            lim_cant_str = ""
            if lim_cant is not None and str(lim_cant).strip() != "" and str(lim_cant).lower().strip() != "nan":
                lim_cant_str = str(lim_cant).strip()
            if lim_cant_str == "N/A":
                lim_cant_str = ""
            if lim_cant_str and lim_cant_str not in lim_cant_options:
                lim_cant_options.append(lim_cant_str)
            try:
                default_index = lim_cant_options.index(lim_cant_str)
            except ValueError:
                default_index = 0
            disabled_cant = False
            
        sb_cant_key = f"nivel_limpiabrisas_cant_txt_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Cantidad de limpiabrisas (L)",
            options=lim_cant_options,
            index=default_index,
            key=sb_cant_key,
            disabled=disabled_cant,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Nivel Limpiabrisas (L)', sb_cant_key)
        )
        
        # 5. Inspección Ducto Admisión
        current_val = row.get('Inspección Ducto Admisión', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"inspeccion_ducto_admision_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Inspección ducto admisión",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Inspección Ducto Admisión', sb_key)
        )
        
        # 6. Drenar Tanques
        current_val = row.get('Drenar Tanques', '')
        if current_val not in ["SI", "NO"]:
            current_val = ""
        options = ["", "SI", "NO"]
        try:
            default_index = options.index(current_val)
        except ValueError:
            default_index = 0
        sb_key = f"drenar_tanques_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Drenar tanques",
            options=options,
            index=default_index,
            key=sb_key,
            on_change=MantenimientoService.on_checklist_field_change,
            args=(row['Móvil'], 'Drenar Tanques', sb_key)
        )
        
        # Observaciones Niveles
        current_obs_niv = row.get('Observaciones Niveles', '')
        if current_obs_niv is None:
            current_obs_niv = ""
        options_niv = ["", "N/A"] + OBSERVACIONES_OPCIONES
        if current_obs_niv and current_obs_niv not in options_niv:
            options_niv.append(current_obs_niv)
        try:
            default_index = options_niv.index(current_obs_niv)
        except ValueError:
            default_index = 0
        idx_val = None if current_obs_niv == "" else default_index
        sb_key = f"observaciones_niveles_sb_mobile_{row['Móvil']}_{first_idx}"
        st.selectbox(
            "Observación Niveles",
            options=options_niv,
            index=idx_val,
            placeholder="Escribir N/A si no tiene novedad",
            key=sb_key,
            on_change=MantenimientoService.on_observaciones_niveles_row_change,
            args=(first_idx, sb_key)
        )
