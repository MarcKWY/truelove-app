import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: OVERLAY BRIDGE DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* GLOBALE REGEL: Jede Schrift in Weiss */
    * { color: #FFFFFF !important; }
    
    .stApp { background-color: #050A14; }
    
    /* Titel in Gold (Ausnahme für den Namen) */
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37 !important;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 3px;
        font-weight: 200;
    }

    /* Das Menüband: Breite 100%, Schrift Weiss, Icons dominant */
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85);
        padding: 20px 10px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        margin-top: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        display: flex;
        justify-content: space-around;
        width: 100%;
    }

    /* Entfernt das zweite Band / Trennlinien unter dem Menü */
    hr { display: none; }
    div[data-testid="stHorizontalBlock"] { border: none !important; }

    div[data-testid="stRadio"] label {
        font-weight: bold !important;
        font-size: 32px !important;
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
        line-height: 1.6;
    }
    
    /* Gold-Akzente für Überschriften beibehalten */
    h2, h3, .spec-card b { color: #D4AF37 !important; }
    
    .stMetric { background-color: rgba(255,255,255,0.05) !important; border-radius: 12px !important; border: 1px solid #D4AF37 !important; }
    
    /* Versteckt das Streamlit-Header-Menü oben */
    #MainMenu, header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# HAUPTBILD
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# NAVIGATION (Nur noch ein Band vorhanden)
menu = st.radio("BRIDGE CONTROL", 
                ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], 
                key="nav_radio_clean",
                horizontal=True,
                label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=250)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=10.0)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({"Datum": datetime.now().strftime("%d.%m"), "Liter": t_lit, "Total": round(t_lit*t_pr, 2), "Wer": t_wer})
            st.rerun()
    
    if st.session_state.tank_daten:
        st.table(pd.DataFrame(st.session_state.tank_daten))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Vollständige Motordaten")
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=250)
    st.markdown("""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO<br>
    <b>Leistung:</b> 425 HP (317 kW)<br>
    <b>Hubraum:</b> 8.1 Liter V8<br>
    <b>Zündfolge:</b> 1-8-4-3-6-5-7-2
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    st.metric("Benzinkosten Total", f"CHF {sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Truelove Bridge v24.3 - White Font Edition")
