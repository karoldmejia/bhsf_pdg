"""Perfil de la población."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from src.theme import PAL, AMARILLO, ROSADO, ROJO, ROSADO_OSC, ROSADO_CLA, RED, BL
from src.ui.components import sec, card, end, kpi


def render(df, cie10_map=None):
    total = len(df)
    pct_fem  = round((df['sexo'].str.upper() == 'FEMENINO').sum() / total * 100, 1) if 'sexo' in df.columns else 0
    pct_afro = round(df['etnia'].astype(str).str.contains('AFRO', na=False).sum() / total * 100, 1) if 'etnia' in df.columns else 0
    edad_p   = round(df['edad'].mean(), 1) if 'edad' in df.columns and df['edad'].notna().any() else '—'
    pct_d    = round(
        df['discapacidad'].dropna().pipe(
            lambda s: s[~s.astype(str).str.upper().isin(
                ['SIN DATO', 'SIN DISCAPACIDAD', 'NO SABE/NO REPORTA', 'NAN', ''])]
        ).count() / total * 100, 1) if 'discapacidad' in df.columns else 0

    sec("INDICADORES DEMOGRÁFICOS")
    k1, k2, k3, k4 = st.columns(4)
    kpi(k1, "", f"{pct_fem}%",  "POBLACIÓN FEMENINA",  " ",                  "red")
    kpi(k2, "", f"{pct_afro}%", "AFRODESCENDIENTE",    "COMUNIDADES ÉTNICAS", "blue")
    kpi(k3, "", str(edad_p),    "EDAD PROMEDIO",        "años",               "green")
    kpi(k4, "", f"{pct_d}%",    "CON DISCAPACIDAD",     "NECESIDAD ESPECIAL", "purple")
    st.markdown("<br>", unsafe_allow_html=True)

    # pirámide poblacional y distribución por sexo
    r2a, r2b = st.columns([3, 2])
    with r2a:
        card("PIRÁMIDE POBLACIONAL", "ESTRUCTURA POR EDAD Y SEXO")
        if 'edad' in df.columns and 'sexo' in df.columns:
            bins = [0, 5, 10, 18, 30, 45, 60, 80, 120]
            lbls = ["0-5", "5-10", "10-18", "18-30", "30-45", "45-60", "60-80", "80+"]
            p = df[['edad', 'sexo']].dropna().copy()
            p['rango'] = pd.cut(p['edad'], bins=bins, labels=lbls, right=False)
            pg = p.groupby(['rango', 'sexo'], observed=True).size().reset_index(name='n')
            m = pg[pg['sexo'].str.upper() == 'MASCULINO'].copy()
            m['n'] = -m['n']
            f = pg[pg['sexo'].str.upper() == 'FEMENINO'].copy()
            mx = max(abs(pg['n'].max()), 1)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=m['rango'].astype(str), x=m['n'],
                                 orientation='h', name='MASCULINO', marker_color=AMARILLO))
            fig.add_trace(go.Bar(y=f['rango'].astype(str), x=f['n'],
                                 orientation='h', name='FEMENINO', marker_color=ROSADO))
            fig.update_layout(
                **BL(320), barmode='relative',
                legend=dict(orientation='h', y=1.1, x=0, title='', font=dict(size=10)),
                xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='',
                           range=[-mx*1.1, mx*1.1],
                           tickvals=[-mx, -mx//2, 0, mx//2, mx],
                           ticktext=[str(abs(mx)), str(abs(mx//2)), '0',
                                     str(mx//2), str(mx)]),
                yaxis=dict(showgrid=False, title=''))
            st.plotly_chart(fig, width="stretch", key="g3")
        end()

    with r2b:
        card("DISTRIBUCIÓN POR SEXO")
        if 'sexo' in df.columns:
            sx = df['sexo'].dropna().value_counts().reset_index()
            sx.columns = ['sexo', 'n']
            sx['sexo'] = sx['sexo'].astype(str).str.strip().str.upper()
            fig3 = px.pie(sx, names='sexo', values='n', hole=0.62,
                          color='sexo',
                          color_discrete_map={'FEMENINO': ROSADO, 'MASCULINO': AMARILLO})
            fig3.update_layout(**BL(320),
                               legend=dict(orientation='h', y=-0.2, x=0.1, font=dict(size=10)))
            fig3.update_traces(
                textposition='auto', textinfo='percent', textfont_size=11,
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            st.plotly_chart(fig3, width="stretch", key="g5")
        end()

    # étnica y grupo etáreo
    r3a, r3b = st.columns(2)
    with r3a:
        card("DISTRIBUCIÓN ÉTNICA", "COMPOSICIÓN DE LA POBLACIÓN")
        if 'etnia' in df.columns:
            et = df['etnia'].dropna().value_counts().reset_index()
            et.columns = ['etnia', 'n']
            _total_et = et['n'].sum()
            _pull_et = [0.08 if (n / _total_et) < 0.05 else 0 for n in et['n']]
            fig2 = px.pie(et, names='etnia', values='n', hole=0.58,
                          color_discrete_sequence=PAL)
            fig2.update_traces(
                pull=_pull_et,
                textposition='inside', textinfo='percent', textfont_size=10,
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            fig2.update_layout(**BL(320),
                               legend=dict(orientation='h', y=-0.25, x=0, font=dict(size=9)))
            st.plotly_chart(fig2, width="stretch", key="g4")
        end()

    with r3b:
        card("GRUPO ETARIO")
        if 'grupo_etareo' in df.columns:
            ge = df['grupo_etareo'].dropna().value_counts().reset_index()
            ge.columns = ['grupo', 'n']
            fig4 = px.bar(ge, x='n', y='grupo', orientation='h',
                          color_discrete_sequence=[ROJO])
            fig4.update_layout(**BL(320),
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''),
                               yaxis=dict(showgrid=False, autorange='reversed', title=''))
            st.plotly_chart(fig4, width="stretch", key="g6")
        end()

    # condición humanitaria, discapacidad y ocupación
    r4a, r4b, r4c = st.columns(3)
    with r4a:
        card("CONDICIÓN HUMANITARIA")
        if 'condicion' in df.columns:
            cn = df['condicion'].dropna().value_counts().head(6).reset_index()
            cn.columns = ['condicion', 'n']
            fig5 = px.bar(cn, x='n', y='condicion', orientation='h',
                          color_discrete_sequence=[RED],
                          labels={'n': 'ATENCIONES', 'condicion': ''},
                          custom_data=['n'])
            fig5.update_traces(
                hovertemplate='<b>%{y}</b><br>Casos: %{x:,}<extra></extra>')
            fig5.update_layout(**BL(380),
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='', tickangle=0),
                               yaxis=dict(showgrid=False, autorange='reversed', title=''))
            st.plotly_chart(fig5, width="stretch", key="g7")
        end()

    with r4b:
        card("DISCAPACIDAD REPORTADA")
        if 'discapacidad' in df.columns:
            disc = (df['discapacidad'].dropna()
                    .pipe(lambda s: s[~s.astype(str).str.upper().isin(
                        ['SIN DATO', 'NAN', '', 'SIN DISCAPACIDAD',
                         'NO SABE/NO REPORTA', 'NO SABE / NO REPORTA'])])
                    .value_counts().head(7).reset_index())
            disc.columns = ['discapacidad', 'n']
            fig6 = px.bar(disc, x='n', y='discapacidad', orientation='h',
                          color_discrete_sequence=[ROJO])
            fig6.update_layout(**BL(380),
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='', tickangle=0),
                               yaxis=dict(showgrid=False, autorange='reversed', title=''))
            st.plotly_chart(fig6, width="stretch", key="g8")
        end()

    with r4c:
        card("OCUPACIÓN")
        if 'ocupacion' in df.columns:
            oc = (df['ocupacion'].dropna()
                  .pipe(lambda s: s[~s.astype(str).str.upper().isin(
                      ['NO SABE/NO REPORTA', 'NO SABE / NO REPORTA', 'OTROS'])])
                  .value_counts().head(8).reset_index())
            oc.columns = ['ocupacion', 'n']
            oc['ocupacion'] = oc['ocupacion'].astype(str).str.upper()
            _total_oc = oc['n'].sum()
            _pull_oc = [0.08 if (n / _total_oc) < 0.05 else 0 for n in oc['n']]
            fig7 = px.pie(oc, names='ocupacion', values='n', hole=0.55,
                        color_discrete_sequence=PAL)
            fig7.update_traces(
                pull=_pull_oc,
                textposition='inside', textinfo='percent', textfont_size=9,
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            fig7.update_layout(**BL(380),
                            legend=dict(orientation='h', y=-0.25, font=dict(size=8)))
            st.plotly_chart(fig7, width="stretch", key="g9")
        end()

    sec("DISTRIBUCIÓN ÉTNICA POR MUNICIPIO")
    if 'etnia' in df.columns and 'municipio' in df.columns:
        card("ETNIA POR MUNICIPIO", "COMPOSICIÓN ÉTNICA POR TERRITORIO")
        em = df.groupby(['municipio', 'etnia']).size().reset_index(name='n')
        top_mp = df['municipio'].value_counts().head(8).index.tolist()

        _color_etnia = {'AFRODESCENDIENTE': ROSADO, 'INDIGENA': AMARILLO,
                        'MESTIZO': ROJO, 'OTRO': ROSADO_OSC}

        fig8 = make_subplots(rows=2, cols=4, specs=[[{'type': 'domain'}]*4]*2, subplot_titles=top_mp)
        for i, mun in enumerate(top_mp):
            sub = em[em['municipio'] == mun]
            fig8.add_trace(go.Pie(
                labels=sub['etnia'], values=sub['n'], hole=0.55,
                marker_colors=[_color_etnia.get(str(e).upper(), ROSADO_CLA) for e in sub['etnia']],
                textinfo='none',
                hovertemplate='%{label}<br>%{percent}<extra></extra>'),
                row=i//4 + 1, col=i%4 + 1)
        fig8.update_layout(**BL(420), showlegend=True,
                        legend=dict(orientation='h', y=-0.05, font=dict(size=9)))
        fig8.update_annotations(font_size=10)
        st.plotly_chart(fig8, width="stretch", key="g10")
        end()