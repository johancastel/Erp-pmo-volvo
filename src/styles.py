# src/styles.py
import streamlit as st
import base64
import os

_cached_logo = None

def get_base64_logo():
    """Obtiene la representación en base64 del logo de Volvo."""
    global _cached_logo
    if _cached_logo is not None:
        return _cached_logo
        
    logo_path = os.path.join(os.path.dirname(__file__), "volvo_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                data = f.read()
            _cached_logo = base64.b64encode(data).decode()
            return _cached_logo
        except Exception:
            pass
    return ""

def inject_custom_css():
    """Inyecta los estilos CSS corporativos de Volvo (Oscuro y Premium) en la app."""
    logo_base64 = get_base64_logo()
    css = """
    <style>
        /* Estilo de la aplicación principal */
        .stApp {
            background-color: #0b1320;
            color: #f4f6f9;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        
        /* Encabezado Principal */
        .volvo-header {
            background-color: #122135; /* Azul Volvo Oscuro */
            padding: 25px;
            color: white;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #005b94;
        }
        .volvo-header-left h1 {
            margin: 0;
            font-size: 26px;
            font-weight: 700;
            letter-spacing: 1px;
            color: white !important;
        }
        .volvo-header-left p {
            margin: 5px 0 0 0;
            font-size: 14px;
            color: #a0b2c6;
        }
        .volvo-logo-text {
            font-size: 28px;
            font-weight: 900;
            letter-spacing: 3px;
            color: white;
            border: 2px solid white;
            padding: 5px 15px;
            font-family: 'Times New Roman', serif;
        }
        
        /* Estilo de Tarjetas Métricas */
        .metric-card {
            background-color: #152232;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #005b94;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            text-align: center;
            transition: transform 0.2s;
        }
        .metric-card:hover {
            transform: translateY(-2px);
        }
        .metric-val {
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 5px;
        }
        .metric-lbl {
            font-size: 13px;
            color: #a0b2c6;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        /* Tarjetas de Patio Interactivas como st.button (Estilo Premium Volvo Oscuro) */
        div[class*="st-key-btn_patio_"] div.stButton > button {
            background-color: #152232 !important;
            color: #ffffff !important;
            border-left: 5px solid #005b94 !important;
            border-top: none !important;
            border-right: none !important;
            border-bottom: none !important;
            border-radius: 8px !important;
            padding: 22px !important;
            height: 130px !important;
            width: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            cursor: pointer !important;
            transition: all 0.2s ease-in-out !important;
            white-space: pre-wrap !important;
            line-height: 1.6 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            text-transform: none !important;
            letter-spacing: 0.5px !important;
        }
        div[class*="st-key-btn_patio_"] div.stButton > button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0 8px 20px rgba(0, 91, 148, 0.3) !important;
            background-color: #1c2e47 !important;
            border-left-color: #007ac5 !important;
            color: #ffffff !important;
        }
        
        /* Tarjetas de Tipo de Novedad Interactivas (Estilo Premium Volvo Oscuro igual a patios) */
        div[class*="st-key-btn_tipo_"] div.stButton > button {
            background-color: #152232 !important;
            color: #ffffff !important;
            border-left: 5px solid #2d3f56 !important; /* Borde grisáceo secundario */
            border-top: none !important;
            border-right: none !important;
            border-bottom: none !important;
            border-radius: 8px !important;
            padding: 22px !important;
            height: 140px !important;
            width: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            cursor: pointer !important;
            transition: all 0.2s ease-in-out !important;
            white-space: pre-wrap !important;
            line-height: 1.4 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            text-transform: none !important;
        }
        div[class*="st-key-btn_tipo_"] div.stButton > button:hover {
            transform: scale(1.03) !important;
            box-shadow: 0 8px 20px rgba(0, 91, 148, 0.3) !important;
            background-color: #1c2e47 !important;
            border-left-color: #007ac5 !important;
            color: #ffffff !important;
        }
        
        /* Tarjeta de Tipo de Novedad Seleccionada (Activa) */
        div[class*="st-key-btn_tipo_"][class*="_selected"] div.stButton > button {
            border-left-color: #007ac5 !important; /* Borde azul vivo activo */
            background-color: #1c2e47 !important;
            box-shadow: 0 8px 20px rgba(0, 122, 197, 0.4) !important;
        }
        
        /* Contenedor de filtros de exportación encapsulado */
        div[class*="st-key-export_filters_container"] {
            border: 1.5px solid #005b94 !important;
            border-radius: 8px !important;
            padding: 20px !important;
            background-color: transparent !important;
            margin-bottom: 25px !important;
        }
        
        /* Estilo del título de filtros fuera del cuadro */
        .export-filters-title {
            margin-top: 15px !important;
            margin-bottom: 10px !important;
        }
        
        /* Configuración barra lateral */
        section[data-testid="stSidebar"] {
            background-color: #04080e !important; /* Negro azulado muy oscuro */
        }
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #ffffff !important;
        }
        
        /* Estilo de ítems de navegación lateral */
        .nav-item-active {
            background-color: #122135;
            padding: 12px 15px;
            border-radius: 6px;
            color: white !important;
            font-weight: 600;
            margin-bottom: 8px;
            border-left: 4px solid #005b94;
            display: flex;
            align-items: center;
        }
        .nav-item-disabled {
            padding: 10px 15px;
            color: #5d6e7c !important;
            margin-bottom: 8px;
            font-size: 14px;
            display: flex;
            align-items: center;
            cursor: not-allowed;
        }
        .nav-icon {
            margin-right: 10px;
            font-size: 16px;
        }
        
        /* Botones de acción */
        div.stButton > button:first-child {
            background-color: #005b94;
            color: white;
            border-radius: 6px;
            padding: 12px 30px;
            font-weight: 600;
            border: 2px solid #005b94;
            font-size: 16px;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        div.stButton > button:first-child:hover {
            background-color: #007ac5;
            border-color: #007ac5;
            color: white;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        
        /* Botón de retroceso */
        .back-btn-container div.stButton > button:first-child {
            background-color: transparent !important;
            color: #a0b2c6 !important;
            border: 2px solid #a0b2c6 !important;
            width: auto !important;
            padding: 6px 15px !important;
            font-size: 14px !important;
            box-shadow: none !important;
        }
        .back-btn-container div.stButton > button:first-child:hover {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #ffffff !important;
            border-color: #ffffff !important;
        }
        
        /* Alertas y notificaciones */
        .stAlert {
            border-radius: 8px !important;
        }
        

        
        /* Ocultar / Mostrar vistas según tamaño de pantalla */
        @media (max-width: 768px) {
            div[class*="st-key-desktop_only_container"],
            div[class*="st-key-desktop_only_rows_container"],
            div[class*="st-key-desktop_only_pagination"] {
                display: none !important;
            }
            div[class*="st-key-mobile_only_container"] {
                display: block !important;
            }
            .export-filters-title {
                margin-top: 38px !important; /* Espacio de 1 centímetro entre tarjetas KPI y filtros en celular */
            }
        }
        @media (min-width: 769px) {
            div[class*="st-key-desktop_only_container"],
            div[class*="st-key-desktop_only_rows_container"],
            div[class*="st-key-desktop_only_pagination"] {
                display: block !important;
            }
            div[class*="st-key-mobile_only_container"] {
                display: none !important;
            }
        }
        
        /* Estilos del Formulario en Tarjetas (Rectángulo con contorno blanco fino) */
        div[class*="st-key-mobile_form_container"],
        div[class*="st-key-mobile_form_container_electric"],
        div[class*="st-key-mobile_form_container_levels"],
        div[class*="st-key-atender_form_container"],
        div[class*="st-key-chart_card_"] {
            background-color: #152232 !important;
            border: 1px solid #ffffff !important;
            border-radius: 8px !important;
            padding: 24px !important;
            margin-top: 20px !important;
            margin-bottom: 30px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        }
        
        /* Contenedores scrollables para gráficas */
        div[class*="st-key-chart_card_local_movil"],
        div[class*="st-key-chart_card_local_grupo"] {
            overflow-x: auto !important;
        }
        div[class*="st-key-chart_card_local_movil"] > div,
        div[class*="st-key-chart_card_local_grupo"] > div {
            overflow-x: auto !important;
        }
        
        /* Contorno destacado y claro para el selector de móviles */
        div[class*="st-key-atender_form_container"] div[data-baseweb="select"] {
            border: 2px solid #a0b2c6 !important;
            border-radius: 4px !important;
            box-shadow: 0 0 8px rgba(160, 178, 198, 0.25) !important;
        }
        div[class*="st-key-atender_form_container"] div[data-baseweb="select"]:hover {
            border-color: #ffffff !important;
        }
        
        /* Contorno azul destacado para el cuadro de entrada de texto de insumos */
        div[class*="st-key-atender_form_container"] div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: 2px solid #007ac5 !important;
            border-radius: 4px !important;
            box-shadow: 0 0 8px rgba(0, 122, 197, 0.25) !important;
        }
        div[class*="st-key-atender_form_container"] div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #0090e7 !important;
            box-shadow: 0 0 12px rgba(0, 144, 231, 0.4) !important;
        }
        
        /* Evitar que los elementos se desvanezcan o cambien de opacidad al interactuar o recargar */
        .element-container,
        [data-testid="stElementContainer"],
        [data-testid="stBlock"],
        div[data-testid="stVerticalBlock"] > div,
        div[data-testid="stAppViewContainer"] section,
        div[data-testid="stAppViewContainer"] [data-testid="stVerticalBlock"] > div,
        div[data-testid="stAppViewContainer"] [data-testid="stElementContainer"],
        div[data-testid="stAppViewContainer"] [data-testid="stBlock"],
        div[data-testid="stAppViewContainer"] .element-container {
            opacity: 1 !important;
            filter: none !important;
            transition: none !important;
            animation: none !important;
        }

        /* Contenedor de descargas en Exportar Datos */
        div[class*="st-key-export_downloads_container"],
        div[class*="st-key-export_volvo_container"] {
            background-color: #152232 !important;
            border: 1px solid #ffffff !important;
            border-radius: 8px !important;
            padding: 24px !important;
            margin-top: 20px !important;
            margin-bottom: 30px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        }
        
        /* Estilo del Botón de Descarga Maestro Destacado (ZIP) y Botón Volvo */
        div[class*="st-key-btn_download_all_zip"] button,
        div[class*="st-key-btn_download_volvo_novedades"] button {
            background-color: #007ac5 !important;
            border: 2px solid #007ac5 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 15px rgba(0, 122, 197, 0.4) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        div[class*="st-key-btn_download_all_zip"] button:hover,
        div[class*="st-key-btn_download_volvo_novedades"] button:hover {
            background-color: #0090e7 !important;
            border-color: #0090e7 !important;
            color: #ffffff !important;
            box-shadow: 0 6px 20px rgba(0, 122, 197, 0.6) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Estilo de los Botones de Descarga Individuales (Secundarios) */
        div[class*="st-key-btn_download_niv"] button,
        div[class*="st-key-btn_download_mec"] button,
        div[class*="st-key-btn_download_elec"] button {
            background-color: #1c2e47 !important;
            color: #a0b2c6 !important;
            border: 1px solid #3a506b !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        div[class*="st-key-btn_download_niv"] button:hover,
        div[class*="st-key-btn_download_mec"] button:hover,
        div[class*="st-key-btn_download_elec"] button:hover {
            background-color: #253d5e !important;
            color: #ffffff !important;
            border-color: #005b94 !important;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25) !important;
        }
    </style>
    """
    css = css.replace("{logo_base64}", logo_base64)
    st.markdown(css, unsafe_allow_html=True)

def draw_volvo_header(title, subtitle, version="VERSION 1.1"):
    """Dibuja el banner superior corporativo."""
    header_html = f"""
    <div class="volvo-header">
        <div class="volvo-header-left">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div style="font-size: 14px; text-align: right;">
            <span style="background-color:#004b87; padding:5px 10px; border-radius:15px; font-weight:600; font-size:12px;">{version}</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def draw_metric_card(val, lbl, border_color="#005b94", text_color=None, value_style=None):
    """Dibuja una tarjeta de métrica con bordes coloreados y hover de Volvo."""
    border_style = f"border-left-color: {border_color};" if border_color else ""
    val_color = f"color: {text_color};" if text_color else ""
    val_styles = f"style='{val_color} {value_style if value_style else ''}'"
    
    card_html = f"""
    <div class="metric-card" style="{border_style}">
        <div class="metric-val" {val_styles}>{val}</div>
        <div class="metric-lbl">{lbl}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def draw_patio_card_html(patio_name, num_vehicles):
    """Genera el código HTML para una tarjeta de selección de patio interactiva y clicable."""
    import urllib.parse
    patio_encoded = urllib.parse.quote(patio_name)
    return f"""
    <a href="/?patio={patio_encoded}" target="_self" style="text-decoration: none;">
        <div class="patio-card-interactive">
            <h4>{patio_name}</h4>
            <p>{num_vehicles} Móviles</p>
        </div>
    </a>
    """

def draw_total_fleet_card_html(total_count):
    """Genera el código HTML para la tarjeta de flota total."""
    return f"""
    <div style="background-color: #003057; padding: 22px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; color: white; margin-bottom: 12px; height: 130px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <h4 style="margin: 0; color: white; font-size: 18px; font-weight: 700; letter-spacing: 0.5px;">TOTAL FLOTA</h4>
        <p style="margin: 8px 0 0 0; font-size: 15px; color: #a0b2c6; font-weight: bold;">🚛 {total_count} Móviles</p>
    </div>
    """
