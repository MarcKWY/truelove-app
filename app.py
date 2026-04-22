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
    .truelove-title { font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 5px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 16px; text-align: center; color: #E0E0E0; opacity: 0.9; letter-spacing: 3px; margin-bottom: 20px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px; }
    h3 { color: #D4AF37 !important; }
    .white-text, .stMetric label, [data-testid="stMetricValue"], label, .stMarkdown p { color: #F8F8F8 !important; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px; }
    .delete-btn>button { background-color: #441111 !important; border: 1px solid #ff4b4b !important; color: white !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN LADEN (Caching für Speed) ---
@st.cache_data(ttl=60)
def fetch_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=5)
        return r.json()[1:]
    except: return []

if 'tank_data' not in st.session_state: st.session_state.tank_data = fetch_data("tanken")
if 'service_data' not in st.session_state: st.session_state.service_data = fetch_data("service")

# Fixkosten
for k, v in {"f_ü": 2200.0, "f_s": 350.0, "f_v": 1150.0, "f_b": 1500.0}.items():
    if k not in st.session_state: st.session_state[k] = v

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["📋 Übersicht", "💰 Finanzen", "⛽ Tanken", "⚙️ Service"], horizontal=True, label_visibility="collapsed")

# --- LOGIK: FILTER NACH JAHR ---
def get_year_stats(selected_year):
    s_year = str(selected_year)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r) > 3 and s_year in r[0])
    serv = sum(float(r[2]) for r in st.session_state.service_data if len(r) > 2 and s_year in r[0])
    fix = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    return sprit, serv, fix

# --- ÜBERSICHT ---
if menu == "📋 Übersicht":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr wählen", [2025, 2026, 2027, 2028], index=1)
    sprit, serv, fix = get_year_stats(sel_year)
    total = sprit + serv + fix
    
    st.metric(f"GESAMTKOSTEN {sel_year}", f"CHF {total:,.2f}")
    c1, c2 = st.columns(2)
    c1.markdown(f"<span class='white-text'>⛽ Benzin:</span> **CHF {sprit:,.2f}**", unsafe_allow_html=True)
    c1.markdown(f"<span class='white-text'>⚙️ Service:</span> **CHF {serv:,.2f}**", unsafe_allow_html=True)
    c2.markdown(f"<span class='white-text'>🏗️ Fixkosten:</span> **CHF {fix:,.2f}**", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Fixkosten</h3>", unsafe_allow_html=True)
    fix_sum = st.session_state.f_ü + st.session_state.f_s + st.session_state.f_v + st.session_state.f_b
    for l, v in [("❄️ Überwintern", st.session_state.f_ü), ("📑 Steuern", st.session_state.f_s), ("🛡️ Versicherung", st.session_state.f_v), ("⚓ Bootsplatz", st.session_state.f_b)]:
        c1, c2 = st.columns(2)
        c1.markdown(f"<span class='white-text'>{l}</span>", unsafe_allow_html=True)
        c2.markdown(f"<span class='white-text'>CHF {v:,.2f}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"<span class='white-text'>**Total Fixkosten: CHF {fix_sum:,.2f}**</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    with st.expander("🛠️ Anpassen"):
        st.session_state.f_ü = st.number_input("Überwintern", value=st.session_state.f_ü)
        st.session_state.f_s = st.number_input("Steuern", value=st.session_state.f_s)
        st.session_state.f_v = st.number_input("Versicherung", value=st.session_state.f_v)
        st.session_state.f_b = st.number_input("Bootsplatz", value=st.session_state.f_b)
        if st.button("Speichern"): st.rerun()

# --- TANKEN ---
elif menu == "⛽ Tanken":
    if os.path.exists("tanken.jpg"):
        c1, c2, c3 = st.columns(3); c2.image("tanken.jpg", width=300)
    st.markdown("<div class='card'><h3>⛽ Tankstopp</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0)
    pr = c2.number_input("CHF/L", value=2.15)
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    if st.button("Speichern ✅"):
        row = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        st.session_state.tank_data.append(row)
        try: requests.post(SCRIPT_URL, json={"sheet":"tanken","method":"append","values":row}, timeout=2)
        except: pass
        st.cache_data.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.tank_data:
        st.table(pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"]))
        with st.expander("🗑️ Eintrag löschen"):
            for i, r in enumerate(st.session_state.tank_data):
                if st.button(f"Lösche {r[0]} - {r[1]}L", key=f"dt_{i}"):
                    st.session_state.tank_data.pop(i); st.cache_data.clear(); st.rerun()

# --- SERVICE ---
elif menu == "⚙️ Service":
    if os.path.exists("motor.jpg"):
        c1, c2, c3 = st.columns(3); c2.image("motor.jpg", width=300)
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    d = st.date_input("Datum", value=date.today(), format="DD.MM.YYYY")
    arb = st.text_input("Was wurde gemacht?")
    kost = st.number_input("Kosten CHF", min_value=0.0)
    if st.button("Speichern ✅"):
        row = [d.strftime("%d.%m.%Y"), arb, kost]
        st.session_state.service_data.append(row)
        try: requests.post(SCRIPT_URL, json={"sheet":"service","method":"append","values":row}, timeout=2)
        except: pass
        st.cache_data.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.service_data:
        st.table(pd.DataFrame(st.session_state.service_data, columns=["Datum", "Arbeit", "CHF"]))
        with st.expander("🗑️ Eintrag löschen"):
            for i, r in enumerate(st.session_state.service_data):
                if st.button(f"Lösche {r[0]} - {r[1]}", key=f"ds_{i}"):
                    st.session_state.service_data.pop(i); st.cache_data.clear(); st.rerun()
