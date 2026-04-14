import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: OVERLAY BRIDGE DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* GLOBALE FARBEN & SCHRIFTEN */
    .stApp { background-color: #050A14; color: #FFFFFF; }
    * { color: #FFFFFF; } 

    /* SCHWARZE SCHRIFT IN EINGABEFELDERN & TABELLEN */
    input, [data-testid="stTable"] td, [data-testid="stTable"] th, .stNumberInput div div input { 
        color: #000000 !important; 
    }
    
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    /* Titel-Styling */
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

    /* MENÜ-BALKEN: EXAKT SO BREIT WIE DAS BILD */
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85) !important;
        padding: 20px 0px !important;
        border-radius: 15px !important;
        border: 2px solid #D4AF37 !important;
        backdrop-filter: blur(10px);
        margin-top: 10px !important;
        display: flex;
        justify-content: space-around;
        
        /* Breite auf 100% des Containers (wie das Bild) */
        width: 100% !important;
        box-sizing: border-box;
    }
    
    /* Entfernt zusätzliche Abstände von Streamlit um das Radio-Widget */
    div[data-testid="stRadio"] { 
        width: 100% !important; 
        border: none !important; 
    }

    /* DOMINANTE ICONS & WEISSE SCHRIFT */
    div[data-testid="stRadio"] label {
        font-weight: bold !important;
        font-size: 35px !important; 
        color: #FFFFFF !important;
        cursor: pointer;
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
    
    h2, h3, .spec-card b { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# HAUPTBILD (Breite ist container_width)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# NAVIGATION (Balken ist jetzt 100% breit)
menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], 
                key="nav_radio_fixed_width", horizontal=True, label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=250)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_lit")
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
    <b>Modell:</b> Mercruiser 496 MAG HO (High Output)<br>
    <b>Leistung:</b> 425 HP (317 kW) @ 4400-4800 RPM<br>
    <b>Typ:</b> V8 Big Block<br>
    <b>Hubraum:</b> 8.1 Liter (496 cu in)<br>
    <b>Bohrung x Hub:</b> 108 mm x 111 mm<br>
    <b>Zündfolge:</b> 1-8-4-3-6-5-7-2<br>
    <b>Ölkapazität:</b> ca. 8.5 Liter<br>
    <b>Kühlsystem:</b> Zweikreiskühlung (Closed Cooling)
    </div>""", unsafe_allow_html=True)
    
    st.write("### 🔧 Service Log & Rechner")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, key="s_preis")
    if st.button("Eintrag speichern"):
        st.session_state.service_historie.append({"Arbeit": s_arbeit, "CHF": s_preis})
        st.rerun()
    
    if st.session_state.service_historie:
        st.table(pd.DataFrame(st.session_state.service_historie))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    serv_sum = sum(i['CHF'] for i in st.session_state.service_historie)
    st.metric("Benzinkosten", f"CHF {sprit_sum:,.2f}")
    st.metric("Servicekosten", f"CHF {serv_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Truelove Bridge v24.6 - Full Width UI")
