import streamlit as st
import os
import pandas as pd
from datetime import datetime
import base64

# --- SETUP: OVERLAY BRIDGE DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# Hilfsfunktion um Bild als Base64 zu laden (für CSS Background)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("boot_gross.jpg")

st.markdown(f"""
    <style>
    /* UI CLEANUP */
    #MainMenu, header, footer {{visibility: hidden;}}
    [data-testid="stDecoration"] {{display: none;}}
    .stApp {{ background-color: #050A14; color: #FFFFFF; }}

    /* TITEL */
    .truelove-title {{
        font-family: 'Georgia', serif;
        font-size: clamp(30px, 8vw, 58px);
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }}
    
    .crownline-subtitle {{
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 18px;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 3px;
        font-weight: 200;
        margin-bottom: 20px;
    }}

    /* DER BILD-CONTAINER */
    .hero-container {{
        position: relative;
        width: 100%;
        height: 450px;
        border-radius: 25px;
        overflow: hidden;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}

    /* DIE STEUERUNG IM BILD */
    .nav-overlay-photo {{
        position: absolute;
        bottom: 30px; /* Abstand vom unteren Bildrand */
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(5, 15, 30, 0.8);
        padding: 10px 20px;
        border-radius: 20px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        z-index: 999;
        width: 80%;
        max-width: 500px;
    }}

    .card {{
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 30px;
    }}
    
    h2, h3, b {{ color: #D4AF37 !important; }}
    
    /* Radio Buttons zentrieren */
    div[data-testid="stHorizontalBlock"] {{ justify-content: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# --- HERO BEREICH (Bild mit Steuerung drin) ---
st.markdown(f"""
    <div class="hero-container">
        <div class="nav-overlay-photo" id="nav-anchor">
        </div>
    </div>
    """, unsafe_allow_html=True)

# Da Streamlit Radio-Buttons nicht direkt in HTML-Strings funktionieren, 
# "schieben" wir den Radio-Button mit einem Trick optisch nach oben.
with st.container():
    # Dieser CSS-Hack positioniert das Streamlit-Widget exakt über dem Platzhalter oben
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child(4) {
            margin-top: -85px; /* Schiebt das Radio-Widget ins Bild hoch */
            z-index: 1000;
        }
        </style>
    """, unsafe_allow_html=True)
    
    menu = st.radio("BRIDGE CONTROL", 
                    ["⛽ Tanken", "⚙️ Motor", "💰 Finanzen"], 
                    horizontal=True,
                    label_visibility="collapsed")

# --- CONTENT BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    # ... (Rest deines Tank-Codes)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Motor & Service")
    # ... (Rest deines Motor-Codes)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    # ... (Rest deines Finanz-Codes)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Bridge Overlay v24.1")
