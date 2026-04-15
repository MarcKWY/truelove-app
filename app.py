import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# --- SETUP: PRO-APP DESIGN ---
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
    .spec-card { background-color: rgba(212, 175, 55, 0.1); padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; border-radius: 10px; }
    .delete-btn>button { background-color: #440000 !important; border: 1px solid #FF0000 !important; margin-top: 10px; }
    h3, b { color: #D4AF37 !important; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; }
    [data-testid="stTable"] td { color: white !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATUM-REINIGER ---
def clean_date(val):
    try:
        # Versucht das ISO Format (2026-04-14...) zu kürzen und umzuwandeln
        if isinstance(val, str) and 'T' in val:
            return datetime.strptime(val.split('T')[0], '%Y-%m-%d').strftime('%d.%m.%Y')
        return val
    except:
        return val

# --- LADE-FUNKTION ---
@st.cache_data(ttl=60)
def fetch_data(sheet_name):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet_name}", timeout=10)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data)
            # DATUM FIX: Spalte 'Datum' wird hier bereinigt
            if 'Datum' in df.columns:
                df['Datum'] = df['Datum'].apply(clean_date)
            return df
        return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"] if sheet_name=="tanken" else ["Datum", "Arbeit", "CHF"])
    except:
        return pd.DataFrame()

def send_action(payload):
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        st.cache_data.clear()
        return True
    except:
        return False

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- TANKEN ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tanken</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    pr = c2.number_input("CHF / L", value=2.15, format="%.2f")
    wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = [datetime.now().strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]
        if send_action({"sheet": "tanken", "method": "append", "values": new_row}):
            st.rerun()

    df_t = fetch_data("tanken")
    if not df_t.empty:
        st.table(df_t)
        st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
        if st.button("Letzten Eintrag löschen 🗑️"):
            new_df = df_t.drop(df_t.index[-1])
            if send_action({"sheet": "tanken", "method": "overwrite", "values": [new_df.columns.tolist()] + new_df.values.tolist()}):
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE ---
elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'><h3>⚙️ Service & Motor</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    st.markdown(f"""<div class='spec-card'><b>Specs:</b> Mercruiser 496 MAG HO<br>317 kW (425 HP) | 8.1L V8</div>""", unsafe_allow_html=True)
    
    arbeit = st.text_input("Was wurde gemacht?")
    preis = st.number_input("Kosten CHF", min_value=0.0, step=0.1)
    
    if st.button("Service speichern"):
        send_action({"sheet": "service", "method": "append", "values": [datetime.now().strftime("%d.%m.%Y"), arbeit, preis]})
        st.rerun()
    
    df_s = fetch_data("service")
    if not df_s.empty:
        st.table(df_s)
        st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
        if st.button("Letzten Service löschen 🗑️"):
            new_df_s = df_s.drop(df_s.index[-1])
            send_action({"sheet": "service", "method": "overwrite", "values": [new_df_s.columns.tolist()] + new_df_s.values.tolist()})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Finanzen</h3>", unsafe_allow_html=True)
    df_t = fetch_data("tanken")
    df_s = fetch_data("service")
    sprit = pd.to_numeric(df_t.iloc[:, 3], errors='coerce').sum() if not df_t.empty else 0
    serv = pd.to_numeric(df_s.iloc[:, 2], errors='coerce').sum() if not df_s.empty else 0
    fix = 2200 + 1500 + 350 + 1150
    
    col1, col2 = st.columns(2)
    col1.metric("OHNE BENZIN", f"CHF {(fix + serv):,.2f}")
    col2.metric("INKL. BENZIN", f"CHF {(fix + serv + sprit):,.2f}")
    st.info(f"⛽ Benzin Total: CHF {sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
