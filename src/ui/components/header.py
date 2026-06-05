# src/ui/components/header.py
import streamlit as st
from src.styles import draw_volvo_header, draw_metric_card

def render_header(title="PMO - VOLVO", subtitle="Control de Alistamiento Diaro y Registro de Novedades"):
    """
    Renders the Volvo top header banner.
    """
    draw_volvo_header(title, subtitle)

def render_metrics(total_vehicles, completed_count, pending_count):
    """
    Renders a row of metric cards summarizing the current patio status.
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        draw_metric_card(
            val=total_vehicles, 
            lbl="Flota Asignada", 
            border_color="#005b94"
        )
    with col2:
        draw_metric_card(
            val=completed_count, 
            lbl="Alistamientos Completados", 
            border_color="#28a745", 
            text_color="#28a745"
        )
    with col3:
        # If there are pending checks, color it orange; otherwise green
        border_col = "#dc3545" if pending_count > 0 else "#28a745"
        text_col = "#dc3545" if pending_count > 0 else "#28a745"
        draw_metric_card(
            val=pending_count, 
            lbl="Alistamientos Pendientes", 
            border_color=border_col, 
            text_color=text_col
        )
