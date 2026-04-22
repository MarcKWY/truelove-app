import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# DEINE FESTE URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

st.markdown("""
    <style>
    /* Alles auf WEISS setzen */
    .stApp { background-color: #050A14; color: #FFFFFF !important; }
    
    /* TITEL IN GOLD */
    .truelove-title { 
        font-family: 'Georgia', serif; 
        font-size: 34px; 
        font-weight: bold; 
        color: #D4AF37 !important; 
        text-align: center; 
        margin-bottom: 0px; 
    }
    
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #FFFFFF; opacity: 0.9; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    
    /* Metric und normale Texte auf WEISS */
    [data-testid="stMetricValue"], label, p, span, .stMarkdown p { color: #FFFFFF !important; }
    
    /* Dropdown-Texte beim Auswählen schwarz */
    div[data-baseweb="select"] * { color: #000000 !important; }
    div[data-baseweb="popover"] * { color: #000000 !important; }

    /* GOLD nur für die CHF-Beträge in der Historie */
    .gold-price { color: #D4AF37 !important; font-weight: bold; }
    
    /* --- DIE RADIKALE BUTTON-LÖSUNG --- */
    /* Erwischt alle Buttons (normale und Form-Submit) */
    .stApp div[data-testid="stForm"] button, 
    .stApp button[kind="secondary"], 
    .stApp button[kind="primaryFormSubmit"] {
        background-color: #D4AF37 !important;
        color: #050A14 !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 10px !important;
        height: 3.5em !important;
        border: none !important;
        display: block !important;
    }
    
    /* AUSNAHME: Lösch-Buttons (Wir nutzen den Key, um sie wieder rot/transparent zu machen) */
    .stApp button[key^="dt_"], .stApp button[key^="ds_"] {
        background-color: transparent !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
        height: 2.2em !important;
        width: auto !important;
        font-weight: normal !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK ---
@st.cache_data(ttl=300)
def load_all_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
        return r.json()
    except: return []

if 'tank_data' not in st.session_state:
    raw = load_all_data("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []
if 'serv_data' not in st.session_state:
    raw = load_all_data("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []
if 'fix_vals' not in st.session_state:
    raw = load_all_data("fixkosten")
    if len(raw) > 0:
        try: st.session_state.fix_vals = [float(x) for x in raw[:4]]
        except: st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]
    else:
        st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]

def fast_sync(payload, local_key, action="append", idx=None):
    if action == "append": st.session_state[local_key].append(payload["values"])
    elif action == "delete": st.session_state[local_key].pop(idx)
    elif action == "update": st.session_state.fix_vals = payload["values"]
    try: requests.post(SCRIPT_URL, json=payload, timeout=5)
    except: pass
    st.cache_data.clear()

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

