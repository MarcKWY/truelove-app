import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

SCRIPT_URL = "https://google.com"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { 
        font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; 
        color: #D4AF37; text-align: center; letter-spacing: 5px; margin-bottom: 0px;
    }
    .crownline-subtitle { 
        font-family: 'Helvetica Neue', sans-serif; font-size: 16px; 
        text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px; margin-bottom: 20px;
    }
    .card { 
        background-color: rgba(255,255,255,0.05); padding: 20px; 
        border-radius: 15px; border: 1px solid #D4AF37; margin-top: 10px;
    }
    h3 { color: #D4AF37 !important; }
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px;
    }
    .delete-btn>button {
        background-color: #441111 !important; border: 1px solid #ff4b4b !important;
        font-size: 10px !important; padding: 0px !important; height: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN LADEN ---
if 'tank_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=5)
        st.session_state.tank_data = r.json()[1:]
    except:
        st.session_state.tank_data = []

if 'service_data' not in st.session_state:
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet=service", timeout=5)
        st.session_state.service_data = r.json()[1:]
    except:
        st.session_state.service_data = []

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN ---
if menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"):
        st.image("tanken.jpg", use_container_width=True)
    
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01)
    pr = c2.number_input("CHF/L", value=2.15)
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)

    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        st.session_state.tank_data.append(new_row)
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()

    st.markdown("<h4>Letzte Tankstopps</h4>", unsafe_allow_html=True)
    for i, row in enumerate(reversed(st.session_state.tank_data)):
        idx = len(st.session_state.tank_data) - 1 - i
        col_a, col_b = st.columns([4, 1])
        col_a.write(f"**{row[0]}**: {row[1]}L für {row[3]} CHF ({row[4]})")
        if col_b.button("🗑️", key=f"del_t_{idx}"):
            st.session_state.tank_data.pop(idx)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE ---
elif menu == "⚙️ Service":
    if os.path.exists("motor.jpg"):
        st.image("motor.jpg", use_container_width=True)

    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Eintrag speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(new_row)
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()

    for i, row in enumerate(reversed(st.session_state.service_data)):
        idx = len(st.session_state.service_data) - 1 - i
        col_a, col_b = st.columns([4, 1])
        col_a.write(f"**{row[0]}**: {row[1]} ({row[2]} CHF)")
        if col_b.button("🗑️", key=f"del_s_{idx}"):
            st.session_state.service_data.pop(idx)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data) if st.session_state.tank_data else 0
    serv = sum(float(r[2]) for r in st.session_state.service_data) if st.session_state.service_data else 0
    fix = 2200 + 1500 + 350 + 1150 
    
    st.metric("FIX + SERVICE", f"CHF {(fix + serv):,.2f}")
    st.metric("TOTAL INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.info(f"⛽ Benzinanteil: CHF {sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
