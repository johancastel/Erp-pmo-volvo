# 01_Modulo_Noveades.py
import streamlit as st
from src.config.settings import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT

# Detect mobile using st.context.headers (Streamlit 1.30+)
is_mobile = False
try:
    ua = st.context.headers.get("user-agent", st.context.headers.get("User-Agent", "")).lower()
    is_mobile = any(k in ua for k in ["mobile", "android", "iphone", "ipad", "ipod", "blackberry", "iemobile", "opera mini"])
except Exception:
    pass

# Determine sidebar state: collapse when a submodule is selected (Ingresar Novedades, Atender Novedades or Exportar Datos)
sidebar_state = "expanded"
if st.session_state.get("menu_actual_radio") is not None:
    sidebar_state = "collapsed"

# Streamlit Page configuration must be the first command executed
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=sidebar_state
)

from src.app import main

if __name__ == "__main__":
    main()
