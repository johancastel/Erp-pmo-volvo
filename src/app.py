# src/app.py
import os
import streamlit as st
import streamlit.components.v1 as components

# Import configurations, styles, and database connection pools
from src.config.settings import (
    PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT,
    DEFAULT_DB_HOST, DEFAULT_DB_USER, DEFAULT_DB_PASSWORD, DEFAULT_DB_NAME, DEFAULT_DB_PORT
)
from src.styles import inject_custom_css, draw_volvo_header
from src.database.connection import get_connection_manager
from src.database.repositories.novedades_repository import NovedadesRepository
from src.services.cache_service import CacheService

# Import pages
from src.ui.components.navigation import render_sidebar
from src.ui.pages.ingreso_novedades import render_ingreso_novedades_page
from src.ui.pages.atender_novedades import render_atender_novedades_page
from src.ui.pages.exportar_datos import render_export_page

def main():
    # 1. Navigation Home parameter redirection handler
    if st.query_params.get("menu") == "home":
        st.session_state.menu_actual_radio = None
        st.session_state.active_patio = None
        if "menu" in st.query_params:
            del st.query_params["menu"]
        st.rerun()

    # 2. Inject Volvo CSS corporate styling
    inject_custom_css()

    # 3. Clean "Add" prefix Javascript injection & Sidebar auto-collapse on mobile
    import time
    timestamp = time.time()
    menu_actual = st.session_state.get("menu_actual_radio")
    
    # Track previous menu selection to trigger auto-collapse only when selection changes
    if "previous_menu" not in st.session_state:
        st.session_state.previous_menu = None
        
    hide_sidebar_trigger = False
    if menu_actual is not None and menu_actual != st.session_state.previous_menu:
        hide_sidebar_trigger = True
        st.session_state.previous_menu = menu_actual
    elif menu_actual is None:
        st.session_state.previous_menu = None

    components.html(f"""
        <script>
            // Force refresh on rerun using unique ID: {timestamp}
            const doc = window.parent.document;
            const observer = new MutationObserver(() => {{
                const menuOptions = doc.querySelectorAll('li[role="option"] div, div[role="option"], div[role="listbox"] div, ul[role="listbox"] li');
                menuOptions.forEach(option => {{
                    const text = option.textContent;
                    if (text) {{
                        if (text.startsWith('Add "') && text.endsWith('"')) {{
                            const val = text.slice(5, -1);
                            option.textContent = val;
                        }} else if (text.startsWith('Add ')) {{
                            const val = text.slice(4);
                            option.textContent = val;
                        }}
                    }}
                }});
            }});
            observer.observe(doc.body, {{ childList: true, subtree: true }});
    
            // Forzar pérdida de foco (blur) en inputs de texto al hacer clic en cualquier botón
            // Esto resuelve el error nativo de Streamlit donde las cajas de texto no envían su valor
            // antes de procesar el clic de un botón (como "Guardar Cambios" o "Aplicar Conexión")
            try {{
                const handleButtonClick = (target) => {{
                    const btn = target.closest && target.closest('button');
                    if (btn) {{
                        const activeEl = doc.activeElement;
                        if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA')) {{
                            activeEl.blur();
                        }}
                    }}
                }};
                doc.addEventListener('mousedown', (e) => handleButtonClick(e.target), {{ capture: true }});
                doc.addEventListener('touchstart', (e) => handleButtonClick(e.target), {{ capture: true }});
            }} catch (e) {{
                console.error("Error setting up button blur listeners:", e);
            }}
            // Auto-colapsar barra lateral
            const collapseSidebar = () => {{
                try {{
                    const topWin = window.parent || window;
                    const doc = topWin.document;
                    
                    // 1. Intentar hacer clic en el overlay de fondo (sólo visible si la barra está abierta en celular)
                    const overlay = doc.querySelector('[data-testid="stSidebarUserCloseOverlay"]');
                    if (overlay) {{
                        overlay.click();
                        return true;
                    }}
                    
                    // 2. Intentar hacer clic en el botón de colapso de la barra lateral si está expandida
                    const sidebar = doc.querySelector('section[data-testid="stSidebar"], [data-testid="stSidebar"]');
                    if (sidebar && sidebar.getAttribute('data-collapsed') === 'false') {{
                        const collapseBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"]');
                        if (collapseBtn) {{
                            collapseBtn.click();
                            return true;
                        }}
                    }}
                }} catch (e) {{
                    console.error("Error in collapseSidebar:", e);
                }}
                return false;
            }};
    
            const shouldHide = {str(hide_sidebar_trigger).lower()};
            if (shouldHide) {{
                // Intentar en múltiples intervalos incondicionales para asegurar la ejecución tras renderizado de React
                setTimeout(collapseSidebar, 150);
                setTimeout(collapseSidebar, 400);
                setTimeout(collapseSidebar, 750);
                setTimeout(collapseSidebar, 1200);
            }}
            
            // Client-side listener to collapse the sidebar immediately when a sidebar menu option is clicked
            try {{
                const setupSidebarRadioListeners = () => {{
                    const sidebarRadioOptions = doc.querySelectorAll('section[data-testid="stSidebar"] div[data-testid="stRadio"] label');
                    sidebarRadioOptions.forEach(option => {{
                        if (!option.dataset.hasCollapseListener) {{
                            option.dataset.hasCollapseListener = "true";
                            option.addEventListener('click', () => {{
                                // Close the sidebar after a very short delay to let the click action propagate
                                setTimeout(collapseSidebar, 50);
                            }});
                        }}
                    }});
                }};
                
                setupSidebarRadioListeners();
                const sidebarObserver = new MutationObserver(setupSidebarRadioListeners);
                sidebarObserver.observe(doc.body, {{ childList: true, subtree: true }});
            }} catch (e) {{
                console.error("Error setting up sidebar radio listeners:", e);
            }}
        </script>
        """, height=0)

    # 4. Initialize Database connection credentials in Session State
    CacheService.initialize_state({
        "db_host": DEFAULT_DB_HOST,
        "db_user": DEFAULT_DB_USER,
        "db_password": DEFAULT_DB_PASSWORD,
        "db_name": DEFAULT_DB_NAME,
        "db_port": DEFAULT_DB_PORT
    })

    # Get cached connection manager
    connection_manager = get_connection_manager()
    repository = NovedadesRepository(connection_manager)

    # 5. Database Initialization
    repository.init_db(
        host=st.session_state.db_host,
        user=st.session_state.db_user,
        password=st.session_state.db_password,
        db_name=st.session_state.db_name,
        port=st.session_state.db_port
    )

    # 6. Database Connection check & active type caching
    if 'db_active' not in st.session_state:
        try:
            conn_test, db_active = connection_manager.get_connection(
                host=st.session_state.db_host,
                user=st.session_state.db_user,
                password=st.session_state.db_password,
                db_name=st.session_state.db_name,
                port=st.session_state.db_port
            )
            conn_test.close()
            st.session_state.db_active = db_active
        except Exception:
            st.session_state.db_active = "SQLite"
            
    db_active = st.session_state.db_active

    # 7. Render Navigation Sidebar
    menu_actual = render_sidebar(connection_manager)

    # 8. Render requested page
    if menu_actual is None:
        # Default home banner
        st.markdown("""
        <div style="background-color: #122135; padding: 25px; border-radius: 8px; margin-bottom: 25px; border-left: 5px solid #005b94; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); text-align: center;">
            <h3 style="margin: 0 0 10px 0; color: white; font-weight: 700; letter-spacing: 0.5px;">Control Operativo de Flota</h3>
            <p style="margin: 0; color: #a0b2c6; font-size: 15px;">Por favor, despliega y selecciona una opción en el menú lateral de <b>Novedades</b> para comenzar.</p>
        </div>
        """, unsafe_allow_html=True)
        
        bus_path = os.path.join(os.path.dirname(__file__), "volvo_bus.png")
        if os.path.exists(bus_path):
            col_img1, col_img2, col_img3 = st.columns([0.6, 2.8, 0.6])
            with col_img2:
                st.image(bus_path, caption="Volvo Electric Bus - Innovación y Eficiencia", use_container_width=True)
        st.stop()

    # Dynamic header title and subtitle based on menu option
    if menu_actual == "Ingresar Novedades":
        header_title = "MÓDULO DE NOVEDADES - INGRESAR NOVEDADES"
        header_subtitle = "Volvo Group Colombia - Registro de novedades de vehículos"
    elif menu_actual == "Atender Novedades":
        header_title = "MÓDULO DE NOVEDADES - ATENDER NOVEDADES"
        header_subtitle = "Volvo Group Colombia - Seguimiento y atención de novedades"
    elif menu_actual == "Exportar Datos":
        header_title = "MÓDULO DE NOVEDADES - EXPORTAR DATOS"
        header_subtitle = "Volvo Group Colombia - Descarga de registros y reportes"
    else:
        header_title = "MÓDULO DE NOVEDADES - CONTROL DE FLOTA"
        header_subtitle = "Volvo Group Colombia - Control Operativo de los móviles"

    # Renders Volvo Banner
    draw_volvo_header(
        title=header_title,
        version="VERSION 1.1",
        subtitle=header_subtitle
    )

    st.write("")

    if menu_actual == "Ingresar Novedades":
        render_ingreso_novedades_page()
    elif menu_actual == "Atender Novedades":
        render_atender_novedades_page()
    elif menu_actual == "Exportar Datos":
        render_export_page()

if __name__ == "__main__":
    main()
