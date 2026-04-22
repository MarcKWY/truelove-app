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
    header[data-testid="stHeader"], [data-testid="stToolbar"], #GithubIcon { 
        background-color: #050A14 !important; 
        display: none !important;
    }
    .stApp { background-color: #050A14; color: #FFFFFF !important; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37 !important; text-align: center; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #FFFFFF; opacity: 0.9; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    [data-testid="stMetricValue"], label, p, span, .stMarkdown p { color: #FFFFFF !important; }
    .gold-price { color: #D4AF37 !important; font-weight: bold; }
    
    .stApp div[data-testid="stForm"] button, 
    .stApp button[kind="secondary"], 
    .stApp button[kind="primaryFormSubmit"] {
        background-color: #D4AF37 !important;
        color: #050A14 !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 10px !important;
        height: 3.5em !important;
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

def fast_sync(payload, local_key, action="append", idx=None):
    if action == "append": st.session_state[local_key].append(payload["values"])
    elif action == "delete": st.session_state[local_key].pop(idx)
    try: requests.post(SCRIPT_URL, json=payload, timeout=5)
    except: pass
    st.cache_data.clear()

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# NUR NOCH DREI TABS DEFINIERT
tab1, tab2, tab3 = st.tabs(["📋 Übersicht", "⛽ Tanken", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_y = st.selectbox("Jahr wählen", [2026, 2027, 2028, 2029], index=0)
    
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    
    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv):,.2f}")
    
    m_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Marc" and str(sel_y) in str(r[0]))
    f_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Fabienne" and str(sel_y) in str(r[0]))
    
    st.write(f"🧔 Marc: CHF {m_sum:,.2f}")
    st.write(f"👩 Fabienne: CHF {f_sum:,.2f}")
    st.divider()
    st.markdown(f"⛽ Benzin: <span class='gold-price'>CHF {sprit:,.2f}</span> | ⚙️ Service: <span class='gold-price'>CHF {serv:,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
with tab2:
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

# --- ⚙️ SERVICE ---
with tab3:
    with st.form("s_form", clear_on_submit=True):
        st.markdown("### ⚙️ Service")
        d_s = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        arb = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten CHF", step=10.0, format="%.2f")
        if st.form_submit_button("EINTRAG SPEICHERN"):
            new_s = [d_s.strftime("%d.%m.%Y"), arb, kost]
            fast_sync({"sheet":"service","method":"append","values":new_s}, "serv_data")
            st.rerun()
