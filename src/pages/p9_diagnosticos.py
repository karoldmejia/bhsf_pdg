"""Todos los diagnósticos por capítulo CIE-10"""
import plotly.express as px
import streamlit as st

from src.theme import SEQ_ROSADO, BL
from src.config import CAPITULOS_CIE10
from src.ui.components import sec, card, end, kpi, notnull


def render(df, cie10_map=None):
    total = len(df)
    st.markdown("""
    <div class="public-note">
    DIAGNÓSTICOS CIE-10 REGISTRADOS EN LAS MISIONES DEL BARCO HOSPITAL SAN RAFFAELE,
    ORGANIZADOS POR CAPÍTULO SEGÚN LA CLASIFICACIÓN INTERNACIONAL DE ENFERMEDADES (OMS).
    SE OCULTAN AUTOMÁTICAMENTE LOS DIAGNÓSTICOS Y CAPÍTULOS SIN CASOS EN LA SELECCIÓN ACTUAL.
    </div>""", unsafe_allow_html=True)

    if 'diagnostico_principal_medicina' not in df.columns or total == 0:
        st.info("SIN DATOS DE DIAGNÓSTICOS DISPONIBLES.")
        return

    _cie = cie10_map or {}

    td_all = (df['diagnostico_principal_medicina'].dropna()
              .pipe(notnull).value_counts().reset_index())
    td_all.columns = ['codigo', 'n']
    td_all = td_all[td_all['n'] > 0].copy()
    td_all['pct']    = (td_all['n'] / total * 100).round(2)
    td_all['nombre'] = td_all['codigo'].apply(
        lambda x: _cie.get(str(x).strip().upper(), ''))
    td_all['etiqueta'] = td_all.apply(
        lambda r: f"{r['codigo']} - {r['nombre']}"
                  if r['nombre'] else r['codigo'], axis=1)
    td_all['letra']  = td_all['codigo'].astype(str).str.strip().str.upper().str[0]

    n_diag_unicos = len(td_all)
    n_total_diag  = int(td_all['n'].sum())

    sec("RESUMEN GENERAL")
    k1, k2, k3 = st.columns(3)
    kpi(k1, "", f"{n_total_diag:,}",
        "ATENCIONES CON DIAGNÓSTICO", "REGISTROS CON CÓDIGO CIE-10", "mag")
    kpi(k2, "", f"{n_diag_unicos:,}",
        "DIAGNÓSTICOS ÚNICOS", "CÓDIGOS CIE-10 CON CASOS", "blue")
    kpi(k3, "", f"{len(td_all[td_all['letra'].str.match(r'[A-Z]')]['letra'].unique()):,}",
        "CAPITULOS CIE-10", "CON CASOS REGISTRADOS", "red")
    st.markdown("<br>", unsafe_allow_html=True)

    capitulos_vistos = {}
    for letra in sorted(td_all['letra'].unique()):
        if letra not in CAPITULOS_CIE10:
            continue
        num_romano, nombre_cap, rango = CAPITULOS_CIE10[letra]
        clave = (num_romano, nombre_cap)
        if clave not in capitulos_vistos:
            capitulos_vistos[clave] = {
                'letras': [], 'rango': rango,
                'nombre': nombre_cap, 'romano': num_romano,
            }
        capitulos_vistos[clave]['letras'].append(letra)

    max_cap = max(
        (td_all[td_all['letra'].isin(info['letras'])]['n'].sum()
         for info in capitulos_vistos.values()), default=1)

    st.markdown("""
    <style>
    .cap-card{background:#fff;border:0.5px solid #E5E7EB;border-radius:12px;margin-bottom:8px;overflow:hidden;}
    .cap-header{display:flex;align-items:center;gap:12px;padding:0.85rem 1.1rem;}
    .cap-badge{min-width:40px;height:40px;border-radius:8px;display:flex;
        align-items:center;justify-content:center;font-size:11px;font-weight:500;flex-shrink:0;}
    .cap-title-main{font-size:13px;font-weight:500;color:#1F2937;}
    .cap-title-sub{font-size:11px;color:#6B7280;margin-top:2px;}
    .cap-stat-val{font-size:13px;font-weight:500;color:#1F2937;text-align:right;}
    .cap-stat-lbl{font-size:10px;color:#6B7280;text-align:right;}
    .cap-pct-bar{height:3px;background:#E5E7EB;}
    .diag-row{display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:0.5px solid #E5E7EB;font-size:12px;}
    .diag-row:last-child{border-bottom:none;}
    .diag-code{font-weight:500;color:#C42C57;min-width:48px;flex-shrink:0;}
    .diag-name{flex:1;color:#1F2937;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
    .diag-bar-wrap{width:80px;height:5px;background:#E5E7EB;border-radius:3px;flex-shrink:0;}
    .diag-bar{height:100%;border-radius:3px;}
    .diag-n{font-size:11px;color:#6B7280;min-width:40px;text-align:right;flex-shrink:0;}
    </style>
    """, unsafe_allow_html=True)

    BADGE_STYLES = [
        'background:#F8E5ED;color:#7A1830;',
        'background:#F9EBE8;color:#8E2F1F;',
        'background:#F9F3E8;color:#8E701F;',
    ]
    BAR_COLORS = ['#C42C57', '#C44D2C', '#C4992C']

    sec("DIAGNÓSTICOS POR CAPÍTULO CIE-10")

    for idx, (clave, info) in enumerate(capitulos_vistos.items()):
        sub = (td_all[td_all['letra'].isin(info['letras'])]
               .sort_values('n', ascending=False).copy())
        if sub.empty:
            continue

        n_cap     = int(sub['n'].sum())
        n_cod     = len(sub)
        pct_cap   = round(n_cap / total * 100, 1)
        pct_barra = round(n_cap / max_cap * 100, 1)
        color_idx = idx % 3
        badge_style = BADGE_STYLES[color_idx]
        bar_color   = BAR_COLORS[color_idx]

        titulo_expander = (
            f"Cap. {info['romano']} — {info['nombre']} "
            f"({info['rango']}) · {n_cap:,} atenciones · "
            f"{n_cod} diagnósticos · {pct_cap}% del total"
        )

        with st.expander(titulo_expander, expanded=False):
            st.markdown(
                f'<div class="cap-header" style="padding:0 0 0.8rem 0;">'
                f'<div class="cap-badge" style="{badge_style}">{info["romano"]}</div>'
                f'<div style="flex:1;min-width:0;">'
                f'<div class="cap-title-main">{info["nombre"]}</div>'
                f'<div class="cap-title-sub">{info["rango"]} &nbsp;·&nbsp; '
                f'{n_cod} diagnósticos con casos</div>'
                f'</div>'
                f'<div style="display:flex;gap:20px;flex-shrink:0;">'
                f'<div><div class="cap-stat-val">{n_cap:,}</div>'
                f'<div class="cap-stat-lbl">atenciones</div></div>'
                f'<div><div class="cap-stat-val">{pct_cap}%</div>'
                f'<div class="cap-stat-lbl">del total</div></div>'
                f'</div></div>'
                f'<div class="cap-pct-bar"><div style="height:3px;width:{pct_barra}%;'
                f'background:{bar_color};border-radius:2px;"></div></div>'
                f'<br>',
                unsafe_allow_html=True)

            sub_top = sub.head(20).copy()
            altura = max(280, min(len(sub_top) * 32, 640))
            fig = px.bar(
                sub_top, x='pct', y='etiqueta', orientation='h',
                color='pct', color_continuous_scale=SEQ_ROSADO,
                custom_data=['n', 'nombre'],
                text=sub_top['n'].apply(lambda x: f'{x:,}'),
                labels={'pct': '% del total de atenciones', 'etiqueta': ''})
            fig.update_traces(
                textposition='outside', textfont_size=10,
                hovertemplate=(
                    '<b>%{customdata[1]}</b><br>'
                    'Porcentaje: %{x:.2f}%<br>'
                    'Casos: %{customdata[0]:,}<extra></extra>'))
            fig.update_layout(
                **BL(altura), coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor='#F3F4F6',
                           title='% sobre total de atenciones', ticksuffix='%'),
                yaxis=dict(showgrid=False, autorange='reversed', tickfont_size=10))
            _key = f"diag_{info['romano'].replace(' ', '_').replace('/', '_')}"
            st.plotly_chart(fig, width="stretch", key=_key)