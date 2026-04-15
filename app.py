import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Deine Web-App URL (Sicherstellen, dass diese exakt stimmt!)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwEhJTco_d0sr8csXaXzq5R9kdSgRoJLJlO5g2NGoO-H2oWFxsOCiatkgsDVcjbmlAT/exec"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important; font-weight: bold !important;
        color: #D4AF37 !important; text-align: center !important;
        letter-spacing: 5px !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }
    .card { background-color: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 20px; border: 1px solid #D4AF37; margin-top: 20px; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN MIT CACHE-KONTROLLE ---
def load_data(sheet_name):
    try:
        # Wir hängen einen Zeitstempel an, damit Google keine alten Daten aus dem Zwischenspeicher schickt
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}&nocache={datetime.now().timestamp()}", timeout=10)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame(columns=data[0] if data else [])
    except Exception as e:
        return pd.DataFrame()

def save_data(row_values, sheet_name):
    # Wir senden nur die NEUE Zeile, das ist viel schneller als die ganze Tabelle
    payload = {
        "sheet": sheet_name,
        "values": row_values
    }
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
menu = st.radio("MENÜ", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp</h3>", unsafe_allow_html=True)
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), t_lit, t_pr, round(t_lit * t_pr, 2), t_wer]
        if save_data(new_row, "tanken"):
            st.success("Gespeichert! lade Daten...")
            st.rerun() # App neu starten, um Tabelle anzuzeigen
    
    df_tanken = load_data("tanken")
    if not df_tanken.empty:
        st.table(df_tanken)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Service speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), s_arbeit, s_preis]
        if save_data(new_row, "service"):
            st.success("Service geloggt!")
            st.rerun()
    
    df_service = load_data("service")
    if not df_service.empty:
        st.table(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    df_t = load_data("tanken")
    df_s = load_data("service")
    sprit = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    st.metric("GESAMTKOSTEN", f"CHF {(sprit + serv + 3700):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
