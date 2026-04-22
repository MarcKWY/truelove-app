import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

# Ersetze diesen Link durch deinen tatsächlichen Google Script Deployment-Link
SCRIPT_URL = "https://google.com..." 

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 5px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 16px; text-align: center; color: #E0E0E0; opacity: 0.9; letter-spacing: 3px; margin-bottom: 20px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    h3 { color: #D4AF37 !important; }
    .white-text, .stMetric label, [data-testid="stMetricValue"], label, .stMarkdown p { color: #F8F8F8 !important; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CACHING LOGIK (Lädt Daten nur 1x alle 10 Min) ---
@st.cache_data(ttl=600)
def load_data(sheet_name):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}", timeout=10)
        return r.json()[1:]
    except:
        return []

# Daten in den Session State laden
if 'tank_data' not in st.session_state: st.session_state.tank_data = load_data("tanken")
if 'service_data' not in st.session_state: st.session_state.service_data = load_data("service")

# Fixkosten (persistiert für die Sitzung)
for key, val in {"fix_überwintern": 2200.0, "fix_steuern": 350.0, "fix_versicherung": 1150.0, "fix_bootsplatz": 1500.0}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["📋 Übersicht", "💰 Finanzen", "⛽ Tanken", "⚙️ Service"], horizontal=True, label_visibility="collapsed")

# Berechnungen
fix_total = st.session_state.fix_überwintern + st.session_state.fix_steuern + st.session_state.fix_versicherung + st.session_state.fix_bootsplatz
sprit_total = sum(float(r[3]) for r in st.session_state.tank_data if len(r) > 3) if st.session_state.tank_data else 0
service_total = sum(float(r[2]) for r in st.session_state.service_data if len(r) > 2) if st.session_state.service_data else 0

# --- ÜBERSICHT ---
if menu == "📋 Übersicht":
    st.markdown("<div class='card'><h3>📋 Gesamtübersicht 2026</h3>", unsafe_allow_html=True)
    grand_total = sprit_total + service_total + fix_total
    st.metric("GESAMTKOSTEN", f"CHF {grand_total:,.2f}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<span class='white-text'>⛽ Benzin:</span> **CHF {sprit_total:,.2f}**", unsafe_allow_html=True)
        st.markdown(f"<span class='white-text'>⚙️ Service:</span> **CHF {service_total:,.2f}**", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<span class='white-text'>🏗️ Fixkosten:</span> **CHF {fix_total:,.2f}**", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Jährliche Fixkosten</h3>", unsafe_allow_html=True)
    for l, v in zip(["❄️ Überwintern", "📑 Steuern", "🛡️ Versicherung", "⚓ Bootsplatz"], 
                     [st.session_state.fix_überwintern, st.session_state.fix_steuern, st.session_state.fix_versicherung, st.session_state.fix_bootsplatz]):
        c1, c2 = st.columns(2)
        c1.markdown(f"<span class='white-text'>{l}</span>", unsafe_allow_html=True)
        c2.markdown(f"<span class='white-text'>CHF {v:,.2f}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<span class='white-text'>**Total Fixkosten: CHF {fix_total:,.2f}**</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    with st.expander("🛠️ Fixkosten anpassen"):
        st.session_state.fix_überwintern = st.number_input("Überwintern", value=st.session_state.fix_überwintern)
        st.session_state.fix_steuern = st.number_input("Steuern", value=st.session_state.fix_steuern)
        st.session_state.fix_versicherung = st.number_input("Versicherung", value=st.session_state.fix_versicherung)
        st.session_state.fix_bootsplatz = st.number_input("Bootsplatz", value=st.session_state.fix_bootsplatz)
        if st.button("Speichern"): st.rerun()

# --- TANKEN ---
elif menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"):
        c1, c2, c3 = st.columns([1,2,1])
        c2.image("tanken.jpg", use_container_width=True)
    st.markdown("<div class='card'><h3>⛽ Tankstopp erfassen</h3>", unsafe_allow_html=True)
    datum_wahl = st.date_input("Datum wählen", value=date.today(), format="DD.MM.YYYY")
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01)
    pr = c2.number_input("CHF/L", value=2.15)
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    if st.button("Speichern ✅"):
        new_row = [datum_wahl.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        st.session_state.tank_data.append(new_row)
        st.cache_data.clear() # Cache leeren für frische Daten
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.tank_data:
        st.table(pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"]))

# --- SERVICE ---
elif menu == "⚙️ Service":
    if os.path.exists("motor.jpg"):
        c1, c2, c3 = st.columns([1,2,1])
        c2.image("motor.jpg", use_container_width=True)
    st.markdown("<div class='card'><h3>⚙️ Service-Log</h3>", unsafe_allow_html=True)
    datum_wahl_s = st.date_input("Datum wählen", value=date.today(), format="DD.MM.YYYY")
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0)
    if st.button("Eintrag speichern"):
        new_row = [datum_wahl_s.strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(new_row)
        st.cache_data.clear()
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":new_row}, timeout=2)
        except: pass
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.service_data:
        st.table(pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"]))
