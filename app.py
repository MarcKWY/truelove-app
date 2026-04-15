import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: PRO-APP DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Deine Web-App URL
SCRIPT_URL = "
https://script.google.com/macros/s/AKfycbwEhJTco_d0sr8csXaXzq5R9kdSgRoJLJlO5g2NGoO-H2oWFxsOCiatkgsDVcjbmlAT/exec"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important; font-weight: bold !important;
        color: #D4AF37 !important; text-align: center !important;
        letter-spacing: 5px !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
        display: block !important;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px; text-align: center; margin-top: -5px;
        color: #FFFFFF; opacity: 0.8; letter-spacing: 3px;
    }

    label, .stRadio label, p, span {
        color: #FFFFFF !important; font-size: 20px !important; font-weight: 500 !important;
    }
    
    input { color: #000000 !important; font-size: 18px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    
    .stButton>button {
        background-color: #8B6914 !important; color: white !important;
        border: 1px solid #D4AF37 !important; border-radius: 10px !important;
        font-size: 20px !important; width: 100%;
    }

    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1);
        padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37;
        line-height: 1.6;
    }
    
    h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    
    [data-testid="stTable"] {
        background-color: #0A1E3C !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ---
def load_data(sheet_name):
    try:
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}&nocache={datetime.now().timestamp()}", timeout=10)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame(columns=data[0] if data else [])
    except:
        return pd.DataFrame()

def save_data(row_values, sheet_name):
    payload = {"sheet": sheet_name, "values": row_values}
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036), index=0)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tanken Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    t_pr = st.number_input("CHF / L", value=2.15, format="%.2f")
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), t_lit, t_pr, round(t_lit * t_pr, 2), t_wer]
        if save_data(new_row, "tanken"):
            st.success("Gespeichert!")
            st.rerun()
    
    df_tanken = load_data("tanken")
    if not df_tanken.empty:
        st.table(df_tanken)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown(f"<div class='card'><h3>⚙️ Service Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown(f"""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO (High Output)<br>
    <b>Leistung:</b> 317 kW (425 HP) | <b>Hubraum:</b> 8.1 Liter V8<br>
    <b>Öl:</b> 8.5 Liter SAE 25W-40 Synthetic Blend | <b>Kühlung:</b> Zweikreiskühlung</div>""", unsafe_allow_html=True)
    
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Eintrag speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), s_arbeit, s_preis]
        if save_data(new_row, "service"):
            st.success("Service geloggt!")
            st.rerun()
    
    df_service = load_data("service")
    if not df_service.empty:
        st.table(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown(f"<div class='card'><h3>💰 Finanzen Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    df_t = load_data("tanken")
    df_s = load_data("service")
    
    # Sicherstellen, dass die Spalten numerisch sind für die Summe
    sprit_sum = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv_sum = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    fix_kosten = 3700.0
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(fix_kosten + serv_sum):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(fix_kosten + serv_sum + sprit_sum):,.2f}")
    st.info(f"⛽ Reiner Sprit {auswahl_jahr}: CHF {sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
