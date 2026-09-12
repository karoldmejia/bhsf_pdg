"""
Constantes puras del dominio: rutas, coordenadas, meses, clasificaciones
CIE-10, SIVIGILA y mapeos de z-score. Sin dependencias de Streamlit.
"""
import numpy as np

# rutas
RUTA_DATOS = "data/archivo_v7.parquet"
RUTA_CIE10 = "data/TablaReferencia_CIE10__1.xlsx"

# coordenadas
COORDS = {
    "BUENAVENTURA":         {"lat": 3.8833,  "lon": -76.9667},
    "EL CHARCO":            {"lat": 2.4833,  "lon": -78.1167},
    "LA TOLA":              {"lat": 2.7667,  "lon": -78.2167},
    "OLAYA HERRERA":        {"lat": 2.346944, "lon": -78.325556},
    "TIMBIQUI":             {"lat": 2.7667,  "lon": -77.6833},
    "GUAPI":                {"lat": 2.5833,  "lon": -77.8833},
    "LITORAL DE SAN JUAN":  {"lat": 4.2586,  "lon": -77.3675},
    "LITORAL SAN JUAN":     {"lat": 4.2586,  "lon": -77.3675},
    "LITORAL DEL SAN JUAN": {"lat": 4.2586,  "lon": -77.3675},
    "NUQUI":                {"lat": 5.7000,  "lon": -77.2667},
    "BAJO BAUDO":           {"lat": 4.9833,  "lon": -76.9833},
    "ISCUANDE":             {"lat": 2.4500,  "lon": -77.9667},
    "MOSQUERA":             {"lat": 2.5000,  "lon": -78.4000},
    "TUMACO":               {"lat": 1.8000,  "lon": -78.7667},
    "BAHIA SOLANO":         {"lat": 6.2333,  "lon": -77.4000},
}

# meses en español
MESES_ES = {
    1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR', 5: 'MAY', 6: 'JUN',
    7: 'JUL', 8: 'AGO', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC',
}

# zscore
ZSCORE_MAP = {
    'MAYOR A +3':           'OBESIDAD SEVERA (> +3)',
    'ENTRE +2 Y +3':        'OBESIDAD (ENTRE +2 Y +3)',
    'ENTRE +1 Y +2':        'SOBREPESO (ENTRE +1 Y +2)',
    'ENTRE -1 Y +1':        'NORMAL (ENTRE -1 Y +1)',
    'ENTRE -2 Y -1':        'RIESGO DE DESNUTRICION (ENTRE -2 Y -1)',
    'ENTRE -3 Y -2':        'DESNUTRICION MODERADA (ENTRE -3 Y -2)',
    'MENOR A -3':           'DESNUTRICION AGUDA SEVERA (< -3)',
    'ENTRE - 1 Y +1':       'NORMAL (ENTRE -1 Y +1)',
    'ENTRE - 2 Y -1':       'RIESGO DE DESNUTRICION (ENTRE -2 Y -1)',
    'ENTRE - 3 Y -2':       'DESNUTRICION MODERADA (ENTRE -3 Y -2)',
    'MENOR A - 3':          'DESNUTRICION AGUDA SEVERA (< -3)',
    'ENTRE 1 Y 2':          'SOBREPESO (ENTRE +1 Y +2)',
    'ENTRE 2 Y 3':          'OBESIDAD (ENTRE +2 Y +3)',
    'ENTRE -1 Y 1':         'NORMAL (ENTRE -1 Y +1)',
    'ENTRE 1Y2':            'SOBREPESO (ENTRE +1 Y +2)',
    'ENTRE -141':           'NORMAL (ENTRE -1 Y +1)',
    'MAYORA 3 L':           'OBESIDAD SEVERA (> +3)',
    'MAYOR A 3':            'OBESIDAD SEVERA (> +3)',
    'MAYOR A+3':            'OBESIDAD SEVERA (> +3)',
    'DESNUTRICION AGUDA SEVERA': 'DESNUTRICION AGUDA SEVERA (< -3)',
    'DESNUTRICION MODERADA':     'DESNUTRICION MODERADA (ENTRE -3 Y -2)',
    'RIESGO DE DESNUTRICION':    'RIESGO DE DESNUTRICION (ENTRE -2 Y -1)',
    'NORMAL':                    'NORMAL (ENTRE -1 Y +1)',
    'SOBREPESO':                 'SOBREPESO (ENTRE +1 Y +2)',
    'OBESIDAD':                  'OBESIDAD (ENTRE +2 Y +3)',
    'OBESIDAD SEVERA':           'OBESIDAD SEVERA (> +3)',
}

# valores considerados "vacíos" al limpiar strings
_NONE_VALS = {
    'nan', 'none', 'na', 'n/a', 'null', 'no aplica', 'sin dato',
    'sin informacion', 'no reporta', 'no sabe/no reporta', '',
}

# capítulos cie-10
CAPITULOS_CIE10 = {
    'A': ('I',    'Enfermedades infecciosas y parasitarias',          'A00-A99'),
    'B': ('I',    'Enfermedades infecciosas y parasitarias',          'B00-B99'),
    'C': ('II',   'Tumores / Neoplasias',                             'C00-C99'),
    'D': ('III',  'Enfermedades de la sangre y sistema inmunitario',  'D00-D89'),
    'E': ('IV',   'Enfermedades endocrinas, nutricionales y metab.',  'E00-E99'),
    'F': ('V',    'Trastornos mentales y del comportamiento',         'F00-F99'),
    'G': ('VI',   'Enfermedades del sistema nervioso',                'G00-G99'),
    'H': ('VII',  'Enfermedades del ojo, oído y apófisis mastoides',  'H00-H99'),
    'I': ('IX',   'Enfermedades del sistema circulatorio',            'I00-I99'),
    'J': ('X',    'Enfermedades del sistema respiratorio',            'J00-J99'),
    'K': ('XI',   'Enfermedades del sistema digestivo',               'K00-K99'),
    'L': ('XII',  'Enfermedades de la piel y tejido subcutáneo',      'L00-L99'),
    'M': ('XIII', 'Enfermedades del sistema osteomuscular',           'M00-M99'),
    'N': ('XIV',  'Enfermedades del sistema genitourinario',          'N00-N99'),
    'O': ('XV',   'Embarazo, parto y puerperio',                      'O00-O99'),
    'P': ('XVI',  'Afecciones originadas en el periodo perinatal',    'P00-P99'),
    'Q': ('XVII', 'Malformaciones congénitas y anomalías cromosómicas','Q00-Q99'),
    'R': ('XVIII','Síntomas, signos y hallazgos anormales',           'R00-R99'),
    'S': ('XIX',  'Traumatismos, envenenamientos y causas externas',  'S00-S99'),
    'T': ('XIX',  'Traumatismos, envenenamientos y causas externas',  'T00-T99'),
    'V': ('XX',   'Causas externas de morbilidad y mortalidad',       'V00-V99'),
    'W': ('XX',   'Causas externas de morbilidad y mortalidad',       'W00-W99'),
    'X': ('XX',   'Causas externas de morbilidad y mortalidad',       'X00-X99'),
    'Y': ('XX',   'Causas externas de morbilidad y mortalidad',       'Y00-Y99'),
    'Z': ('XXI',  'Factores que influyen en el estado de salud',      'Z00-Z99'),
}

# clasificación sivigila
CLASIF_CRONICAS = [
    'I00','I01','I02','I03','I04','I05','I06','I07','I08','I09','I10','I11','I12',
    'I13','I14','I15','I20','I21','I22','I23','I24','I25','I26','I27','I28','I30',
    'E10','E11','E12','E13','E14','C00','C01','C02','C03','C04','C05','C06','C07',
    'J30','J31','J32','J33','J34','J35','J36','J37','J38','J40','J41','J42','J43',
    'J44','J45','J46','J47',
]
CLASIF_INFECCIOSAS = [
    'A00','A01','A02','A03','A04','A05','A06','A07','A08','A09','A15','A16','A17',
    'A18','A19','A20','A21','A22','A23','A24','A25','A26','A27','A28','A30','A31',
    'A32','A33','A34','A35','A36','A37','A38','A39','A40','A41','A49','A50','A51',
    'A52','A53','A54','A55','A56','A57','A58','A59','A60','A63','A64','A90','A91',
    'A92','A93','A94','A95','A96','A97','A98','A99','B00','B01','B02','B03','B04',
    'B05','B06','B07','B08','B09','B15','B16','B17','B18','B19','B20','B21','B22',
    'B23','B24','B25','B26','B50','B51','B52','B53','B54','B55','B56','B57','B58',
    'B59','B60','B64','B65','B66','B67','B68','B69','B70','B71','B72','B73','B74',
    'B75','B76','B77','B78','B79','B80','B81','B82','B83',
]
CLASIF_NUTRICIONAL = [
    'E40','E41','E42','E43','E44','E45','E46','E50','E51','E52','E53','E54',
    'E55','E56','E58','E59','E60','E61','E63','E64',
]
ENF_NOTIFICACION = {
    'A09X':'ENFERMEDAD DIARREICA AGUDA','A162':'TUBERCULOSIS SOSPECHA',
    'A539':'SÍFILIS','A90X':'DENGUE SOSPECHA','A920':'CHIKUNGUNA SOSPECHA',
    'A928':'ZIKA SOSPECHA','A959':'FIEBRE AMARILLA SOSPECHA','B019':'VARICELA',
    'B059':'SARAMPIÓN','B180':'HEPATITIS B','B24X':'VIH',
    'B54X':'MALARIA SOSPECHA','B559':'LEISHMANIASIS SOSPECHA',
    'B575':'CHAGAS SOSPECHA','D649':'SÍNDROME ANÉMICO',
    'E43X':'DESNUTRICIÓN AGUDA SEVERA <5A','E440':'DESNUTRICIÓN AGUDA MODERADA <5A',
    'E441':'RIESGO DE DESNUTRICIÓN','J128':'IRA POR VIRUS NUEVO',
    'J129':'IRA GRAVE','J189':'INFECCIÓN RESPIRATORIA AGUDA',
    'O369':'MORBILIDAD MATERNA EXTREMA','O95X':'MORTALIDAD MATERNA',
    'O981':'SÍFILIS GESTACIONAL','R456':'VIOLENCIA DE GÉNERO E INTRAFAMILIAR',
    'T742':'VIOLENCIA SEXUAL','T758':'LESIONES DE CAUSA EXTERNA','U072':'COVID-19',
}