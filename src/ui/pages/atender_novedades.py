# src/ui/pages/atender_novedades.py
import datetime
import time
import pandas as pd
import streamlit as st
from src.config.settings import PATIOS_CONFIG
from src.styles import draw_metric_card
from src.database.repositories.novedades_repository import NovedadesRepository
from src.constants.choices import TECNICOS_OPCIONES


def draw_bar_chart_with_labels(data_series, x_label, y_label, color):
    """
    Renders a bar chart using Altair with numeric value labels displayed on top of the bars.
    """
    import altair as alt
    if data_series.empty:
        st.info("Sin datos para mostrar.")
        return
        
    # Convert series to dataframe
    df_chart = data_series.reset_index()
    df_chart.columns = [x_label, y_label]
    
    # Check if this is the criticality chart to color bars individually
    if x_label == "Criticidad":
        color_encoding = alt.Color(
            'Criticidad:N',
            scale=alt.Scale(
                domain=['1', '2', '3', 'SIN CRITICIDAD'],
                range=['#ffeb3b', '#ffa500', '#d9534f', '#a0b2c6']
            ),
            legend=None
        )
        bars = alt.Chart(df_chart).mark_bar(
            cornerRadiusTopLeft=4, 
            cornerRadiusTopRight=4
        ).encode(
            x=alt.X(f'{x_label}:N', title=None, sort=None),
            y=alt.Y(f'{y_label}:Q', title=None),
            color=color_encoding
        )
    else:
        # Create Altair bar chart with rounded top corners
        bars = alt.Chart(df_chart).mark_bar(
            color=color, 
            cornerRadiusTopLeft=4, 
            cornerRadiusTopRight=4
        ).encode(
            x=alt.X(f'{x_label}:N', title=None, sort=None),
            y=alt.Y(f'{y_label}:Q', title=None)
        )
    
    # Add text labels on top of the bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='#a0b2c6',
        fontWeight='bold',
        fontSize=11
    ).encode(
        text=f'{y_label}:Q'
    )
    
    # Combine bars and text
    chart = (bars + text).properties(
        height=220
    ).configure_axis(
        grid=False,
        labelColor='#a0b2c6',
        titleColor='#a0b2c6'
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=True)

def draw_trend_chart(data_series, period_label, color):
    """
    Renders a line chart using Altair with numeric value labels displayed on top of the nodes.
    """
    import altair as alt
    if data_series.empty:
        st.info("Sin datos históricos para mostrar.")
        return
        
    df_chart = data_series.reset_index()
    df_chart.columns = [period_label, 'Novedades']
    
    # Base line chart
    line = alt.Chart(df_chart).mark_line(
        color=color,
        strokeWidth=3
    ).encode(
        x=alt.X(f'{period_label}:N', title=None, sort=None),
        y=alt.Y('Novedades:Q', title=None)
    )
    
    # Add dots/points on the line
    points = alt.Chart(df_chart).mark_circle(
        color=color,
        size=80
    ).encode(
        x=alt.X(f'{period_label}:N', sort=None),
        y=alt.Y('Novedades:Q')
    )
    
    # Add text labels on top of the dots
    text = points.mark_text(
        align='center',
        baseline='bottom',
        dy=-10,
        color='#a0b2c6',
        fontWeight='bold',
        fontSize=11
    ).encode(
        text='Novedades:Q'
    )
    
    # Combine line, points, and text
    chart = (line + points + text).properties(
        height=220
    ).configure_axis(
        grid=False,
        labelColor='#a0b2c6',
        titleColor='#a0b2c6'
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=True)

def draw_mobile_novedades_stacked_chart(df_pending_patio):
    """
    Renders a stacked bar chart using Altair showing all mobiles in the patio with pending novelties,
    color-coded by their criticality levels, with a dynamic scrollable width.
    """
    import altair as alt
    if df_pending_patio.empty:
        st.info("Sin datos para mostrar.")
        return

    # Clean criticidad values to strings robustly
    def clean_crit(val):
        if val is None or pd.isna(val):
            return 'SIN CRITICIDAD'
        try:
            num = float(val)
            if num.is_integer():
                return str(int(num))
            return str(num)
        except (ValueError, TypeError):
            s = str(val).strip().upper()
            return s if s else 'SIN CRITICIDAD'

    # Get all mobiles in terms of total pending novelties, sorted by volume descending
    all_mobiles = df_pending_patio['movil'].value_counts().index.tolist()
    if not all_mobiles:
        st.info("Sin móviles para mostrar.")
        return

    df_top = df_pending_patio[df_pending_patio['movil'].isin(all_mobiles)].copy()
    df_top['criticidad_clean'] = df_top['criticidad'].apply(clean_crit)

    # Group by movil and criticidad_clean
    df_grouped = df_top.groupby(['movil', 'criticidad_clean']).size().reset_index(name='Novedades')
    df_grouped['crit_rank'] = df_grouped['criticidad_clean'].map({'3': 3, '2': 2, '1': 1, 'SIN CRITICIDAD': 0})
    df_totals = df_top.groupby('movil').size().reset_index(name='Total')

    # Color scale definition
    color_scale = alt.Scale(
        domain=['1', '2', '3', 'SIN CRITICIDAD'],
        range=['#ffeb3b', '#ffa500', '#d9534f', '#a0b2c6']
    )

    # Calculate dynamic width based on number of mobiles to keep bars readable (60px per bar)
    chart_width = max(300, len(all_mobiles) * 60)

    # Stacked bar chart
    bars = alt.Chart(df_grouped).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4
    ).encode(
        x=alt.X('movil:N', title=None, sort=all_mobiles),
        y=alt.Y('Novedades:Q', title=None, stack='zero'),
        color=alt.Color(
            'criticidad_clean:N',
            scale=color_scale,
            legend=alt.Legend(
                title=None,
                orient='bottom',
                labelColor='#a0b2c6',
                symbolType='square'
            )
        ),
        order=alt.Order('crit_rank:Q', sort='descending'),
        tooltip=[
            alt.Tooltip('movil:N', title='Móvil'),
            alt.Tooltip('criticidad_clean:N', title='Criticidad'),
            alt.Tooltip('Novedades:Q', title='Novedades')
        ]
    )

    # Total label on top of each stack
    text = alt.Chart(df_totals).mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='#a0b2c6',
        fontWeight='bold',
        fontSize=11
    ).encode(
        x=alt.X('movil:N', sort=all_mobiles),
        y=alt.Y('Total:Q'),
        text='Total:Q'
    )

    chart = (bars + text).properties(
        height=220,
        width=chart_width
    ).configure_axis(
        grid=False,
        labelColor='#a0b2c6',
        titleColor='#a0b2c6'
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(chart, use_container_width=False)

def draw_grupo_funcion_scroll_chart(df_pending_patio):
    """
    Renders a bar chart using Altair showing all functional groups with pending novelties in the patio,
    sorted by volume descending, with a dynamic scrollable width.
    """
    import altair as alt
    if df_pending_patio.empty:
        st.info("Sin datos para mostrar.")
        return
        
    df_pending_patio_grupo = df_pending_patio.copy()
    df_pending_patio_grupo['grupo_clean'] = df_pending_patio_grupo['grupo_funcion'].fillna('SIN GRUPO').str.upper().str.strip()
    df_pending_patio_grupo['grupo_clean'] = df_pending_patio_grupo['grupo_clean'].replace('', 'SIN GRUPO')
    
    grupo_counts = df_pending_patio_grupo['grupo_clean'].value_counts()
    if grupo_counts.empty:
        st.info("Sin grupos de función para mostrar.")
        return
        
    df_chart = grupo_counts.reset_index()
    df_chart.columns = ["Grupo Función", "Novedades"]
    
    # Calculate dynamic width based on number of groups (e.g. 70px per group)
    chart_width = max(300, len(grupo_counts) * 70)
    
    # Base bars
    bars = alt.Chart(df_chart).mark_bar(
        color="#005b94", 
        cornerRadiusTopLeft=4, 
        cornerRadiusTopRight=4
    ).encode(
        x=alt.X('Grupo Función:N', title=None, sort=None),
        y=alt.Y('Novedades:Q', title=None),
        tooltip=[
            alt.Tooltip('Grupo Función:N', title='Grupo Función'),
            alt.Tooltip('Novedades:Q', title='Novedades')
        ]
    )
    
    # Add text labels on top of the bars
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='#a0b2c6',
        fontWeight='bold',
        fontSize=11
    ).encode(
        text='Novedades:Q'
    )
    
    chart = (bars + text).properties(
        height=220,
        width=chart_width
    ).configure_axis(
        grid=False,
        labelColor='#a0b2c6',
        titleColor='#a0b2c6'
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(chart, use_container_width=False)

def render_atender_novedades_page():
    """
    Renders the 'Atender Novedades' interactive dashboard and correction interface.
    """
    st.markdown('<h3 style="color: white; font-weight: 700; margin-bottom: 20px;">Novedades</h3>', unsafe_allow_html=True)
    
    # 1. Initialize repository and load raw novelties
    repository = NovedadesRepository()
    try:
        df_raw = repository.load_novedades_volvo_raw(
            host=st.session_state.db_host,
            user=st.session_state.db_user,
            password=st.session_state.db_password,
            db_name=st.session_state.db_name,
            port=st.session_state.db_port
        )
    except Exception as e:
        st.error(f"Error cargando base de datos de novedades: {str(e)}")
        return

    # 2. Map mobiles to patios using PATIOS_CONFIG
    mobile_to_patio = {}
    for patio_name, mobiles in PATIOS_CONFIG.items():
        for m in mobiles:
            mobile_to_patio[m] = patio_name
            
    df_raw['patio'] = df_raw['movil'].map(mobile_to_patio).fillna('Desconocido')
    
    # Standardize state naming for filtering
    df_raw['estado_upper'] = df_raw['estado'].fillna('PENDIENTE').str.upper().str.strip()
    
    # Split pending and corrected
    df_pending = df_raw[df_raw['estado_upper'] == 'PENDIENTE']
    df_corrected = df_raw[df_raw['estado_upper'] == 'CORREGIDA']
    
    # 3. Overall KPI Metrics (Hidden per user request)
    total_count = len(df_raw)
    pending_count = len(df_pending)
    corrected_count = len(df_corrected)
    
    # col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    # with col_kpi1:
    #     draw_metric_card(str(total_count), "Total Novedades", border_color="#005b94")
    # with col_kpi2:
    #     draw_metric_card(str(pending_count), "Novedades Pendientes", border_color="#ffa500", text_color="#ffa500")
    # with col_kpi3:
    #     draw_metric_card(str(corrected_count), "Novedades Corregidas", border_color="#2e7d32", text_color="#2e7d32")
    
    # st.write("")

    # Initialize selected patio in session state if not present
    if 'atender_selected_patio' not in st.session_state:
        st.session_state.atender_selected_patio = None

    # ==================== VISTA GLOBAL (DASHBOARD) ====================
    if st.session_state.atender_selected_patio is None:
        if pending_count == 0:
            st.success("🟢 **¡Felicidades!** No hay novedades pendientes por atender en el sistema en este momento.")
        else:
            col_chart1, col_chart2, col_chart3 = st.columns(3)
            
            with col_chart1:
                st.markdown('<h4 style="color: white; font-weight: 600; font-size: 16px; margin-bottom: 10px;">Novedades Pendientes por Patio</h4>', unsafe_allow_html=True)
                with st.container(key="chart_card_patio"):
                    # Count by patio and show
                    patio_counts = df_pending['patio'].value_counts()
                    draw_bar_chart_with_labels(patio_counts, "Patio", "Novedades", "#ffa500")
                    
            with col_chart2:
                st.markdown('<h4 style="color: white; font-weight: 600; font-size: 16px; margin-bottom: 10px;">Novedades Pendientes por Criticidad</h4>', unsafe_allow_html=True)
                with st.container(key="chart_card_criticidad"):
                    # Clean and order criticality to ensure '1', '2', '3' are always shown
                    df_pending_crit = df_pending.copy()
                    
                    def clean_criticidad(val):
                        if val is None or pd.isna(val):
                            return 'SIN CRITICIDAD'
                        try:
                            num = float(val)
                            if num.is_integer():
                                return str(int(num))
                            return str(num)
                        except (ValueError, TypeError):
                            s = str(val).strip().upper()
                            return s if s else 'SIN CRITICIDAD'
                            
                    df_pending_crit['criticidad_clean'] = df_pending_crit['criticidad'].apply(clean_criticidad)
                    crit_counts = df_pending_crit['criticidad_clean'].value_counts()
                    
                    logical_order = ['1', '2', '3']
                    all_indices = logical_order + [i for i in crit_counts.index if i not in logical_order]
                    crit_counts = crit_counts.reindex(all_indices).fillna(0).astype(int)
                    
                    draw_bar_chart_with_labels(crit_counts, "Criticidad", "Novedades", "#d9534f")

            with col_chart3:
                st.markdown('<h4 style="color: white; font-weight: 600; font-size: 16px; margin-bottom: 10px;">Novedades Pendientes por Grupo Función</h4>', unsafe_allow_html=True)
                with st.container(key="chart_card_grupo"):
                    # Clean and count by functional group
                    df_pending_grupo = df_pending.copy()
                    df_pending_grupo['grupo_clean'] = df_pending_grupo['grupo_funcion'].fillna('SIN GRUPO').str.upper().str.strip()
                    grupo_counts = df_pending_grupo['grupo_clean'].value_counts()
                    
                    draw_bar_chart_with_labels(grupo_counts, "Grupo Función", "Novedades", "#005b94")
                    
            st.write("")
            
            # Historical trend chart block
            st.markdown('<h4 style="color: white; font-weight: 600; font-size: 16px; margin-top: 15px; margin-bottom: 10px;">Historial de Novedades Registradas en el Tiempo</h4>', unsafe_allow_html=True)
            with st.container(key="chart_card_trend"):
                col_t1, col_t2 = st.columns([1.5, 8.5])
                with col_t1:
                    trend_mode = st.radio(
                        "Agrupar por:",
                        options=["Meses", "Semanas"],
                        key="trend_grouping_mode",
                        horizontal=False
                    )
                with col_t2:
                    df_raw['fecha_dt'] = pd.to_datetime(df_raw['fecha_novedad'], errors='coerce')
                    df_time = df_raw.dropna(subset=['fecha_dt'])
                    
                    if df_time.empty:
                        st.info("No hay datos de fecha válidos para mostrar el histórico.")
                    else:
                        if trend_mode == "Meses":
                            df_time['periodo'] = df_time['fecha_dt'].dt.to_period('M').astype(str)
                            period_lbl = "Mes"
                        else:
                            df_time['periodo'] = df_time['fecha_dt'].dt.to_period('W').apply(lambda r: r.start_time.strftime('%Y-%m-%d'))
                            period_lbl = "Semana (Inicia)"
                        
                        trend_counts = df_time.groupby('periodo').size().sort_index()
                        draw_trend_chart(trend_counts, period_lbl, "#007ac5")
                        
            st.write("")
            

        # Interactive Patios Grid for Entering/Drill-down
        st.markdown('<h4 style="color: white; font-weight: 600; font-size: 16px; margin-top: 25px; margin-bottom: 15px;">Patio</h4>', unsafe_allow_html=True)
        patios_keys = list(PATIOS_CONFIG.keys())
        
        # Divide into rows of 4 columns
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        col_p5, col_p6, col_p7, _ = st.columns(4)
        p_cols = [col_p1, col_p2, col_p3, col_p4, col_p5, col_p6, col_p7]
        
        for idx, p_name in enumerate(patios_keys):
            p_pending_cnt = len(df_pending[df_pending['patio'] == p_name])
            with p_cols[idx]:
                btn_label = f"🏢 {p_name}\n({p_pending_cnt} Pendientes)"
                if st.button(btn_label, key=f"btn_patio_atender_{p_name}", use_container_width=True):
                    st.session_state.atender_selected_patio = p_name
                    st.rerun()

    # ==================== VISTA DE PATIO (DRILL-DOWN) ====================
    else:
        selected_patio = st.session_state.atender_selected_patio
        
        # Back Button
        if st.button("Volver", key="btn_back_to_dashboard"):
            st.session_state.atender_selected_patio = None
            st.rerun()
            
        st.markdown(f'<h3 style="color: white; font-weight: 700; margin-top: 10px;">Patio: {selected_patio}</h3>', unsafe_allow_html=True)
        
        df_pending_patio = df_pending[df_pending['patio'] == selected_patio]
        pending_patio_count = len(df_pending_patio)
        
        if pending_patio_count == 0:
            st.success(f"🟢 **¡Todo al día!** No hay novedades pendientes por atender en el patio **{selected_patio}**.")
        else:
            # Layout local stats
            col_p_kpi1, col_p_kpi2 = st.columns([1.5, 2.5])
            with col_p_kpi1:
                draw_metric_card(str(pending_patio_count), f"Pendientes en {selected_patio}", border_color="#ffa500", text_color="#ffa500")
                
            # Local charts layout
            col_pl_chart1, col_pl_chart2, col_pl_chart3 = st.columns(3)
            with col_pl_chart1:
                st.markdown('<h5 style="color: white; font-weight: 600; font-size: 14px; margin-bottom: 5px;">Criticidad en este Patio</h5>', unsafe_allow_html=True)
                with st.container(key="chart_card_local_crit"):
                    df_pending_patio_crit = df_pending_patio.copy()
                    
                    def clean_criticidad_local(val):
                        if val is None or pd.isna(val):
                            return 'SIN CRITICIDAD'
                        try:
                            num = float(val)
                            if num.is_integer():
                                return str(int(num))
                            return str(num)
                        except (ValueError, TypeError):
                            s = str(val).strip().upper()
                            return s if s else 'SIN CRITICIDAD'
                            
                    df_pending_patio_crit['criticidad_clean'] = df_pending_patio_crit['criticidad'].apply(clean_criticidad_local)
                    crit_local = df_pending_patio_crit['criticidad_clean'].value_counts()
                    
                    logical_order = ['1', '2', '3']
                    all_indices = logical_order + [i for i in crit_local.index if i not in logical_order]
                    crit_local = crit_local.reindex(all_indices).fillna(0).astype(int)
                    draw_bar_chart_with_labels(crit_local, "Criticidad", "Novedades", "#d9534f")
                
            with col_pl_chart2:
                st.markdown('<h5 style="color: white; font-weight: 600; font-size: 14px; margin-bottom: 5px;">Móviles con más Novedades</h5>', unsafe_allow_html=True)
                with st.container(key="chart_card_local_movil"):
                    draw_mobile_novedades_stacked_chart(df_pending_patio)
                
            with col_pl_chart3:
                st.markdown('<h5 style="color: white; font-weight: 600; font-size: 14px; margin-bottom: 5px;">Grupo Función en este Patio</h5>', unsafe_allow_html=True)
                with st.container(key="chart_card_local_grupo"):
                    draw_grupo_funcion_scroll_chart(df_pending_patio)
                
        # "Atender Novedades" Form card (styled with fine white border)
        st.markdown('<h4 style="color: white; font-weight: 700; margin-top: 25px; margin-bottom: 10px;">Atender Novedades</h4>', unsafe_allow_html=True)
        
        with st.container(key="atender_form_container"):
            # Clean criticidad values to strings robustly to filter mobiles correctly
            def clean_crit_val(val):
                if val is None or pd.isna(val):
                    return 'SIN CRITICIDAD'
                try:
                    num = float(val)
                    if num.is_integer():
                        return str(int(num))
                    return str(num)
                except (ValueError, TypeError):
                    s = str(val).strip().upper()
                    return s if s else 'SIN CRITICIDAD'

            df_pending_patio_clean = df_pending_patio.copy()
            df_pending_patio_clean['criticidad_clean'] = df_pending_patio_clean['criticidad'].apply(clean_crit_val)

            # 1. Criticality filter selectbox
            selected_criticidad = st.selectbox(
                "Filtrar por Nivel de Criticidad",
                options=["Todos", "1", "2", "3"],
                index=0,
                key="atender_criticidad_filter"
            )

            # Apply criticality filter to the mobile options
            if selected_criticidad != "Todos":
                df_filtered_patio = df_pending_patio_clean[df_pending_patio_clean['criticidad_clean'] == selected_criticidad]
            else:
                df_filtered_patio = df_pending_patio_clean

            pending_mobiles_in_patio = sorted(list(df_filtered_patio['movil'].unique()))
            
            if not pending_mobiles_in_patio:
                if selected_criticidad != "Todos":
                    st.info(f"No hay móviles con novedades de criticidad '{selected_criticidad}' en este patio.")
                else:
                    st.write("No hay móviles con novedades pendientes en este patio.")
            else:
                # Spacer
                st.write("")
                
                # 2. Mobile selector selectbox
                selected_movil = st.selectbox(
                    "Selecciona un Móvil para Atender",
                    options=pending_mobiles_in_patio,
                    index=None,
                    placeholder="Seleccionar...",
                    key="atender_movil_selectbox"
                )
                
                if selected_movil is not None:
                    # Filter the mobile novelties based on chosen criticality level
                    df_mob_pending_all = df_pending_patio_clean[df_pending_patio_clean['movil'] == selected_movil]
                    if selected_criticidad != "Todos":
                        df_mob_pending = df_mob_pending_all[df_mob_pending_all['criticidad_clean'] == selected_criticidad]
                        st.info(f"ℹ️ Mostrando únicamente novedades con **Criticidad {selected_criticidad}**. Para ver todas las novedades del móvil, selecciona **'Todos'** en el filtro de criticidad superior.")
                    else:
                        df_mob_pending = df_mob_pending_all
                    
                    if df_mob_pending.empty:
                        st.success(f"No hay novedades pendientes para el móvil {selected_movil} con la criticidad seleccionada.")
                    else:
                        st.write(f"Se encontraron **{len(df_mob_pending)}** novedades pendientes para el móvil **{selected_movil}**:")
                        st.write("---")
                        
                        resoluciones = []
                        
                        for idx, row in df_mob_pending.iterrows():
                            db_id = row['id']
                            novedad_text = row['novedad']
                            obs_text = row['observaciones']
                            criticidad_val = row['criticidad']
                            fecha_nov_val = row['fecha_novedad']
                            
                            # Map criticality to color dynamically
                            try:
                                crit_num = float(criticidad_val)
                                if crit_num.is_integer():
                                    crit_str = str(int(crit_num))
                                else:
                                    crit_str = str(crit_num)
                            except (ValueError, TypeError):
                                crit_str = str(criticidad_val).strip() if criticidad_val is not None else ""
                                
                            if crit_str == "3":
                                badge_color = "#d9534f" # Red
                                badge_text_color = "#ffffff"
                                border_left_color = "#d9534f"
                                badge_label = "Criticidad 3"
                            elif crit_str == "2":
                                badge_color = "#ffa500" # Orange
                                badge_text_color = "#ffffff"
                                border_left_color = "#ffa500"
                                badge_label = "Criticidad 2"
                            elif crit_str == "1":
                                badge_color = "#ffeb3b" # Lighter Yellow
                                badge_text_color = "#122135"
                                border_left_color = "#ffeb3b"
                                badge_label = "Criticidad 1"
                            else:
                                badge_color = "#a0b2c6" # Gray
                                badge_text_color = "#ffffff"
                                border_left_color = "#a0b2c6"
                                badge_label = f"Criticidad: {criticidad_val}" if criticidad_val else "Sin Criticidad"
                            
                            # Detail row container with thicker 8px left border to display as a prominent color bar
                            st.markdown(f"""
                            <div style="background-color: #1a293b; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 8px solid {border_left_color};">
                                <span style="background-color: {badge_color}; padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 11px; color: {badge_text_color};">{badge_label}</span>
                                <span style="color: #8899a6; font-size: 12px; margin-left: 10px;">Reportado el: {fecha_nov_val}</span>
                                <p style="margin: 8px 0 4px 0; font-weight: bold; font-size: 15px; color: white;">Novedad: {novedad_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_i1, col_i2, col_i3, col_i4 = st.columns([2.0, 2.0, 1.0, 1.2])
                            
                            with col_i1:
                                tech_select = st.selectbox(
                                    "Nombre del Técnico",
                                    options=[""] + TECNICOS_OPCIONES,
                                    key=f"tech_{db_id}"
                                )
                                
                            with col_i2:
                                insumos_input = st.text_input(
                                    "Insumos / Parte Números",
                                    placeholder="Ej: N/A, 982103",
                                    key=f"insumos_{db_id}"
                                )
                                
                            with col_i3:
                                cantidad_input = st.text_input(
                                    "Cantidad",
                                    placeholder="Ej: 1, N/A",
                                    key=f"cantidad_{db_id}"
                                )
                                
                            with col_i4:
                                st.markdown("<p style='font-size: 14px; margin-bottom: 12px; font-weight: bold; color: white;'>Actividad Resuelta</p>", unsafe_allow_html=True)
                                is_resolved = st.checkbox(
                                    "Resuelta",
                                    key=f"check_{db_id}",
                                    label_visibility="collapsed"
                                )
                                
                            resoluciones.append({
                                'id': db_id,
                                'tecnico': tech_select,
                                'insumos': insumos_input,
                                'cantidad': cantidad_input,
                                'resolved': is_resolved,
                                'novedad': novedad_text
                            })
                            st.write("---")
                            
                        # Save action button
                        if st.button("Guardar", key="btn_save_corrections"):
                            invalid_tech = []
                            invalid_insumos = []
                            invalid_cantidad = []
                            valid_updates = []
                            
                            for res in resoluciones:
                                if res['resolved']:
                                    has_error = False
                                    if not res['tecnico'].strip():
                                        invalid_tech.append(res['novedad'])
                                        has_error = True
                                    if not res['insumos'].strip():
                                        invalid_insumos.append(res['novedad'])
                                        has_error = True
                                    if not res['cantidad'].strip():
                                        invalid_cantidad.append(res['novedad'])
                                        has_error = True
                                        
                                    if not has_error:
                                        valid_updates.append(res)
                                        
                            error_triggered = False
                            if invalid_tech:
                                st.error(f"**Error:** Debes seleccionar el técnico encargado para las siguientes novedades: {', '.join(invalid_tech)}")
                                error_triggered = True
                            if invalid_insumos:
                                st.error(f"**Error:** Debes indicar los insumos utilizados (o escribir 'N/A') para las siguientes novedades: {', '.join(invalid_insumos)}")
                                error_triggered = True
                            if invalid_cantidad:
                                st.error(f"**Error:** Debes indicar la cantidad (o escribir 'N/A') para las siguientes novedades: {', '.join(invalid_cantidad)}")
                                error_triggered = True
                                
                            if error_triggered:
                                pass
                            elif not valid_updates:
                                st.warning("⚠️ No has marcado ninguna novedad como 'Resuelta'. Selecciona el checkbox (la paloma) de la novedad que deseas corregir.")
                            else:
                                success_count = 0
                                today_str = datetime.date.today().strftime('%Y-%m-%d')
                                
                                # Perform updates
                                for res in valid_updates:
                                    try:
                                        repository.resolver_novedad(
                                            host=st.session_state.db_host,
                                            user=st.session_state.db_user,
                                            password=st.session_state.db_password,
                                            db_name=st.session_state.db_name,
                                            port=st.session_state.db_port,
                                            db_id=res['id'],
                                            tecnico_correccion=res['tecnico'],
                                            insumos_usados=res['insumos'],
                                            cantidad=res['cantidad'],
                                            fecha_correccion=today_str
                                        )
                                        success_count += 1
                                    except PermissionError as pe:
                                        st.error(str(pe))
                                    except Exception as e:
                                        st.error(f"Error resolviendo novedad '{res['novedad']}': {str(e)}")
                                        
                                if success_count > 0:
                                    st.success(f"🎉 ¡Se han registrado {success_count} novedades como **CORREGIDAS** con éxito!")
                                    time.sleep(1.2)
                                    st.rerun()
