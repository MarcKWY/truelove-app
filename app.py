import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

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
    label, p, span { color: #FFFFFF !important; font-size: 20px !important; }
    h3, b { color: #D4AF37 !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ---
def load_data(sheet_name):
    try:
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}", timeout=10)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"] if sheet_name=="tanken" else ["Datum", "Arbeit", "CHF"])
    except:
        return pd.DataFrame()

def save_all_data(df, sheet_name):
    # Diese Funktion überschreibt das ganze Sheet (fürs Löschen wichtig)
    payload = {"sheet": sheet_name, "method": "overwrite", "values": [df.columns.tolist()] + df.values.tolist()}
    requests.post(SCRIPT_URL, json=payload, timeout=10)

def append_data(row, sheet_name):
    # Schnelles Hinzufügen einer Zeile
    payload = {"sheet": sheet_name, "method": "append", "values": row}
    requests.post(SCRIPT_URL, json=payload, timeout=10)

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
auswahl_jahr = st.selectbox("📅 Saison", options=range(2025, 2036))
menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tanken</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    t_lit = col1.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = col2.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), t_lit, t_pr, round(t_lit * t_pr, 2), t_wer]
        append_data(new_row, "tanken")
        st.success("Gespeichert!")
        st.rerun()

    df_tanken = load_data("tanken")
    if not df_tanken.empty:
        st.table(df_tanken)
        if st.button("Letzten Eintrag löschen 🗑️"):
            df_tanken = df_tanken.drop(df_tanken.index[-1])
            save_all_data(df_tanken, "tanken")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Service speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), s_arbeit, s_preis]
        append_data(new_row, "service")
        st.rerun()
    
    df_service = load_data("service")
    if not df_service.empty:
        st.table(df_service)
        if st.button("Letzten Service löschen 🗑️"):
            df_service = df_service.drop(df_service.index[-1])
            save_all_data(df_service, "service")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Gesamtkosten</h3>", unsafe_allow_html=True)
    f_winter = st.number_input("❄️ Winterlager", value=2200.0)
    f_platz = st.number_input("⚓ Bootsplatz", value=1500.0)
    f_steuer = st.number_input("📜 Steuern", value=350.0)
    f_vers = st.number_input("🛡️ Versicherung", value=1150.0)
    
    df_t = load_data("tanken")
    df_s = load_data("service")
    
    sprit = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    fix = f_winter + f_platz + f_steuer + f_vers
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(fix + serv):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.info(f"⛽ Nur Benzin: CHF {sprit:,.2f} | 🔧 Nur Service: CHF {serv:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
