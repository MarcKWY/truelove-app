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
    /* Hintergrund und Standard-Schrift (Helles Weiss statt Silber) */
    .stApp { background-color: #050A14; color: #F0F2F6; }
    
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37; text-align: center; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #E0E0E0; opacity: 0.9; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    
    /* Goldene Schrift für CHF Beträge */
    .gold-price { color: #D4AF37 !important; font-weight: bold; }
    
    /* Beschriftungen (Labels, "Zahler", "Jahr wählen" etc.) in lesbarem Gold/Weiss */
    label, .stMarkdown p, .stSelectbox label, .stRadio label { 
        color: #D4AF37 !important; 
        font-weight: 500 !important;
        font-size: 16px !important;
    }

    /* Tab-Texte verbessern */
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; font-weight: bold; }

    /* Goldener Speicher-Button mit schwarzer Schrift */
    div.stButton > button:first-child {
        background-color: #D4AF37 !important;
        color: #050A14 !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 10px;
        border: none;
        height: 3.5em;
    }
    
    /* Diskreter Lösch-Button */
    .stButton > button[key^="dt_"], .stButton > button[key^="ds_"] {
        background-color: transparent !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
        font-size: 11px;
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
    else: st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]

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

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_y = st.selectbox("Jahr wählen", [2024, 2025, 2026, 2027], index=2)
    y_str = str(sel_y)
    
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and y_str in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and y_str in str(r[0]))
    fix_sum = sum(st.session_state.fix_vals)
    
    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv + fix_sum):,.2f}")
    
    m_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Marc" and y_str in str(r[0]))
    f_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Fabienne" and y_str in str(r[0]))
    
    st.markdown(f"🧔 Marc: <span class='gold-price'>CHF {m_sum:,.2f}</span>", unsafe_allow_html=True)
    st.markdown(f"👩 Fabienne: <span class='gold-price'>CHF {f_sum:,.2f}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"⛽ Benzin: <span class='gold-price'>CHF {sprit:,.2f}</span> | ⚙️ Service: <span class='gold-price'>CHF {serv:,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
with tab2:
    if os.path.exists("tanken.jpg"): 
        st.image("tanken.jpg", width=250)
    with st.form("t_form", clear_on_submit=True):
        st.markdown("### ⛽ Neuer Tankstopp")
        d = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        lit = st.number_input("Liter", step=0.1, format="%.2f")
        pr = st.number_input("CHF/L", value=2.15, format="%.2f")
        wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
        if st.form_submit_button("EINTRAG SPEICHERN"):
            new = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
            fast_sync({"sheet":"tanken","method":"append","values":new}, "tank_data")
            st.rerun()

    st.markdown("### Historie")
    for i, r in enumerate(reversed(st.session_state.tank_data)):
        idx = len(st.session_state.tank_data) - 1 - i
        c1, c2 = st.columns([0.85, 0.15])
        c1.markdown(f"📅 {r[0]} | {float(r[1]):.2f}L | <span class='gold-price'>CHF {float(r[3]):,.2f}</span> ({r[4]})", unsafe_allow_html=True)
        if c2.button("🗑️", key=f"dt_{idx}"):
            fast_sync({"sheet":"tanken","method":"delete","index":idx}, "tank_data", "delete", idx)
            st.rerun()

# --- 💰 FINANZEN ---
with tab3:
    st.markdown("<div class='card'><h3>💰 Fixkosten</h3>", unsafe_allow_html=True)
    v = st.session_state.fix_vals
    n_ü = st.number_input("Überwintern", value=v[0], step=50.0, format="%.2f")
    n_s = st.number_input("Steuern", value=v[1], step=10.0, format="%.2f")
    n_v = st.number_input("Versicherung", value=v[2], step=10.0, format="%.2f")
    n_b = st.number_input("Bootsplatz", value=v[3], step=50.0, format="%.2f")
    if st.button("EINTRAG SPEICHERN"):
        fast_sync({"sheet":"fixkosten","method":"update","values":[n_ü, n_s, n_v, n_b]}, "fix_vals", "update")
    st.markdown(f"Total: <span class='gold-price'>CHF {sum([n_ü,n_s,n_v,n_b]):,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⚙️ SERVICE ---
with tab4:
    if os.path.exists("motor.jpg"): 
        st.image("motor.jpg", width=250)
    with st.form("s_form", clear_on_submit=True):
        st.markdown("### ⚙️ Service")
        d_s = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        arb = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten CHF", step=10.0, format="%.2f")
        if st.form_submit_button("EINTRAG SPEICHERN"):
            new_s = [d_s.strftime("%d.%m.%Y"), arb, kost]
            fast_sync({"sheet":"service","method":"append","values":new_s}, "serv_data")
            st.rerun()

    st.markdown("### Historie")
    for i, r in enumerate(reversed(st.session_state.serv_data)):
        idx = len(st.session_state.serv_data) - 1 - i
        c1, c2 = st.columns([0.85, 0.15])
        c1.markdown(f"📅 {r[0]} | {r[1]} | <span class='gold-price'>CHF {float(r[2]):,.2f}</span>", unsafe_allow_html=True)
        if c2.button("🗑️", key=f"ds_{idx}"):
            fast_sync({"sheet":"service","method":"delete","index":idx}, "serv_data", "delete", idx)
            st.rerun()
