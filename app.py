import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

SCRIPT_URL = "https://google.com"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { 
        font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; 
        color: #D4AF37; text-align: center; letter-spacing: 5px; margin-bottom: 0px;
    }
    .crownline-subtitle { 
        font-family: 'Helvetica Neue', sans-serif; font-size: 16px; 
        text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px; margin-bottom: 20px;
    }
    .card { 
        background-color: rgba(255,255,255,0.05); padding: 20px; 
        border-radius: 15px; border: 1px solid #D4AF37; margin-top: 10px; margin-bottom: 20px;
    }
    h3 { color: #D4AF37 !important; }
    .stMetric label { color: #D4AF37 !important; font-weight: bold !important; }
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px;
    }
    .stButton>button[kind="secondary"] {
        background-color: #441111 !important; border: 1px solid #ff4b4b !important;
        color: white !important; width: auto !important;
    }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN INITIALISIEREN ---
if 'tank_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=5)
        st.session_state.tank_data = r.json()[1:]
    except: st.session_state.tank_data = []

if 'service_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=service", timeout=5)
        st.session_state.service_data = r.json()[1:]
    except: st.session_state.service_data = []

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["📋 Übersicht", "💰 Finanzen", "⛽ Tanken", "⚙️ Service"], horizontal=True, label_visibility="collapsed")

# Fixkosten Definition
fix_kosten = {
    "❄️ Überwintern": 2200.00,
    "📑 Steuern": 350.00,
    "🛡️ Versicherung": 1150.00,
    "⚓ Bootsplatz": 1500.00
}

# Berechnungen für alle Bereiche
sprit_total = sum(float(r[3]) for r in st.session_state.tank_data) if st.session_state.tank_data else 0
service_total = sum(float(r[2]) for r in st.session_state.service_data) if st.session_state.service_data else 0
fix_total = sum(fix_kosten.values())

# --- ÜBERSICHT ---
if menu == "📋 Übersicht":
    st.markdown("<div class='card'><h3>📋 Gesamtübersicht</h3>", unsafe_allow_html=True)
    grand_total = sprit_total + service_total + fix_total
    
    st.metric("GESAMTKOSTEN", f"CHF {grand_total:,.2f}")
    
    col1, col2 = st.columns(2)
    col1.write(f"⛽ Benzin: **CHF {sprit_total:,.2f}**")
    col1.write(f"⚙️ Service: **CHF {service_total:,.2f}**")
    col2.write(f"🏗️ Fixkosten: **CHF {fix_total:,.2f}**")
    
    st.progress(min(sprit_total / max(grand_total, 1), 1.0))
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Jährliche Fixkosten</h3>", unsafe_allow_html=True)
    for posten, betrag in fix_kosten.items():
        c1, c2 = st.columns([2, 1])
        c1.write(posten)
        c2.write(f"CHF {betrag:,.2f}")
    st.divider()
    st.write(f"**Total Fixkosten: CHF {fix_total:,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TANKEN ---
elif menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", use_container_width=True)
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01)
    pr = c2.number_input("CHF/L", value=2.15)
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)

    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        st.session_state.tank_data.append(new_row)
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.tank_data:
        df = pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"])
        st.table(df)
        with st.expander("Einträge löschen"):
            for i, row in enumerate(st.session_state.tank_data):
                if st.button(f"🗑️ {row[0]} - {row[1]}L", key=f"del_t_{i}"):
                    st.session_state.tank_data.pop(i)
                    st.rerun()

# --- SERVICE ---
elif menu == "⚙️ Service":
    if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Eintrag speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(new_row)
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.service_data:
        df_s = pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"])
        st.table(df_s)
        with st.expander("Einträge löschen"):
            for i, row in enumerate(st.session_state.service_data):
                if st.button(f"🗑️ {row[1]}", key=f"del_s_{i}"):
                    st.session_state.service_data.pop(i)
                    st.rerun()
