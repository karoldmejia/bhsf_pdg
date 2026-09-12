"""Cobertura geográfica."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.theme import SEQ_ROSADO, ROSADO_XCL, ROSADO, ROJO, BL
from src.ui.components import sec, card, end, mapcard, kpi, ibox, abox
from src.config import COORDS


def render(df, cie10_map=None):
    total = len(df)
    mps   = int(df['municipio'].nunique())    if 'municipio'    in df.columns else 0
    deps  = int(df['departamento'].nunique()) if 'departamento' in df.columns else 0
    coms  = int(df['comunidadentidad'].dropna().nunique()) if 'comunidadentidad' in df.columns else 0
    pacs  = int(df['id'].dropna().nunique())  if 'id'           in df.columns else total

    sec("NÚMEROS DE IMPACTO")
    k1, k2, k3, k4, k5 = st.columns(5)
    kpi(k1, "", f"{total:,}",  "ATENCIONES TOTALES",   "REGISTROS ANALIZADOS")
    kpi(k2, "", f"{pacs:,}",   "PERSONAS ÚNICAS",      "IDs DISTINTOS",          "blue")
    kpi(k3, "", str(mps),      "MUNICIPIOS ATENDIDOS",  "PACÍFICO COLOMBIANO",    "red")
    kpi(k4, "", str(deps),     "DEPARTAMENTOS",         "CUBIERTOS",              "green")
    kpi(k5, "", str(coms),     "COMUNIDADES",           "PUNTOS DE PRESENCIA",    "purple")
    st.markdown("<br>", unsafe_allow_html=True)

    cm, cb = st.columns([5, 3])
    with cm:
        mapcard("COBERTURA GEOGRÁFICA - PACÍFICO COLOMBIANO",
                "BURBUJA PROPORCIONAL AL VOLUMEN DE ATENCIONES POR MUNICIPIO")
        if 'municipio' in df.columns:
            geo = df.groupby('municipio').size().reset_index(name='n')
            geo['lat'] = geo['municipio'].map(lambda m: COORDS.get(m, {}).get('lat'))
            geo['lon'] = geo['municipio'].map(lambda m: COORDS.get(m, {}).get('lon'))
            geo = geo.dropna(subset=['lat', 'lon'])
            if not geo.empty:
                fig = go.Figure()
                fig.add_trace(go.Scattermapbox(
                    lat=geo['lat'], lon=geo['lon'], mode='markers',
                    marker=dict(
                        size=geo['n'] / geo['n'].max() * 55 + 14,
                        color=geo['n'],
                        colorscale=[[0, ROSADO_XCL], [0.3, ROSADO], [0.7, ROSADO], [1, ROJO]],
                        showscale=True,
                        colorbar=dict(title="ATENCIONES", thickness=12, len=0.5, tickfont=dict(size=9), x=1.01),
                        opacity=0.85, sizemode='diameter'),
                    text=geo.apply(
                        lambda r: f"<b>{r['municipio']}</b><br>ATENCIONES: {r['n']:,}", axis=1),
                    hoverinfo='text'))
                fig.add_trace(go.Scattermapbox(
                    lat=geo['lat'], lon=geo['lon'], mode='text',
                    text=geo['municipio'].str.title(),
                    textfont=dict(size=10, color="#000000"),
                    hoverinfo='skip'))
                fig.update_layout(
                    mapbox=dict(style='carto-positron', zoom=5.2,
                                center={"lat": 3.8, "lon": -77.6}),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans,sans-serif", size=11),
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=450, showlegend=False)
                st.plotly_chart(fig, width="stretch", key="g1")
        end()

    with cb:
        card("TOP MUNICIPIOS ATENDIDOS", "RANKING POR VOLUMEN DE ATENCIONES")
        if 'municipio' in df.columns:
            tm = df['municipio'].value_counts().head(10).reset_index()
            tm.columns = ['municipio', 'n']
            fig2 = px.bar(tm, x='n', y='municipio', orientation='h',
                        color='n', color_continuous_scale=SEQ_ROSADO,
                        labels={'n': 'ATENCIONES', 'municipio': ''})
            fig2.update_layout(**BL(450), coloraxis_showscale=False,
                            xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''),
                            yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig2, width="stretch", key="g2")
        end()

    c1, c2, c3 = st.columns(3)
    with c1:
        ibox("Municipio más atendido",
            "El Charco (Nariño) concentra el mayor volumen de atenciones.", "El Charco")
    with c2:
        ibox("Presencia territorial",
            f"El barco atendió {mps} municipios en {deps} departamentos del litoral Pacífico.",
            f"{mps} municipios")
    with c3:
        abox("Contexto humanitario",
            "El 99.8% de la población es desplazada o víctima del conflicto armado.", "99.8%")