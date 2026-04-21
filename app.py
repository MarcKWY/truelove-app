import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

SCRIPT_URL = "https://google.com"

# CSS für das edle Gold-Design
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
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px;
    }
    /* Style für Lösch-Buttons */
    .stButton>button[kind="secondary"] {
        background-color: #441111 !important; border: 1px solid #ff4b4b !important;
        color: white !important; width: auto !important; padding: 0px 10px !important;
    }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN INITIALISIEREN ---
if 'tank_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=5)
        st.session_state.tank_data = r.json()[1:]
    except:
        st.session_state.tank_data = []

if 'service_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=service", timeout=5)
        st.session_state.service_data = r.json()[1:]
    except:
        st.session_state.service_data = []

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# Hauptbild (immer oben sichtbar wie in V1)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN ---
if menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"):
        st.image("tanken.jpg", use_container_width=True)
    
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    pr = c2.number_input("CHF/L", value=2.15, format="%.2f")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)

    if st.button("Speichern ✅"):
        total = round(lit * pr, 2)
        new_row = [datetime.now().strftime("%d.%m.%Y"), lit, pr, total, wer]
        st.session_state.tank_data.append(new_row)
        try:
            requests.post(SCRIPT_URL, json={"sheet": "tanken", "method": "append", "values": new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.tank_data:
        st.markdown("<h3>Letzte Tankstopps</h3>", unsafe_allow_html=True)
        # Tabelle für die Optik
        df = pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"])
        st.table(df)
        
        # Lösch-Bereich
        with st.expander("Einträge löschen"):
            for i, row in enumerate(st.session_state.tank_data):
                if st.button(f"🗑️ Lösche: {row[0]} - {row[1]}L ({row[4]})", key=f"del_t_{i}"):
                    st.session_state.tank_data.pop(i)
                    st.rerun()

# --- SERVICE ---
elif menu == "⚙️ Service":
    if os.path.exists("motor.jpg"):
        st.image("motor.jpg", use_container_width=True)

    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0, step=0.05)
    
    if st.button("Eintrag speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(new_row)
        try:
            requests.post(SCRIPT_URL, json={"sheet": "service", "method": "append", "values": new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.service_data:
        df_s = pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"])
        st.table(df_s)
        
        with st.expander("Einträge löschen"):
            for i, row in enumerate(st.session_state.service_data):
                if st.button(f"🗑️ Lösche: {row[1]} ({row[2]} CHF)", key=f"del_s_{i}"):
                    st.session_state.service_data.pop(i)
                    st.rerun()

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data) if st.session_state.tank_data else 0
    serv = sum(float(r[2]) for r in st.session_state.service_data) if st.session_state.service_data else 0
    fix = 2200 + 1500 + 350 + 1150 
    
    col1, col2 = st.columns(2)
    col1.metric("FIX + SERVICE", f"CHF {(fix + serv):,.2f}")
    col2.metric("TOTAL INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.info(f"⛽ Benzinanteil bisher: CHF {sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
