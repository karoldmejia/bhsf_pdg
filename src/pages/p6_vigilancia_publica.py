"""Vigilancia en salud pública (SIVIGILA)"""
import pandas as pd
import plotly.express as px
import streamlit as st

from src.theme import SEQ_R, ROSADO, RED, AMARILLO, AMBER, TEAL, BL
from src.config import CLASIF_CRONICAS, CLASIF_INFECCIOSAS, CLASIF_NUTRICIONAL, ENF_NOTIFICACION
from src.ui.components import sec, card, end, notnull


def render(df, cie10_map=None):
    st.markdown("""
    <div class="public-note">
    Esta sección presenta el análisis de diagnósticos según la clasificación del
    <b>Sistema Nacional de Vigilancia en Salud Pública (SIVIGILA)</b> del Instituto Nacional de Salud.
    Los códigos CIE-10 son clasificados automáticamente según las categorías de vigilancia epidemiológica.
    </div>""", unsafe_allow_html=True)

    dcol = 'diagnostico_principal_medicina'
    if dcol not in df.columns:
        st.info("SIN DATOS DE DIAGNÓSTICOS DISPONIBLES.")
        return

    df2 = df.copy()
    df2['_cod3'] = df2[dcol].fillna('').astype(str).str.strip().str.upper().str[:3]
    df2['_cod4'] = df2[dcol].fillna('').astype(str).str.strip().str.upper().str[:4]

    def clasificar(cod3, cod4):
        cod3 = str(cod3) if pd.notna(cod3) else ''
        cod4 = str(cod4) if pd.notna(cod4) else ''
        if any(cod3.startswith(c[:3]) for c in CLASIF_CRONICAS):
            return 'CRÓNICAS NO TRANSMISIBLES'
        if any(cod3.startswith(c[:3]) for c in CLASIF_INFECCIOSAS):
            return 'INFECCIOSAS'
        if any(cod3.startswith(c[:3]) for c in CLASIF_NUTRICIONAL):
            return 'NUTRICIONAL'
        if (cod4 in ENF_NOTIFICACION or
                cod3 + 'X' in ENF_NOTIFICACION or
                cod3 + '9' in ENF_NOTIFICACION):
            return 'NOTIFICACIÓN OBLIGATORIA'
        return 'OTRAS'

    df2['_categoria'] = df2.apply(lambda r: clasificar(r['_cod3'], r['_cod4']), axis=1)
    total_diag = df2[dcol].dropna().pipe(notnull).count()

    colores_cat = {
        'CRÓNICAS NO TRANSMISIBLES': ROSADO,
        'INFECCIOSAS':               RED,
        'NUTRICIONAL':               AMARILLO,
        'NOTIFICACIÓN OBLIGATORIA':  AMBER,
        'OTRAS':                     TEAL,
    }

    sec("CLASIFICACIÓN DE DIAGNÓSTICOS POR CATEGORÍA SIVIGILA")
    cats = df2.groupby('_categoria')[dcol].count().reset_index()
    cats.columns = ['categoria', 'n']
    cols = st.columns(len(cats))
    for i, (_, row) in enumerate(cats.iterrows()):
        pct = round(row['n'] / total_diag * 100, 1) if total_diag > 0 else 0
        color = colores_cat.get(row['categoria'], ROSADO)
        cols[i].markdown(
            f'<div class="sivigila-card" style="border-left-color:{color}">'
            f'<div class="sivigila-title">{str(row["categoria"]).upper()}</div>'
            f'<div class="sivigila-count" style="color:{color}">{row["n"]:,}</div>'
            f'<div style="font-size:0.7rem;color:#9CA3AF">{pct}% DEL TOTAL</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cats_otras = cats[cats['categoria'] == 'OTRAS']
    cats_resto = cats[cats['categoria'] != 'OTRAS'].sort_values('n', ascending=True)
    cats_ordenado = pd.concat([cats_otras, cats_resto], ignore_index=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        card("DIAGNÓSTICOS POR CATEGORÍA", "DISTRIBUCIÓN SEGÚN CLASIFICACIÓN SIVIGILA")
        cats_ordenado['pct'] = (cats_ordenado['n'] / total_diag * 100).round(1)
        fig = px.bar(cats_ordenado, x='pct', y='categoria', orientation='h',
                     color='categoria', color_discrete_map=colores_cat,
                     custom_data=['n', 'pct'],
                     labels={'pct': '% DEL TOTAL', 'categoria': ''})
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>%{customdata[1]:.1f}% — %{customdata[0]:,} CASOS<extra></extra>')
        fig.update_layout(**BL(360), showlegend=False, bargap=0.15,
                          xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                     title='% DEL TOTAL', ticksuffix='%'),
                          yaxis=dict(showgrid=False, autorange='reversed'))
        st.plotly_chart(fig, width="stretch", key="g32")
        end()

    with c2:
        card("PROPORCIÓN POR CATEGORÍA", "DISTRIBUCIÓN PORCENTUAL")
        fig2 = px.pie(cats_ordenado, names='categoria', values='n', hole=0.55,
                      color='categoria', color_discrete_map=colores_cat)
        fig2.update_layout(**BL(300),
                           legend=dict(orientation='h', y=-0.2, font=dict(size=9)))
        fig2.update_traces(textposition='inside', textinfo='percent', textfont_size=9)
        st.plotly_chart(fig2, width="stretch", key="g33")
        end()

    sec("ENFERMEDADES DE NOTIFICACIÓN OBLIGATORIA")
    notif_data = []
    for cod, nombre in ENF_NOTIFICACION.items():
        mask_notif = ((df2['_cod4'] == cod) |
                      (df2['_cod3'] == cod[:3]) |
                      (df2['_cod3'] + cod[-1:] == cod))
        n = int(mask_notif.sum())
        if n > 0:
            notif_data.append({'codigo': cod, 'enfermedad': nombre, 'casos': n})

    if notif_data:
        notif_df = pd.DataFrame(notif_data).sort_values('casos', ascending=False)
        card("CASOS DE ENFERMEDADES DE NOTIFICACIÓN OBLIGATORIA", "SEGÚN CÓDIGOS CIE-10 DEL SIVIGILA")
        _tot_notif = notif_df['casos'].sum()
        notif_df['pct'] = (notif_df['casos'] / _tot_notif * 100).round(1)
        fig3 = px.bar(notif_df, x='pct', y='enfermedad', orientation='h',
                      color='pct', color_continuous_scale=SEQ_R,
                      custom_data=['casos', 'pct'],
                      labels={'pct': '% DEL TOTAL', 'enfermedad': ''})
        fig3.update_traces(
            hovertemplate='<b>%{y}</b><br>%{customdata[1]:.1f}% — %{customdata[0]:,} CASOS<extra></extra>')
        fig3.update_layout(**BL(max(300, len(notif_data) * 30)), coloraxis_showscale=False,
                           xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                      title='% DEL TOTAL', ticksuffix='%'),
                           yaxis=dict(showgrid=False, autorange='reversed'))
        st.plotly_chart(fig3, width="stretch", key="g34")
        end()
    else:
        st.info("NO SE DETECTARON CASOS DE ENFERMEDADES DE NOTIFICACIÓN OBLIGATORIA EN LA SELECCIÓN ACTUAL.")

    sec("TOP DIAGNÓSTICOS POR CATEGORÍA")
    tab_cron, tab_inf, tab_nut = st.tabs(["CRÓNICAS", "INFECCIOSAS", "NUTRICIONAL"])
    for tab, cat_name in [
        (tab_cron, 'CRÓNICAS NO TRANSMISIBLES'),
        (tab_inf,  'INFECCIOSAS'),
        (tab_nut,  'NUTRICIONAL'),
    ]:
        with tab:
            sub = (df2[df2['_categoria'] == cat_name][dcol]
                   .dropna().pipe(notnull).value_counts().head(10).reset_index())
            sub.columns = ['codigo', 'n']
            _cie = cie10_map or {}
            sub['descripcion'] = sub['codigo'].apply(
                lambda c: _cie.get(str(c).strip().upper(), c))
            sub['label'] = sub.apply(
                lambda r: f"{r['codigo']} - {r['descripcion']}"
                          if r['descripcion'] != r['codigo'] else r['codigo'], axis=1)
            if not sub.empty:
                _tot_sub = sub['n'].sum()
                sub['pct'] = (sub['n'] / _tot_sub * 100).round(1)
                fig_s = px.bar(sub, x='pct', y='label', orientation='h',
                               color_discrete_sequence=[colores_cat.get(cat_name, ROSADO)],
                               custom_data=['n', 'pct'])
                fig_s.update_traces(
                    hovertemplate='<b>%{y}</b><br>%{customdata[1]:.1f}% — %{customdata[0]:,} CASOS<extra></extra>')
                fig_s.update_layout(**BL(300),
                                    xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                               title='% DEL TOTAL', ticksuffix='%'),
                                    yaxis=dict(showgrid=False, autorange='reversed', title=''))
                _key_name = cat_name.replace(' ', '_')
                st.plotly_chart(fig_s, width="stretch", key=f"plt_p7_{_key_name}")
            else:
                st.info(f"SIN DIAGNÓSTICOS CLASIFICADOS COMO {cat_name} EN LA SELECCIÓN ACTUAL.")