# src/ui/pages/exportar_datos.py
import datetime
import pandas as pd
import streamlit as st
from src.config.settings import PATIOS_CONFIG
from src.styles import draw_metric_card
from src.database.repositories.novedades_repository import NovedadesRepository
from src.services.export_service import ExportService

def draw_downloads_section(df_filtered, patio_select, start_date, end_date, estado_novedades="Todos"):
    """
    Generates and displays the download buttons for complete ZIP report,
    individual reports (Niveles, Mechanical, Electrical) in Excel (Consorcio Express),
    and the historical novelty report in Excel (Volvo format).
    Uses ExportService for byte generation.
    """
    st.write("")
    
    st.markdown('<h4 style="color: white; font-weight: 600; font-size: 18px; margin-bottom: 15px; margin-top: 15px;"> Consorcio Express</h4>', unsafe_allow_html=True)
    
    with st.container(key="export_downloads_container"):
        # 1. Master ZIP Download Button
        zip_data = None
        try:
            zip_data = ExportService.generate_zip_report(
                df_filtered=df_filtered,
                patio_select=patio_select,
                start_date=start_date,
                default_tecnico=st.session_state.get('tecnico_name', '')
            )
        except Exception as e:
            st.error(f"Error generando reporte completo (ZIP): {str(e)}")
            
        if zip_data:
            st.download_button(
                label="Alistamiento consolidado",
                data=zip_data,
                file_name=f"alistamiento_completo_CEXP_{patio_select.replace(' ', '_')}_{datetime.date.today()}.zip",
                mime="application/zip",
                use_container_width=True,
                key="btn_download_all_zip"
            )
            st.write("") # Margin spacer
            
        # 2. Individual Excel Buttons
        col_xlsx_niv, col_xlsx_mec, col_xlsx_elec = st.columns(3)
        
        with col_xlsx_niv:
            excel_data_niv = None
            try:
                excel_data_niv = ExportService.generate_xlsx(
                    df_filtered=df_filtered,
                    patio_select=patio_select,
                    start_date=start_date,
                    report_type="niveles",
                    default_tecnico=st.session_state.get('tecnico_name', '')
                )
            except Exception as e:
                st.error(f"Error generando Excel de Niveles: {str(e)}")
                
            if excel_data_niv:
                st.download_button(
                    label="Alistamiento Niveles - CEXP",
                    data=excel_data_niv,
                    file_name=f"alistamiento_niveles_CEXP_{patio_select.replace(' ', '_')}_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_download_niv"
                )

        with col_xlsx_mec:
            excel_data_mec = None
            try:
                excel_data_mec = ExportService.generate_xlsx(
                    df_filtered=df_filtered,
                    patio_select=patio_select,
                    start_date=start_date,
                    report_type="mecanico",
                    default_tecnico=st.session_state.get('tecnico_name', '')
                )
            except Exception as e:
                st.error(f"Error generando Excel Mecánico: {str(e)}")
                
            if excel_data_mec:
                st.download_button(
                    label="Alistamiento Mecánico - CEXP",
                    data=excel_data_mec,
                    file_name=f"alistamiento_mecanico_CEXP_{patio_select.replace(' ', '_')}_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_download_mec"
                )
                
        with col_xlsx_elec:
            excel_data_elec = None
            try:
                excel_data_elec = ExportService.generate_xlsx(
                    df_filtered=df_filtered,
                    patio_select=patio_select,
                    start_date=start_date,
                    report_type="electrico",
                    default_tecnico=st.session_state.get('tecnico_name', '')
                )
            except Exception as e:
                st.error(f"Error generando Excel Eléctrico: {str(e)}")
                
            if excel_data_elec:
                st.download_button(
                    label="Alistamiento Eléctrico - CEXP",
                    data=excel_data_elec,
                    file_name=f"alistamiento_electrico_CEXP_{patio_select.replace(' ', '_')}_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="btn_download_elec"
                )

    # 3. Volvo Novelty Export Section
    st.markdown('<h4 style="color: white; font-weight: 600; font-size: 18px; margin-bottom: 15px; margin-top: 25px;"> Volvo</h4>', unsafe_allow_html=True)
    
    with st.container(key="export_volvo_container"):
        repository = NovedadesRepository()
        df_nov_all = pd.DataFrame()
        try:
            df_nov_all = repository.load_novedades_volvo(
                host=st.session_state.db_host,
                user=st.session_state.db_user,
                password=st.session_state.db_password,
                db_name=st.session_state.db_name,
                port=st.session_state.db_port
            )
        except Exception as e:
            st.error(f"Error cargando base de datos de novedades Volvo: {str(e)}")
            
        df_nov_filtered = pd.DataFrame()
        if not df_nov_all.empty:
            df_nov_filtered = df_nov_all.copy()
            
            # Filter by Patio
            if patio_select != "Todos los Patios":
                allowed_moviles = PATIOS_CONFIG.get(patio_select, [])
                df_nov_filtered = df_nov_filtered[df_nov_filtered['ID'].isin(allowed_moviles)]
                
            # Filter by Date
            if start_date and end_date:
                df_nov_filtered['Fecha_Parsed'] = pd.to_datetime(df_nov_filtered['FECHA NOVEDAD'], errors='coerce')
                df_nov_filtered = df_nov_filtered[
                    (df_nov_filtered['Fecha_Parsed'].dt.date >= start_date) & 
                    (df_nov_filtered['Fecha_Parsed'].dt.date <= end_date)
                ]
                df_nov_filtered = df_nov_filtered.drop(columns=['Fecha_Parsed'])
                
            # Filter by novelty state (Volvo only)
            if estado_novedades != "Todos":
                df_nov_filtered = df_nov_filtered[
                    df_nov_filtered['ESTADO'].str.upper() == estado_novedades.upper()
                ]
                
        # Always generate the Volvo Excel sheet (even if empty, it returns the template with headers/logo)
        excel_data_volvo = None
        try:
            excel_data_volvo = ExportService.generate_novedades_volvo_xlsx(df_nov_filtered)
        except Exception as e:
            st.error(f"Error generando Excel en formato Volvo: {str(e)}")
            
        if excel_data_volvo is not None:
            st.download_button(
                label="Historial de Novedades",
                data=excel_data_volvo,
                file_name=f"historial_novedades_VOLVO_{patio_select.replace(' ', '_')}_{datetime.date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="btn_download_volvo_novedades"
            )
            if df_nov_filtered.empty:
                st.info("ℹ️ No se encontraron novedades registradas que coincidan con los filtros seleccionados (la descarga contendrá el formato de planilla vacío).")
        else:
            st.error("Error: No se pudo preparar el archivo de descarga de Volvo.")

def render_export_page():
    """
    Renders the reporting query filters, KPI metric cards, preview dataframe,
    and download buttons.
    """
    st.subheader(" Exportación de Novedades y Reportes")
    st.write("Consulta y exporta el historial de novedades de todos los patios de la flota.")
    
    repository = NovedadesRepository()
    
    # Load all records
    with st.spinner("Cargando base de datos completa..."):
        try:
            df_all = repository.load_all_data(
                host=st.session_state.db_host,
                user=st.session_state.db_user,
                password=st.session_state.db_password,
                db_name=st.session_state.db_name,
                port=st.session_state.db_port
            )
        except Exception as e:
            st.error(f"Error al cargar los datos de novedades: {str(e)}")
            return
  
    if df_all.empty:
        st.info("ℹ️ No hay registros guardados en la base de datos actualmente.")
        return

    # Visual container placeholders
    kpis_placeholder = st.container()
    filters_placeholder = st.container()
    downloads_placeholder = st.container()

    # Renders Query Filters Section
    with filters_placeholder:
        st.markdown('<h4 class="export-filters-title" style="color: white; font-weight: 600; font-size: 18px; margin-bottom: 15px;"> Filtros de Consulta</h4>', unsafe_allow_html=True)
        with st.container(key="export_filters_container"):
            patios_options = ["Todos los Patios"] + list(PATIOS_CONFIG.keys())
            patio_select = st.selectbox(" Centro de Operaciones (Patio)", options=patios_options)
            
            df_all['Fecha_Parsed'] = pd.to_datetime(df_all['Fecha Registro'], errors='coerce')
            min_dt = df_all['Fecha_Parsed'].min()
            max_dt = df_all['Fecha_Parsed'].max()
            
            today = datetime.date.today()
            start_def = today - datetime.timedelta(days=30)
            end_def = today
            
            if pd.notnull(min_dt):
                min_val = min_dt.date()
            else:
                min_val = datetime.date(2025, 1, 1)
                
            if pd.notnull(max_dt):
                max_val = max_dt.date()
            else:
                max_val = today + datetime.timedelta(days=1)
                
            if min_val > start_def:
                start_def = min_val
                
            date_mode = st.radio(
                " Filtro de Fecha",
                options=["Día Único", "Rango de Fechas"],
                horizontal=True,
                index=1
            )
            
            if date_mode == "Día Único":
                try:
                    date_val = st.date_input(
                        " Seleccione Fecha (Registro)",
                        value=today,
                        min_value=min_val,
                        max_value=max_val + datetime.timedelta(days=1)
                    )
                except Exception:
                    date_val = st.date_input(
                        " Seleccione Fecha (Registro)",
                        value=today
                    )
            else:
                try:
                    date_val = st.date_input(
                        " Rango de Fechas (Registro)",
                        value=(start_def, end_def),
                        min_value=min_val,
                        max_value=max_val + datetime.timedelta(days=1)
                    )
                except Exception:
                    date_val = st.date_input(
                        " Rango de Fechas (Registro)",
                        value=(today - datetime.timedelta(days=30), today)
                    )
            
            estado_novedades = st.selectbox(
                " Estado Novedades (Solo Volvo)",
                options=["Todos", "Pendiente", "Ejecutada"],
                key="export_estado_novedades"
            )

    # Filter operations
    df_filtered = df_all.copy()
    
    if patio_select != "Todos los Patios":
        df_filtered = df_filtered[df_filtered['Patio'] == patio_select]
        
    start_date, end_date = None, None
    if date_mode == "Rango de Fechas":
        if isinstance(date_val, (tuple, list)):
            if len(date_val) == 2:
                start_date, end_date = date_val
            elif len(date_val) == 1:
                start_date = date_val[0]
                end_date = date_val[0]
        else:
            start_date = date_val
            end_date = date_val
    else:
        start_date = date_val
        end_date = date_val
        
    if start_date and end_date:
        matching_date_mask = (
            (df_filtered['Fecha_Parsed'].dt.date >= start_date) & 
            (df_filtered['Fecha_Parsed'].dt.date <= end_date)
        )
        df_filtered = df_filtered[matching_date_mask]
        
    if 'Fecha_Parsed' in df_filtered.columns:
        df_filtered = df_filtered.drop(columns=['Fecha_Parsed'])
    if 'Fecha_Parsed' in df_all.columns:
        df_all = df_all.drop(columns=['Fecha_Parsed'])

    # Calculate active patio fleet sizes
    if patio_select != "Todos los Patios":
        configured_mobiles = PATIOS_CONFIG.get(patio_select, [])
    else:
        configured_mobiles = []
        for mob_list in PATIOS_CONFIG.values():
            configured_mobiles.extend(mob_list)

    total_unique_vehicles = len(configured_mobiles)
    con_fugas = len(df_filtered[df_filtered['Revisión de Fugas'] == 'SI'])
    con_obs = len(df_filtered[(df_filtered['Observaciones'] != '') & (df_filtered['Observaciones'].notnull())])
    
    # Render KPI metrics cards
    with kpis_placeholder:
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            draw_metric_card(total_unique_vehicles, "Total Flota", border_color="#005b94")
        with kpi2:
            draw_metric_card(con_fugas, "Con Fugas Encontrados", border_color="#d9534f", text_color="#d9534f")
        with kpi3:
            draw_metric_card(con_obs, "Con Observaciones / Reportes", border_color="#f0ad4e", text_color="#f0ad4e")

    # Preview section removed as requested

    # Render Downloads section
    with downloads_placeholder:
        draw_downloads_section(df_filtered, patio_select, start_date, end_date, estado_novedades)
