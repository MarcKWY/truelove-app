import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Deine neue Web-App URL
SCRIPT_URL = "https://google.com"

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
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; }
    label, p, span { color: #FFFFFF !important; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ZUM LADEN & SPEICHERN ---
def load_data(sheet_name):
    try:
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}")
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except:
        if sheet_name == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_data(df, sheet_name):
    # Wir senden den kompletten Inhalt der Tabelle als JSON an dein Skript
    payload = {
        "sheet": sheet_name,
        "values": [df.columns.tolist()] + df.values.tolist()
    }
    requests.post(SCRIPT_URL, json=payload)

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036))
menu = st.radio("MENÜ", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True)

# Daten laden
df_tanken = load_data("tanken")
df_service = load_data("service")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp</h3>", unsafe_allow_html=True)
    t_lit = st.number_input("Liter", min_value=0.0)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime("%d.%m.%Y"), "Liter": t_lit, "CHF/L": t_pr, "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer}])
        df_tanken = pd.concat([df_tanken, new_row], ignore_index=True)
        save_data(df_tanken, "tanken")
        st.success("Gespeichert!")
        st.rerun()
    
    st.table(df_tanken)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_preis}])
        df_service = pd.concat([df_service, new_row], ignore_index=True)
        save_data(df_service, "service")
        st.success("Service gespeichert!")
        st.rerun()
    
    st.table(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    sprit = pd.to_numeric(df_tanken["Total CHF"]).sum() if not df_tanken.empty else 0
    serv = pd.to_numeric(df_service["CHF"]).sum() if not df_service.empty else 0
    st.metric("TOTAL KOSTEN", f"CHF {(sprit + serv + 3700):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
