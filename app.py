import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

# --- CSS ---
st.markdown("""
<style>
.stApp { background-color:#050A14; color:white; }
.truelove-title { font-size:34px; font-weight:bold; color:#D4AF37; text-align:center; }
.crownline-subtitle { text-align:center; margin-bottom:15px; opacity:0.9; }
.card { padding:15px; border:1px solid #D4AF37; border-radius:15px; margin-bottom:15px; }
.gold-price { color:#D4AF37; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data(ttl=300)
def load_all_data(sheet):
    try:
        return requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10).json()
    except:
        return []

# --- FIXKOSTEN (NUR LESEN!) ---
def load_fixkosten():
    data = load_all_data("fixkosten")
    try:
        row = data[1]  # Zeile 2 im Sheet
        return [
            float(row[0]),
            float(row[1]),
            float(row[2]),
            float(row[3])
        ]
    except:
        return [2200.0, 350.0, 1150.0, 1500.0]

# --- SESSION STATE ---
if "tank_data" not in st.session_state:
    raw = load_all_data("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []

if "serv_data" not in st.session_state:
    raw = load_all_data("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []

# 🔥 Fixkosten werden IMMER frisch geladen (kein Update mehr!)
st.session_state.fix_vals = load_fixkosten()

# --- SYNC ---
def fast_sync(payload):
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
    except:
        pass
    st.cache_data.clear()

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<div class='crownline-subtitle'>CROWNLINE 286 SC</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- ÜBERSICHT ---
with tab1:
    sel_y = st.selectbox("Jahr wählen", [2026, 2027, 2028, 2029])

    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    fix_sum = sum(st.session_state.fix_vals)

    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv + fix_sum):,.2f}")

# --- TANKEN ---
with tab2:
    with st.form("tank", clear_on_submit=True):
        d = st.date_input("Datum", date.today())
        lit = st.number_input("Liter")
        pr = st.number_input("CHF/L", value=2.15)
        wer = st.radio("Zahler", ["Marc", "Fabienne"])

        if st.form_submit_button("Speichern"):
            new = [d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr,2), wer]
            fast_sync({"sheet":"tanken","method":"append","values":new})
            st.rerun()

# --- FINANZEN (FIXKOSTEN NUR ANZEIGE!) ---
with tab3:
    v = st.session_state.fix_vals

    st.markdown("### Fixkosten (aus Google Sheets)")
    st.write(f"Überwintern: {v[0]}")
    st.write(f"Steuern: {v[1]}")
    st.write(f"Versicherung: {v[2]}")
    st.write(f"Bootsplatz: {v[3]}")

    st.markdown(f"**Total: CHF {sum(v):,.2f}**")

    st.info("👉 Fixkosten direkt in Google Sheets bearbeiten (Zeile 2)")

# --- SERVICE ---
with tab4:
    with st.form("service", clear_on_submit=True):
        d = st.date_input("Datum", date.today())
        arb = st.text_input("Arbeit")
        kost = st.number_input("Kosten")

        if st.form_submit_button("Speichern"):
            fast_sync({"sheet":"service","method":"append","values":[d.strftime("%d.%m.%Y"), arb, kost]})
            st.rerun()

    st.markdown("### Historie")
    for r in st.session_state.serv_data:
        st.write(r)
