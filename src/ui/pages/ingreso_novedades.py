# src/ui/pages/ingreso_novedades.py
import datetime
import pandas as pd
import streamlit as st
from src.config.settings import PATIOS_CONFIG
from src.constants.choices import TECNICOS_OPCIONES
from src.styles import draw_metric_card
from src.database.repositories.novedades_repository import NovedadesRepository
from src.services.validation_service import ValidationService
from src.services.cache_service import CacheService
from src.services.mantenimiento_service import MantenimientoService
from src.ui.tables.desktop_grid import render_desktop_grid
from src.ui.forms.levels_form import render_levels_form
from src.ui.forms.mechanical_form import render_mechanical_form
from src.ui.forms.electrical_form import render_electrical_form

def render_maintenance_form(row, first_idx, row_data, current_tipo):
    """
    Renders a simplified form for Mantenimiento Correctivo or Mantenimiento Preventivo,
    consisting only of Activities and Observations.
    """
    mantenimiento_service = MantenimientoService()
    
    if current_tipo == "CORRECTIVO":
        tipo_label = "Mantenimiento Correctivo"
        header_title = "Actividades a Realizar y Observaciones"
        input_label_prefix = "Actividad a realizar"
        input_placeholder = "Escribe la actividad a realizar..."
    else:
        tipo_label = "Mantenimiento Preventivo"
        header_title = "Actividades Pendientes y Observaciones"
        input_label_prefix = "Actividad pendiente"
        input_placeholder = "Escribe la actividad pendiente..."
        
    st.markdown(f"<h4 style='color: #ffffff; margin-top:15px; margin-bottom: 5px; font-weight:700; font-size:18px;'>{tipo_label}</h4>", unsafe_allow_html=True)
    
    with st.container(key="mobile_form_container"):
        st.markdown(f"<h5 style='color: #ffffff; margin-top:0px; margin-bottom: 10px; font-weight:600;'>{header_title}</h5>", unsafe_allow_html=True)
        
        for idx_num, (index_df, vehicle_row) in enumerate(row_data.iterrows()):
            # Detalles / Novedades (Actividades Ejecutadas / Pendientes / A realizar)
            current_detalles = vehicle_row.get('Detalles / Novedades', '')
            if current_detalles is None:
                current_detalles = ""
            txt_key = f"detalles_txt_maint_{vehicle_row['Móvil']}_{index_df}"
            
            st.text_input(
                f"{input_label_prefix} #{idx_num + 1} *",
                value=current_detalles,
                key=txt_key,
                placeholder=input_placeholder,
                on_change=MantenimientoService.on_detalles_row_change,
                args=(index_df, txt_key)
            )
            
            # Observaciones
            current_obs = vehicle_row.get('Observaciones', '')
            if current_obs is None:
                current_obs = ""
            
            from src.constants.choices import OBSERVACIONES_OPCIONES
            options = ["", "N/A"] + OBSERVACIONES_OPCIONES
            if current_obs and current_obs not in options:
                options.append(current_obs)
                
            try:
                default_index = options.index(current_obs)
            except ValueError:
                default_index = 0
                
            idx_val = None if current_obs == "" else default_index
            sb_key = f"observaciones_sb_maint_{vehicle_row['Móvil']}_{index_df}"
            
            st.selectbox(
                f"Observación #{idx_num + 1} *",
                options=options,
                index=idx_val,
                placeholder="Seleccione la observación de la actividad...",
                key=sb_key,
                on_change=MantenimientoService.on_observaciones_row_change,
                args=(index_df, sb_key)
            )
            
            # Delete button if more than 1 row exists
            if len(row_data) > 1:
                if st.button("❌ Eliminar esta Actividad", key=f"del_row_btn_maint_{vehicle_row['Móvil']}_{index_df}", use_container_width=True):
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
        if st.button("➕ Agregar otra Actividad", key=f"add_row_btn_maint_{row['Móvil']}", use_container_width=True, disabled=btn_add_disabled):
            new_df, success, msg = mantenimiento_service.add_mechanical_activity(
                st.session_state.df_master, row['Móvil'], st.session_state.modified_moviles
            )
            if success:
                st.session_state.df_master = new_df
                st.rerun()
            else:
                st.toast(msg)

def render_ingreso_novedades_page():
    repository = NovedadesRepository()
    mantenimiento_service = MantenimientoService(repository)

    # ----------------- SUB-MODULE 1: PATIO SELECTION -----------------
    if 'active_patio' not in st.session_state:
        st.session_state.active_patio = None

    if st.session_state.active_patio is None:
        st.subheader("Centro de Operaciones")
        st.write("Selecciona el patio a gestionar y registrar novedades:")
        
        patios_list = [
            (patio_name, len(PATIOS_CONFIG[patio_name]))
            for patio_name in ["20 DE JULIO", "CALLE 191", "CONEJERA", "EEMB", "ENGATIVA", "GAVIOTAS", "SUBA"]
        ]
        
        def draw_patio_card(patio_name, num_vehicles, col_obj):
            with col_obj:
                st.markdown('<div class="patio-card-container">', unsafe_allow_html=True)
                clean_key = f"btn_patio_{patio_name.replace(' ', '_').lower()}"
                if st.button(patio_name, key=clean_key, use_container_width=True):
                    st.session_state.active_patio = patio_name
                    st.session_state.active_tipo_novedad = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                    
        col1, col2, col3, col4 = st.columns(4)
        for i, (patio_name, count) in enumerate(patios_list[:4]):
            draw_patio_card(patio_name, count, [col1, col2, col3, col4][i])
            
        col5, col6, col7 = st.columns(3)
        for i, (patio_name, count) in enumerate(patios_list[4:]):
            draw_patio_card(patio_name, count, [col5, col6, col7][i])
            
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
        return

    # ----------------- SUB-MODULE 2: ACTIVE PATIO PANEL -----------------
    patio = st.session_state.active_patio
    
    # Initialize page state variables
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'modified_moviles' not in st.session_state:
        st.session_state.modified_moviles = set()
    if 'prev_search_query' not in st.session_state:
        st.session_state.prev_search_query = ""

    # Back button (context-aware)
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    if st.session_state.get('active_tipo_novedad') is not None:
        if st.button("Volver"):
            st.session_state.active_tipo_novedad = None
            st.session_state.clear_search_on_next_run = True
            st.rerun()
    else:
        if st.button("Volver"):
            st.session_state.active_patio = None
            st.session_state.active_tipo_novedad = None
            if 'tecnico_name' in st.session_state: 
                del st.session_state.tecnico_name
            if 'df_master' in st.session_state: 
                del st.session_state.df_master
            if 'df_master_patio_name' in st.session_state: 
                del st.session_state.df_master_patio_name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader(f"{patio}")
    
    # Validate technician identity registration
    if not st.session_state.get('tecnico_name', '').strip():
        st.write("")
        st.warning("⚠️ **Identificación Requerida:** Para poder gestionar y editar los datos del taller, debes registrar tu nombre como Técnico Responsable.")
        
        st.markdown("""
        <div style="background-color: #152232; padding: 22px; border-radius: 8px; border-left: 5px solid #f0ad4e; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);">
            <h4 style="margin-top:0; color: #ffffff; font-weight:600;"> Registro de Técnico</h4>
            <p style="color: #a0b2c6; font-size: 14px; margin-bottom: 0;">Ingresa tu nombre completo para habilitar la planilla de alistamiento del patio.</p>
        </div>
        """, unsafe_allow_html=True)
        
        tecnico_input = st.selectbox(
            "Nombre del Técnico Responsable *",
            options=TECNICOS_OPCIONES,
            index=None,
            placeholder="Selecciona un Técnico...",
            key="temp_tecnico_selectbox"
        )
        
        col_enter, _ = st.columns([1, 3])
        with col_enter:
            if st.button("Ingresar", use_container_width=True):
                if tecnico_input:
                    st.session_state.tecnico_name = tecnico_input
                    st.rerun()
                else:
                    st.error("Por favor, selecciona tu nombre antes de ingresar.")
        return

    # Load active patio data
    btn_recargar = st.sidebar.button("🔄 Recargar Datos del Patio")
        
    if ('df_master' not in st.session_state 
        or st.session_state.get('df_master_patio_name') != patio 
        or btn_recargar):
        
        st.session_state.df_master = repository.load_patio_data(
            patio_name=patio,
            host=st.session_state.db_host,
            user=st.session_state.db_user,
            password=st.session_state.db_password,
            db_name=st.session_state.db_name,
            port=st.session_state.db_port
        )
        st.session_state.df_master_patio_name = patio
        st.session_state.current_page = 0
        st.session_state.modified_moviles = set()
        
        # Ensure every vehicle configured has at least one pending (empty) row in memory
        df_master = st.session_state.df_master
        configured_mobiles = PATIOS_CONFIG.get(patio, [])
        new_rows_to_append = []
        for movil_id in configured_mobiles:
            pending_rows = df_master[
                (df_master['Móvil'] == movil_id) & 
                (df_master['Técnico'].astype(str).str.strip() == '')
            ]
            if pending_rows.empty:
                new_row = {
                    'id': None,
                    'Móvil': movil_id,
                    'Nivel Aceite Motor (SI/NO)': '',
                    'Nivel Aceite Motor (L)': '',
                    'Nivel Refrigerante (SI/NO)': '',
                    'Nivel Refrigerante (L)': '',
                    'Nivel Aceite Hidráulico (SI/NO)': '',
                    'Nivel Aceite Hidráulico (L)': '',
                    'Nivel Limpiabrisas (SI/NO)': '',
                    'Nivel Limpiabrisas (L)': '',
                    'Inspección Ducto Admisión': '',
                    'Drenar Tanques': '',
                    'Observaciones Niveles': '',
                    'Revisión de Fugas': '',
                    'Separador de Humedad': '',
                    'Inspección Embrague': '',
                    'Inspección Palanca': '',
                    'Inspección Ventilador': '',
                    'Inspección Suspensión': '',
                    'Inspección Frenos': '',
                    'Inspección Dirección': '',
                    'Elec. Luces': '',
                    'Elec. Tablero': '',
                    'Elec. Rutero': '',
                    'Elec. Arranque': '',
                    'Elec. Puertas': '',
                    'Elec. Baterías': '',
                    'Detalles / Novedades': '',
                    'Observaciones': '',
                    'Detalles Eléctrico': '',
                    'Observaciones Eléctrico': '',
                    'Insumos / SAP': '',
                    'Técnico': '',
                    'Fecha Registro': '',
                    'Tipo Novedad': 'ALISTAMIENTO'
                }
                new_rows_to_append.append(new_row)
        if new_rows_to_append:
            df_master = pd.concat([df_master, pd.DataFrame(new_rows_to_append)], ignore_index=True)
            st.session_state.df_master = df_master
        
        # Fill nulls with empty strings to prevent selectbox failures
        fill_cols = [
            'Nivel Aceite Motor (SI/NO)', 'Nivel Aceite Motor (L)',
            'Nivel Refrigerante (SI/NO)', 'Nivel Refrigerante (L)',
            'Nivel Aceite Hidráulico (SI/NO)', 'Nivel Aceite Hidráulico (L)',
            'Nivel Limpiabrisas (SI/NO)', 'Nivel Limpiabrisas (L)',
            'Inspección Ducto Admisión', 'Drenar Tanques', 'Observaciones Niveles',
            'Detalles / Novedades', 'Observaciones', 'Detalles Eléctrico', 'Observaciones Eléctrico', 'Insumos / SAP',
            'Tipo Novedad'
        ]
        for c in fill_cols:
            if c in st.session_state.df_master.columns:
                if c == 'Tipo Novedad':
                    st.session_state.df_master[c] = st.session_state.df_master[c].fillna("ALISTAMIENTO").replace("", "ALISTAMIENTO")
                else:
                    st.session_state.df_master[c] = st.session_state.df_master[c].fillna("")
                
        CacheService.clear_checklist_widget_state()

    # RENDER KPIS / METRICS FOR ACTIVE PATIO
    total_unique_vehicles = st.session_state.df_master['Móvil'].nunique()
    df_registered = st.session_state.df_master[st.session_state.df_master['Técnico'].astype(str).str.strip() != '']
    
    all_mobiles = st.session_state.df_master['Móvil'].unique()
    alistados = []
    for m in all_mobiles:
        m_rows = st.session_state.df_master[st.session_state.df_master['Móvil'] == m]
        if (m_rows['Técnico'].astype(str).str.strip() != '').any():
            alistados.append(m)
        elif ValidationService.check_checklist_filled(st.session_state.df_master, m):
            alistados.append(m)
            
    alistados_count = len(alistados)
    
    con_fugas = 0
    sin_fugas = 0
    for m in alistados:
        m_rows = st.session_state.df_master[st.session_state.df_master['Móvil'] == m]
        completed_rows = m_rows[m_rows['Técnico'].astype(str).str.strip() != '']
        if not completed_rows.empty:
            fuga_val = completed_rows.iloc[-1]['Revisión de Fugas']
        else:
            pending_rows = m_rows[m_rows['Técnico'].astype(str).str.strip() == '']
            fuga_val = pending_rows.iloc[0]['Revisión de Fugas'] if not pending_rows.empty else ""
            
        if fuga_val == 'SI':
            con_fugas += 1
        elif fuga_val == 'NO':
            sin_fugas += 1
    
    if not df_registered.empty:
        fechas_dt = pd.to_datetime(df_registered['Fecha Registro'], errors='coerce')
        if not fechas_dt.isna().all():
            ult_registro = df_registered.loc[fechas_dt.idxmax()]
        else:
            ult_registro = df_registered.iloc[-1]
        lbl_tecnico = f"{ult_registro['Técnico']} ({ult_registro['Fecha Registro']})"
    else:
        lbl_tecnico = "Sin reportes recientes"
        
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        draw_metric_card(f"{alistados_count} de {total_unique_vehicles}", "Móviles Alistados", border_color="#005b94")
    with kpi2:
        draw_metric_card(con_fugas, "Con Fugas Reportadas", border_color="#d9534f", text_color="#d9534f")
    with kpi3:
        draw_metric_card(sin_fugas, "Flota Sin Fugas", border_color="#5cb85c", text_color="#5cb85c")
    with kpi4:
        draw_metric_card(lbl_tecnico, "Último Reporte en Patio", border_color="#f0ad4e", text_color="#f0ad4e", value_style="font-size:14px; padding: 11px 0;")

    st.write("---")
    
    # Mode selection buttons (Alistamiento vs Mantenimiento Correctivo vs Mantenimiento Preventivo)
    if 'active_tipo_novedad' not in st.session_state:
        st.session_state.active_tipo_novedad = None
        
    if st.session_state.active_tipo_novedad is None:
        st.markdown("<p style='font-size: 14px; font-weight: 600; color: #a0b2c6; margin-bottom: 8px; margin-top: 10px;'>Seleccione el Tipo de Novedad a Registrar:</p>", unsafe_allow_html=True)
        col_ali, col_corr, col_prev = st.columns(3)
        with col_ali:
            is_sel = st.session_state.active_tipo_novedad == "ALISTAMIENTO"
            key_ali = f"btn_tipo_alistamiento{'_selected' if is_sel else ''}"
            if st.button(
                "Alistamiento", 
                key=key_ali, 
                use_container_width=True
            ):
                st.session_state.active_tipo_novedad = "ALISTAMIENTO"
                st.session_state.clear_search_on_next_run = True
                st.rerun()
        with col_corr:
            is_sel = st.session_state.active_tipo_novedad == "CORRECTIVO"
            key_corr = f"btn_tipo_correctivo{'_selected' if is_sel else ''}"
            if st.button(
                "Mantenimiento\nCorrectivo", 
                key=key_corr, 
                use_container_width=True
            ):
                st.session_state.active_tipo_novedad = "CORRECTIVO"
                st.session_state.clear_search_on_next_run = True
                st.rerun()
        with col_prev:
            is_sel = st.session_state.active_tipo_novedad == "PREVENTIVO"
            key_prev = f"btn_tipo_preventivo{'_selected' if is_sel else ''}"
            if st.button(
                "Mantenimiento\nPreventivo", 
                key=key_prev, 
                use_container_width=True
            ):
                st.session_state.active_tipo_novedad = "PREVENTIVO"
                st.session_state.clear_search_on_next_run = True
                st.rerun()
    else:
        # Show chosen mode header without duplicate change button
        active_mode = st.session_state.active_tipo_novedad
        tipo_label = {
            "ALISTAMIENTO": "Alistamiento",
            "CORRECTIVO": "Mantenimiento Correctivo",
            "PREVENTIVO": "Mantenimiento Preventivo"
        }.get(active_mode, "")
        
        st.markdown(f"<h3 style='color: #ffffff; margin-top: 5px; margin-bottom: 10px; font-size: 20px; font-weight: 700;'>{tipo_label}</h3>", unsafe_allow_html=True)
        st.write("---")

    if st.session_state.active_tipo_novedad is not None:
        if st.session_state.get('clear_search_on_next_run'):
            st.session_state.main_search_selectbox = None
            st.session_state.clear_search_on_next_run = False

        lista_moviles = sorted(list(st.session_state.df_master['Móvil'].unique()))
        search_query = st.selectbox(
            "Buscar/Seleccionar Móvil en este Patio",
            options=lista_moviles,
            index=None,
            placeholder="Escribe o selecciona el ID del móvil a buscar (ej: CO-0617, Z10-7125)...",
            key="main_search_selectbox"
        )
            
        # Apply filters
        df_filtered = st.session_state.df_master.copy()
        df_filtered = df_filtered[df_filtered['Técnico'].astype(str).str.strip() == '']
        
        if search_query:
            df_filtered = df_filtered[df_filtered['Móvil'] == search_query]
            
        if search_query != st.session_state.prev_search_query:
            st.session_state.prev_search_query = search_query
            CacheService.clear_checklist_widget_state()
            
        # 1. Verification of Search Query (Móvil)
        if search_query:
            # 2. Form Checklist Container (Shown if search_query is active, visible on both desktop & mobile)
            row_data = st.session_state.df_master[
                (st.session_state.df_master['Móvil'] == search_query) &
                (st.session_state.df_master['Técnico'].astype(str).str.strip() == '')
            ]
            
            if row_data is not None and not row_data.empty:
                first_idx = row_data.index[0]
                
                # Sync row's Tipo Novedad with currently selected global active_tipo_novedad for all pending rows of this vehicle
                active_mode = st.session_state.active_tipo_novedad
                for idx in row_data.index:
                    if st.session_state.df_master.at[idx, 'Tipo Novedad'] != active_mode:
                        st.session_state.df_master.at[idx, 'Tipo Novedad'] = active_mode
                        st.session_state.modified_moviles.add(search_query)
                
                row = st.session_state.df_master.loc[first_idx]
                
                # Wrap in a clean container visible on all screen widths
                with st.container(key="active_checklist_form_container"):
                    if active_mode == "ALISTAMIENTO":
                        render_levels_form(row, first_idx, row_data)
                        render_mechanical_form(row, first_idx, row_data)
                        render_electrical_form(row, first_idx, row_data)
                    else:
                        render_maintenance_form(row, first_idx, row_data, active_mode)
            else:
                st.warning("No se encontraron registros pendientes para este móvil.")

        st.write("")
                    
        # SAVE ACTION SECTION
        st.write("---")
        col_btn, col_info = st.columns([1, 1])
        with col_btn:
            btn_guardar = st.button(" Guardar Cambios del Patio", key="btn_save_changes", use_container_width=True)
            
        with col_info:
            num_modificados = len(st.session_state.modified_moviles)
            if num_modificados > 0:
                st.warning(f"⚠️ {num_modificados} móvil(es) modificado(s) sin guardar.")
            else:
                st.info("ℹ️ No hay cambios pendientes por guardar.")
                
        if btn_guardar:
            tecnico_name_val = st.session_state.get('tecnico_name', '').strip()
            if not tecnico_name_val:
                st.error("⚠️ **Error:** Debes ingresar tu **Nombre de Técnico Responsable** para poder guardar los cambios.")
            else:
                mobiles_to_validate = []
                if search_query:
                    mobiles_to_validate = [search_query]
                else:
                    mobiles_to_validate = list(st.session_state.modified_moviles)
                
                # Run checklists validations
                incomplete_mobiles = []
                for movil_id in mobiles_to_validate:
                    if not ValidationService.check_checklist_filled(st.session_state.df_master, movil_id):
                        incomplete_mobiles.append(movil_id)
                
                if incomplete_mobiles:
                    if st.session_state.active_tipo_novedad in ['CORRECTIVO', 'PREVENTIVO']:
                        st.error(f"**Error al guardar:** Para el móvil {', '.join(incomplete_mobiles)}, debes describir las actividades ejecutadas y seleccionar una Observación.")
                    else:
                        st.error(f"**Error al guardar:** Para el móvil {', '.join(incomplete_mobiles)}, debes completar la lista de chequeo (asegúrate de ingresar cantidades numéricas válidas para los fluidos marcados como SI), ingresar las Actividades ejecutadas y seleccionar una Observación.")
                else:
                    if num_modificados > 0:
                        with st.spinner("Guardando cambios en la base de datos..."):
                            try:
                                updated_count = repository.save_patio_changes_custom(
                                    modified_moviles=st.session_state.modified_moviles,
                                    df_master=st.session_state.df_master,
                                    tecnico_name=tecnico_name_val,
                                    patio_name=patio,
                                    host=st.session_state.db_host,
                                    user=st.session_state.db_user,
                                    password=st.session_state.db_password,
                                    db_name=st.session_state.db_name,
                                    port=st.session_state.db_port
                                )
                                # Reset modifications and master
                                st.session_state.modified_moviles = set()
                                if 'df_master' in st.session_state:
                                    del st.session_state.df_master
                                CacheService.clear_checklist_widget_state()
                                st.session_state.clear_search_on_next_run = True
                                st.success(f"✅ ¡Guardado exitoso! Se actualizaron {updated_count} móvil(es) en {patio} ({st.session_state.db_active}).")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Error al guardar datos: {str(ex)}")
                    else:
                        st.session_state.clear_search_on_next_run = True
                        st.info("ℹ️ No se detectaron cambios nuevos para guardar.")
                        st.rerun()
