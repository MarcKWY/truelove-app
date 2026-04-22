import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://google.com"

st.markdown("""
    <style>
    header[data-testid="stHeader"], [data-testid="stToolbar"], #GithubIcon { display: none !important; }
    .stApp { background-color: #050A14; color: #FFFFFF !important; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37 !important; text-align: center; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    .gold-price { color: #D4AF37 !important; font-weight: bold; }
    .stApp button { background-color: #D4AF37 !important; color: #050A14 !important; font-weight: bold !important; width: 100% !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK ---
@st.cache_data(ttl=300)
def load_all_data(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
        return r.json()
    except: return []

if 'tank_data' not in st.session_state:
    raw = load_all_data("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []
if 'serv_data' not in st.session_state:
    raw = load_all_data("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []

def fast_sync(payload, local_key, action="append"):
    if action == "append": st.session_state[local_key].append(payload["values"])
    try: requests.post(SCRIPT_URL, json=payload, timeout=5)
    except: pass
    st.cache_data.clear()

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)

# HIER SIND NUR NOCH 2 TABS – "Finanzen" ist physikalisch gelöscht
tab1, tab2 = st.tabs(["📊 Statistik", "📝 Logbuch Eintrag"])

with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_y = st.selectbox("Jahr", [2026, 2027, 2028], index=0)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    st.metric(f"Total {sel_y}", f"CHF {(sprit + serv):,.2f}")
    st.write(f"⛽ Benzin: CHF {sprit:,.2f}")
    st.write(f"⚙️ Service: CHF {serv:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    mode = st.radio("Eintragstyp", ["⛽ Tanken", "⚙️ Service"], horizontal=True)
    with st.form("entry_form"):
        d = st.date_input("Datum", date.today())
        if mode == "⛽ Tanken":
            lit = st.number_input("Liter", step=0.1)
            pr = st.number_input("CHF/L", value=2.15)
            wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            if st.form_submit_button("TANKEN SPEICHERN"):
                fast_sync({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]}, "tank_data")
                st.rerun()
        else:
            arb = st.text_input("Arbeiten")
            kost = st.number_input("Kosten", step=10.0)
            if st.form_submit_button("SERVICE SPEICHERN"):
                fast_sync({"sheet":"service","method":"append","values":[d.strftime("%d.%m.%Y"), arb, kost]}, "serv_data")
                st.rerun()
