import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# HIER DEINE URL EINTRAGEN
SCRIPT_URL = "DEINE_GOOGLE_URL_HIER"

# --- SPEED-OPTIMIERUNG (CACHING) ---
@st.cache_data(ttl=600) # Speichert Daten für 10 Minuten im Cache
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
        return r.json()
    except: return []

def send_request(payload):
    with st.spinner('Speichere Daten...'):
        try:
            requests.post(SCRIPT_URL, json=payload, timeout=10)
            st.cache_data.clear() # Cache leeren, damit neue Daten geladen werden
            st.rerun()
        except: st.error("Fehler beim Speichern!")

# --- DATEN INITIAL LADEN ---
raw_tank = fetch_data("tanken")
tank_list = raw_tank[1:] if len(raw_tank) > 1 else []

raw_serv = fetch_data("service")
serv_list = raw_serv[1:] if len(raw_serv) > 1 else []

raw_fix = fetch_data("fixkosten")
f_ü, f_s, f_v, f_b = (float(raw_fix[1][0]), float(raw_fix[1][1]), float(raw_fix[1][2]), float(raw_fix[1][3])) if len(raw_fix) > 1 else (2200.0, 350.0, 1150.0, 1500.0)

# --- DESIGN & BILDER ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>TRUELOVE</h1>", unsafe_allow_html=True)

# Bild Logik: Zeigt Bild nur wenn Datei existiert
if os.path.exists("boot_gross.jpg"):
    st.image("boot_gross.jpg", use_container_width=True)

# --- NAVIGATION ---
menu = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with menu[0]:
    sel_year = st.selectbox("Jahr", [2024, 2025, 2026])
    sprit = sum(float(r[3]) for r in tank_list if str(sel_year) in str(r[0]))
    serv = sum(float(r[2]) for r in serv_list if str(sel_year) in str(r[0]))
    total = sprit + serv + f_ü + f_s + f_v + f_b
    
    st.metric("Gesamt CHF", f"{total:,.2f}")
    st.write(f"⛽ Benzin: **{sprit:,.2f}** | ⚙️ Service: **{serv:,.2f}**")

# --- ⛽ TANKEN ---
with menu[1]:
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    with st.form("tank_form"):
        d = st.date_input("Datum", date.today())
        lit = st.number_input("Liter", step=0.1, format="%.2f")
        pr = st.number_input("Preis CHF/L", value=2.15, format="%.2f")
        wer = st.selectbox("Wer?", ["Marc", "Fabienne"])
        if st.form_submit_button("Speichern"):
            send_request({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]})

    # Liste mit Löschfunktion
    for i, r in enumerate(reversed(tank_list)):
        col1, col2 = st.columns([4, 1])
        col1.write(f"📅 {r[0]} | {float(r[1]):.2f}L | {float(r[3]):.2f} CHF")
        if col2.button("🗑️", key=f"del_t_{i}"):
            send_request({"sheet":"tanken","method":"delete","index": len(tank_list)-1-i})

# --- ⚙️ SERVICE ---
with menu[3]:
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    with st.form("serv_form"):
        d_s = st.date_input("Datum", date.today())
        txt = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten", step=10.0, format="%.2f")
        if st.form_submit_button("Eintragen"):
            send_request({"sheet":"service","method":"append","values":[d_s.strftime("%d.%m.%Y"), txt, kost]})

    for i, r in enumerate(reversed(serv_list)):
        col1, col2 = st.columns([4, 1])
        col1.write(f"📅 {r[0]} | {r[1]} | {float(r[2]):.2f} CHF")
        if col2.button("🗑️", key=f"del_s_{i}"):
