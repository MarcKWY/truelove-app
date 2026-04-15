mport streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhDxQNTjyCGLLR5hZwUo_7tQ5wEohouVXHrbn-FJzDKUPJ8c0MmbzfwfiOxUYDyRwE/exec"

# CSS für Design
st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 40px; font-weight: bold; color: #D4AF37; text-align: center; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; }
    h3 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-LOGIK (LOKALER SPEICHER FÜR SPEED) ---
if 'tank_data' not in st.session_state:
    try:
        # Nur beim allerersten Laden einmal kurz warten
        r = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=5)
        st.session_state.tank_data = r.json()[1:]
    except:
        st.session_state.tank_data = []

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
menu = st.radio("MENU", ["⛽ Tanken", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tanken</h3>", unsafe_allow_html=True)
    lit = st.number_input("Liter", step=0.01, format="%.2f")
    pr = st.number_input("CHF/L", value=2.15, format="%.2f")
    wer = st.radio("Wer?", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        timestamp = datetime.now().strftime("%d.%m.%Y")
        total = round(lit * pr, 2)
        new_row = [timestamp, lit, pr, total, wer]
        
        # 1. SOFORT LOKAL ANZEIGEN (KEINE WARTEZEIT)
        st.session_state.tank_data.append(new_row)
        
        # 2. IM HINTERGRUND ZU GOOGLE (DU MERKST ES NICHT)
        try:
            requests.post(SCRIPT_URL, json={"sheet": "tanken", "method": "append", "values": new_row}, timeout=1)
        except:
            pass
        st.rerun()

    # Tabelle anzeigen
    if st.session_state.tank_data:
        df = pd.DataFrame(st.session_state.tank_data, columns=["Datum", "Liter", "CHF/L", "Total", "Wer"])
        # Formatierung auf 2 Stellen
        df["Liter"] = df["Liter"].map(lambda x: f"{float(x):.2f}")
        df["CHF/L"] = df["CHF/L"].map(lambda x: f"{float(x):.2f}")
        df["Total"] = df["Total"].map(lambda x: f"{float(x):.2f}")
        st.table(df)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Übersicht</h3>", unsafe_allow_html=True)
    if st.session_state.tank_data:
        total_sprit = sum(float(row[3]) for row in st.session_state.tank_data)
        st.metric("Total Benzin", f"CHF {total_sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
