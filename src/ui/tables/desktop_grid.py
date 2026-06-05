# src/ui/tables/desktop_grid.py
import streamlit as st
from src.constants.choices import OBSERVACIONES_OPCIONES
from src.services.mantenimiento_service import MantenimientoService

def render_desktop_grid(df_page, search_query):
    """
    Renders the interactive matrix grid (3 rows per vehicle) for desktop views.
    Binds fields and actions to MantenimientoService callbacks.
    """
    mantenimiento_service = MantenimientoService()
    
    # 1. Table Headers
    header_container = st.container(key="desktop_only_container")
    
    # Row 0 Headers (Niveles)
    hdr_nv1, hdr_nv2, hdr_nv3, hdr_nv4, hdr_nv5, hdr_nv6, hdr_nv7, hdr_nv8, hdr_nv9, hdr_nv10, hdr_nv11, hdr_nv12 = header_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
    with hdr_nv1:
        st.markdown(
            """
            <div style="
                height: 160px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 13px;
                color: #005b94;
                border-bottom: 3px solid #005b94;
                letter-spacing: 0.5px;
                text-align: center;
            ">
                📋 NIVELES
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv2:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    ACEITE MOTOR (SI/NO)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv3:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    CANT. ACEITE MOTOR (L)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv4:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    REFRIGERANTE (SI/NO)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv5:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    CANT. REFRIGERANTE (L)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv6:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    ACEITE HIDRÁULICO (SI/NO)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv7:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    CANT. ACEITE HIDR. (L)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv8:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    LIMPIABRISAS (SI/NO)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv9:
        st.markdown(
            """
            <div style="height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;">
                <div style="writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;">
                    CANT. LIMPIABRISAS (L)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv10:
        st.markdown(
            """
            <div style="
                height: 160px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 11px;
                color: #ffffff;
                border-bottom: 3px solid #005b94;
                letter-spacing: 0.5px;
                text-align: center;
            ">
                DUCTO ADMISIÓN /<br>DRENAR TANQUES
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv11:
        st.markdown(
            """
            <div style="
                height: 160px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 11px;
                color: #ffffff;
                border-bottom: 3px solid #005b94;
                letter-spacing: 0.5px;
                text-align: center;
            ">
                OBSERVACIÓN NIVELES<br>(CONSIGNAR NOVEDADES)
            </div>
            """,
            unsafe_allow_html=True
        )
    with hdr_nv12:
        st.markdown("<div style='height: 160px; border-bottom: 3px solid #005b94;'></div>", unsafe_allow_html=True)

    # Row 1 Headers (Mechanical + Actions)
    hdr_col1, hdr_col2, hdr_col3, hdr_col4, hdr_col5, hdr_col6, hdr_col7, hdr_col8, hdr_col9, hdr_col10, hdr_col11, hdr_col12 = header_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
    with hdr_col1:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 15px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px;'>MÓVIL</div>", unsafe_allow_html=True)
    with hdr_col2:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>REVISION DE FUGAS<br>(MOTOR, TRANSMISIÓN,<br>DIFERENCIAL, DIRECCIÓN)</div></div>", unsafe_allow_html=True)
    with hdr_col3:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>SEPARADOR DE HUMEDAD<br>DEL COMBUSTIBLE</div></div>", unsafe_allow_html=True)
    with hdr_col4:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>INSPECCIÓN SISTEMA<br>DE EMBRAGUE - LINEAS DEL<br>CIRCUITO Y PEDAL DE MANDO</div></div>", unsafe_allow_html=True)
    with hdr_col5:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>INSPECCIÓN FUNCIÓN DE<br>PALANCA DE VELOCIDADES,<br>GUAYAS DE LA TRANSMISIÓN</div></div>", unsafe_allow_html=True)
    with hdr_col6:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>INSPECCIÓN VISUAL DEL<br>VENTILADOR Y CORREAS</div></div>", unsafe_allow_html=True)
    with hdr_col7:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>INSPECCIÓN SISTEMA DE<br>SUSPENSIÓN DELANTERA-<br>TRASERA</div></div>", unsafe_allow_html=True)
    with hdr_col8:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>FRENOS REVISIÓN<br>BANDAS, CUBOS, TUBERIAS DE<br>AIRE Y CONEXIONES</div></div>", unsafe_allow_html=True)
    with hdr_col9:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>INSPECCIÓN SISTEMA DE<br>DIRECCIÓN<br>(CAJA, BOMBA Y TERMINALES)</div></div>", unsafe_allow_html=True)
    with hdr_col10:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; white-space: nowrap; text-align: center;'>ACTIVIDADES ADICIONALES EJECUTADAS</div>", unsafe_allow_html=True)
    with hdr_col11:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; text-align: center;'>OBSERVACIÓN<br>(CONSIGNAR CORRECCIONES Y NOVEDADES PARA PROGRAMAR)</div>", unsafe_allow_html=True)
    with hdr_col12:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; text-align: center;'>INSUMOS INSTALADOS CODIGO SAP/<br>CANTIDAD</div>", unsafe_allow_html=True)

    # Row 2 Headers (Electrical + Spacers)
    hdr_el1, hdr_el2, hdr_el3, hdr_el4, hdr_el5, hdr_el6, hdr_el7, hdr_el8, hdr_el9, hdr_el10, hdr_el11, hdr_el12 = header_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
    with hdr_el1:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 13px; color: #005b94; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; text-align: center;'>ALISTAMIENTO ELÉCTRICO</div>", unsafe_allow_html=True)
    with hdr_el2:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR LUCES EXTERNAS<br>E INTERNAS, PITO, LIMPIABRISAS,<br>DESEMPAÑADOR, ESTACIONARIAS</div></div>", unsafe_allow_html=True)
    with hdr_el3:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR TABLERO DE<br>INSTRUMENTOS Y MULTIPLEXADO<br>(MANOMETROS, GASOMETRO, TESTIGOS)</div></div>", unsafe_allow_html=True)
    with hdr_el4:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR RUTERO E<br>INFORMADORES</div></div>", unsafe_allow_html=True)
    with hdr_el5:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR FUNCIONAMIENTO<br>DE ARRANQUE Y ALTERNADOR</div></div>", unsafe_allow_html=True)
    with hdr_el6:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR APERTURA Y<br>CIERRE DE PUERTAS EXTERIOR<br>E INTERIOR</div></div>", unsafe_allow_html=True)
    with hdr_el7:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; border-bottom: 3px solid #005b94;'><div style='writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-weight: bold; font-size: 11px; color: #a0b2c6; line-height: 1.2; text-align: center; letter-spacing: 0.5px;'>VERIFICAR SUJECIÓN BATERIAS<br>Y ESTADO BORNES</div></div>", unsafe_allow_html=True)
    for extra_hdr in [hdr_el8, hdr_el9, hdr_el12]:
        with extra_hdr:
            st.markdown("<div style='height: 160px; border-bottom: 3px solid #005b94;'></div>", unsafe_allow_html=True)
    with hdr_el10:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; white-space: nowrap; text-align: center;'>ACTIVIDADES ADICIONALES ELÉCTRICO</div>", unsafe_allow_html=True)
    with hdr_el11:
        st.markdown("<div style='height: 160px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: #ffffff; border-bottom: 3px solid #005b94; letter-spacing: 0.5px; text-align: center;'>OBSERVACIÓN ELÉCTRICO<br>(CONSIGNAR CORRECCIONES Y NOVEDADES PARA PROGRAMAR)</div>", unsafe_allow_html=True)
            
    st.write("") # Spacer

    # 2. Rows of Data
    desktop_rows_container = st.container(key="desktop_only_rows_container")
    for index_df, row in df_page.iterrows():
        # Row 1: Niveles
        row_niv1, row_niv2, row_niv3, row_niv4, row_niv5, row_niv6, row_niv7, row_niv8, row_niv9, row_niv10, row_niv11, row_niv12 = desktop_rows_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
        with row_niv1:
            st.markdown(
                f"<div style='background-color: #152232; border: 1px solid #1e293b; border-radius: 4px; height: 38px; display: flex; align-items: center; padding-left: 15px; font-weight: 600; color: #f4f6f9;'>"
                f"{row['Móvil']}"
                f"</div>",
                unsafe_allow_html=True
            )
        with row_niv2:
            current_val = row.get('Nivel Aceite Motor (SI/NO)', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
            sb_key = f"nivel_aceite_motor_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Aceite Motor SI/NO",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Aceite Motor (SI/NO)', sb_key)
            )
        with row_niv3:
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
                
            sb_cant_key = f"nivel_aceite_motor_cant_txt_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Cant Aceite Motor",
                options=mot_cant_options,
                index=default_index,
                key=sb_cant_key,
                disabled=disabled_cant,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Aceite Motor (L)', sb_cant_key)
            )
        with row_niv4:
            current_val = row.get('Nivel Refrigerante (SI/NO)', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
            sb_key = f"nivel_refrigerante_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Refrigerante SI/NO",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Refrigerante (SI/NO)', sb_key)
            )
        with row_niv5:
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
                
            sb_cant_key = f"nivel_refrigerante_cant_txt_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Cant Refrigerante",
                options=ref_cant_options,
                index=default_index,
                key=sb_cant_key,
                disabled=disabled_cant,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Refrigerante (L)', sb_cant_key)
            )
        with row_niv6:
            current_val = row.get('Nivel Aceite Hidráulico (SI/NO)', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
            sb_key = f"nivel_aceite_hidraulico_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Aceite Hidráulico SI/NO",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Aceite Hidráulico (SI/NO)', sb_key)
            )
        with row_niv7:
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
                
            sb_cant_key = f"nivel_aceite_hidraulico_cant_txt_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Cant Aceite Hidráulico",
                options=hid_cant_options,
                index=default_index,
                key=sb_cant_key,
                disabled=disabled_cant,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Aceite Hidráulico (L)', sb_cant_key)
            )
        with row_niv8:
            current_val = row.get('Nivel Limpiabrisas (SI/NO)', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
            sb_key = f"nivel_limpiabrisas_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Limpiabrisas SI/NO",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Limpiabrisas (SI/NO)', sb_key)
            )
        with row_niv9:
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
                
            sb_cant_key = f"nivel_limpiabrisas_cant_txt_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Cant Limpiabrisas",
                options=lim_cant_options,
                index=default_index,
                key=sb_cant_key,
                disabled=disabled_cant,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Nivel Limpiabrisas (L)', sb_cant_key)
            )
        with row_niv10:
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                current_val = row.get('Inspección Ducto Admisión', '')
                if current_val not in ["SI", "NO"]:
                    current_val = ""
                options = ["", "SI", "NO"]
                try:
                    default_index = options.index(current_val)
                except ValueError:
                    default_index = 0
                sb_key = f"inspeccion_ducto_admision_sb_{row['Móvil']}_{index_df}"
                st.selectbox(
                    "Ducto Admisión",
                    options=options,
                    index=default_index,
                    key=sb_key,
                    label_visibility="collapsed",
                    on_change=MantenimientoService.on_checklist_field_change,
                    args=(row['Móvil'], 'Inspección Ducto Admisión', sb_key)
                )
            with sub_col2:
                current_val = row.get('Drenar Tanques', '')
                if current_val not in ["SI", "NO"]:
                    current_val = ""
                options = ["", "SI", "NO"]
                try:
                    default_index = options.index(current_val)
                except ValueError:
                    default_index = 0
                sb_key = f"drenar_tanques_sb_{row['Móvil']}_{index_df}"
                st.selectbox(
                    "Drenar Tanques",
                    options=options,
                    index=default_index,
                    key=sb_key,
                    label_visibility="collapsed",
                    on_change=MantenimientoService.on_checklist_field_change,
                    args=(row['Móvil'], 'Drenar Tanques', sb_key)
                )
        with row_niv11:
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
            sb_key = f"observaciones_niveles_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Obs Niveles",
                options=options_niv,
                index=idx_val,
                placeholder="Escribir N/A si no tiene novedad",
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_observaciones_niveles_row_change,
                args=(index_df, sb_key)
            )
        with row_niv12:
            st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)

        # Row 2: Mecánico
        row_col1, row_col2, row_col3, row_col4, row_col5, row_col6, row_col7, row_col8, row_col9, row_col10, row_col11, row_col12 = desktop_rows_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
        with row_col1:
            st.markdown(
                f"<div style='background-color: #122135; border: 1px solid #1e293b; border-radius: 4px; height: 38px; display: flex; align-items: center; padding-left: 15px; font-size: 11px; font-weight: bold; color: #005b94;'>"
                f"⚙️ Mecánico"
                f"</div>",
                unsafe_allow_html=True
            )
        with row_col2:
            current_val = row.get('Revisión de Fugas', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"fuga_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Fuga",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Revisión de Fugas', sb_key)
            )
        with row_col3:
            current_val = row.get('Separador de Humedad', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"separador_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Separador",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Separador de Humedad', sb_key)
            )
        with row_col4:
            current_val = row.get('Inspección Embrague', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"embrague_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Embrague",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Embrague', sb_key)
            )
        with row_col5:
            current_val = row.get('Inspección Palanca', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"palanca_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Palanca",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Palanca', sb_key)
            )
        with row_col6:
            current_val = row.get('Inspección Ventilador', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"ventilador_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Ventilador",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Ventilador', sb_key)
            )
        with row_col7:
            current_val = row.get('Inspección Suspensión', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"suspension_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Suspensión",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Suspensión', sb_key)
            )
        with row_col8:
            current_val = row.get('Inspección Frenos', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"frenos_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Frenos",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Frenos', sb_key)
            )
        with row_col9:
            current_val = row.get('Inspección Dirección', '')
            if current_val not in ["SI", "NO"]:
                current_val = ""
            options = ["", "SI", "NO"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"direccion_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Dirección",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Inspección Dirección', sb_key)
            )
        with row_col10:
            inp_key = f"detalles_txt_{row['Móvil']}_{index_df}"
            current_detalles = row.get('Detalles / Novedades', '')
            if current_detalles is None:
                current_detalles = ""
            
            vehicle_rows = st.session_state.df_master[st.session_state.df_master['Móvil'] == row['Móvil']]
            num_rows = len(vehicle_rows)
            
            if num_rows > 1:
                txt_col, btn_add, btn_del = st.columns([5, 1, 1])
            else:
                txt_col, btn_add = st.columns([6, 1])
                btn_del = None
                
            with txt_col:
                st.text_input(
                    "Detalles",
                    value=current_detalles,
                    key=inp_key,
                    label_visibility="collapsed",
                    placeholder="Escribir N/A si no se realiza alguna actividad",
                    on_change=MantenimientoService.on_detalles_row_change,
                    args=(index_df, inp_key)
                )
            last_row_obs = str(vehicle_rows.iloc[-1].get('Observaciones', '')).strip()
            btn_add_disabled = not last_row_obs
            with btn_add:
                if st.button("➕", key=f"add_row_btn_{row['Móvil']}_{index_df}", help="Agregar otra actividad mecánica", disabled=btn_add_disabled):
                    new_df, success, msg = mantenimiento_service.add_mechanical_activity(
                        st.session_state.df_master, row['Móvil'], st.session_state.modified_moviles
                    )
                    if success:
                        st.session_state.df_master = new_df
                        st.rerun()
                    else:
                        st.toast(msg)
            if btn_del is not None:
                with btn_del:
                    if st.button("❌", key=f"del_row_btn_{row['Móvil']}_{index_df}", help="Eliminar esta actividad mecánica"):
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
                        
        with row_col11:
            current_obs = row.get('Observaciones', '')
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
                
            sb_key = f"observaciones_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Observación",
                options=options,
                index=idx_val,
                placeholder="Escribir N/A si no tiene novedad",
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_observaciones_row_change,
                args=(index_df, sb_key)
            )
        with row_col12:
            current_val = row.get('Insumos / SAP', '')
            if current_val is None:
                current_val = ''
            else:
                current_val = str(current_val).strip()
            
            sb_key = f"insumos_sb_{row['Móvil']}_{index_df}"
            options = ["", "NO", "N/A"]
            if current_val and current_val not in options:
                options.append(current_val)
                
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            st.selectbox(
                "Insumos / SAP",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                accept_new_options=True,
                placeholder="Escribe o selecciona...",
                on_change=MantenimientoService.on_insumos_change_callback,
                args=(row['Móvil'], 'Insumos / SAP', sb_key)
            )

        # Row 3: Eléctrico
        row_el1, row_el2, row_el3, row_el4, row_el5, row_el6, row_el7, row_el8, row_el9, row_el10, row_el11, row_el12 = desktop_rows_container.columns([2.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 4.0, 7.0, 3.0])
        with row_el1:
            st.markdown(
                f"<div style='background-color: #122135; border: 1px solid #1e293b; border-radius: 4px; height: 38px; display: flex; align-items: center; padding-left: 15px; font-size: 11px; font-weight: bold; color: #005b94;'>"
                f"⚡ Eléctrico"
                f"</div>",
                unsafe_allow_html=True
            )
        with row_el2:
            current_val = row.get('Elec. Luces', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"luces_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Luces",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Luces', sb_key)
            )
        with row_el3:
            current_val = row.get('Elec. Tablero', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"tablero_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Tablero",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Tablero', sb_key)
            )
        with row_el4:
            current_val = row.get('Elec. Rutero', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"rutero_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Rutero",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Rutero', sb_key)
            )
        with row_el5:
            current_val = row.get('Elec. Arranque', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"arranque_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Arranque",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Arranque', sb_key)
            )
        with row_el6:
            current_val = row.get('Elec. Puertas', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"puertas_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Puertas",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Puertas', sb_key)
            )
        with row_el7:
            current_val = row.get('Elec. Baterías', '')
            if current_val not in ["SI", "NO", "N/A"]:
                current_val = ""
            options = ["", "SI", "NO", "N/A"]
            try:
                default_index = options.index(current_val)
            except ValueError:
                default_index = 0
                
            sb_key = f"baterias_sb_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Baterías",
                options=options,
                index=default_index,
                key=sb_key,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_checklist_field_change,
                args=(row['Móvil'], 'Elec. Baterías', sb_key)
            )
        with row_el10:
            current_detalles_elec = row.get('Detalles Eléctrico', '')
            if current_detalles_elec is None:
                current_detalles_elec = ""
            inp_key_elec = f"detalles_txt_elec_{row['Móvil']}_{index_df}"
            
            vehicle_rows = st.session_state.df_master[st.session_state.df_master['Móvil'] == row['Móvil']]
            num_rows = len(vehicle_rows)
            
            if num_rows > 1:
                txt_col, btn_add, btn_del = st.columns([5, 1, 1])
            else:
                txt_col, btn_add = st.columns([6, 1])
                btn_del = None
                
            with txt_col:
                st.text_input(
                    "Detalles Eléctrico",
                    value=current_detalles_elec,
                    key=inp_key_elec,
                    label_visibility="collapsed",
                    placeholder="Escribir N/A si no se realiza alguna actividad",
                    on_change=MantenimientoService.on_detalles_elec_row_change,
                    args=(index_df, inp_key_elec)
                )
            last_row_obs_elec = str(vehicle_rows.iloc[-1].get('Observaciones Eléctrico', '')).strip()
            btn_add_disabled = not last_row_obs_elec
            with btn_add:
                if st.button("➕", key=f"add_row_btn_elec_{row['Móvil']}_{index_df}", help="Agregar otra actividad eléctrica", disabled=btn_add_disabled):
                    new_df, success, msg = mantenimiento_service.add_electrical_activity(
                        st.session_state.df_master, row['Móvil'], st.session_state.modified_moviles
                    )
                    if success:
                        st.session_state.df_master = new_df
                        st.rerun()
                    else:
                        st.toast(msg)
            if btn_del is not None:
                with btn_del:
                    if st.button("❌", key=f"del_row_btn_elec_{row['Móvil']}_{index_df}", help="Eliminar esta actividad eléctrica"):
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
        
        with row_el11:
            current_obs_elec = row.get('Observaciones Eléctrico', '')
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
            sb_key_elec = f"observaciones_sb_elec_{row['Móvil']}_{index_df}"
            st.selectbox(
                "Observación Eléctrico",
                options=options,
                index=idx_val,
                placeholder="Escribir N/A si no tiene novedad",
                key=sb_key_elec,
                label_visibility="collapsed",
                on_change=MantenimientoService.on_observaciones_elec_row_change,
                args=(index_df, sb_key_elec)
            )
        for extra_col in [row_el8, row_el9, row_el12]:
            with extra_col:
                st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
        
        # Dashed separation border
        st.markdown("<div style='height: 12px; border-bottom: 1px dashed rgba(255,255,255,0.1); margin-bottom: 12px;'></div>", unsafe_allow_html=True)
