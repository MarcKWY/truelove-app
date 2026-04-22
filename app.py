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
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 34px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 3px; margin-bottom: 0px; }
    .crownline-subtitle { font-family: 'Helvetica Neue', sans-serif; font-size: 14px; text-align: center; color: #E0E0E0; opacity: 0.8; letter-spacing: 2px; margin-bottom: 15px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 15px; }
    
    /* Goldener Speicher-Button */
    div.stButton > button:first-child {
        background-color: #D4AF37 !important;
        color: #050A14 !important;
        font-weight: bold !important;
        border-radius: 10px;
        border: none;
        width: 100%;
        height: 3em;
    }
    /* Lösch-Button (kleiner und rot) */
    .stButton > button[key^="del"] {
        background-color: #440000 !important;
        color: white !important;
        border: 1px solid #ff4b4b !important;
        font-size: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SPEED-FUNKTIONEN ---
@st.cache_data(ttl=600)
def get_all_data():
    """Lädt alle Blätter auf einmal für mehr Speed"""
    try:
        tanken = requests.get(f"{SCRIPT_URL}?sheet=tanken", timeout=15).json()
        service = requests.get(f"{SCRIPT_URL}?sheet=service", timeout=15).json()
        fix = requests.get(f"{SCRIPT_URL}?sheet=fixkosten", timeout=15).json()
        return tanken, service, fix
    except:
        return [], [], []

def send_request(payload):
    with st.spinner('Synchronisiere mit Google...'):
        try:
            requests.post(SCRIPT_URL, json=payload, timeout=15)
            st.cache_data.clear()
            st.success("Erfolgreich gespeichert!")
            st.rerun()
        except:
            st.error("Fehler bei der Übertragung.")

# --- DATEN LADEN ---
t_raw, s_raw, f_raw = get_all_data()

tank_list = t_raw[1:] if len(t_raw) > 1 else []
serv_list = s_raw[1:] if len(s_raw) > 1 else []

if len(f_raw) > 1:
    f_ü, f_s, f_v, f_b = map(float, f_raw[:4])
else:
    f_ü, f_s, f_v, f_b = 2200.0, 350.0, 1150.0, 1500.0

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", use_container_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Übersicht", "⛽ Tanken", "💰 Finanzen", "⚙️ Service"])

# --- 📋 ÜBERSICHT ---
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    sel_year = st.selectbox("Jahr", [2024, 2025, 2026])
    y_str = str(sel_year)
    
    sprit = sum(float(r[3]) for r in tank_list if len(r) > 3 and y_str in str(r[0]))
    serv = sum(float(r[2]) for r in serv_list if len(r) > 2 and y_str in str(r[0]))
    
    # Wer hat wie viel bezahlt (Tanken)
    marc_total = sum(float(r[3]) for r in tank_list if len(r) > 4 and r[4] == "Marc" and y_str in str(r[0]))
    fabi_total = sum(float(r[3]) for r in tank_list if len(r) > 4 and r[4] == "Fabienne" and y_str in str(r[0]))

    st.metric(f"GESAMT {sel_year}", f"CHF {(sprit + serv + f_ü + f_s + f_v + f_b):,.2f}")
    
    col_a, col_b = st.columns(2)
    col_a.write(f"🧔 **Marc:** CHF {marc_total:,.2f}")
    col_b.write(f"👩 **Fabienne:** CHF {fabi_total:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⛽ TANKEN ---
with tab2:
    with st.form("tank_form"):
        st.markdown("### ⛽ Neuer Tankstopp")
        d = st.date_input("Datum", date.today())
        c1, c2 = st.columns(2)
        lit = c1.number_input("Liter", step=0.1, format="%.2f")
        pr = c2.number_input("CHF/L", value=2.15, format="%.2f")
        wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
        if st.form_submit_button("JETZT SPEICHERN"):
            send_request({"sheet":"tanken","method":"append","values":[d.strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer]})

    st.markdown("### 📜 Historie")
    if tank_list:
        # DataFrame für bessere Übersicht
        df_tank = pd.DataFrame(tank_list, columns=["Datum", "Liter", "Preis", "Total", "Wer"])
        for i, row in df_tank.iloc[::-1].iterrows():
            with st.container():
                col1, col2, col3 = st.columns([0.25, 0.55, 0.2])
                col1.write(f"**{row['Datum']}**")
                color = "#D4AF37" if row['Wer'] == "Marc" else "#FF69B4"
                col2.markdown(f"{row['Liter']}L | **{row['Total']:.2f} CHF** | <span style='color:{color}'>{row['Wer']}</span>", unsafe_allow_html=True)
                if col3.button("🗑️", key=f"del_t_{i}"):
                    send_request({"sheet":"tanken","method":"delete","index": i})
                st.divider()

# --- 💰 FINANZEN ---
with tab3:
    st.markdown("<div class='card'><h3>💰 Fixkosten</h3>", unsafe_allow_html=True)
    n_ü = st.number_input("Überwintern", value=f_ü, format="%.2f")
    n_s = st.number_input("Steuern", value=f_s, format="%.2f")
    n_v = st.number_input("Versicherung", value=f_v, format="%.2f")
    n_b = st.number_input("Bootsplatz", value=f_b, format="%.2f")
    if st.button("FIXKOSTEN AKTUALISIEREN"):
        send_request({"sheet":"fixkosten","method":"update","values":[n_ü, n_s, n_v, n_b]})
    st.markdown("</div>", unsafe_allow_html=True)

# --- ⚙️ SERVICE ---
with tab4:
    with st.form("serv_form"):
        st.markdown("### ⚙️ Service-Eintrag")
        d_s = st.date_input("Datum", date.today())
        arb = st.text_input("Was wurde gemacht?")
        kost = st.number_input("Kosten CHF", step=10.0, format="%.2f")
        if st.form_submit_button("SERVICE SPEICHERN"):
            send_request({"sheet":"service","method":"append","values":[d_s.strftime("%d.%m.%Y"), arb, kost]})
    
    st.markdown("### 📜 Historie")
    if serv_list:
        for i, r in enumerate(reversed(serv_list)):
            c1, c2, c3 = st.columns([0.25, 0.55, 0.2])
            c1.write(f"**{r[0]}**")
            c2.write(f"{r[1]} | **{float(r[2]):.2f} CHF**")
            if c3.button("🗑️", key=f"del_s_{i}"):
                send_request({"sheet":"service","method":"delete","index": len(serv_list)-1-i})
            st.divider()
