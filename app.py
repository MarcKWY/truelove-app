import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# HIER DEINEN AKTUELLEN GOOGLE SCRIPT LINK EINTRAGEN
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxDI47uPR3ecg16RI3GQUaRoUZYFQ7HoMyFYwMh423JE21OvsV0VR13Q5wT4iWtMPcJJg/exec" 

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 38px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 3px; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #E0E0E0; opacity: 0.8; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    h3 { color: #D4AF37 !important; font-size: 20px; }
    .gold-text { color: #D4AF37 !important; font-weight: bold; }
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; border-radius: 10px;
    }
    .del-btn>button { background-color: #440000 !important; border: 1px solid #ff4b4b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ---
@st.cache_data(ttl=5)
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=5)
        return r.json()
    except: return []

def send_request(payload):
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
        st.cache_data.clear()
        st.rerun()
    except:
        st.error("Verbindung fehlgeschlagen")

# --- DATEN LADEN ---
if 'menu_select' not in st.session_state: st.session_state.menu_select = "📋 Übersicht"

raw_tank = fetch_data("tanken")
tank_list = raw_tank[1:] if len(raw_tank) > 1 else []

raw_serv = fetch_data("service")
serv_list = raw_serv[1:] if len(raw_serv) > 1 else []

raw_fix = fetch_data("fixkosten")
if len(raw_fix) > 1:
    f_ü, f_s, f_v, f_b = map(float, raw_fix[1][:4])
else:
    f_ü, f_s, f_v, f_b = 2200.0, 350.0, 1150.0, 1500.0

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# --- NAVIGATION ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📋 Übersicht", use_container_width=True): st.session_state.menu_select = "📋 Übersicht"
    if st.button("⛽ Tanken", use_container_width=True): st.session_state.menu_select = "⛽ Tanken"
with col_nav2:
    if st.button("💰 Finanzen", use_container_width=True): st.session_state.menu_select = "💰 Finanzen"
    if st.button("⚙️ Service", use_container_width=True): st.session_state.menu_select = "⚙️ Service"

st.divider()

# --- LOGIK ---
sel_menu = st.session_state.menu_select

# --- 📋 ÜBERSICHT ---
if sel_menu == "📋 Übersicht":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr wählen", [2024, 2025, 2026, 2027], index=1)
    
    y_str = str(sel_year)
    sprit = sum(float(r[3]) for r in tank_list if len(r) > 3 and y_str in str(r[0]))
    serv = sum(float(r[2]) for r in serv_list if len(r) > 2 and y_str in str(r[0]))
    fix = f_ü + f_s + f_v + f_b
    
    st.metric(f"GESAMT {sel_year}", f"CHF {(sprit + serv + fix):,.2f}")
    st.markdown(f"⛽ Benzin: <span class='gold-text'>CHF {sprit:,.2f}</span><br>⚙️ Service: <span class='gold-text'>CHF {serv:,.2f}</span><br>🏗️ Fixkosten: <span class='gold-text'>CHF {fix:,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💰 FINANZEN ---
elif sel_menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Fixkosten anpassen</h3>", unsafe_allow_html=True)
    n_ü = st.number_input("Überwintern", value=f_ü, step=50.0, format="%.2f")
    n_s = st.number_input("Steuern", value=f_s, step=10.0, format="%.2f")
    n_v = st.number_input("Versicherung", value=f_v, step=10.0, format="%.2f")
    n_b = st.number_input("Bootsplatz", value=f_b, step=50.0, format="%.2f")
    
    if st.button("Speichern"):
        send_request({"sheet":"fixkosten","method":"update","values":[n_ü, n_s, n_v, n_b]})
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
elif sel_menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    lit = st.number_input("Liter", min_value=0.0, format="%.2f")
    pr = st.number_input("CHF/L", value=2.15, format="%.2f")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    if st.button("Eintragen"):
        send_request({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]})
    st.markdown("</div>", unsafe_allow_html=True)
    
    for i, r in enumerate(tank_list):
        with st.expander(f"⛽ {r[0]} - {float(r[3]):.2f} CHF"):
            st.write(f"Menge: {float(r[1]):.2f} L | Preis: {float(r[2]):.2f} CHF/L | Wer: {r[4]}")
            if st.button("Löschen", key=f"del_t_{i}"):
                send_request({"sheet":"tanken","method":"delete","index": i})

# --- ⚙️ SERVICE ---
elif sel_menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0, format="%.2f")
    if st.button("Eintragen"):
        send_request({"sheet":"service","method":"append","values":[d.strftime("%d.%m.%Y"), arb, kost]})
    st.markdown("</div>", unsafe_allow_html=True)
    
    for i, r in enumerate(serv_list):
        with st.expander(f"⚙️ {r[0]} - {float(r[2]):.2f} CHF"):
            st.write(f"Arbeit: {r[1]}")
            if st.button("Löschen", key=f"del_s_{i}"):
                send_request({"sheet":"service","method":"delete","index": i})
