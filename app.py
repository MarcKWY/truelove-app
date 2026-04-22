import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# DEINE FESTE URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec" 

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37; text-align: center; margin-bottom: 0px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    div.stButton > button:first-child { background-color: #D4AF37 !important; color: #050A14 !important; font-weight: bold !important; width: 100%; border-radius: 10px; }
    .stButton > button[key^="del"] { background-color: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; font-size: 11px; padding: 2px 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK (INSTANT SPEED) ---
def load_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
        return r.json()[1:]
    except: return []

# Einmaliges Laden beim Start
if 'tank_data' not in st.session_state:
    st.session_state.tank_data = load_data("tanken")
if 'serv_data' not in st.session_state:
    st.session_state.serv_data = load_data("service")

def sync_action(payload, local_list, action="append"):
    """Führt die Aktion lokal sofort aus und sendet sie dann an Google"""
    if action == "append":
        local_list.append(payload["values"])
    elif action == "delete":
        local_list.pop(payload["index"])
    
    # Der eigentliche Sync-Befehl an Google (ohne die App zu blockieren)
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
    except:
        pass 

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with tab1:
    sel_year = st.selectbox("Jahr", [2024, 2025, 2026, 2027], index=2)
    y = str(sel_year)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and y in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and y in str(r[0]))
    
    st.metric(f"GESAMT {sel_year}", f"CHF {(sprit + serv + 5200):,.2f}") # 5200 als Platzhalter Fixkosten
    
    m_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Marc" and y in str(r[0]))
    f_sum = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>4 and r[4]=="Fabienne" and y in str(r[0]))
    
    c1, c2 = st.columns(2)
    c1.write(f"🧔 Marc: **{m_sum:,.2f}**")
    c2.write(f"👩 Fabienne: **{f_sum:,.2f}**")

# --- ⛽ TANKEN ---
with tab2:
    with st.form("t_form", clear_on_submit=True):
        d = st.date_input("Datum", date.today())
        lit = st.number_input("Liter", step=0.1)
        pr = st.number_input("CHF/L", value=2.15)
        wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
        if st.form_submit_button("SPEICHERN"):
            new_row = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
            sync_action({"sheet":"tanken","method":"append","values":new_row}, st.session_state.tank_data)
            st.rerun()

    for i, r in enumerate(reversed(st.session_state.tank_data)):
        idx = len(st.session_state.tank_data) - 1 - i
        col1, col2 = st.columns([0.85, 0.15])
        col1.write(f"📅 {r[0]} | {r[1]}L | **{r[3]} CHF** ({r[4]})")
        if col2.button("🗑️", key=f"del_t_{idx}"):
            sync_action({"sheet":"tanken","method":"delete","index":idx}, st.session_state.tank_data, "delete")
            st.rerun()

# --- ⚙️ SERVICE ---
with tab4:
    with st.form("s_form", clear_on_submit=True):
        d_s = st.date_input("Datum", date.today())
        arb = st.text_input("Was?")
        kost = st.number_input("CHF")
        if st.form_submit_button("SERVICE SPEICHERN"):
            new_s = [d_s.strftime("%d.%m.%Y"), arb, kost]
            sync_action({"sheet":"service","method":"append","values":new_s}, st.session_state.serv_data)
            st.rerun()

    for i, r in enumerate(reversed(st.session_state.serv_data)):
        idx = len(st.session_state.serv_data) - 1 - i
        col1, col2 = st.columns([0.85, 0.15])
        col1.write(f"📅 {r[0]} | {r[1]} | **{r[2]} CHF**")
        if col2.button("🗑️", key=f"del_s_{idx}"):
            sync_action({"sheet":"service","method":"delete","index":idx}, st.session_state.serv_data, "delete")
            st.rerun()
