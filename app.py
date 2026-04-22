import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# DEINE FESTE SCRIPT URL
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec" 

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 3px; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #E0E0E0; opacity: 0.8; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    .gold-text { color: #D4AF37 !important; font-weight: bold; }
    
    /* Goldene Eingabe-Buttons */
    div.stButton > button:first-child {
        background-color: #D4AF37 !important;
        color: #050A14 !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 10px;
    }
    
    /* Kleinerer Lösch-Button */
    .stButton > button[key^="del"] {
        background-color: transparent !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
        padding: 2px 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ---
@st.cache_data(ttl=60) # Schnellerer Cache für bessere Performance
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=15)
        return r.json()
    except:
        return []

def send_request(payload):
    try:
        with st.spinner('Verarbeite...'):
            requests.post(SCRIPT_URL, json=payload, timeout=15)
            st.cache_data.clear()
            st.rerun()
    except:
        st.error("Verbindung zu Google fehlgeschlagen.")

# --- DATEN LADEN ---
raw_tank = fetch_data("tanken")
tank_list = raw_tank[1:] if len(raw_tank) > 1 else []

raw_serv = fetch_data("service")
serv_list = raw_serv[1:] if len(raw_serv) > 1 else []

raw_fix = fetch_data("fixkosten")
if len(raw_fix) > 1:
    f_ü, f_s, f_v, f_b = map(float, raw_fix[1][:4])
else:
    f_ü, f_s, f_v, f_b = 2200.0, 350.0, 1150.0, 1500.0

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# --- NAVIGATION ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr wählen", [2024, 2025, 2026, 2027], index=2)
    y_str = str(sel_year)
    
    sprit = sum(float(r[3]) for r in tank_list if len(r) > 3 and y_str in str(r[0]))
    serv = sum(float(r[2]) for r in serv_list if len(r) > 2 and y_str in str(r[0]))
    fix = f_ü + f_s + f_v + f_b
    
    # Wer hat wie viel bezahlt (Tanken)
    marc_t = sum(float(r[3]) for r in tank_list if len(r) > 4 and r[4] == "Marc" and y_str in str(r[0]))
    fabi_t = sum(float(r[3]) for r in tank_list if len(r) > 4 and r[4] == "Fabienne" and y_str in str(r[0]))

    st.metric(f"GESAMT {sel_year}", f"CHF {(sprit + serv + fix):,.2f}")
    
    col_m, col_f = st.columns(2)
    col_m.markdown(f"🧔 **Marc:**<br><span style='color:#D4AF37; font-size:18px;'>CHF {marc_t:,.2f}</span>", unsafe_allow_html=True)
    col_f.markdown(f"👩 **Fabienne:**<br><span style='color:#FF69B4; font-size:18px;'>CHF {fabi_t:,.2f}</span>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"⛽ Benzin: <span class='gold-text'>CHF {sprit:,.2f}</span><br>⚙️ Service: <span class='gold-text'>CHF {serv:,.2f}</span><br>🏗️ Fixkosten: <span class='gold-text'>CHF {fix:,.2f}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
with tab2:
    if os.path.exists("tanken.jpg"): 
        st.image("tanken.jpg", width=250)
    with st.form("tank_form"):
        d = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        lit = st.number_input("Liter", min_value=0.0, format="%.2f")
        pr = st.number_input("CHF/L", value=2.15, format="%.2f")
        wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
        if st.form_submit_button("Eintrag Speichern"):
            send_request({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]})
    
    st.markdown("### 📜 Historie")
    if tank_list:
        for i, r in enumerate(reversed(tank_list)):
            with st.container():
                c1, c2 = st.columns([0.85, 0.15])
                # Farbe basierend auf Zahler
                p_color = "#D4AF37" if r[4] == "Marc" else "#FF69B4"
                c1.markdown(f"📅 {r[0]} | {float(r[1]):.2f}L | **{float(r[3]):.2f} CHF** | <span style='color:{p_color}; font-weight:bold;'>{r[4]}</span>", unsafe_allow_html=True)
                if c2.button("🗑️", key=f"del_t_{i}"):
                    send_request({"sheet":"tanken","method":"delete","index": len(tank_list)-1-i})
                st.divider()
    else:
        st.info("Keine Tankdaten vorhanden.")

# --- 💰 FINANZEN ---
with tab3:
    st.markdown("<div class='card'><h3>💰 Fixkosten</h3>", unsafe_allow_html=True)
    n_ü = st.number_input("Überwintern", value=f_ü, format="%.2f")
    n_s = st.number_input("Steuern", value=f_s, format="%.2f")
    n_v = st.number_input("Versicherung", value=f_v, format="%.2f")
    n_b = st.number_input("Bootsplatz", value=f_b, format="%.2f")
    if st.button("Fixkosten aktualisieren"):
        send_request({"sheet":"fixkosten","method":"update","values":[n_ü, n_s, n_v, n_b]})
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⚙️ SERVICE ---
with tab4:
    if os.path.exists("motor.jpg"): 
        st.image("motor.jpg", width=250)
    with st.form("serv_form"):
        d_s = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        arb = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten CHF", min_value=0.0, format="%.2f")
        if st.form_submit_button("Service Speichern"):
            send_request({"sheet":"service","method":"append","values":[d_s.strftime("%d.%m.%Y"), arb, kost]})
    
    st.markdown("### 📜 Historie")
    if serv_list:
        for i, r in enumerate(reversed(serv_list)):
            with st.container():
                c1, c2 = st.columns([0.85, 0.15])
                c1.write(f"📅 {r[0]} | {r[1]} | **{float(r[2]):.2f} CHF**")
                if c2.button("🗑️", key=f"del_s_{i}"):
                    send_request({"sheet":"service","method":"delete","index": len(serv_list)-1-i})
                st.divider()
    else:
        st.info("Keine Servicedaten vorhanden.")
