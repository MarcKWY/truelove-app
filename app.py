import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: LUXURY YACHT DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp { 
        background: radial-gradient(circle at top, #0d1b2a 0%, #050a14 100%); 
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Titel-Styling */
    .truelove-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(40px, 8vw, 70px);
        font-weight: 100;
        color: #D4AF37;
        text-align: center;
        letter-spacing: 12px;
        margin-bottom: 0px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .crownline-subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.6);
        text-align: center;
        margin-top: -10px;
        letter-spacing: 6px;
        text-transform: uppercase;
    }

    /* Schwebendes Glas-Menü */
    .nav-overlay-photo {
        background: rgba(15, 23, 42, 0.7); 
        padding: 10px 20px;
        border-radius: 50px; /* Rundere Ecken für Modernität */
        border: 1px solid rgba(212, 175, 55, 0.4);
        backdrop-filter: blur(15px);
        position: relative;
        margin-top: -60px; /* Etwas weniger aggressiv */
        z-index: 999;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }

    /* Content Karten */
    .card {
        background: rgba(255, 255, 255, 0.03);
        padding: 30px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .spec-card { 
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(0,0,0,0) 100%); 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 4px solid #D4AF37;
    }
    
    /* Goldene Akzente für Tabellen & Eingaben */
    h2, h3, b { color: #f1d592 !important; font-weight: 300; }
    
    /* Streamlit UI Elemente anpassen */
    .stButton>button {
        border-radius: 30px !important;
        border: 1px solid #D4AF37 !important;
        background-color: transparent !important;
        color: #D4AF37 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #D4AF37 !important;
        color: #050a14 !important;
        box-shadow: 0 0 15px rgba(212,175,55,0.4);
    }

    /* Verstecke Radio-Label und style Buttons */
    div[data-testid="stRadio"] label { font-size: 12px; color: #D4AF37; }
    
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC • EXCLUSIVE EDITION</p>", unsafe_allow_html=True)

# HAUPTBILD 
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)
else:
    st.info("Füge 'boot_gross.jpg' hinzu, um das volle Design zu sehen.")

# NAVIGATION
st.markdown("<div class='nav-overlay-photo'>", unsafe_allow_html=True)
menu = st.radio("BRIDGE CONTROL", 
                ["⛽ Tanken", "⚙️ Motor", "💰 Finanzen"], 
                key="nav_photo_overlay",
                horizontal=True,
                label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Den Rest deines Codes (Logik) hier weiterführen...
# [Hier folgt dein bestehender Code für Tanken, Motor, Finanzen]
