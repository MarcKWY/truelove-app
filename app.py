import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: ORIGINAL PRO-APP DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhDxQNTjyCGLLR5hZwUo_7tQ5wEohouVXHrbn-FJzDKUPJ8c0MmbzfwfiOxUYDyRwE/exec"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important; font-weight: bold !important;
        color: #D4AF37 !important; text-align: center !important;
        letter-spacing: 5px !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px; text-align: center; margin-top: -5px; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px;
    }
    label, .stRadio label, p, span { color: #FFFFFF !important; font-size: 20px !important; font-weight: 500 !important; }
    div[data-testid="stRadio"] label { font-size: 45px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    .stButton>button {
        background-color: #8B6914 !important; color: white !important;
        border: 1px solid #D4AF37 !important; border-radius: 10px !important; font-size: 20px !important; width: 100%;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.3); margin-top: 20px;
    }
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1); padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; line-height: 1.6;
    }
    h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    /* TABELLEN DESIGN WIE AM ANFANG */
    [data-testid="stTable"] {
        background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; border-radius: 10px !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SPEED-FUNKTIONEN (CACHING) ---
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {}

def get_data(sheet):
    if sheet not in st.session_state.data_cache:
        try:
            r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10)
            data = r.json()
            df = pd.DataFrame(data[1:], columns=data[0]) if len(data) > 1 else pd.DataFrame(columns=data[0])
            st.session_state.data_cache[sheet] = df
        except:
            return pd.DataFrame()
    return st.session_state.data_cache[sheet]

def sync_save(row, sheet):
    payload = {"sheet": sheet, "method": "append", "values": row}
    requests.post(SCRIPT_URL, json=payload, timeout=10)
    if sheet in st.session_state.data_cache:
        del st.session_state.data_cache[sheet] # Cache löschen für Refresh

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN BEREICH ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tankstopp</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    col1, col2 = st.columns(2)
    lit = col1.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    pr = col2.number_input("CHF / L", value=2.15, format="%.2f")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        sync_save(new_row, "tanken")
        st.rerun()
    
    df_t = get_data("tanken")
    if not df_t.empty:
        st.table(df_t)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE BEREICH ---
elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'><h3>⚙️ Service & Motor</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    st.markdown(f"""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO<br>
    <b>Leistung:</b> 317 kW (425 HP) | <b>Hubraum:</b> 8.1 Liter V8<br>
    <b>Zündfolge:</b> 1-8-4-3-6-5-7-2 | <b>Öl:</b> 8.5 Liter SAE 25W-40</div>""", unsafe_allow_html=True)
    
    arbeit = st.text_input("Was wurde gemacht?")
    preis = st.number_input("Kosten CHF", min_value=0.0, step=0.1)
    
    if st.button("Service speichern"):
        sync_save([datetime.now().strftime("%d.%m.%Y"), arbeit, preis], "service")
        st.rerun()
    
    df_s = get_data("service")
    if not df_s.empty:
        st.table(df_s)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Kostenübersicht</h3>", unsafe_allow_html=True)
    f_winter = st.number_input("❄️ Winterlager", value=2200.0)
    f_platz = st.number_input("⚓ Bootsplatz", value=1500.0)
    f_steuer = st.number_input("📜 Steuern", value=350.0)
    f_vers = st.number_input("🛡️ Versicherung", value=1150.0)
    
    df_t = get_data("tanken")
    df_s = get_data("service")
    
    sprit = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    fix = f_winter + f_platz + f_steuer + f_vers
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(fix + serv):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
