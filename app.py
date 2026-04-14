import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- INSTA-LOG v22.2 (STABLE) ---
st.set_page_config(page_title="Truelove Insta-Log", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: #ffffff; }
    .insta-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    .img-overlay {
        background: rgba(0, 50, 100, 0.8);
        color: #D4AF37;
        padding: 8px 15px;
        border-radius: 12px;
        font-weight: bold;
        position: relative;
        margin-top: -45px;
        margin-left: 10px;
        display: inline-block;
        border: 1px solid #D4AF37;
    }
    .like-text { color: #D4AF37; font-weight: bold; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher initialisieren
if 'insta_tank' not in st.session_state: st.session_state.insta_tank = []
if 'likes' not in st.session_state: st.session_state.likes = 0

# --- HEADER ---
st.markdown("<h1 style='text-align: center; letter-spacing: 5px;'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37;'>INSTA-LOG EDITION</p>", unsafe_allow_html=True)

# 1. HAUPTBILD (DEIN NEUES FOTO)
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)
else:
    st.warning("Bild 'boot_gross.jpg' nicht gefunden. Bitte auf GitHub hochladen!")

# Like-Bereich stabilisiert
col_l1, col_l2 = st.columns(2)
with col_l1:
    if st.button("❤️ Like", use_container_width=True):
        st.session_state.likes += 1
        st.rerun()
with col_l2:
    st.markdown(f"<p class='like-text'>{st.session_state.likes} Likes</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 2. TANK-FEED
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("tanken.jpg"): 
    st.image("tanken.jpg", use_container_width=True)
    liter_sum = sum(i['Liter'] for i in st.session_state.insta_tank)
    st.markdown(f"<div class='img-overlay'>⛽ {liter_sum:.1f} L Saison</div>", unsafe_allow_html=True)

with st.expander("Tanken eintragen"):
    lit = st.number_input("Liter", min_value=0.0, key="lit_input")
    pr = st.number_input("Preis pro Liter (CHF)", value=2.15, key="price_input")
    who = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="who_input")
    if st.button("Eintrag posten", use_container_width=True):
        if lit > 0:
            st.session_state.insta_tank.append({"Liter": lit, "CHF": round(lit*pr, 2), "Wer": who})
            st.rerun()

if st.session_state.insta_tank:
    last = st.session_state.insta_tank[-1]
    st.write(f"**Letzter Post:** {last['Wer']} hat {last['Liter']}L getankt.")
st.markdown("</div>", unsafe_allow_html=True)

# 3. SAISON-BILANZ
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
total_sprit = sum(i['CHF'] for i in st.session_state.insta_tank)
st.write("### 📊 Saison-Statistik")
st.metric("Gesamtkosten (Fix + Sprit)", f"CHF {5200 + total_sprit:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Truelove Insta-Log v22.2 | Stable Build")
