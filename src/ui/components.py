"""Helpers de UI (html y markdown de Streamlit)."""
import streamlit as st
import pandas as pd


def sec(label: str):
    st.markdown(
        f'<div class="sec-wrap"><div class="sec-line"></div>'
        f'<div class="sec-label">{label}</div><div class="sec-line"></div></div>',
        unsafe_allow_html=True)


def card(title: str, sub: str = ""):
    s = f'<div class="chart-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>{s}',unsafe_allow_html=True)


def end():
    st.markdown("</div>", unsafe_allow_html=True)


def mapcard(title: str, sub: str = ""):
    s = f'<div class="chart-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="map-card"><div class="chart-title">{title}</div>{s}',
                unsafe_allow_html=True)


def kpi(col, icon, val, label, sub="", color=""):
    col.markdown(
        f'<div class="kpi-card {color}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-n">{val}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f'</div>', unsafe_allow_html=True)


def ibox(title: str, text: str, stat=None):
    s = f'<div class="insight-stat">{stat}</div>' if stat else ""
    st.markdown(
        f'<div class="insight"><div class="insight-title">{title}</div>'
        f'{s}<div class="insight-text">{text}</div></div>',
        unsafe_allow_html=True)


def abox(title: str, text: str, stat=None):
    s = f'<div class="insight-stat">{stat}</div>' if stat else ""
    st.markdown(
        f'<div class="alert-red">'
        f'<div class="insight-title" style="color:rgba(255,255,255,0.6)">{title}</div>'
        f'{s}<div class="insight-text">{text}</div></div>',
        unsafe_allow_html=True)


def notnull(s: pd.Series) -> pd.Series:
    return s[~s.astype(str).str.strip().str.upper().isin(['NAN', 'NONE', ''])]