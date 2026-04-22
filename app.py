import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import os

st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

@st.cache_data(ttl=300)
def load_all_data(sheet):
    try:
        return requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10).json()
    except:
        return []

# --- FIX: IMMER FRISCH LADEN ---
def load_fixkosten():
    raw = load_all_data("fixkosten")
    try:
        if len(raw) >= 2:
            row = raw[1]
            return [
                float(row[0]),
                float(row[1]),
                float(row[2]),
                float(row[3])
            ]
    except:
        pass
    return [2200.0, 350.0, 1150.0, 1500.0]

# --- INIT ---
if 'tank_data' not in st.session_state:
    raw = load_all_data("tanken")
    st.session_state.tank_data = raw[1:] if len(raw) > 1 else []

if 'serv_data' not in st.session_state:
    raw = load_all_data("service")
    st.session_state.serv_data = raw[1:] if len(raw) > 1 else []

# 🔥 HIER IST DER WICHTIGE FIX
st.session_state.fix_vals = load_fixkosten()

# --- SYNC ---
def fast_sync(payload, local_key, action="append", idx=None):
    if action == "append":
        st.session_state[local_key].append(payload["values"])
    elif action == "delete":
        st.session_state[local_key].pop(idx)
    elif action == "update":
        payload["values"] = [float(x) for x in payload["values"]]
        st.session_state.fix_vals = payload["values"]

    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
    except:
        pass

    st.cache_data.clear()

# --- UI ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

with tab1:
    sel_y = st.selectbox("Jahr wählen", [2026, 2027, 2028, 2029])
    sprit = sum(float(r[3]) for r in st.session_state.tank_data if len(r)>3 and str(sel_y) in str(r[0]))
    serv = sum(float(r[2]) for r in st.session_state.serv_data if len(r)>2 and str(sel_y) in str(r[0]))
    fix_sum = sum(st.session_state.fix_vals)
    st.metric(f"GESAMT {sel_y}", f"CHF {(sprit + serv + fix_sum):,.2f}")

with tab3:
    v = st.session_state.fix_vals
    n1 = st.number_input("Überwintern", value=v[0])
    n2 = st.number_input("Steuern", value=v[1])
    n3 = st.number_input("Versicherung", value=v[2])
    n4 = st.number_input("Bootsplatz", value=v[3])

    if st.button("Speichern"):
        fast_sync({"sheet":"fixkosten","method":"update","values":[n1,n2,n3,n4]}, "fix_vals", "update")

    st.write("Total:", sum([n1,n2,n3,n4]))
