import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Deine Web-App URL (Bitte prüfen, ob sie noch aktuell ist!)
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
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 16px; text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px; }
    .card { background-color: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 20px; border: 1px solid #D4AF37; margin-top: 20px; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; border-radius: 10px !important; }
    label, p, span { color: #FFFFFF !important; font-size: 20px !important; }
    h3, b { color: #D4AF37 !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; color: white !important; border: 1px solid #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

def load_data(sheet_name):
    try:
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}", timeout=10)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame(columns=data[0] if data else [])
    except:
        if sheet_name == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_data(df, sheet_name):
    payload = {"sheet": sheet_name, "values": [df.columns.tolist()] + df.values.tolist()}
    requests.post(SCRIPT_URL, json=payload, timeout=10)

# Daten laden
df_tanken = load_data("tanken")
df_service = load_data("service")

# HEADER
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime("%d.%m.%Y"), "Liter": t_lit, "CHF/L": t_pr, "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer}])
        df_tanken = pd.concat([df_tanken, new_row], ignore_index=True)
        save_data(df_tanken, "tanken")
        st.success("Im Google Sheet gespeichert!")
        st.rerun()
    
    if not df_tanken.empty:
        st.table(df_tanken)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service & Motor</h3>", unsafe_allow_html=True)
    st.markdown("<b>Specs:</b> 317 kW (425 HP) | 8.1L V8")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Service speichern"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_preis}])
        df_service = pd.concat([df_service, new_row], ignore_index=True)
        save_data(df_service, "service")
        st.success("Service geloggt!")
        st.rerun()
    
    if not df_service.empty:
        st.table(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Finanzen</h3>", unsafe_allow_html=True)
    sprit = pd.to_numeric(df_tanken["Total CHF"], errors='coerce').sum()
    serv = pd.to_numeric(df_service["CHF"], errors='coerce').sum()
    st.metric("INKL. BENZIN", f"CHF {(sprit + serv + 3700):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
