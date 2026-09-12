import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#F8F4F7;}
.block-container{padding:0 1.2rem 2rem !important;}

section[data-testid="stSidebar"]{background:linear-gradient(180deg,#7A1830 0%,#C42C57 100%) !important;}
section[data-testid="stSidebar"] *{color:rgba(255,255,255,0.9) !important;}
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSelectbox label{
    color:rgba(255,255,255,0.5) !important;font-size:0.68rem !important;
    font-weight:600 !important;text-transform:uppercase !important;letter-spacing:0.09em !important;}
section[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,0.15) !important;}

section[data-testid="stSidebar"] [data-baseweb="tag"]{
    background-color:#7A1830 !important;
    border:1px solid rgba(255,255,255,0.25) !important;
    border-radius:6px !important;}
section[data-testid="stSidebar"] [data-baseweb="tag"] span{
    color:#FFFFFF !important;}
section[data-testid="stSidebar"] [data-baseweb="tag"] [data-testid="stMultiSelectDeleteButton"] svg,
section[data-testid="stSidebar"] [data-baseweb="tag"] svg{
    fill:#FFFFFF !important;stroke:#FFFFFF !important;}

@media (max-width: 640px){
    .hero{flex-direction:column;min-height:auto;}
    .hero-left{min-width:unset;width:100%;padding:1rem;justify-content:flex-start;}
    .hero-left img{max-width:160px !important;}
    .hero-right{padding:1rem;justify-content:flex-start;}
    .hero-title{font-size:1.3rem;}
    .hero-badge{font-size:0.72rem;padding:0.3rem 0.8rem;}
    .block-container{padding:0 0.5rem 2rem !important;}
}

.hero{border-radius:16px;margin-bottom:1.2rem;overflow:hidden;
    display:flex;min-height:120px;box-shadow:0 4px 24px rgba(196,44,87,0.25);}
.hero-left{background:#FFFFFF;padding:1.6rem 2rem;display:flex;align-items:center;
    justify-content:center;min-width:260px;flex-shrink:0;}
.hero-right{background:linear-gradient(135deg,#7A1830 0%,#C42C57 40%,#C44D2C 70%,#C4992C 100%);
    flex:1;padding:1.6rem 2rem;display:flex;align-items:center;
    justify-content:space-between;flex-wrap:wrap;gap:1rem;position:relative;overflow:hidden;}
.hero-right::before{content:'';position:absolute;top:-80px;right:-80px;width:280px;height:280px;
    background:radial-gradient(circle,rgba(255,255,255,0.1) 0%,transparent 70%);border-radius:50%;}
.hero-eyebrow{font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.14em;
    color:rgba(255,255,255,0.7) !important;margin-bottom:0.5rem;}
.hero-title{font-family:'DM Serif Display',serif;font-size:2rem;font-weight:400;
    color:#FFFFFF !important;margin:0 0 0.3rem;line-height:1.15;}
.hero-sub{font-size:0.85rem;color:rgba(255,255,255,0.85) !important;margin:0;font-weight:300;}
.hero-badge{background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
    border-radius:24px;padding:0.4rem 1.1rem;font-size:0.78rem;color:#FFFFFF;
    font-weight:600;white-space:nowrap;}

.kpi-card{background:#fff;border-radius:14px;padding:1.1rem 1.2rem 1.3rem;
    border-left:4px solid #C42C57;box-shadow:0 2px 8px rgba(196,44,87,0.1);
    min-height:130px;display:flex;flex-direction:column;justify-content:flex-start;}
.kpi-card.red{border-left-color:#C44D2C;}
.kpi-card.blue{border-left-color:#D15533;}
.kpi-card.green{border-left-color:#C4992C;}
.kpi-card.purple{border-left-color:#D1335F;}
.kpi-card.teal{border-left-color:#D8B253;}
.kpi-card.mag{border-left-color:#C42C57;}
.kpi-icon{font-size:1.3rem;margin-bottom:0.4rem;opacity:0.85;}
.kpi-n{font-family:'DM Serif Display',serif;font-size:2rem;font-weight:400;
    color:#111827;line-height:1;margin-bottom:0.2rem;}
.kpi-label{font-size:0.69rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;color:#9CA3AF;}
.kpi-sub{font-size:0.76rem;color:#6B7280;margin-top:0.1rem;min-height:1.1rem;display:block;}

.sec-wrap{margin:1rem 0 0.6rem;display:flex;align-items:center;gap:10px;}
.sec-line{flex:1;height:1px;background:#E5E7EB;}
.sec-label{font-size:0.64rem;font-weight:700;text-transform:uppercase;
    letter-spacing:0.12em;color:#9CA3AF;white-space:nowrap;}

.chart-card{background:#fff;border-radius:13px;padding:1rem 1.2rem 0.5rem;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:0.85rem;
    min-height:80px;display:flex;flex-direction:column;justify-content:flex-start;}
.chart-title{font-size:0.77rem;font-weight:700;text-transform:uppercase;
    letter-spacing:0.06em;color:#1F2937;margin-bottom:0.1rem;}
.chart-sub{font-size:0.67rem;color:#9CA3AF;margin-bottom:0.5rem;}

.insight{background:linear-gradient(135deg,#C42C57 0%,#7A1830 100%);
    border-radius:12px;padding:1rem 1.3rem;margin-bottom:0.85rem;
    min-height:110px;display:flex;flex-direction:column;justify-content:flex-start;}
.insight-title{font-size:0.69rem;font-weight:700;text-transform:uppercase;
    letter-spacing:0.09em;color:rgba(255,255,255,0.6);margin-bottom:0.3rem;}
.insight-stat{font-family:'DM Serif Display',serif;font-size:1.8rem;color:#fff;line-height:1;}
.insight-text{font-size:0.83rem;color:rgba(255,255,255,0.9);line-height:1.5;margin-top:0.2rem;}
.alert-red{background:linear-gradient(135deg,#8B0000 0%,#C01A2D 100%);
    border-radius:12px;padding:1rem 1.3rem;margin-bottom:0.85rem;}
.map-card{background:#fff;border-radius:13px;padding:1rem 1.2rem 0.5rem;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:0.85rem;border-top:3px solid #C42C57;
    min-height:80px;display:flex;flex-direction:column;justify-content:flex-start;}

.sivigila-card{background:#fff;border-radius:12px;padding:0.8rem 1rem;
    border-left:3px solid #C42C57;box-shadow:0 1px 3px rgba(0,0,0,0.06);margin-bottom:0.5rem;
    min-height:90px;display:flex;flex-direction:column;justify-content:flex-start;}
.sivigila-title{font-size:0.75rem;font-weight:700;color:#1F2937;margin-bottom:0.2rem;text-transform:uppercase;letter-spacing:0.04em;}
.sivigila-count{font-size:1.4rem;font-weight:700;color:#C42C57;
    font-family:'DM Serif Display',serif;}

.blog-card{background:#fff;border-radius:12px;padding:1rem 1.2rem;
    border-left:4px solid #C42C57;box-shadow:0 1px 4px rgba(0,0,0,0.07);margin-bottom:0.8rem;}
.blog-autor{font-size:0.72rem;font-weight:600;color:#C42C57;margin-bottom:0.2rem;}
.blog-texto{font-size:0.85rem;color:#374151;line-height:1.5;}
.blog-fecha{font-size:0.65rem;color:#9CA3AF;margin-top:0.3rem;}

.public-note{background:#FFF8FE;border:1px solid #C42C57;border-radius:10px;
    padding:0.7rem 1rem;margin-bottom:1rem;font-size:0.8rem;color:#7A1830;}

.stTabs [data-baseweb="tab-list"]{background:transparent;gap:4px;}
.stTabs [data-baseweb="tab"]{background:#fff;border-radius:8px 8px 0 0;border:none;
    padding:0.5rem 1rem;font-size:0.8rem;font-weight:500;color:#6B7280;}
.stTabs [aria-selected="true"]{background:#C42C57 !important;color:#fff !important;}
#MainMenu,footer{visibility:hidden;}

header{
    visibility:visible;
    position:absolute;
    top:0;
    left:0;
    right:0;
    pointer-events:none;
    background:transparent !important;
}
header [data-testid="stToolbar"]{visibility:hidden;}

[data-testid="stSidebarCollapseButton"]{visibility:visible !important;}

button[data-testid="stExpandSidebarButton"]{
    position: fixed !important;
    top: 0.5rem !important;
    left: 0.5rem !important;
    z-index: 999999 !important;
    visibility: visible !important;
    display: flex !important;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)