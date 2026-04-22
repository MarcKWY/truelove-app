import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# HIER DEINEN GOOGLE SCRIPT LINK EINTRAGEN
SCRIPT_URL = "https://google.com" 

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 38px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 3px; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #E0E0E0; opacity: 0.8; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    h3 { color: #D4AF37 !important; font-size: 20px; }
    .white-text, label, .stMarkdown p { color: #F8F8F8 !important; }
    
    /* GOLDENE ZAHLEN (METRICS) */
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-weight: bold !important; }
    .gold-text { color: #D4AF37 !important; font-weight: bold; }
    
    /* Navigation Buttons */
    .stButton>button { 
        background-color: #8B6914 !important; color: white !important; 
        border: 1px solid #D4AF37 !important; border-radius: 10px; height: 50px;
    }
    
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN INITIALISIEREN ---
if 'menu_select' not in st.session_state: st.session_state.menu_select = "📋 Übersicht"

@st.cache_data(ttl=30)
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=5)
        return r.json()
    except: return []

# Daten laden
raw_tank = fetch_data("tanken")
st.session_state.tank_data = raw_tank[1:] if len(raw_tank) > 0 else []

raw_serv = fetch_data("service")
st.session_state.service_data = raw_serv[1:] if len(raw_serv) > 0 else []

# Fixkosten (Initialisierung)
if 'f_ü' not in st.session_state:
    st.session_state.f_ü, st.session_state.f_s, st.session_state.f_v, st.session_state.f_b = 2200.0, 350.0, 1150.0, 1500.0

# --- HEADER (BILD GANZ OBEN) ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# --- NAVIGATION (UNTER DEM BILD) ---
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("📋 Übersicht", use_container_width=True): st.session_state.menu_select = "📋 Übersicht"
    if st.button("⛽ Tanken", use_container_width=True): st.session_state.menu_select = "⛽ Tanken"
with col_nav2:
    if st.button("💰 Finanzen", use_container_width=True): st.session_state.menu_select = "💰 Finanzen"
    if st.button("⚙️ Service", use_container_width=True): st.session_state.menu_select = "⚙️ Service"

st.divider()

# --- LOGIK ---
sel_menu = st.session_state.menu_select

def get_stats(year):
    y_str = str(year)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r) > 3 and y_str in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.service_data if len(r) > 2 and y_str in str(r[0]))
    fix = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    return sprit, serv, fix

# --- 📋 ÜBERSICHT ---
if sel_menu == "📋 Übersicht":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr wählen", [2024, 2025, 2026, 2027], index=2)
    sprit, serv, fix = get_stats(sel_year)
    
    st.metric(f"GESAMT {sel_year}", f"CHF {(sprit + serv + fix):,.2f}")
    
    st.markdown(f"""
    ⛽ Benzin: <span class='gold-text'>CHF {sprit:,.2f}</span><br>
    ⚙️ Service: <span class='gold-text'>CHF {serv:,.2f}</span><br>
    🏗️ Fixkosten: <span class='gold-text'>CHF {fix:,.2f}</span>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💰 FINANZEN ---
elif sel_menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Fixkosten anpassen</h3>", unsafe_allow_html=True)
    st.session_state.f_ü = st.number_input("Überwintern", value=st.session_state.f_ü, step=50.0)
    st.session_state.f_s = st.number_input("Steuern", value=st.session_state.f_s, step=10.0)
    st.session_state.f_v = st.number_input("Versicherung", value=st.session_state.f_v, step=10.0)
    st.session_state.f_b = st.number_input("Bootsplatz", value=st.session_state.f_b, step=50.0)
    
    fix_total = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    st.markdown(f"<h4>Total Fixkosten: <span class='gold-text'>CHF {fix_total:,.2f}</span></h4>", unsafe_allow_html=True)
    
    if st.button("Speichern"):
        try:
            requests.post(SCRIPT_URL, json={"sheet":"fixkosten","method":"update","values":[st.session_state.f_ü, st.session_state.f_s, st.session_state.f_v, st.session_state.f_b]}, timeout=3)
            st.success("Erfolgreich gespeichert!")
        except: st.error("Fehler beim Senden")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
elif sel_menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=250)
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    lit = st.number_input("Liter", min_value=0.0)
    pr = st.number_input("CHF/L", value=2.15)
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    if st.button("Eintragen"):
        row = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":row}, timeout=3)
        except: pass
        st.cache_data.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.tank_data:
        st.table(pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"]).iloc[::-1])

# --- ⚙️ SERVICE ---
elif sel_menu == "⚙️ Service":
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=250)
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0)
    if st.button("Eintragen"):
        row = [d.strftime("%d.%m.%Y"), arb, kost]
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":row}, timeout=3)
        except: pass
        st.cache_data.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.service_data:
        st.table(pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"]).iloc[::-1])
