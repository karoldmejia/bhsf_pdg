"""Entry point. Solo orquesta: importa módulos, monta tabs y llama render()."""
import warnings
warnings.filterwarnings("ignore")

import streamlit as st

from src.config import RUTA_DATOS
from src.styles import inject_css
from src.assets import logo_hero, logo_eu_footer
from src.data.loader import cargar, cargar_cie10
from src.ui.sidebar import sidebar
from src.auth import requiere_acceso
from src.pages import (
    p1_cobertura, p2_perfil, p3_salud_poblacion, p4_maternoinfantil,
    p5_salud_mental_vbg, p6_vigilancia_publica, p7_temporal,
    p8_comunidad, p9_diagnosticos,
)

st.set_page_config(
    page_title="Barco Hospital San Raffaele - Impacto Territorial",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


def main():
    try:
        df_raw = cargar(RUTA_DATOS)
    except FileNotFoundError:
        st.error(f"Archivo no encontrado: '{RUTA_DATOS}'. Ajusta la variable RUTA_DATOS.")
        st.stop()

    cie10_map = cargar_cie10()
    df = sidebar(df_raw)
    if df.empty:
        st.warning("Sin registros para los filtros seleccionados.")
        st.stop()

    # Hero
    st.markdown(
        f'<div class="hero">'
        f'<div class="hero-left">{logo_hero()}</div>'
        f'<div class="hero-right">'
        f'<div style="position:relative;z-index:1;color:#fff !important;">'
        f'<div class="hero-eyebrow">Fundación Italocolombiana del Monte Tabor - Pacífico colombiano</div>'
        f'<h1 class="hero-title">Barco Hospital San Raffaele</h1>'
        f'<p class="hero-sub">Plataforma de análisis y visualización del impacto territorial - Misiones 2023-2025</p>'
        f'</div>'
        f'<div class="hero-badge" style="position:relative;z-index:1;">{len(df):,} atenciones analizadas</div>'
        f'</div></div>',
        unsafe_allow_html=True)

    # Pestañas
    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
        "Cobertura Territorial",
        "Perfil de la Población",
        "Salud de la Población",
        "Salud Maternoinfantil",
        "Salud Mental y Violencias Basadas en Género",
        "Vigilancia en Salud Pública",
        "Análisis Temporal",
        "Comunidad y Opiniones",
        "Todos los Diagnósticos",
    ])
    with t1: p1_cobertura.render(df, cie10_map)
    with t2: p2_perfil.render(df, cie10_map)
    with t3: p3_salud_poblacion.render(df, cie10_map)
    with t4: p4_maternoinfantil.render(df, cie10_map)
    with t5: p5_salud_mental_vbg.render(df, cie10_map)
    with t6:
        if requiere_acceso("t6"):
            p6_vigilancia_publica.render(df, cie10_map)
    with t7:
        if requiere_acceso("t7"):
            p7_temporal.render(df, cie10_map)
    with t8:
        if requiere_acceso("t8"):
            p8_comunidad.render(df, cie10_map)
    with t9:
        if requiere_acceso("t9"):
            p9_diagnosticos.render(df, cie10_map)

    # Footer
    st.markdown(
        f'<div style="text-align:center;padding:2rem 0 1rem;font-size:0.7rem;color:#9CA3AF;'
        f'border-top:1px solid #E5E7EB;margin-top:1rem">'
        f'{logo_eu_footer()}'
        f'<div>Barco Hospital San Raffaele - Fundación Italocolombiana del Monte Tabor</div>'
        f'<div>Datos anonimizados - Uso exclusivo institucional</div>'
        f'</div>',
        unsafe_allow_html=True)


if __name__ == "__main__":
    main()