mport streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* Clean UI: Keine Banner, kein Menü oben */
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 3px;
        font-weight: 200;
        margin-bottom: 20px;
    }

    /* Das Menü-Feld */
    .nav-overlay-photo {
        background-color: rgba(5, 15, 30, 0.9);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        
        /* Positionierung: Zieht das Menü HOCH in das Bild */
        position: relative;
        margin-top: -100px; 
        z-index: 999;
        
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }

    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    
    h2, h3, b { color: #D4AF37 !important; }
    
    /* Zentriert die Radio-Buttons im Menü */
    div[data-testid="stHorizontalBlock"] { justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# --- HAUPTBILD ---
# Wir nutzen use_container_width=True für die volle Breite
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# --- NAVIGATION (Wird durch CSS nach oben geschoben) ---
st.markdown("<div class='nav-overlay-photo'>", unsafe_allow_html=True)
menu = st.radio("BRIDGE CONTROL", 
                ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], 
                key="nav_radio",
                horizontal=True,
                label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- INHALT ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    # ... hier dein Code für Tanken ...
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Motor & Service")
    # ... hier dein Code für Motor ...
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    # ... hier dein Code für Finanzen ...
    st.markdown("</div>", unsafe_allow_html=True)
