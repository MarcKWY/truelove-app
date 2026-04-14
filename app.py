import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- INSTA-LOG UI SETUP ---
st.set_page_config(page_title="Truelove Insta-Log", layout="centered")

st.markdown("""
    <style>
    /* Dunkler, edler Hintergrund für den Feed-Look */
    .stApp { background-color: #050a14; color: #ffffff; }
    
    /* Die Insta-Karten */
    .insta-card {
        position: relative;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    
    /* Overlay für Zahlen direkt auf dem Bild */
    .img-overlay {
        background: rgba(0, 31, 63, 0.7);
        color: #D4AF37;
        padding: 10px 20px;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin-top: -50px;
        position: relative;
        border: 1px solid #D4AF37;
    }

    h1, h2 { font-family: 'Helvetica Neue', sans-serif; font-weight: 200; letter-spacing: 3px; }
    .stButton>button { background-color: transparent; border: 1px solid #D4AF37; color: #D4AF37; border-radius: 30px; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'insta_tank' not in st.session_state: st.session_state.insta_tank = []
if 'insta_serv' not in st.session_state: st.session_state.insta_serv = []

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37;'>CROWNLINE 286 SC | V8 496 MAG HO</p>", unsafe_allow_html=True)

# --- DER FEED ---

# 1. TANKEN (Insta-Style)
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("tanken.jpg"): 
    st.image("tanken.jpg", use_container_width=True)
    st.markdown(f"<div class='img-overlay'>⛽ {sum(i['Liter'] for i in st.session_state.insta_tank):.1f} L</div>", unsafe_allow_html=True)

st.write("### ⛽ Tank-Update")
with st.expander("Tanken erfassen"):
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, key="i_lit")
    pr = c2.number_input("CHF/L", value=2.15, key="i_pri")
    who = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="i_who")
    if st.button("Log posten"):
        st.session_state.insta_tank.append({"Liter": lit, "CHF": round(lit*pr, 2), "Wer": who})
        st.rerun()

if st.session_state.insta_tank:
    st.write(f"Zuletzt getankt: {st.session_state.insta_tank[-1]['Wer']} ({st.session_state.insta_tank[-1]['Liter']}L)")
st.markdown("</div>", unsafe_allow_html=True)

# 2. MOTOR (Insta-Style)
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("motor.jpg"): 
    st.image("motor.jpg", use_container_width=True)
    st.markdown("<div class='img-overlay'>⚙️ 317 KW POWER</div>", unsafe_allow_html=True)

st.write("### 🔧 Technik-Check")
st.markdown("""
- **V8 496 MAG HO** | 8.2L Big Block
- Zweikreiskühlung (Closed System)
- WOT: 4600-5000 RPM
""")
with st.expander("Service-Kosten eintragen"):
    s_c = st.number_input("CHF", min_value=0.0, key="i_serv_c")
    if st.button("Service speichern"):
        st.session_state.insta_serv.append(s_c)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 3. KOSTEN (Insta-Style)
st.markdown("<div class='insta-card'>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)
    
total_fix = 5200 # Versicherung, Platz, Winterlager, Steuer
total_sprit = sum(i['CHF'] for i in st.session_state.insta_tank)
total_serv = sum(st.session_state.insta_serv)

st.write("### 💰 Saison-Investment")
c1, c2 = st.columns(2)
c1.metric("Basis + Service", f"CHF {total_fix + total_serv:,.2f}")
c2.metric("Total mit Sprit", f"CHF {total_fix + total_serv + total_sprit:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove v22.0 | Insta-Log Edition")
