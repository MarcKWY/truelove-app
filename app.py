import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 55px !important;
        font-weight: bold !important;
        color: #D4AF37 !important;
        text-align: center !important;
        margin-bottom: 0px !important;
        letter-spacing: 5px !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
        display: block !important;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 18px;
        text-align: center;
        margin-top: -5px;
        color: #FFFFFF;
        opacity: 0.8;
    }
    label, .stRadio label, p, span {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stRadio"] label { font-size: 45px !important; }
    input { color: #000000 !important; font-size: 18px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
    }
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        margin-top: 10px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #D4AF37;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    [data-testid="stTable"] {
        background-color: #0A1E3C !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Speicher initialisieren
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# JAHRESFILTER
aktuelles_jahr = datetime.now().year
auswahl_jahr = st.selectbox("📅 Geschäftsjahr wählen", options=range(aktuelles_jahr, aktuelles_jahr-5, -1), index=0)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- FILTER LOGIK ---
def filter_nach_jahr(daten_liste, jahr):
    return [eintrag for eintrag in daten_liste if str(jahr) in eintrag.get("Datum", "")]

tank_jahr = filter_nach_jahr(st.session_state.tank_daten, auswahl_jahr)
service_jahr = filter_nach_jahr(st.session_state.service_historie, auswahl_jahr)

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tanken {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    t_pr = st.number_input("CHF / L", value=2.15, format="%.2f")
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({
                "Datum": datetime.now().strftime("%d.%m.%Y"), 
                "Liter": f"{t_lit:.2f}", "CHF/L": f"{t_pr:.2f}",
                "Total CHF": f"{(t_lit*t_pr):.2f}", "Wer": t_wer
            })
            st.rerun()
    
    if tank_jahr:
        st.table(pd.DataFrame(tank_jahr))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown(f"<div class='card'><h3>⚙️ Service {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown("""<div class='spec-card'><b>Mercruiser 496 MAG HO</b><br>431 PS (317 kW) | 8.1L V8</div>""", unsafe_allow_html=True)
    
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Eintrag speichern"):
        if s_arbeit:
            st.session_state.service_historie.append({
                "Datum": datetime.now().strftime("%d.%m.%Y"), 
                "Arbeit": s_arbeit, "CHF": f"{s_preis:.2f}"
            })
            st.rerun()
    
    if service_jahr:
        st.table(pd.DataFrame(service_jahr))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown(f"<div class='card'><h3>💰 Finanzen {auswahl_jahr}</h3>", unsafe_allow_html=True)
    f_winter = st.number_input("❄️ Winterlager (CHF)", value=2200.0, format="%.2f")
    f_platz = st.number_input("⚓ Bootsplatz (CHF)", value=1500.0, format="%.2f")
    f_steuer = st.number_input("📜 Steuern (CHF)", value=350.0, format="%.2f")
    f_vers = st.number_input("🛡️ Versicherung (CHF)", value=1150.0, format="%.2f")
    
    sprit_sum = sum(float(i['Total CHF']) for i in tank_jahr)
    serv_sum = sum(float(i['CHF']) for i in service_jahr)
    fix_sum = f_winter + f_platz + f_steuer + f_vers
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(fix_sum + serv_sum):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(fix_sum + serv_sum + sprit_sum):,.2f}")
    st.info(f"⛽ Benzin {auswahl_jahr}: CHF {sprit_sum:,.2f} | ⚙️ Service {auswahl_jahr}: CHF {serv_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Truelove Bridge v25.3 - Jahresübersicht {auswahl_jahr}")
