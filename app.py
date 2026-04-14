import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# CSS für das Design und das "Hochschieben" des Menüs
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 3px;
    }

    /* Das Menü, das ins Bild geschoben wird */
    .nav-overlay-photo {
        background-color: rgba(5, 15, 30, 0.9);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        position: relative;
        margin-top: -100px; /* Schiebt das Menü ins Bild */
        z-index: 999;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
    }

    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    
    h2, h3, b { color: #D4AF37 !important; }
    div[data-testid="stHorizontalBlock"] { justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher initialisieren (WICHTIG gegen Fehlermeldungen)
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# --- BILD ---
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)
else:
    st.warning("Bild 'boot_gross.jpg' nicht gefunden. Bitte im Ordner ablegen.")

# --- NAVIGATION ---
st.markdown("<div class='nav-overlay-photo'>", unsafe_allow_html=True)
menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Motor", "💰 Finanzen"], 
                horizontal=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIK DER BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    
    t_lit = st.number_input("Liter", min_value=0.0, step=1.0)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({
                "Datum": datetime.now().strftime("%d.%m"), 
                "Liter": t_lit, 
                "Total": round(t_lit*t_pr, 2), 
                "Wer": t_wer
            })
            st.rerun()

    if st.session_state.tank_daten:
        st.table(pd.DataFrame(st.session_state.tank_daten))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Motor & Service")
    st.info("Hier können Service-Einträge erfasst werden.")
    # Platzhalter für deine Service-Logik
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    # Einfache Berechnung
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    st.metric("Benzinkosten Total", f"CHF {sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
