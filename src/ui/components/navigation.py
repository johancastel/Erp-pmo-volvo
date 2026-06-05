# src/ui/components/navigation.py
import streamlit as st
import pymysql
from src.styles import get_base64_logo

def render_sidebar(connection_manager):
    """
    Renders the corporate sidebar navigation, including logo, menu selection,
    disabled modules, and database configuration pool settings.
    """
    with st.sidebar:
        # 1. Volvo logo link to Home
        logo_base64 = get_base64_logo()
        if logo_base64:
            st.markdown(
                f'<div style="text-align:center; padding: 15px 0;">'
                f'<a href="/?menu=home" target="_self" style="text-decoration: none; display: inline-block;">'
                f'<img src="data:image/png;base64,{logo_base64}" style="width: 160px; filter: brightness(0) invert(1); transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\'">'
                f'</a>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="text-align:center; padding: 10px 0;">'
                '<a href="/?menu=home" target="_self" style="text-decoration: none;">'
                '<span class="volvo-logo-text">VOLVO</span>'
                '</a>'
                '</div>',
                unsafe_allow_html=True
            )
            
        st.markdown("<h3 style='margin-top:10px; margin-bottom: 20px; font-weight:600; text-align:center;'>PMO - Colombia</h3>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 12px; text-transform: uppercase; color: #8899a6; font-weight:700; margin-bottom:10px;'>Módulos Disponibles</p>", unsafe_allow_html=True)

        # 2. Main Navigation Menu
        if "menu_actual_radio" not in st.session_state:
            st.session_state.menu_actual_radio = None
            
        novedades_expanded = st.session_state.menu_actual_radio is not None
        
        with st.expander("Novedades", expanded=novedades_expanded):
            menu_actual = st.radio(
                "Acción de Novedades",
                options=["Ingresar Novedades", "Atender Novedades", "Exportar Datos"],
                key="menu_actual_radio",
                index=None,
                label_visibility="collapsed"
            )
        
        # Disabled sections (Upcoming)
        st.markdown('<div class="nav-item-disabled"><span class="nav-icon"></span> Turnos Personal (Próximamente)</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item-disabled"><span class="nav-icon"></span> Entrega de Turnos (Próximamente)</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item-disabled"><span class="nav-icon"></span> Kilometraje (Próximamente)</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-item-disabled"><span class="nav-icon"></span> Planeación y Prog. (Próximamente)</div>', unsafe_allow_html=True)
        
        # 3. Database configuration panel
        st.write("---")
        with st.expander("⚙️ Conexión MySQL Local"):
            st.write("Parámetros de conexión a la base de datos:")
            db_host = st.text_input("Host", value=st.session_state.db_host)
            db_user = st.text_input("User", value=st.session_state.db_user)
            db_password = st.text_input("Password", value=st.session_state.db_password, type="password")
            db_name = st.text_input("Database", value=st.session_state.db_name)
            db_port = st.number_input("Port", value=st.session_state.db_port, step=1)
            
            if st.button("Aplicar y Probar Conexión"):
                st.session_state.db_host = db_host
                st.session_state.db_user = db_user
                st.session_state.db_password = db_password
                st.session_state.db_name = db_name
                st.session_state.db_port = db_port
                
                # Reset connection cache in ConnectionManager and session
                connection_manager.clear_db_type_cache()
                if 'db_initialized' in st.session_state: 
                    del st.session_state.db_initialized
                if 'db_active' in st.session_state: 
                    del st.session_state.db_active
                
                # Test new connection
                try:
                    conn = pymysql.connect(
                        host=db_host,
                        user=db_user,
                        password=db_password,
                        port=int(db_port),
                        connect_timeout=2
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                    cursor.close()
                    conn.close()
                    st.success("🔌 ¡Conexión MySQL exitosa!")
                    
                    # Force data reload
                    if 'df_master' in st.session_state: 
                        del st.session_state.df_master
                    if 'df_master_patio_name' in st.session_state: 
                        del st.session_state.df_master_patio_name
                    st.rerun()
                except Exception as e:
                    st.error(f"Error de conexión MySQL. Detalle: {str(e)}")
                    
            if st.button("Desconectar Base"):
                # Force database type to SQLite
                connection_manager._db_type = "SQLite"
                st.session_state.db_active = "SQLite"
                
                # Force data reload
                if 'df_master' in st.session_state: 
                    del st.session_state.df_master
                if 'df_master_patio_name' in st.session_state: 
                    del st.session_state.df_master_patio_name
                
                st.info("🔌 Desconectado de MySQL. Usando base de datos SQLite interna de respaldo.")
                st.rerun()
                    
        return menu_actual
