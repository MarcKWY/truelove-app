import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: BRIDGE CONTROL FULL WIDTH ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* Hintergrund & Grundschrift */
    .stApp { background-color: #050A14; color: #FFFFFF; }
    * { color: #FFFFFF; }

    /* UI CLEANUP */
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    
    /* TITEL */
    .truelove-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 58px;
        font-weight: bold;
        text-align: center;
        letter-spacing: 8px;
        margin-bottom: 0px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 18px;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 4px;
        opacity: 0.8;
    }

    /* NAVIGATION: EXAKT SO BREIT WIE DAS BILD */
    div[data-testid="stRadio"] {
        width: 100% !important;
    }

    div[data-testid="stRadio"] > div {
        background-color: rgba(15, 25, 45, 0.7);
        padding: 25px 0px !important;
        border-radius: 15px !important;
        border: 2px solid #D4AF37 !important; /* Goldener Rahmen */
        backdrop-filter: blur(10px);
        margin-top: 20px !important;
        
        display: flex !important;
        justify-content: space-around !important;
        width: 100% !important; /* Volle Breite */
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
    }

    /* ENTFERNT DIE RADIO-PUNKTE (Kugeln) */
    div[data-testid="stRadio"] [data-testid="stWidgetLabel"] { display: none; }
    div[data-testid="stRadio"] input { display: none; }
    div[data-testid="stRadio"] .st-bd { display: none; } 
    div[data-testid="stRadio"] .st-af { display: none; }
    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 40px !important; /* MASSIVE ICONS */
        font-weight: bold !important;
        cursor: pointer;
    }
    
    /* Der Text unter/neben den Icons */
    div[data-testid="stRadio"] label {
        flex-direction: column !important;
        align-items: center !important;
        cursor: pointer;
    }

    /* CARD DESIGN FÜR INHALT */
    .card {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 30px;
    }
    
    .spec-card { 
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.1), transparent);
        padding: 20px; 
        border-radius: 12px; 
        border-left: 5px solid #D4AF37;
    }
    
    h2, h3, b { color: #D4AF37 !important; }
    
    /* Schwarze Schrift für Eingaben */
    input { color: #000000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# HAUPTBILD (Breite definiert den Standard)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# NAVIGATION (Jetzt exakt bündig zum Bild)
menu = st.radio("BRIDGE", 
                ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], 
                key="nav_full_width",
                horizontal=True,
                label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ⛽ Tank-Management")
    # Hier folgt deine Tank-Logik...
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Motor-Spezifikationen")
    st.markdown("""<div class='spec-card'>
    <b>Mercruiser 496 MAG HO</b><br>
    • 425 PS / 8.1L V8 Big Block<br>
    • Closed Cooling (Zweikreiskühlung)<br>
    • Zündfolge: 1-8-4-3-6-5-7-2
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💰 Boots-Finanzen")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Truelove Bridge System v24.7")
