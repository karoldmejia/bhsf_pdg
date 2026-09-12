#  Barco Hospital San Raffaele
## Plataforma de Visualización y Análisis del Impacto Territorial
### Pacífico Colombiano · Misiones 2023–2025
### ID: TG2_10

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboard-barco-hospital-san-raffaele.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple?logo=plotly)
![License](https://img.shields.io/badge/Uso-Institucional-red)

---

## Descripción

Este repositorio contiene la plataforma interactiva de análisis y visualización del impacto territorial del **Barco Hospital San Raffaele**, embarcación de la Fundación Italocolombiana del Monte Tabor que presta servicios de salud en comunidades del litoral Pacífico colombiano de difícil acceso.

La plataforma permite explorar, filtrar y visualizar **85,863 atenciones médicas** registradas entre 2023 y 2025 en municipios de los departamentos de Valle del Cauca, Cauca, Nariño y Chocó.

Este proyecto es el producto final de la **Fase 2** del Trabajo de Grado de la Maestría en Ciencia de Datos de la Universidad ICESI.

---

## Demo en vivo

 **[dashboard-barco-hospital-san-raffaele.streamlit.app](https://dashboard-bhsf.streamlit.app/)**

>  Los datos están anonimizados. No contienen nombres, cédulas ni información que permita identificar a los pacientes. Uso exclusivo institucional y académico.

---

## Funcionalidades del Dashboard

El dashboard está organizado en **5 pestañas temáticas**:

| Pestaña | Contenido |
|---------|-----------|
| **P1 · Alcance geográfico** | Mapa interactivo de burbujas, cobertura por municipio y departamento, KPIs territoriales |
| **P2 · ¿A quién atendemos?** | Pirámide poblacional, distribución étnica, condición humanitaria, discapacidad, ocupación |
| **P3 · Servicios prestados** | Tipos de atención, equipo profesional, diagnósticos CIE-10, laboratorios, remisiones |
| **P4 · Materno-infantil y VBG** | Gestantes, lactantes, anticoncepción, z-score nutricional, violencia basada en género, salud mental |
| **P5 · Tendencia temporal** | Evolución mensual 2023–2025, comparativa anual, servicios en el tiempo, operación por día |

### Filtros globales (sidebar)
- Año de misión (2023, 2024, 2025)
- Proyecto
- Departamento
- Municipio
- Grupo etáreo

---

##  Estructura del repositorio

```
barco-hospital-dashboard/
│
├── .streamlit/
│   └── config.toml          # Tema visual institucional (magenta #BC076F)
│
├── data/
│   ├── archivo.parquet      # Dataset consolidado y anonimizado (85,863 registros)
│   └── TablaReferencia_CIE10__1.xlsx  # Tabla de referencia diagnóstica CIE-10
│
├── .gitignore               # Exclusiones de Git (venv, cache, etc.)
├── app_impacto.py           # Aplicación principal Streamlit (841 líneas)
├── requirements.txt         # Dependencias Python
└── README.md                # Este archivo
```

---

## Instalación local

### Prerrequisitos
- Python 3.10 o superior
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Yacaicedo6/barco-hospital-dashboard.git
cd barco-hospital-dashboard

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar el entorno (Windows)
.venv\Scripts\activate

# 4. Activar el entorno (Mac/Linux)
source .venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Ejecutar la aplicación
streamlit run app_impacto.py
```

La app quedará disponible en `http://localhost:8501`

---

## Stack tecnológico

| Tecnología | Uso |
|------------|-----|
| **Python 3.10+** | Lenguaje principal |
| **Streamlit** | Framework de la aplicación web |
| **Pandas** | Procesamiento y transformación de datos |
| **Plotly** | Visualizaciones interactivas y mapas |
| **PyArrow** | Lectura eficiente del formato Parquet |
| **OpenPyXL** | Lectura de la tabla de referencia CIE-10 |
| **GitHub** | Control de versiones y alojamiento del código |
| **Streamlit Cloud** | Despliegue y hosting de la aplicación |

---

## Contexto del proyecto

El **Barco Hospital San Raffaele** opera en el litoral Pacífico colombiano, una de las regiones con mayor índice de necesidades básicas insatisfechas del país. Las comunidades atendidas son mayoritariamente:

- Afrodescendientes e indígenas
- Víctimas del conflicto armado (99.8% de los casos)
- Poblaciones sin acceso regular a servicios de salud

La plataforma permite a la Fundación Italocolombiana del Monte Tabor tomar decisiones basadas en datos sobre la distribución de recursos, priorización de territorios y medición del impacto de sus misiones humanitarias.

---

## Pipeline de datos

```
Registros clínicos Excel (2023-2025)
        ↓
Limpieza y normalización (Python + Pandas)
        ↓
Análisis Exploratorio de Datos - EDA
        ↓
Exportación a formato Parquet (optimizado)
        ↓
Plataforma de visualización Streamlit
        ↓
Despliegue en Streamlit Cloud (URL pública)
```

---

## Autores

| Nombre | Rol |
|--------|-----|
| **María José Caicedo** | Investigadora — Maestría en Ciencia de Datos, Universidad ICESI |
| **Sandra Milena Ramírez** | Investigadora — Maestría en Ciencia de Datos, Universidad ICESI |
| **Yan David Caicedo** | Investigador — Maestría en Ciencia de Datos, Universidad ICESI |

**Director de Trabajo de Grado:** Milton Orlando Sarria

**Institución:** Universidad ICESI · Facultad de Ingeniería, Diseño y Ciencias Aplicadas  
**Programa:** Maestría en Ciencia de Datos  
**Año:** 2026

---

## Instituciones vinculadas

- **Universidad ICESI** — Cali, Colombia
- **Fundación Italocolombiana del Monte Tabor** — Operadora del Barco Hospital San Raffaele

---

## Licencia y uso

Este proyecto es de uso **exclusivo institucional y académico**. Los datos han sido anonimizados conforme a la normativa colombiana de protección de datos (Ley 1581 de 2012). No está permitida su reproducción o uso comercial sin autorización expresa de la Fundación Italocolombiana del Monte Tabor y la Universidad ICESI.

---

<div align="center">
  <sub>Barco Hospital San Raffaele · Fundación Italocolombiana del Monte Tabor · Universidad ICESI · 2026</sub>
</div>
