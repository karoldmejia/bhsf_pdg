"""Salud mental y violencias basadas en género"""
import pandas as pd
import plotly.express as px
import streamlit as st

from src.theme import (
    SEQ_R, ROSADO, ROSADO_OSC, ROSADO_MED,
    ROJO, ROJO_MED, AMARILLO, BL,
)
from src.config import MESES_ES
from src.ui.components import sec, card, end, kpi, notnull


def render(df, cie10_map=None):
    n_vbg      = int(df['tipo_de_vbg1'].dropna().pipe(notnull).count()) if 'tipo_de_vbg1' in df.columns else 0
    n_sm       = int(df['sintomatologia_salud_mental'].dropna().pipe(notnull).count()) if 'sintomatologia_salud_mental' in df.columns else 0
    n_sev_alto = 0
    if 'nivel_de_severidad_salud_mental' in df.columns:
        n_sev_alto = int(df['nivel_de_severidad_salud_mental'].astype(str).str.upper()
                         .isin(['ALTO', 'SEVERO', 'GRAVE', 'MODERADO ALTO', 'MUY ALTO', 'ALTA']).sum())

    sec("INDICADORES - SALUD MENTAL Y VIOLENCIAS BASADAS EN GÉNERO")
    k1, k2, k3, k4 = st.columns(4)
    kpi(k1, "", f"{n_vbg:,}",      "CASOS VBG",                "VIOLENCIAS BASADAS EN GÉNERO", "red")
    kpi(k2, "", f"{n_sm:,}",       "SALUD MENTAL",             "INTERVENCIONES PSICOSOCIALES", "purple")
    kpi(k3, "", f"{n_sev_alto:,}", "SEVERIDAD ALTA",           "CASOS CON NIVEL ALTO/SEVERO",  "red")
    _n_seg = int(df['seguimiento_a_remision_salud_mental'].dropna().pipe(notnull).count()) if 'seguimiento_a_remision_salud_mental' in df.columns else 0
    kpi(k4, "", f"{_n_seg:,}",     "SEGUIMIENTO SALUD MENTAL", "REGISTROS CON SEGUIMIENTO",    "blue")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="public-note" style="margin-bottom:0.8rem">'
        '<b>Nota sobre las cifras de salud mental:</b> Los indicadores de esta sección '
        'pueden mostrar valores distintos entre sí porque cada uno contabiliza un campo '
        'diferente del mismo registro de atención psicosocial. El indicador '
        '<b>Intervenciones Psicosociales</b> cuenta registros con sintomatología '
        'documentada; <b>Diagnósticos de Psicología</b> cuenta registros con impresión '
        'diagnóstica registrada; y <b>Tipo de Atención</b> cuenta registros con tipo '
        'de consulta diligenciado. No todos los profesionales completan todos los campos '
        'en cada atención, lo que genera diferencias entre los conteos. '
        'Esto es normal en registros clínicos de campo.'
        '</div>',
        unsafe_allow_html=True)

    sec("VIOLENCIAS BASADAS EN GÉNERO")
    c1, c3 = st.columns(2)
    with c1:
        card("TIPO DE VIOLENCIA BASADA EN GÉNERO", "DISTRIBUCIÓN POR TIPO DE VIOLENCIA")
        if 'tipo_de_vbg1' in df.columns:
            vbg = df['tipo_de_vbg1'].dropna().pipe(notnull).value_counts().reset_index()
            vbg.columns = ['tipo', 'n']
            fig = px.bar(vbg, x='n', y='tipo', orientation='h',
                         color='tipo',
                         color_discrete_map={
                             'SEXUAL':      ROSADO_OSC,
                             'FISICA':      ROJO,
                             'ABUSO':       AMARILLO,
                             'PSICOLOGICA': ROJO_MED},
                         labels={'n': 'CASOS', 'tipo': ''})
            fig.update_layout(**BL(280), showlegend=False, bargap=0.05,
                              xaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='CASOS'),
                              yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig, width="stretch", key="g24")
        else:
            st.info("SIN DATOS DE VIOLENCIAS BASADAS EN GÉNERO.")
        end()

    with c3:
        card("TIEMPO DE ATENCIÓN EN VIOLENCIAS BASADAS EN GÉNERO", "TIEMPO TRANSCURRIDO HASTA LA ATENCIÓN")
        t_col = 'tiempo_de_vbg1' if 'tiempo_de_vbg1' in df.columns else None
        if t_col:
            def _norm_tiempo_vbg(val):
                v = str(val).strip().upper()
                if any(x in v for x in ['MENOR A 72', 'MENOR 72', '<72', '< A 72', '<A72',
                                        'MENOR A  HORAS', '< A  HORAS', '< 72']):
                    return 'MENOR A 72 HORAS'
                if any(x in v for x in ['MAYOR A 72', 'MAYOR 72', '>72', '> 72', '> A 72',
                                        '>A72', '>72 HORAS', '> 72 HORAS']) or v == '120':
                    return 'MAYOR A 72 HORAS'
                if any(x in v for x in ['MAYOR A 6', '> 6 MES', 'MAS DE 6', 'MAYOR 6',
                                        '>6 MES', '>6MES']):
                    return 'MAYOR A 6 MESES'
                if any(x in v for x in ['ENTRE 72', '72 H Y 6', '72H Y 6', '72 HORA',
                                        'ENTRE 72 H', 'ENTRE 3']):
                    return 'ENTRE 72 HORAS Y 6 MESES'
                return 'ENTRE 72 HORAS Y 6 MESES'

            tv_raw = df[t_col].dropna().pipe(notnull).apply(_norm_tiempo_vbg)
            tv = tv_raw.value_counts().reset_index()
            tv.columns = ['tiempo', 'n']
            _tot_tv = tv['n'].sum()
            tv['pct'] = (tv['n'] / _tot_tv * 100).round(1)
            _col_tv = {
                'MENOR A 72 HORAS':         '#D15533',
                'MAYOR A 72 HORAS':         '#C44D2C',
                'MAYOR A 6 MESES':          '#C42C57',
                'ENTRE 72 HORAS Y 6 MESES': '#D1A433',
            }
            fig3 = px.bar(tv, x='pct', y='tiempo', orientation='h',
                          color='tiempo', color_discrete_map=_col_tv,
                          custom_data=['n', 'pct'],
                          labels={'pct': '% DE CASOS', 'tiempo': ''})
            fig3.update_traces(
                hovertemplate='<b>%{y}</b><br>%{customdata[1]:.1f}% — %{customdata[0]:,} CASOS<extra></extra>')
            fig3.update_layout(**BL(280), showlegend=False,
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                          title='% DE CASOS', ticksuffix='%', tickangle=0),
                               yaxis=dict(showgrid=False, autorange='reversed',
                                          tickfont=dict(size=12)))
            st.plotly_chart(fig3, width="stretch", key="g25")
        else:
            st.info("SIN DATOS DE TIEMPO DE ATENCIÓN.")
        end()

    card("VIOLENCIAS BASADAS EN GÉNERO POR MUNICIPIO Y TIPO", "DISTRIBUCIÓN TERRITORIAL")
    if 'tipo_de_vbg1' in df.columns and 'municipio' in df.columns:
        hm_df2 = df[df['tipo_de_vbg1'].notna()].copy()
        hm_df2 = hm_df2[~hm_df2['tipo_de_vbg1'].astype(str).str.strip().str.upper().isin(['NONE', 'NAN', ''])]
        hm2 = (hm_df2.groupby(['municipio', 'tipo_de_vbg1']).size().reset_index(name='n')
               .pivot(index='municipio', columns='tipo_de_vbg1', values='n').fillna(0))
        if not hm2.empty:
            hm2.columns.name = 'TIPO DE VIOLENCIA'
            hm2.index.name = 'MUNICIPIO'
            fig_hm2 = px.imshow(hm2, color_continuous_scale=SEQ_R,
                                aspect='auto', labels={'color': 'CASOS',
                                                       'x': 'TIPO DE VIOLENCIA',
                                                       'y': 'MUNICIPIO'})
            fig_hm2.update_layout(**BL(380, mb=80))
            fig_hm2.update_xaxes(tickangle=0, tickfont_size=11, title='')
            fig_hm2.update_yaxes(title='')
            st.plotly_chart(fig_hm2, width="stretch", key="g26")
        else:
            st.info("SIN DATOS SUFICIENTES.")
    else:
        st.info("SIN DATOS PARA EL HEATMAP.")
    end()

    sec("INDICADORES DE SALUD MENTAL")
    c4, c5 = st.columns(2)
    with c4:
        card("SINTOMATOLOGÍA EN SALUD MENTAL", "MOTIVOS DE CONSULTA PSICOSOCIAL")
        sm_col = 'sintomatologia_salud_mental'
        if sm_col in df.columns:
            sm_df = df[sm_col].dropna().pipe(notnull)
            sm_df = sm_df[~sm_df.astype(str).str.upper().str.contains(
                'GESTANT|EMBARAZO|OBSTETRI', na=False)]
            if len(sm_df) > 0:
                sm = sm_df.value_counts().head(8).reset_index()
                sm.columns = ['sintoma', 'n']
                _total_sm = len(sm_df)
                sm['pct'] = (sm['n'] / _total_sm * 100).round(1)
                fig4 = px.bar(sm, x='pct', y='sintoma', orientation='h',
                              color_discrete_sequence=[ROSADO],
                              custom_data=['n'],
                              labels={'pct': '% DE CONSULTAS', 'sintoma': ''})
                fig4.update_traces(
                    hovertemplate='<b>%{y}</b><br>Porcentaje: %{x:.1f}%<br>Casos: %{customdata[0]:,}<extra></extra>')
                fig4.update_layout(**BL(280),
                                   xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                              title='% DE CONSULTAS', ticksuffix='%'),
                                   yaxis=dict(showgrid=False, autorange='reversed'))
                st.plotly_chart(fig4, width="stretch", key="g27")
            else:
                st.info("SIN DATOS DE SINTOMATOLOGÍA.")
        else:
            st.info("SIN DATOS DE SALUD MENTAL.")
        end()

    with c5:
        card("DIAGNÓSTICOS DE PSICOLOGÍA", "IMPRESIÓN DIAGNÓSTICA EN SALUD MENTAL")
        diag_psic = next((col for col in [
            'impresion_diagnostica_salud_mental',
            'impresion_diagnostica_salud_mental2',
            'impresion_diagnostica_salud_mental_nombre',
        ] if col in df.columns), None)
        if diag_psic:
            _cie = cie10_map or {}
            _total_dp = len(df[diag_psic].dropna().pipe(notnull))
            dp = df[diag_psic].dropna().pipe(notnull).value_counts().head(10).reset_index()
            dp.columns = ['diagnostico', 'n']
            dp['pct'] = (dp['n'] / _total_dp * 100).round(1)
            dp['descripcion'] = dp['diagnostico'].apply(
                lambda x: _cie.get(str(x).strip().upper(), ''))
            dp['etiqueta'] = dp.apply(
                lambda r: f"{r['diagnostico']} - {r['descripcion'][:35]}"
                          if r['descripcion'] else r['diagnostico'], axis=1)
            fig5 = px.bar(dp, x='pct', y='etiqueta', orientation='h',
                          color_discrete_sequence=[ROSADO],
                          custom_data=['n', 'diagnostico', 'descripcion'],
                          labels={'pct': '% DE ATENCIONES', 'etiqueta': ''})
            fig5.update_traces(
                hovertemplate='<b>%{customdata[1]}</b><br>%{customdata[2]}<br>Porcentaje: %{x:.1f}%<br>Casos: %{customdata[0]:,}<extra></extra>')
            fig5.update_layout(**BL(300),
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                          title='% DE ATENCIONES', ticksuffix='%'),
                               yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig5, width="stretch", key="g28")
        else:
            st.info("Columna de diagnóstico psicológico no encontrada.")
        end()

    c6, c7 = st.columns(2)
    with c6:
        card("DESENCADENANTE PRINCIPAL EN SALUD MENTAL", "FACTORES ASOCIADOS A LA CONSULTA")
        desc_col = 'desencadenante_principal_salud_mental'
        if desc_col in df.columns:
            _total_desc = len(df[desc_col].dropna().pipe(notnull))
            desc = df[desc_col].dropna().pipe(notnull).value_counts().head(8).reset_index()
            desc.columns = ['desencadenante', 'n']
            desc['pct'] = (desc['n'] / _total_desc * 100).round(1)
            fig6 = px.bar(desc, x='pct', y='desencadenante', orientation='h',
                          color_discrete_sequence=[ROSADO],
                          custom_data=['n'],
                          labels={'pct': '% DE CONSULTAS', 'desencadenante': ''})
            fig6.update_traces(
                hovertemplate='<b>%{y}</b><br>Porcentaje: %{x:.1f}%<br>Casos: %{customdata[0]:,}<extra></extra>')
            fig6.update_layout(**BL(260),
                               xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                                          title='% DE CONSULTAS', ticksuffix='%'),
                               yaxis=dict(showgrid=False, autorange='reversed'))
            st.plotly_chart(fig6, width="stretch", key="g29")
        else:
            st.info("SIN DATOS DE DESENCADENANTE.")
        end()

    with c7:
        card("TIPOS DE VBG EN EL TIEMPO",
             "EVOLUCIÓN TEMPORAL POR TIPO DE VIOLENCIA BASADA EN GÉNERO")
        if 'tipo_de_vbg1' in df.columns and '_fecha' in df.columns:
            _df_vt = df[df['tipo_de_vbg1'].notna()].copy()
            _df_vt = _df_vt[~_df_vt['tipo_de_vbg1'].astype(str).str.upper().isin(['NONE', 'NAN', ''])]
            if not _df_vt.empty and _df_vt['_fecha'].notna().any():
                _df_vt['periodo'] = _df_vt['_fecha'].dt.to_period('M').astype(str)
                _df_vt['mes_label'] = _df_vt['_fecha'].apply(
                    lambda d: f"{MESES_ES.get(d.month, str(d.month))} {d.year}"
                    if pd.notna(d) else None)
                _vt = (_df_vt.groupby(['mes_label', 'periodo', 'tipo_de_vbg1'])
                       .size().reset_index(name='casos'))
                _vt['tot_mes'] = _vt.groupby('periodo')['casos'].transform('sum')
                _vt['pct'] = (_vt['casos'] / _vt['tot_mes'] * 100).round(1)
                _vt = _vt.sort_values('periodo')

                _orden_periodos = (_vt[['periodo', 'mes_label']]
                                   .drop_duplicates()
                                   .sort_values('periodo')['mes_label'].tolist())

                _col_vt = {'SEXUAL': '#C42C57', 'FISICA': '#D15533',
                           'PSICOLOGICA': '#D1A433', 'ABUSO': '#C44D2C',
                           'OTRAS': '#9D1F3E', 'ECONOMICA': '#8E701F',
                           'ACOSO': '#7A1830'}

                fig_vt = px.bar(
                    _vt, x='mes_label', y='casos', color='tipo_de_vbg1',
                    color_discrete_map=_col_vt,
                    category_orders={'mes_label': _orden_periodos},
                    labels={'mes_label': '', 'casos': 'CASOS', 'tipo_de_vbg1': 'TIPO'},
                    custom_data=['tipo_de_vbg1', 'pct'])
                fig_vt.update_traces(
                    hovertemplate='<b>%{customdata[0]}</b><br>PERIODO: %{x}<br>'
                                  'CASOS: %{y:,}<br>FRECUENCIA: %{customdata[1]:.1f}%<extra></extra>')
                fig_vt.update_layout(
                    **BL(280, mb=80), barmode='stack',
                    legend=dict(orientation='h', y=1.08, x=0, font=dict(size=9), title=''),
                    xaxis=dict(tickangle=45, showgrid=False, title='', tickfont=dict(size=9)),
                    yaxis=dict(showgrid=True, gridcolor='#F3F4F6', title='CASOS'))
                st.plotly_chart(fig_vt, width="stretch", key="g30")
            else:
                st.info("SIN DATOS TEMPORALES DE VBG.")
        else:
            st.info("SIN DATOS DE VBG O FECHAS.")
        end()