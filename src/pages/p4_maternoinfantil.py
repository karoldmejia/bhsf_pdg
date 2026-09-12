"""Salud maternoinfantil"""
import plotly.express as px
import streamlit as st

from src.theme import SEQ_ROSADO, ZSCORE_COLORS, ROSADO, BL
from src.ui.components import sec, card, end, kpi, notnull


def render(df, cie10_map=None):
    _NO_V = {'NO', 'NAN', 'NONE', 'N', '0', 'FALSE', '', 'NO APLICA', 'SIN DATO'}

    def _es_si_p5(serie):
        return ~serie.fillna('').astype(str).str.strip().str.upper().isin(_NO_V)

    n_g5 = int(_es_si_p5(df['gestante']).sum()) if 'gestante' in df.columns else 0
    n_l5 = int(_es_si_p5(df['madre_lactante']).sum()) if 'madre_lactante' in df.columns else 0

    sec("SALUD MATERNO INFANTIL")
    _n_val_gest = 0
    if 'desencadenante_principal_salud_mental' in df.columns:
        _vals_gest = df['desencadenante_principal_salud_mental'].dropna().astype(str)
        _n_val_gest = int(_vals_gest.str.upper().str.contains(
            'VALORACION PSICOSOCIAL.*GESTANTE|MUJER GESTANTE', na=False).sum())

    km1, km2, km3 = st.columns(3)
    kpi(km1, "", f"{n_g5:,}",       "GESTANTES ATENDIDAS",              "MUJERES EMBARAZADAS", "red")
    kpi(km2, "", f"{n_l5:,}",       "MADRES LACTANTES",                 "IDENTIFICADAS",       "blue")
    kpi(km3, "", f"{_n_val_gest:,}", "VALORACIÓN PSICOSOCIAL EN LA GESTANTE", "ATENCIÓN PSICOSOCIAL", "purple")
    st.markdown("<br>", unsafe_allow_html=True)

    card("GESTANTES POR GRUPO ETARIO", "DISTRIBUCIÓN ETARIA DE GESTANTES")
    if 'gestante' in df.columns and 'grupo_etareo' in df.columns:
        gest5 = df[_es_si_p5(df['gestante'].fillna(''))]
        if not gest5.empty and gest5['grupo_etareo'].notna().any():
            ge5 = gest5['grupo_etareo'].dropna().value_counts().reset_index()
            ge5.columns = ['grupo', 'n']
            fig_g5 = px.bar(ge5, x='n', y='grupo', orientation='h',
                            color_discrete_sequence=[ROSADO])
            fig_g5.update_layout(**BL(300),
                                 xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='CASOS',
                                            tickangle=0, tickfont=dict(size=12)),
                                 yaxis=dict(showgrid=False, autorange='reversed', title='',
                                            tickfont=dict(size=12)))
            st.plotly_chart(fig_g5, width="stretch", key="g21")
        else:
            st.info("SIN DATOS DE GESTANTES CON GRUPO ETARIO.")
    end()

    sec("DIAGNÓSTICO NUTRICIONAL INFANTIL")
    c1, c2 = st.columns([3, 3])
    with c1:
        card("Z SCORE - PESO PARA LA TALLA", "ESTADO NUTRICIONAL SEGÚN CLASIFICACIÓN OMS")
        if 'zscore_peso_para_la_talla' in df.columns:
            zs = df['zscore_peso_para_la_talla'].dropna().pipe(notnull).value_counts().reset_index()
            zs.columns = ['diagnostico_nutricional', 'n']
            fig = px.bar(zs, x='n', y='diagnostico_nutricional', orientation='h',
                         color='diagnostico_nutricional',
                         color_discrete_map=ZSCORE_COLORS,
                         labels={'n': 'CASOS', 'diagnostico_nutricional': ''})
            fig.update_layout(**BL(280), showlegend=False, bargap=0.05,
                              xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='CASOS'),
                              yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig, width="stretch", key="g22")
        else:
            st.info("SIN DATOS DE ZSCORE.")
        end()

    with c2:
        card("DISTRIBUCIÓN NUTRICIONAL", "PROPORCIÓN POR CATEGORÍA")
        if 'zscore_peso_para_la_talla' in df.columns:
            zs2 = df['zscore_peso_para_la_talla'].dropna().pipe(notnull).value_counts().reset_index()
            zs2.columns = ['diagnostico_nutricional', 'n']
            fig2 = px.pie(zs2, names='diagnostico_nutricional', values='n', hole=0.55,
                          color='diagnostico_nutricional',
                          color_discrete_map=ZSCORE_COLORS)
            _total_zs2 = zs2['n'].sum()
            _pull_zs2 = [0.08 if (n / _total_zs2) < 0.08 else 0 for n in zs2['n']]
            fig2.update_traces(
                pull=_pull_zs2,
                textposition='auto', textinfo='percent', textfont_size=9,
                insidetextorientation='horizontal',
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            fig2.update_layout(**BL(320),
                               legend=dict(orientation='h', y=-0.3, x=0, font=dict(size=8)))
            st.plotly_chart(fig2, width="stretch", key="g23")
        else:
            st.info("SIN DATOS.")
        end()