"""
Paleta institucional FICMTB, escalas y helper de layout Plotly.
"""

# colores institucionales
ROJO     = "#C44D2C"
AMARILLO = "#C4992C"
ROSADO   = "#C42C57"

ROJO_OSC     = "#8E2F1F"
AMARILLO_OSC = "#8E701F"
ROSADO_OSC   = "#7A1830"

ROJO_MED     = "#D15533"
AMARILLO_MED = "#D1A433"
ROSADO_MED   = "#9D1F3E"

ROJO_CLA     = "#E5A08F"
AMARILLO_CLA = "#E7D38F"
ROSADO_CLA   = "#E88BB3"

ROJO_XCL     = "#F9EBE8"
AMARILLO_XCL = "#F9F3E8"
ROSADO_XCL   = "#F8E5ED"

# paleta categórica
PAL = [
    ROSADO, ROJO_OSC, AMARILLO, ROSADO_OSC, ROJO,
    AMARILLO_OSC, ROSADO_CLA, ROJO_MED, AMARILLO_MED, ROSADO_MED,
]

# Escalas secuenciales
SEQ_ROSADO   = [ROSADO_XCL, "#F0B8D0", ROSADO_CLA, ROSADO, ROSADO_MED, ROSADO_OSC]
SEQ_ROJO     = [ROJO_XCL,   "#EFC5BC", ROJO_CLA,   ROJO,   ROJO_MED,   ROJO_OSC  ]
SEQ_AMARILLO = [AMARILLO_XCL, "#F0E3BC", AMARILLO_CLA, AMARILLO, AMARILLO_MED, AMARILLO_OSC]
SEQ_R        = [ROSADO_XCL, ROSADO_CLA, ROSADO, ROJO, ROJO_MED, ROJO_OSC]

# Compatibilidad con nombres viejos usados en el monolito
RED   = ROJO_OSC
RED2  = ROJO_CLA
GREEN  = AMARILLO_MED
AMBER  = ROJO_MED
TEAL   = ROSADO_MED
NAVY   = ROSADO_OSC
PURPLE = ROJO_MED

# Colores por categoria ZSCORE (dependen de los tonos institucionales)
ZSCORE_COLORS = {
    'OBESIDAD SEVERA (> +3)':                 ROSADO_OSC,
    'OBESIDAD (ENTRE +2 Y +3)':               ROJO_OSC,
    'SOBREPESO (ENTRE +1 Y +2)':              ROJO,
    'NORMAL (ENTRE -1 Y +1)':                 AMARILLO_CLA,
    'RIESGO DE DESNUTRICION (ENTRE -2 Y -1)': AMARILLO,
    'DESNUTRICION MODERADA (ENTRE -3 Y -2)':  ROSADO,
    'DESNUTRICION AGUDA SEVERA (< -3)':       ROSADO_MED,
}


def BL(h=300, ml=4, mr=4, mt=30, mb=4):
    """Layout base para figuras Plotly."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans,sans-serif", size=11, color="#374151"),
        margin=dict(l=ml, r=mr, t=mt, b=mb),
        height=h,
    )