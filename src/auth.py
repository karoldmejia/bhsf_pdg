"""Control de acceso por clave institucional."""
import streamlit as st


def requiere_acceso(pestana: str = "") -> bool:
    """
    Devuelve True si el usuario está autenticado.
    El parámetro 'pestana' garantiza keys únicos por pestaña.
    """
    if st.session_state.get('acceso_hospital', False):
        return True

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_centro, _ = st.columns([1, 2, 1])
    with col_centro:
        st.markdown(
            '<div style="background:#fff;border-radius:16px;padding:2rem 2rem 1.8rem;'
            'border-top:4px solid #C42C57;box-shadow:0 2px 12px rgba(196,44,87,0.12);">'
            '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#C42C57;margin-bottom:0.5rem">Acceso restringido</div>'
            '<div style="font-size:0.95rem;font-weight:500;color:#1F2937;margin-bottom:0.4rem">'
            'Contenido exclusivo del equipo</div>'
            '<div style="font-size:0.82rem;color:#6B7280;line-height:1.5;margin-bottom:1.2rem">'
            'Esta sección es de uso exclusivo del equipo del Barco Hospital San Raffaele. '
            'Ingresa la clave institucional para continuar.</div>'
            '</div>',
            unsafe_allow_html=True)

        clave = st.text_input(
            "Clave de acceso",
            type="password",
            placeholder="Ingresa la clave institucional",
            key=f"input_clave_{pestana}")

        if st.button("Ingresar", use_container_width=True, type="primary", key=f"btn_clave_{pestana}"):
            try:
                clave_correcta = st.secrets["CLAVE_HOSPITAL"]
            except Exception:
                clave_correcta = "barco2025"  # TODO: eliminar antes de producción

            if clave == clave_correcta:
                st.session_state['acceso_hospital'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Verifica con el equipo del Barco Hospital.")

    return False