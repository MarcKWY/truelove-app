import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: DESIGN ---
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
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 16px; text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px; }
    .card { background-color: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 20px; border: 1px solid #D4AF37; margin-top: 20px; }
    .spec-card { background-color: rgba(212, 175, 55, 0.1); padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; line-height: 1.6; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    h3, b { color: #D4AF37 !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN MIT CACHE (FÜR SPEED) ---
@st.cache_data(ttl=300) # Speichert Daten für 5 Minuten zwischen
def load_data(sheet_name):
    try:
        response = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}", timeout=10)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame(columns=data[0] if data else [])
    except:
        return pd.DataFrame()

def save_action(payload):
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        st.cache_data.clear() # Cache leeren, damit neue Daten geladen werden
        return True
    except:
        return False

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tanken</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    col1, col2 = st.columns(2)
    t_lit = col1.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = col2.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), t_lit, t_pr, round(t_lit * t_pr, 2), t_wer]
        if save_action({"sheet": "tanken", "method": "append", "values": new_row}):
            st.success("Gespeichert!")
            st.rerun()

    df_tanken = load_data("tanken")
    if not df_tanken.empty:
        st.table(df_tanken)
        if st.button("Letzten Eintrag löschen 🗑️"):
            new_df = df_tanken.drop(df_tanken.index[-1])
            if save_action({"sheet": "tanken", "method": "overwrite", "values": [new_df.columns.tolist()] + new_df.values.tolist()}):
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE ---
elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    st.markdown("""<div class='spec-card'><b>Specs:</b> Mercruiser 496 MAG HO<br>317 kW (425 HP) | 8.1L V8</div>""", unsafe_allow_html=True)
    
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Service speichern"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), s_arbeit, s_preis]
        if save_action({"sheet": "service", "method": "append", "values": new_row}):
            st.success("Erfolgreich!")
            st.rerun()
    
    df_service = load_data("service")
    if not df_service.empty:
        st.table(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Finanzen</h3>", unsafe_allow_html=True)
    df_t = load_data("tanken")
    df_s = load_data("service")
    
    sprit = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    
    f_winter = st.number_input("Winterlager", value=2200.0)
    f_platz = st.number_input("Bootsplatz", value=1500.0)
    f_fix = f_winter + f_platz + 350.0 + 1150.0
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(f_fix + serv):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(f_fix + serv + sprit):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
