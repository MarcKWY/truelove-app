import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    /* ALLE BESCHRIFTUNGEN (Labels, Marc/Fabienne, etc.) WEISS UND GRÖSSER */
    label, .stRadio label, div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 500 !important;
    }

    /* SPEZIELL FÜR DIE MENÜ-ICONS (Extrem groß wie gewünscht) */
    div[data-testid="stRadio"] label {
        font-size: 45px !important;
    }

    /* EINGABEFELDER: Schrift im Feld bleibt schwarz für Lesbarkeit, Label darüber weiss */
    input { color: #000000 !important; font-size: 18px !important; }

    /* BILDER MIT GOLDRAND */
    img {
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
    }

    /* BUTTON DESIGN */
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
    }

    /* Titel-Styling */
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37 !important;
        text-align: center;
        margin-bottom: 0px;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        text-align: center;
        margin-top: -10px;
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

    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
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
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown("""<div style='background-color: rgba(212, 175, 55, 0.1); padding: 15px; border-left: 5px solid #D4AF37; border-radius: 10px;'>
    <b>Mercruiser 496 MAG HO</b><br>425 PS / 8.1L V8 Big Block<br>Zündfolge: 1-8-4-3-6-5-7-2</div>""", unsafe_allow_html=True)
    
    st.write("### 🔧 Service Log")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
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
    st.metric("Benzinkosten Total", f"CHF {sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
