"""Sidebar de filtros globales. Devuelve el DataFrame filtrado."""
import streamlit as st
import pandas as pd

from src.assets import logo_html


def sidebar(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        _ltag = logo_html()
        st.markdown(
            f'<div style="padding:1.4rem 0 1.2rem">'
            f'<div style="margin-bottom:10px">{_ltag}</div>'
            f'<div style="font-size:0.63rem;color:rgba(255,255,255,0.4);'
            f'text-transform:uppercase;letter-spacing:0.1em;margin-top:4px">'
            f'Filtros globales</div></div>',
            unsafe_allow_html=True)
        st.markdown("---")

        anios = sorted(df['_anio'].dropna().unique().astype(int).tolist())
        sa = st.multiselect("Año de misión", anios, default=anios)

        if 'proyecto' in df.columns:
            proys = sorted(df['proyecto'].dropna().unique().tolist())
            sp = st.multiselect("Proyecto", proys, default=proys)
        else:
            sp = []

        if 'departamento' in df.columns:
            deps = sorted(df['departamento'].dropna().unique().tolist())
            sd = st.multiselect("Departamento", deps, default=deps)
        else:
            sd = []

        if 'municipio' in df.columns:
            dfd = df[df['departamento'].isin(sd)] if (sd and 'departamento' in df.columns) else df
            mps = sorted(dfd['municipio'].dropna().unique().tolist())
            sm = st.multiselect("Municipio", mps, default=mps)
        else:
            sm = []

        if 'comunidadentidad' in df.columns:
            dfc = df.copy()
            if sm and 'municipio' in df.columns:
                dfc = dfc[dfc['municipio'].isin(sm)]
            coms_disp = sorted(dfc['comunidadentidad'].dropna().unique().tolist())
            sc = st.multiselect("Comunidad / Entidad", coms_disp, default=coms_disp)
        else:
            sc = []

        if 'grupo_etareo' in df.columns:
            ges = sorted(df['grupo_etareo'].dropna().unique().tolist())
            sge = st.multiselect("Grupo etario", ges, default=ges)
        else:
            sge = []

        st.markdown("---")
        st.markdown(
            '<div style="font-size:0.62rem;color:rgba(255,255,255,0.3);'
            'text-align:center;line-height:1.8">Datos anonimizados - Misiones 2023-2025<br>'
            'Fundación Italocolombiana del Monte Tabor</div>',
            unsafe_allow_html=True)

    mask = pd.Series(True, index=df.index)
    if sa  and '_anio'            in df.columns: mask &= df['_anio'].isin(sa)
    if sp  and 'proyecto'         in df.columns: mask &= df['proyecto'].isin(sp)
    if sm  and 'municipio'        in df.columns: mask &= df['municipio'].isin(sm)
    if sc  and 'comunidadentidad' in df.columns: mask &= (df['comunidadentidad'].isin(sc) | df['comunidadentidad'].isna())
    if sge and 'grupo_etareo'     in df.columns: mask &= df['grupo_etareo'].isin(sge)
    return df[mask].copy()