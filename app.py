import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection # Erfordert: pip install st-gsheets-connection

# --- SETUP: PRO-APP DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important;
        font-weight: bold !important;
        color: #D4AF37 !important;
        text-align: center !important;
        margin-bottom: 0px !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }
    label, .stRadio label, p, span { color: #FFFFFF !important; font-size: 20px !important; }
    div[data-testid="stRadio"] label { font-size: 45px !important; }
    input { color: #000000 !important; font-size: 18px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85); padding: 15px;
        border-radius: 15px; border: 2px solid #D4AF37; margin-top: 10px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05); padding: 25px;
        border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 20px;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- VERBINDUNG ZU GOOGLE SHEETS ---
# (Du musst eine Google Sheet URL in den Streamlit Secrets hinterlegen)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    tank_data = conn.read(worksheet="Tankstellen")
    service_data = conn.read(worksheet="Service")
except:
    # Fallback, falls Google Sheets noch nicht konfiguriert ist
    if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
    if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8;'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2026, 2036), index=0)
st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- LOGIK (Hier geht es weiter wie bisher) ---
# ... (Hier fügen wir die Speicher-Logik für Google Sheets ein)

st.info("💡 Diese App kann auf dem Home-Bildschirm deines Handys installiert werden.")
