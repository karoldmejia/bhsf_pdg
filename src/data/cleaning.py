"""Funciones puras de limpieza/normalización de columnas."""
import re as _re
import numpy as np
import pandas as pd

from src.config import ZSCORE_MAP, _NONE_VALS
from src.theme import ZSCORE_COLORS


def limpiar_etnia(s: pd.Series) -> pd.Series:
    return (s.astype(str).str.strip()
             .str.replace(r'^[A-GZa-gz]\.\s*', '', regex=True)
             .str.upper()
             .replace({
                 'AFROCOLOMBIANO/NEGRO': 'AFRODESCENDIENTE',
                 'AFROCOLOMBIANO': 'AFRODESCENDIENTE',
                 'AFROCOLOMBIANA': 'AFRODESCENDIENTE',
                 'INDIGENA': 'INDIGENA',
                 'NAN': np.nan, '': np.nan,
             }))


def limpiar_cat(s: pd.Series) -> pd.Series:
    return (s.astype(str).str.strip()
             .str.replace(r'^[A-Za-z0-9]\.\s*', '', regex=True)
             .replace({'nan': np.nan, 'NAN': np.nan, 'none': np.nan,
                       'None': np.nan, 'NONE': np.nan, '': np.nan}))


def limpiar_vbg(s: pd.Series) -> pd.Series:
    def _map_vbg(val):
        v = _re.sub(r'^[A-Za-z]\.\s*', '', str(val)).strip().upper()
        if v in ('VIOLENCIA FISICA', 'FISICA', 'MALTRATO FISICO', 'FISOCA'):
            return 'FISICA'
        if v == 'ABUSO':
            return 'ABUSO'
        if 'SEXUAL' in v and 'FISICA' not in v and 'PSICOLOG' not in v:
            return 'SEXUAL'
        if 'PSICOLOG' in v and 'FISICA' not in v:
            return 'PSICOLOGICA'
        if v in ('NO APLICA', 'NAN', 'NONE', ''):
            return np.nan
        return v if v else np.nan
    return s.apply(_map_vbg)


def mapear_zscore(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip().str.upper()
    s = s.str.replace(r'\s+', ' ', regex=True)
    s = s.str.replace(r'^[A-Za-z0-9]\.\s*', '', regex=True)
    mapped = s.replace(ZSCORE_MAP)

    def _fallback(val):
        v = str(val).upper().strip()
        if v in ZSCORE_MAP:
            return ZSCORE_MAP[v]
        if 'MAYOR' in v and '3' in v:   return 'OBESIDAD SEVERA (> +3)'
        if '2' in v and '3' in v:        return 'OBESIDAD (ENTRE +2 Y +3)'
        if '1' in v and '2' in v:        return 'SOBREPESO (ENTRE +1 Y +2)'
        if '-3' in v and '-2' in v:      return 'DESNUTRICION MODERADA (ENTRE -3 Y -2)'
        if '-2' in v and '-1' in v:      return 'RIESGO DE DESNUTRICION (ENTRE -2 Y -1)'
        if 'MENOR' in v or '-3' in v:    return 'DESNUTRICION AGUDA SEVERA (< -3)'
        if '-1' in v or 'NORMAL' in v:   return 'NORMAL (ENTRE -1 Y +1)'
        return val

    return mapped.apply(lambda x: _fallback(x) if x not in ZSCORE_COLORS else x)


def limpiar_none_col(s: pd.Series) -> pd.Series:
    return s.where(~s.astype(str).str.strip().str.lower().isin(_NONE_VALS),
                   other=np.nan)