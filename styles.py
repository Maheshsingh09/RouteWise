"""Global CSS for the Streamlit UI."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;}
.stApp{background:#f0f4f8;color:#1e293b;}
[data-testid="stSidebar"]{background:#1e293b !important;border-right:2px solid #334155;}
[data-testid="stSidebar"] *{color:#f1f5f9 !important;}
.rw-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;margin-bottom:12px;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.rw-card.best{border-color:#2563eb;background:#eff6ff;}
.rw-card.alt{border-color:#ea580c;background:#fff7ed;}
.rw-card.tsp{border-color:#0d9488;background:#f0fdfa;}
.rw-card.danger{border-color:#dc2626;background:#fef2f2;}
.rw-card.info{border-color:#7c3aed;background:#faf5ff;}
.rw-card.warn{border-color:#f59e0b;background:#fffbeb;}
.rw-card h4{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin:0 0 8px 0;}
.dist-badge{font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;margin-bottom:8px;}
.dist-badge.blue{color:#2563eb;}.dist-badge.orange{color:#ea580c;}.dist-badge.teal{color:#0d9488;}
.route-arrow{color:#2563eb;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;}
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;margin-left:6px;}
.badge-blue{background:#dbeafe;color:#1d4ed8;border:1px solid #93c5fd;}
.badge-orange{background:#ffedd5;color:#c2410c;border:1px solid #fdba74;}
.badge-teal{background:#ccfbf1;color:#0f766e;border:1px solid #5eead4;}
.badge-purple{background:#ede9fe;color:#6d28d9;border:1px solid #c4b5fd;}
.badge-red{background:#fee2e2;color:#b91c1c;border:1px solid #fca5a5;}
.logo-banner{display:flex;align-items:center;gap:14px;padding:18px 22px;background:linear-gradient(135deg,#1e40af 0%,#1e293b 100%);border-radius:14px;border:1px solid #1e3a8a;margin-bottom:20px;}
.logo-banner .icon{font-size:36px;}.logo-banner .title{font-size:22px;font-weight:700;color:#fff;}
.logo-banner .sub{font-size:11px;color:#93c5fd;text-transform:uppercase;letter-spacing:1px;}
.user-table{width:100%;border-collapse:collapse;font-size:13px;}
.user-table th{background:#f8fafc;color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:1px;padding:8px 12px;text-align:left;border-bottom:1px solid #e2e8f0;}
.user-table td{padding:9px 12px;border-bottom:1px solid #f1f5f9;color:#334155;}
.user-table tr:hover td{background:#f8fafc;}
.pill-admin{background:#dbeafe;color:#1d4ed8;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.pill-courier{background:#ccfbf1;color:#0f766e;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.pill-customer{background:#ede9fe;color:#6d28d9;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.pill-active{background:#dcfce7;color:#15803d;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.pill-inactive{background:#fee2e2;color:#b91c1c;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.seg-table{width:100%;border-collapse:collapse;font-size:12px;font-family:'JetBrains Mono',monospace;}
.seg-table th{color:#64748b;text-align:left;padding:4px 8px;font-size:10px;text-transform:uppercase;letter-spacing:1px;}
.seg-table td{padding:4px 8px;color:#475569;border-bottom:1px solid #f1f5f9;}
.stTextInput>div>div>input,.stSelectbox>div>div,.stNumberInput>div>div>input{background:#fff !important;border:1px solid #cbd5e1 !important;color:#1e293b !important;border-radius:8px !important;}
.stButton>button{background:#2563eb !important;color:#fff !important;border:none !important;border-radius:8px !important;font-weight:600 !important;padding:8px 20px !important;transition:all .15s ease !important;}
.stButton>button:hover{background:#1d4ed8 !important;transform:translateY(-1px) !important;}
div[data-testid="stMetric"]{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;box-shadow:0 1px 3px rgba(0,0,0,.05);}
div[data-testid="stMetric"] label{color:#64748b !important;font-size:11px !important;}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{color:#2563eb !important;font-family:'JetBrains Mono',monospace !important;}
hr{border-color:#e2e8f0 !important;}
h1,h2,h3{color:#0f172a !important;}
p,li,label{color:#475569 !important;}
.stAlert{background:#fff !important;border:1px solid #e2e8f0 !important;color:#1e293b !important;}
.stSlider>div{color:#1e293b !important;}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
