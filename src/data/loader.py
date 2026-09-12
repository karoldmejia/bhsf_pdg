"""Carga de datos con @st.cache_data y normalización inicial."""
import numpy as np
import pandas as pd
import streamlit as st

from src.config import COORDS, RUTA_CIE10
from src.data.cleaning import (
    limpiar_etnia, limpiar_cat, limpiar_vbg, mapear_zscore, limpiar_none_col,
)


@st.cache_data(show_spinner="Cargando tabla CIE-10...")
def cargar_cie10(ruta: str = RUTA_CIE10) -> dict:
    try:
        cie = pd.read_excel(ruta, usecols=[1, 3], header=0)
        cie.columns = ['codigo', 'descripcion']
        cie = cie.dropna(subset=['codigo'])
        cie['codigo'] = cie['codigo'].astype(str).str.strip().str.upper()
        cie['descripcion'] = cie['descripcion'].astype(str).str.strip()
        return dict(zip(cie['codigo'], cie['descripcion']))
    except Exception:
        return {}


@st.cache_data(show_spinner="Cargando datos de misiones...")
def cargar(ruta: str) -> pd.DataFrame:
    df = pd.read_parquet(ruta)

    # Normalizar nombres de columnas
    df.columns = (df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True))

    # Fechas
    for c in ['fecha_de_actividad', 'fecha', 'f_de_nacimiento']:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce')
    fc = next((c for c in ['fecha_de_actividad', 'fecha'] if c in df.columns), None)
    df['_fecha'] = df[fc] if fc else pd.NaT
    df['_anio']  = df['_fecha'].dt.year       if fc else np.nan
    df['_mes']   = df['_fecha'].dt.month      if fc else np.nan
    df['_dow']   = df['_fecha'].dt.dayofweek  if fc else np.nan

    # Numéricas
    for c in ['edad', 'peso', 'talla', 'imc', 'total_laboratorios', 'semanas_de_gestacion_primera_consulta']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Categóricas con limpieza específica
    if 'etnia' in df.columns:
        df['etnia'] = limpiar_etnia(df['etnia'])
    if 'sexo' in df.columns:
        df['sexo'] = (df['sexo'].astype(str).str.upper().str.strip().replace({'MUJER': 'FEMENINO', 'HOMBRE': 'MASCULINO', 'NAN': np.nan, '': np.nan}))
    for c in ['condicion', 'discapacidad', 'grupo_etareo', 'sintomatologia_salud_mental', 'nivel_de_severidad_salud_mental', 'desencadenante_principal_salud_mental', 'primera_consulta_o_seguimiento']:
        if c in df.columns:
            df[c] = limpiar_cat(df[c])
    if 'zscore_peso_para_la_talla' in df.columns:
        df['zscore_peso_para_la_talla'] = mapear_zscore(df['zscore_peso_para_la_talla'])
    if 'tipo_de_vbg1' in df.columns:
        df['tipo_de_vbg1'] = limpiar_vbg(df['tipo_de_vbg1'])

    # Municipio / departamento
    if 'municipio' in df.columns:
        df['municipio'] = (df['municipio'].astype(str).str.upper().str.strip().replace({'LITORAL SAN JUAN': 'LITORAL DE SAN JUAN', 'LITORAL DEL SAN JUAN': 'LITORAL DE SAN JUAN',}))
    if 'departamento' in df.columns:
        df['departamento'] = df['departamento'].astype(str).str.upper().str.strip()

    # Coordenadas
    if 'municipio' in df.columns:
        df['_lat'] = df['municipio'].map(lambda m: COORDS.get(m, {}).get('lat'))
        df['_lon'] = df['municipio'].map(lambda m: COORDS.get(m, {}).get('lon'))

    # Reemplazo final de "none-like" en columnas object
    for _c in df.select_dtypes(include=['object']).columns:
        if not _c.startswith('_'):
            df[_c] = limpiar_none_col(df[_c])

    return df