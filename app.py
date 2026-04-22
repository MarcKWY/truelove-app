import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

st.markdown("""
    <style>
    /* GitHub Header & Katzen-Logo radikal entfernen */
    header[data-testid="stHeader"], [data-testid="stToolbar"], #GithubIcon { display: none !important; }
    .stApp { background-color: #050A14; color: #FFFFFF !important; }
    
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37 !important; text-align: center; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #FFFFFF; opacity: 0.9; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    
    [data-testid="stMetricValue"], label, p, span, .stMarkdown p { color: #FFFFFF !important; }
    div[data-baseweb="select"] * { color: #000000 !important; }
    div[data-baseweb="popover"] * { color: #000000 !important; }
    .gold-price { color: #D4AF37 !important; font-weight: bold; }
    
    .stApp div[data-testid="stForm"] button, .stApp button[kind="secondary"], .stApp button[kind="primaryFormSubmit"] {
        background-color: #D4AF37 !important; color: #050A14 !important; font-weight: bold !important; width: 100% !important; border-radius: 10px !important; height: 3.5em !important; border: none !important;
    }
    .stApp button[key^="dt_"], .stApp button[key^="ds_"] { background-color: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; width: auto !important; height: 2em !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK ---
def load_raw(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
        return r.json()
    except: return []

def safe_float(val):
    try: return float(val)
    except: return 0.0

# Daten laden ohne harten Cache, um "0"-Werte zu vermeiden
if 'tank_data' not in st.session_state:
    raw = load_raw("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []
if 'serv_data' not in st.session_state:
    raw = load_raw("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []
if 'fix_vals' not in st.session_state:
    raw = load_raw("fixkosten")
    if raw and len(raw) > 0:
        st.session_state.fix_vals = [safe_float(x) for x in raw[0][:4]]
    else:
        st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]

def sync_and_reload(payload, local_key, action, idx=None):
    if action == "append": st.session_state[local_key].append(payload["values"])
    elif action == "delete": st.session_state[local_key].pop(idx)
    elif action == "update": st.session_state.fix_vals = payload["values"]
    
    requests.post(SCRIPT_URL, json=payload, timeout=10)
    st.cache_data.clear()
    st.rerun()

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_y = st.selectbox("Jahr wählen", [2024, 2025, 2026], index=1)
    
    sprit = sum(safe_float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(safe_float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    fix_sum = sum(st.session_state.fix_vals)
    
    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv + fix_sum):,.2f}")
    st.write(f"🧔 Marc: CHF {sum(safe_float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=='Marc' and str(sel_y) in str(r[0])):,.2f}")
    st.write(f"👩 Fabienne: CHF {sum(safe_float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=='Fabienne' and str(sel_y) in str(r[0])):,.2f}")
    st.divider()
    st.markdown(f"⛽ Benzin: <span class='gold-price'>CHF {sprit:,.2f}</span> | ⚙️ Service: <span class='gold-price'>CHF {serv:,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    with st.form("t_form", clear_on_submit=True):
        st.markdown("### ⛽ Neuer Tankstopp")
        d = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        lit = st.number_input("Liter", step=0.1)
        pr = st.number_input("CHF/L", value=2.15)
        wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
        if st.form_submit_button("SPEICHERN"):
            sync_and_reload({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]}, "tank_data", "append")

    for i, r in enumerate(reversed(st.session_state.tank_data)):
        idx = len(st.session_state.tank_data) - 1 - i
        c1, c2 = st.columns([0.85, 0.15])
        c1.markdown(f"📅 {r[0]} | {safe_float(r[1]):.2f}L | <span class='gold-price'>CHF {safe_float(r[3]):,.2f}</span>", unsafe_allow_html=True)
        if c2.button("🗑️", key=f"dt_{idx}"):
            sync_and_reload({"sheet":"tanken","method":"delete","index":idx}, "tank_data", "delete", idx)

with tab3:
    st.markdown("<div class='card'><h3>💰 Fixkosten</h3>", unsafe_allow_html=True)
    v = st.session_state.fix_vals
    n_ü = st.number_input("Überwintern", value=v[0])
    n_s = st.number_input("Steuern", value=v[1])
    n_v = st.number_input("Versicherung", value=v[2])
    n_b = st.number_input("Bootsplatz", value=v[3])
    if st.button("FIXKOSTEN SPEICHERN"):
        sync_and_reload({"sheet":"fixkosten","method":"update","values":[n_ü, n_s, n_v, n_b]}, "fix_vals", "update")
    st.markdown(f"**Total: CHF {sum([n_ü,n_s,n_v,n_b]):,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    with st.form("s_form", clear_on_submit=True):
        st.markdown("### ⚙️ Service")
        d_s = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        arb = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten CHF", step=10.0)
        if st.form_submit_button("SERVICE SPEICHERN"):
            sync_and_reload({"sheet":"service","method":"append","values":[d_s.strftime("%d.%m.%Y"), arb, kost]}, "serv_data", "append")

    for i, r in enumerate(reversed(st.session_state.serv_data)):
        idx = len(st.session_state.serv_data) - 1 - i
        c1, c2 = st.columns([0.85, 0.15])
        c1.markdown(f"📅 {r[0]} | {r[1]} | <span class='gold-price'>CHF {safe_float(r[2]):,.2f}</span>", unsafe_allow_html=True)
        if c2.button("🗑️", key=f"ds_{idx}"):
            sync_and_reload({"sheet":"service","method":"delete","index":idx}, "serv_data", "delete", idx)
