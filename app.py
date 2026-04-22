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
    .truelove-title { font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 5px; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 16px; text-align: center; color: #E0E0E0; opacity: 0.9; letter-spacing: 3px; margin-bottom: 20px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    h3 { color: #D4AF37 !important; }
    .white-text, .stMetric label, [data-testid="stMetricValue"], label, .stMarkdown p { color: #F8F8F8 !important; }
    
    /* Tabs Design */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(212, 175, 55, 0.1); 
        border-radius: 5px 5px 0px 0px; 
        color: #D4AF37 !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: rgba(212, 175, 55, 0.3) !important; border-bottom: 2px solid #D4AF37 !important; }

    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN INITIALISIEREN ---
@st.cache_data(ttl=60)
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=5)
        return r.json()[1:]
    except: return []

if 'tank_data' not in st.session_state: st.session_state.tank_data = fetch_data("tanken")
if 'service_data' not in st.session_state: st.session_state.service_data = fetch_data("service")

# Fixkosten-Initialisierung (falls noch nicht vorhanden)
if 'f_ü' not in st.session_state: st.session_state.f_ü = 2200.0
if 'f_s' not in st.session_state: st.session_state.f_s = 350.0
if 'f_v' not in st.session_state: st.session_state.f_v = 1150.0
if 'f_b' not in st.session_state: st.session_state.f_b = 1500.0

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# --- MENÜ-ORDNUNG (TABS) ---
tab_ü, tab_f, tab_t, tab_s = st.tabs(["📋 Übersicht", "💰 Finanzen", "⛽ Tanken", "⚙️ Service"])

# Summen-Logik
def get_stats(year):
    y_str = str(year)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r) > 3 and y_str in r[0])
    serv = sum(float(r[2]) for r in st.session_state.service_data if len(r) > 2 and y_str in r[0])
    fix = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    return sprit, serv, fix

# --- 📋 ÜBERSICHT ---
with tab_ü:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr wählen", [2025, 2026, 2027, 2028], index=1)
    sprit, serv, fix = get_stats(sel_year)
    total = sprit + serv + fix
    
    st.metric(f"GESAMTKOSTEN {sel_year}", f"CHF {total:,.2f}")
    c1, c2 = st.columns(2)
    c1.markdown(f"<span class='white-text'>⛽ Benzin:</span> **CHF {sprit:,.2f}**", unsafe_allow_html=True)
    c1.markdown(f"<span class='white-text'>⚙️ Service:</span> **CHF {serv:,.2f}**", unsafe_allow_html=True)
    c2.markdown(f"<span class='white-text'>🏗️ Fixkosten:</span> **CHF {fix:,.2f}**", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💰 FINANZEN ---
with tab_f:
    st.markdown("<div class='card'><h3>💰 Jährliche Fixkosten</h3>", unsafe_allow_html=True)
    
    # Bearbeitbare Felder
    st.session_state.f_ü = st.number_input("❄️ Überwintern (CHF)", value=st.session_state.f_ü, step=50.0)
    st.session_state.f_s = st.number_input("📑 Steuern (CHF)", value=st.session_state.f_s, step=10.0)
    st.session_state.f_v = st.number_input("🛡️ Versicherung (CHF)", value=st.session_state.f_v, step=10.0)
    st.session_state.f_b = st.number_input("⚓ Bootsplatz (CHF)", value=st.session_state.f_b, step=50.0)
    
    fix_sum = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    st.divider()
    st.markdown(f"<h4>Total Fixkosten: CHF {fix_sum:,.2f}</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
with tab_t:
    if os.path.exists("tanken.jpg"):
        c1, c2, c3 = st.columns([1,2,1]); c2.image("tanken.jpg", use_container_width=True)
    
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY", key="tank_date")
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, key="tank_lit")
    pr = c2.number_input("CHF/L", value=2.15, key="tank_pr")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="tank_wer")
    
    if st.button("Speichern ✅", key="save_tank"):
        row = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        st.session_state.tank_data.append(row)
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.tank_data:
        st.table(pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"]))
        with st.expander("🗑️ Eintrag löschen"):
            for i, r in enumerate(st.session_state.tank_data):
                if st.button(f"Lösche {r[0]} - {r[1]}L", key=f"del_t_{i}"):
                    st.session_state.tank_data.pop(i); st.rerun()

# --- ⚙️ SERVICE ---
with tab_s:
    if os.path.exists("motor.jpg"):
        c1, c2, c3 = st.columns([1,2,1]); c2.image("motor.jpg", use_container_width=True)
    
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY", key="serv_date")
    arb = st.text_input("Was wurde gemacht?", key="serv_arb")
    kost = st.number_input("Kosten CHF", min_value=0.0, key="serv_kost")
    
    if st.button("Speichern ✅", key="save_serv"):
        row = [d.strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(row)
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.service_data:
        st.table(pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"]))
        with st.expander("🗑️ Eintrag löschen"):
            for i, r in enumerate(st.session_state.service_data):
                if st.button(f"Lösche {r[0]} - {r[1]}", key=f"del_s_{i}"):
                    st.session_state.service_data.pop(i); st.rerun()
