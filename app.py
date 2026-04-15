import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Dein funktionierender Google-Link
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhDxQNTjyCGLLR5hZwUo_7tQ5wEohouVXHrbn-FJzDKUPJ8c0MmbzfwfiOxUYDyRwE/exec"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { 
        font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; 
        color: #D4AF37; text-align: center; letter-spacing: 5px; 
    }
    .crownline-subtitle { 
        font-family: 'Helvetica Neue', sans-serif; font-size: 16px; 
        text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px; 
    }
    .card { 
        background-color: rgba(255,255,255,0.05); padding: 15px; 
        border-radius: 15px; border: 1px solid #D4AF37; margin-top: 20px;
    }
    h3 { color: #D4AF37 !important; }
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px;
    }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK (BLITZSCHNELL DURCH CACHING) ---
if 'tank_data' not in st.session_state:
    try:
        # Einmaliges Laden beim Start
        r = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=10)
        st.session_state.tank_data = r.json()[1:]
    except:
        st.session_state.tank_data = []

if 'service_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=service", timeout=10)
        st.session_state.service_data = r.json()[1:]
    except:
        st.session_state.service_data = []

# --- UI HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    pr = c2.number_input("CHF/L", value=2.15, format="%.2f")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        timestamp = datetime.now().strftime("%d.%m.%Y")
        total = round(lit * pr, 2)
        new_row = [timestamp, lit, pr, total, wer]
        
        # Sofort lokal speichern (keine Verzögerung)
        st.session_state.tank_data.append(new_row)
        
        # Hintergrund-Sync zu Google
        try:
            requests.post(SCRIPT_URL, json={"sheet": "tanken", "method": "append", "values": new_row}, timeout=2)
        except:
            pass
        st.rerun()

    if st.session_state.tank_data:
        df = pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"])
        # Saubere Formatierung für die Anzeige
        df["Liter"] = df["Liter"].map(lambda x: f"{float(x):.2f}")
        df["CHF/L"] = df["CHF/L"].map(lambda x: f"{float(x):.2f}")
        df["Total"] = df["Total"].map(lambda x: f"{float(x):.2f}")
        st.table(df)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE ---
elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0, step=0.05)
    
    if st.button("Eintrag speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(new_row)
        try:
            requests.post(SCRIPT_URL, json={"sheet": "service", "method": "append", "values": new_row}, timeout=2)
        except:
            pass
        st.rerun()

    if st.session_state.service_data:
        df_s = pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"])
        df_s["CHF"] = df_s["CHF"].map(lambda x: f"{float(x):.2f}")
        st.table(df_s)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    sprit = sum(float(row[3]) for row in st.session_state.tank_data) if st.session_state.tank_data else 0
    serv = sum(float(row[2]) for row in st.session_state.service_data) if st.session_state.service_data else 0
    fix = 2200 + 1500 + 350 + 1150 # Deine Fixkosten
    
    col1, col2 = st.columns(2)
    col1.metric("FIX + SERVICE", f"CHF {(fix + serv):,.2f}")
    col2.metric("TOTAL INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.info(f"⛽ Benzinanteil: CHF {sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
