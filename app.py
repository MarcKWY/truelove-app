 streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- INSTA-LOG v22.1 ---
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

# Daten-Speicher (inkl. Like-Zähler)
if 'insta_tank' not in st.session_state: st.session_state.insta_tank = []
if 'insta_serv' not in st.session_state: st.session_state.insta_serv = []
if 'likes' not in st.session_state: st.session_state.likes = 0

# --- HEADER ---
st.markdown("<h1 style='text-align: center; letter-spacing: 5px;'>TRUELOVE</h1>", unsafe_allow_html=True)

# 1. HAUPTBILD & LIKE-BUTTON
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)
    
col_like1, col_like2 = st.columns([1, 3])
with col_like1:
    if st.button("❤️ Like"):
        st.session_state.likes += 1
with col_like2:
    st.markdown(f"<p class='like-text'>{st.session_state.likes} Mal Spass auf dem Wasser!</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 2. TANK-FEED
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("tanken.jpg"): 
    st.image("tanken.jpg", use_container_width=True)
    st.markdown(f"<div class='img-overlay'>⛽ {sum(i['Liter'] for i in st.session_state.insta_tank):.1f} L verbraucht</div>", unsafe_allow_html=True)

with st.expander("Tanken eintragen"):
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, key="new_lit")
    pr = c2.number_input("CHF/L", value=2.15)
    who = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    if st.button("Posten"):
        st.session_state.insta_tank.append({"Liter": lit, "CHF": round(lit*pr, 2), "Wer": who})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 3. STATISTIK
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
total_sprit = sum(i['CHF'] for i in st.session_state.insta_tank)
st.write("### 📊 Saison-Bilanz")
st.metric("Gesamtkosten inkl. Benzin", f"CHF {5200 + total_sprit:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Truelove Insta-Log v22.1")
