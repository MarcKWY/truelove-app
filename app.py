import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

st.markdown("""
    <style>
    header[data-testid="stHeader"], [data-testid="stToolbar"], #GithubIcon { display:none !important; }
    .stApp { background-color: #050A14; color: #FFFFFF !important; }
    .truelove-title { font-size:34px; font-weight:bold; color:#D4AF37; text-align:center; }
    .crownline-subtitle { text-align:center; margin-bottom:15px; }
    .card { padding:15px; border-radius:15px; border:1px solid #D4AF37; margin-bottom:15px; }
    .gold-price { color:#D4AF37; font-weight:bold; }
    </style>
""", unsafe_allow_html=True)

# --- DATEN ---
@st.cache_data(ttl=300)
def load_all_data(sheet):
    try:
        return requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10).json()
    except:
        return []

if 'tank_data' not in st.session_state:
    raw = load_all_data("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []

if 'serv_data' not in st.session_state:
    raw = load_all_data("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []

# 🔥 FINALER FIX → IMMER ZEILE 2 LESEN
if 'fix_vals' not in st.session_state:
    raw = load_all_data("fixkosten")
    try:
        if len(raw) >= 2:
            row = raw[1]  # ← DAS IST DER KEY FIX
            st.session_state.fix_vals = [
                float(str(row[0]).replace(",", ".")),
                float(str(row[1]).replace(",", ".")),
                float(str(row[2]).replace(",", ".")),
                float(str(row[3]).replace(",", "."))
            ]
        else:
            st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]
    except:
        st.session_state.fix_vals = [2200.0, 350.0, 1150.0, 1500.0]

# --- SYNC ---
def fast_sync(payload, local_key, action="append", idx=None):
    if action == "append":
        st.session_state[local_key].append(payload["values"])
    elif action == "delete":
        st.session_state[local_key].pop(idx)
    elif action == "update":
        clean = [float(x) for x in payload["values"]]
        st.session_state.fix_vals = clean
        payload["values"] = clean

    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
    except:
        pass

    st.cache_data.clear()

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# Übersicht
with tab1:
    sel_y = st.selectbox("Jahr wählen", [2026, 2027, 2028, 2029], index=0)
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    fix_sum = sum(st.session_state.fix_vals)
    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv + fix_sum):,.2f}")

# Tanken
with tab2:
    with st.form("t_form", clear_on_submit=True):
        d = st.date_input("Datum", date.today(), format="DD.MM.YYYY")
        lit = st.number_input("Liter")
        pr = st.number_input("CHF/L", value=2.15)
        wer = st.radio("Zahler", ["Marc", "Fabienne"])
        if st.form_submit_button("Speichern"):
            new = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr,2), wer]
            fast_sync({"sheet":"tanken","method":"append","values":new}, "tank_data")
            st.rerun()

# Finanzen
with tab3:
    v = st.session_state.fix_vals
    n1 = st.number_input("Überwintern", value=v[0])
    n2 = st.number_input("Steuern", value=v[1])
    n3 = st.number_input("Versicherung", value=v[2])
    n4 = st.number_input("Bootsplatz", value=v[3])

    if st.button("Speichern"):
        fast_sync({"sheet":"fixkosten","method":"update","values":[n1,n2,n3,n4]}, "fix_vals", "update")

    st.write("Total:", sum([n1,n2,n3,n4]))

# Service
with tab4:
    with st.form("s_form", clear_on_submit=True):
        d = st.date_input("Datum", date.today())
        arb = st.text_input("Arbeit")
        kost = st.number_input("Kosten")
        if st.form_submit_button("Speichern"):
            fast_sync({"sheet":"service","method":"append","values":[d.strftime("%d.%m.%Y"), arb, kost]}, "serv_data")
            st.rerun()
