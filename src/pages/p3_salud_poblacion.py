"""Salud de la población: MG, SSR, diagnósticos."""
import unicodedata
import pandas as pd
import plotly.express as px
import streamlit as st

from src.theme import SEQ_ROSADO, PAL, ROSADO, AMARILLO, ROJO, BL
from src.ui.components import sec, card, end, kpi, notnull


def render(df, cie10_map=None):
    sec("MEDICINA GENERAL - SERVICIOS PRESTADOS")
    c1, c2 = st.columns([4, 3])

    with c1:
        card("TIPOS DE ATENCIÓN PRESTADA", "ACTIVIDADES POR VOLUMEN")
        if 'actividad' in df.columns:
            act = df['actividad'].dropna().value_counts().head(15).reset_index()
            act.columns = ['actividad', 'n']
            fig = px.bar(act, x='n', y='actividad', orientation='h',
                         color='n', color_continuous_scale=SEQ_ROSADO,
                         labels={'n': 'ATENCIONES', 'actividad': ''})
            fig.update_layout(**BL(450), coloraxis_showscale=False,
                              xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='', type='log'),
                              yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig, width="stretch", key="g11")
        end()

    with c2:
        card("PROFESIONAL QUE REALIZA LA ATENCIÓN", "EQUIPO MULTIDISCIPLINARIO")
        if 'profesional_que_realiza_la_atencion' in df.columns:
            pr = df['profesional_que_realiza_la_atencion'].dropna().value_counts().head(8).reset_index()
            pr.columns = ['profesional', 'n']
            _total_pr = pr['n'].sum()
            _pull_pr = [0.08 if (n / _total_pr) < 0.05 else 0 for n in pr['n']]
            fig2 = px.pie(pr, names='profesional', values='n', hole=0.55,
                          color_discrete_sequence=PAL)
            fig2.update_traces(
                pull=_pull_pr,
                textposition='inside', textinfo='percent', textfont_size=9,
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            fig2.update_layout(**BL(380),
                               legend=dict(orientation='h', y=-0.2, font=dict(size=9)))
            st.plotly_chart(fig2, width="stretch", key="g12")
        end()

    c3, c4 = st.columns(2)
    with c3:
        card("PRIMERA CONSULTA VS SEGUIMIENTO ODONTOLOGÍA", "CONTINUIDAD DEL CUIDADO")
        if 'primera_consulta_o_seguimiento' in df.columns:
            pc = df['primera_consulta_o_seguimiento'].dropna().value_counts().reset_index()
            pc.columns = ['tipo', 'n']
            pc['tipo'] = pc['tipo'].astype(str).str.upper()
            fig3 = px.bar(pc, x='tipo', y='n', color='tipo',
                          color_discrete_sequence=[ROSADO, AMARILLO, ROJO],
                          labels={'n': 'ATENCIONES', 'tipo': ''})
            fig3.update_layout(**BL(280), showlegend=False,
                               xaxis=dict(showgrid=False, title=''),
                               yaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''))
            st.plotly_chart(fig3, width="stretch", key="g13")
        end()

    with c4:
        card("LABORATORIOS REALIZADOS", "CAPACIDAD DIAGNÓSTICA EN ZONAS SIN ACCESO")
        lab = {
            'malaria': 'MALARIA', 'vih': 'VIH', 'sifilis': 'SIFILIS',
            'hepatitis_b': 'HEPATITIS B', 'hepatitis_c': 'HEPATITIS C',
            'glucosa': 'GLUCOSA', 'hemograma': 'HEMOGRAMA',
            'parcial_de_orina': 'PARCIAL ORINA', 'coprologico': 'COPROLÓGICO',
            'dengue': 'DENGUE', 'toxoplasma_igg__igm': 'TOXOPLASMA',
        }
        ld = [{'examen': n, 'n': int(df[c].dropna().count())}
              for c, n in lab.items() if c in df.columns and df[c].dropna().count() > 0]
        if ld:
            ldf = pd.DataFrame(ld).sort_values('n', ascending=False)
            fig5 = px.bar(ldf, x='n', y='examen', orientation='h',
                          color='n', color_continuous_scale=SEQ_ROSADO)
            fig5.update_layout(**BL(320), coloraxis_showscale=False,
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''),
                               yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig5, width="stretch", key="g14")
        end()

    sec("TIPO DE REMISION Y SEGUIMIENTO")
    c5, c6 = st.columns(2)
    with c5:
        card("TIPO DE REMISIÓN MÉDICA", "ESPECIALIDADES REFERIDAS")
        if 'tipo_de_remision_medicina' in df.columns:
            rem = (df['tipo_de_remision_medicina'].dropna()
                   .pipe(notnull).value_counts().head(10).reset_index())
            rem.columns = ['remision', 'n']
            fig6b = px.bar(rem, x='n', y='remision', orientation='h',
                           color_discrete_sequence=[ROJO])
            fig6b.update_layout(**BL(300),
                                xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''),
                                yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig6b, width="stretch", key="g15")
        end()

    with c6:
        card("SEGUIMIENTO A REMISIONES", "EFECTIVIDAD DEL SEGUIMIENTO")
        seg_col_p3 = 'seguimiento_a_remision_salud_mental'
        if seg_col_p3 in df.columns:
            seg_p3 = df[seg_col_p3].dropna().pipe(notnull)
            seg_p3 = seg_p3[~seg_p3.astype(str).str.upper().isin(['SI', 'NO', 'S', 'N'])]
            if len(seg_p3) > 0:
                seg_df_p3 = seg_p3.value_counts().reset_index()
                seg_df_p3.columns = ['seguimiento', 'n']
                fig_seg_p3 = px.bar(seg_df_p3, x='n', y='seguimiento', orientation='h',
                                    color_discrete_sequence=[ROJO])
                fig_seg_p3.update_layout(**BL(300),
                                         xaxis=dict(tickangle=0, showgrid=True, gridcolor='#F3F4F6', title=''),
                                         yaxis=dict(showgrid=False, autorange='reversed', title=''))
                st.plotly_chart(fig_seg_p3, width="stretch", key="g16")
            else:
                st.info("SIN CATEGORÍAS DE SEGUIMIENTO DETALLADAS.")
        else:
            st.info("SIN DATOS DE SEGUIMIENTO.")
        end()

    sec("SALUD SEXUAL Y REPRODUCTIVA")
    c7, c8 = st.columns(2)
    with c7:
        card("METODO ANTICONCEPTIVO SELECCIONADO", "SALUD SEXUAL Y REPRODUCTIVA")
        if 'metodo_anticonceptivo_seleccionado' in df.columns:
            mac = (df['metodo_anticonceptivo_seleccionado'].dropna()
                   .pipe(notnull).value_counts().head(8).reset_index())
            mac.columns = ['metodo', 'n']
            fig = px.bar(mac, x='n', y='metodo', orientation='h',
                         color_discrete_sequence=[ROSADO])
            fig.update_layout(**BL(300),
                              xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title=''),
                              yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig, width="stretch", key="g17")
        else:
            st.info("SIN DATOS DE ANTICONCEPCIÓN.")
        end()

    with c8:
        card("TIPO DE ATENCIÓN ANTICONCEPCIÓN", "DISTRIBUCIÓN DE ATENCIONES SSR")
        if 'tipo_de_atencion_anticoncepcion' in df.columns:
            def _norm_anticoncep(s):
                s2 = unicodedata.normalize('NFD', str(s)).encode('ascii', 'ignore').decode('utf-8')
                s2 = s2.strip().upper()
                if 'ASESORI' in s2:
                    return 'Asesoría'
                if 'CONTROL' in s2:
                    return 'Control'
                if 'SEGUIMIENTO' in s2:
                    return 'Seguimiento'
                return str(s).strip().title()
            tac_raw = df['tipo_de_atencion_anticoncepcion'].dropna().pipe(notnull)
            tac_norm = tac_raw.apply(_norm_anticoncep)
            tac = tac_norm.value_counts().head(8).reset_index()
            tac.columns = ['tipo', 'n']
            tac['tipo'] = tac['tipo'].astype(str).str.upper()
            _total_tac = tac['n'].sum()
            _pull_tac = [0.08 if (n / _total_tac) < 0.05 else 0 for n in tac['n']]
            fig8 = px.pie(tac, names='tipo', values='n', hole=0.55,
                          color_discrete_sequence=PAL)
            fig8.update_traces(
                pull=_pull_tac,
                textposition='inside', textinfo='percent', textfont_size=9,
                hovertemplate='<b>%{label}</b><br>Porcentaje: %{percent}<br>Casos: %{value:,}<extra></extra>')
            fig8.update_layout(**BL(300),
                               legend=dict(orientation='h', y=-0.2, font=dict(size=9)))
            st.plotly_chart(fig8, width="stretch", key="g18")
        else:
            st.info("SIN DATOS DE TIPO DE ATENCIÓN ANTICONCEPCIÓN.")
        end()

    _total_sp = len(df)
    _n_uniq_sp = int(df['id'].dropna().nunique()) if 'id' in df.columns else _total_sp
    sec("TOP 12 DIAGNÓSTICOS PRINCIPALES")
    col_t12, col_kpi_t12 = st.columns([5, 1])
    with col_kpi_t12:
        st.markdown("<br><br>", unsafe_allow_html=True)
        kpi(col_kpi_t12, "", f"{_n_uniq_sp:,}", "PERSONAS ÚNICAS", "TOTAL REGISTROS", "mag")
    with col_t12:
        card("TOP 12 DIAGNÓSTICOS PRINCIPALES", "FRECUENCIA RELATIVA SOBRE EL TOTAL DE ATENCIONES (%)")
        if 'diagnostico_principal_medicina' in df.columns and _total_sp > 0:
            _td_sp = df['diagnostico_principal_medicina'].dropna().pipe(notnull).value_counts().head(12).reset_index()
            _td_sp.columns = ['diagnostico', 'n']
            _td_sp['frec_rel'] = (_td_sp['n'] / _total_sp * 100).round(2)
            _cie_sp = cie10_map or {}
            _td_sp['nombre_cie10'] = _td_sp['diagnostico'].apply(
                lambda x: _cie_sp.get(str(x).strip().upper(), x))
            _td_sp['etiqueta'] = _td_sp.apply(
                lambda r: f"{r['diagnostico']} - {r['nombre_cie10']}"
                          if r['nombre_cie10'] != r['diagnostico'] else r['diagnostico'], axis=1)
            _fig_sp = px.bar(_td_sp, x='frec_rel', y='etiqueta', orientation='h',
                             color='frec_rel', color_continuous_scale=SEQ_ROSADO,
                             labels={'frec_rel': '% DEL TOTAL', 'etiqueta': ''},
                             custom_data=['n'])
            _fig_sp.update_traces(
                hovertemplate='<b>%{y}</b><br>FRECUENCIA: %{x:.2f}%<br>CASOS: %{customdata[0]:,}<extra></extra>')
            _fig_sp.update_layout(**BL(420), coloraxis_showscale=False,
                                  xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                             title='% SOBRE TOTAL ATENCIONES', ticksuffix='%'),
                                  yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(_fig_sp, width="stretch", key="g19")
        else:
            st.info("SIN DATOS DE DIAGNÓSTICOS.")
        end()

    sec("DISTRIBUCIÓN TERRITORIAL DE DIAGNÓSTICOS")
    c_mun1, c_mun2 = st.columns([5, 3])
    with c_mun1:
        card("DIAGNÓSTICOS POR MUNICIPIO", "TOP 8 DIAGNÓSTICOS EN LOS PRINCIPALES MUNICIPIOS")
        dcol_m = 'diagnostico_principal_medicina'
        if dcol_m in df.columns and 'municipio' in df.columns:
            td2_m = df[dcol_m].dropna().pipe(notnull).value_counts().head(8).index.tolist()
            tm2_m = df['municipio'].dropna().value_counts().head(7).index.tolist()
            hm_raw_m = (df[df[dcol_m].isin(td2_m) & df['municipio'].isin(tm2_m)]
                        .groupby(['municipio', dcol_m]).size().reset_index(name='n')
                        .pivot(index='municipio', columns=dcol_m, values='n').fillna(0))
            if not hm_raw_m.empty:
                hm_raw_m.columns = [str(col) for col in hm_raw_m.columns]
                fig_mun = px.imshow(hm_raw_m, color_continuous_scale=SEQ_ROSADO,
                                    aspect='auto', labels={'color': 'CASOS'})
                fig_mun.update_layout(**BL(340))
                fig_mun.update_xaxes(tickangle=0, tickfont_size=10)
                st.plotly_chart(fig_mun, width="stretch", key="g20")
        end()

    with c_mun2:
        card("RESUMEN POR MUNICIPIO")
        if 'municipio' in df.columns and 'departamento' in df.columns:
            tbl_m = (df.groupby(['departamento', 'municipio'])
                    .agg(Atenciones=('municipio', 'count')).reset_index()
                    .sort_values('Atenciones', ascending=False)
                    .rename(columns={'departamento': 'DEPTO', 'municipio': 'MUNICIPIO'}))
            tbl_m['%'] = (tbl_m['Atenciones'] / tbl_m['Atenciones'].sum() * 100).round(1).astype(str) + '%'
            st.dataframe(tbl_m, use_container_width=True, hide_index=True, height=300)
        end()