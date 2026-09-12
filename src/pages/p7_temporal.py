"""Análisis temporal (uso institucional)"""
import pandas as pd
import plotly.express as px
import streamlit as st

from src.theme import SEQ_ROSADO, AMARILLO, ROJO, ROSADO, NAVY, AMBER, BL
from src.config import MESES_ES
from src.ui.components import sec, card, end


def _formato_mes_es(periodo_str):
    try:
        parts = str(periodo_str).split('-')
        anio, mes = int(parts[0]), int(parts[1])
        return f"{MESES_ES.get(mes, parts[1])} {anio}"
    except Exception:
        return str(periodo_str)


def render(df, cie10_map=None):
    st.markdown("""
    <div class="public-note" style="background:#FFF3E0;border-color:#D97706;color:#92400E">
    Sección de uso institucional. Esta información está destinada al equipo del Barco Hospital
    San Raffaele para análisis interno y toma de decisiones operativas.
    </div>""", unsafe_allow_html=True)

    if df['_fecha'].isna().all():
        st.info("SIN DATOS TEMPORALES DISPONIBLES.")
        return

    sec("EVOLUCIÓN DEL PROGRAMA")
    c1, c2 = st.columns([5, 3])
    cmap = {str(y): c for y, c in [
        (2023, AMARILLO), (2024, ROJO), (2025, ROSADO),
        ('2023.0', AMARILLO), ('2024.0', ROJO), ('2025.0', ROSADO)]}

    with c1:
        card("ATENCIONES POR MES", "EVOLUCIÓN MENSUAL 2023-2025")
        tmp = (df.dropna(subset=['_fecha'])
               .assign(periodo=df['_fecha'].dt.to_period('M').astype(str))
               .groupby(['periodo', '_anio']).size().reset_index(name='n'))
        tmp['_anio'] = tmp['_anio'].astype(str)
        tmp['mes_label'] = tmp['periodo'].apply(_formato_mes_es)
        fig = px.bar(tmp, x='mes_label', y='n', color='_anio',
                     color_discrete_map=cmap, barmode='stack',
                     labels={'n': 'ATENCIONES', 'mes_label': '', '_anio': 'AÑO'})
        fig.update_layout(**BL(300, mb=80),
                          legend=dict(orientation='h', y=1.08, x=0, title='', font=dict(size=10)),
                          xaxis=dict(tickangle=90, showgrid=False, tickfont_size=9),
                          yaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''))
        st.plotly_chart(fig, width="stretch", key="g36")
        end()

    with c2:
        card("COMPARATIVA ANUAL", "TOTAL POR AÑO DE MISIÓN")
        anual = df.groupby('_anio').size().reset_index(name='n')
        anual['_anio'] = pd.to_numeric(anual['_anio'], errors='coerce')
        anual = anual.dropna(subset=['_anio'])
        anual['_anio'] = anual['_anio'].astype(int)
        anual = anual[anual['_anio'].between(2023, 2027)]
        anual['_anio'] = anual['_anio'].astype(str)
        cmap2 = {'2023': AMARILLO, '2024': ROJO, '2025': ROSADO, '2026': NAVY, '2027': AMBER}
        fig2 = px.bar(anual, x='_anio', y='n', color='_anio',
                      color_discrete_map=cmap2,
                      labels={'n': 'ATENCIONES', '_anio': 'AÑO'},
                      category_orders={'_anio': ['2023', '2024', '2025', '2026', '2027']})
        fig2.update_layout(**BL(280), showlegend=False,
                           xaxis=dict(showgrid=False, title='', type='category'),
                           yaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''))
        st.plotly_chart(fig2, width="stretch", key="g37")
        end()

    sec("SERVICIOS A LO LARGO DEL TIEMPO")
    c3, c4 = st.columns(2)
    with c3:
        card("HEATMAP: ACTIVIDAD POR MES", "INTENSIDAD DE CADA SERVICIO MES A MES")
        if 'actividad' in df.columns:
            top_act = df['actividad'].value_counts().head(8).index.tolist()
            df_act = (df[df['actividad'].isin(top_act)].dropna(subset=['_fecha'])
                      .assign(mes=df['_mes'].map(MESES_ES))
                      .groupby(['actividad', 'mes']).size().reset_index(name='n'))
            orden_mes = list(MESES_ES.values())
            df_act['mes'] = pd.Categorical(df_act['mes'], categories=orden_mes, ordered=True)
            pivot = df_act.pivot(index='actividad', columns='mes', values='n').fillna(0)
            cols_ordenadas = [m for m in orden_mes if m in pivot.columns]
            pivot = pivot[cols_ordenadas]

            def _etiqueta_corta(act):
                act = str(act)
                if '(' in act and ')' in act:
                    return act[act.find('(') + 1:act.find(')')]
                return act[:30]
            pivot.index = [_etiqueta_corta(a) for a in pivot.index]

            if not pivot.empty:
                fig3 = px.imshow(pivot, color_continuous_scale=SEQ_ROSADO, aspect='auto',
                                 labels={'color': 'ATENCIONES', 'x': 'MES', 'y': 'ACTIVIDAD'})
                fig3.update_layout(**BL(340, ml=160, mr=60))
                fig3.update_xaxes(tickangle=0, tickfont_size=10)
                fig3.update_yaxes(tickfont_size=10)
                st.plotly_chart(fig3, width="stretch", key="g38")
        else:
            st.info("SIN COLUMNA DE ACTIVIDAD.")
        end()

    with c4:
        card("ATENCIONES POR DÍA DE LA SEMANA", "OPERACIÓN EN TERRENO")
        if df['_dow'].notna().any():
            dow_map = {0: 'LUN', 1: 'MAR', 2: 'MIÉ', 3: 'JUE', 4: 'VIE', 5: 'SÁB', 6: 'DOM'}
            ht = (df.dropna(subset=['_dow', '_anio'])
                  .groupby(['_dow', '_anio']).size().reset_index(name='n'))
            ht['dia'] = ht['_dow'].map(dow_map)
            ht['_anio'] = ht['_anio'].astype(str)
            cmap3 = {'2023': AMARILLO, '2024': ROJO, '2025': ROSADO,
                     '2023.0': AMARILLO, '2024.0': ROJO, '2025.0': ROSADO}
            fig4 = px.bar(ht, x='dia', y='n', color='_anio',
                          color_discrete_map=cmap3, barmode='group',
                          category_orders={'dia': ['LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB', 'DOM']},
                          labels={'n': 'ATENCIONES', 'dia': '', '_anio': 'AÑO'})
            fig4.update_layout(**BL(340),
                               legend=dict(orientation='h', y=1.08, x=0, font=dict(size=10)),
                               xaxis=dict(showgrid=False, title=''),
                               yaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''))
            st.plotly_chart(fig4, width="stretch", key="g39")
        else:
            st.info("SIN DATOS TEMPORALES.")
        end()