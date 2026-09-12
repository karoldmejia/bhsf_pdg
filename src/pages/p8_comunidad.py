"""Blog/foro comunitario."""
import streamlit as st
from datetime import datetime

from src.ui.components import sec


def render(df, cie10_map=None):
    st.markdown("""
    <div class="public-note" style="background:#FDF6F0;border-color:#C4992C;color:#6B3A0F">
    <b>Espacio comunitario</b> - Comparte tu experiencia, sugerencias o comentarios sobre las misiones del Barco Hospital San Raffaele. Tu opinión es importante para mejorar nuestros servicios. <b>Las opiniones publicadas aquí podrán ser comentadas y respondidas por personas del equipo interno del Barco Hospital San Raffaele.</b>
    </div>""", unsafe_allow_html=True)

    if 'foro_comentarios' not in st.session_state:
        st.session_state['foro_comentarios'] = [
            {"autor": "Equipo San Raffaele", "fecha": "01/05/2025",
             "texto": "Bienvenidos al espacio comunitario del Barco Hospital San Raffaele. "
                      "Este es un lugar para compartir experiencias y sugerencias."},
            {"autor": "Comunidad El Charco", "fecha": "15/04/2025",
             "texto": "Muy agradecidos por la atención recibida. El equipo médico fue muy "
                      "profesional y amable con toda la comunidad."},
        ]

    sec("PUBLICAR COMENTARIO")
    with st.form("foro_form", clear_on_submit=True):
        col_a, col_b = st.columns([2, 3])
        with col_a:
            nombre = st.text_input("Tu nombre o comunidad", "")
        with col_b:
            categoria = st.selectbox("Categoría", [
                "Experiencia de atención",
                "Sugerencia de mejora",
                "Agradecimiento",
                "Solicitud de información",
                "Otro",
            ])
        comentario = st.text_area("Tu comentario o sugerencia", "", height=100)
        enviado = st.form_submit_button("Publicar comentario", width="stretch")

        if enviado:
            if nombre.strip() and comentario.strip():
                st.session_state['foro_comentarios'].insert(0, {
                    "autor": nombre.strip(),
                    "fecha": datetime.now().strftime("%d/%m/%Y"),
                    "texto": f"[{categoria}] {comentario.strip()}",
                })
                st.success("Comentario publicado correctamente.")
            else:
                st.warning("Por favor completa tu nombre y comentario antes de publicar.")

    sec("COMENTARIOS DE LA COMUNIDAD")
    for com in st.session_state['foro_comentarios']:
        st.markdown(
            f'<div class="blog-card">'
            f'<div class="blog-autor">{com["autor"]}</div>'
            f'<div class="blog-texto">{com["texto"]}</div>'
            f'<div class="blog-fecha">{com["fecha"]}</div>'
            f'</div>', unsafe_allow_html=True)