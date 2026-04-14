import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    label, .stRadio label, div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stRadio"] label { font-size: 45px !important; }
    input { color: #000000 !important; font-size: 18px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
    }

    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37 !important;
        text-align: center;
        margin-bottom: 0px;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        text-align: center;
        margin-top: -10px;
    }
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        margin-top: 10px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #D4AF37;
        line-height: 1.6;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=10.0)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    c1, c2 = st.columns(2)
    if c1.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({"Datum": datetime.now().strftime("%d.%m"), "Liter": t_lit, "Total": round(t_lit*t_pr, 2), "Wer": t_wer})
            st.rerun()
    if c2.button("Letzten Eintrag löschen 🗑️"):
        if st.session_state.tank_daten:
            st.session_state.tank_daten.pop()
            st.rerun()
    
    if st.session_state.tank_daten:
        st.table(pd.DataFrame(st.session_state.tank_daten))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Vollständige Motordaten")
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown("""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO (High Output)<br>
    <b>Leistung:</b> 425 HP (317 kW) @ 4400-4800 RPM<br>
    <b>Hubraum:</b> 8.1 Liter V8 Big Block<br>
    <b>Bohrung x Hub:</b> 108 mm x 111 mm<br>
    <b>Zündfolge:</b> 1-8-4-3-6-5-7-2<br>
    <b>Einspritzung:</b> Multi-Port EFI (PCM 555)<br>
    <b>Ölkapazität:</b> 8.5 Liter SAE 25W-40 Synthetic Blend<br>
    <b>Kühlung:</b> Zweikreiskühlung (Closed Cooling)</div>""", unsafe_allow_html=True)
    
    st.write("### 🔧 Service Log")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    c3, c4 = st.columns(2)
    if c3.button("Eintrag speichern"):
        if s_arbeit:
            st.session_state.service_historie.append({"Datum": datetime.now().strftime("%d.%m"), "Arbeit": s_arbeit, "CHF": s_preis})
            st.rerun()
    if c4.button("Letzten Service löschen 🗑️"):
        if st.session_state.service_historie:
            st.session_state.service_historie.pop()
            st.rerun()
    
    if st.session_state.service_historie:
        st.table(pd.DataFrame(st.session_state.service_historie))
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Fixkosten & Übersicht")
    
    # Eingabefelder für Fixkosten
    f_winter = st.number_input("❄️ Winterlager (CHF)", value=2200.0)
    f_platz = st.number_input("⚓ Bootsplatz (CHF)", value=1500.0)
    f_steuer = st.number_input("📜 Steuern (CHF)", value=350.0)
    f_vers = st.number_input("🛡️ Versicherung (CHF)", value=1150.0)
    
    # Berechnungen
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    serv_sum = sum(i['CHF'] for i in st.session_state.service_historie)
    fix_sum = f_winter + f_platz + f_steuer + f_vers
    
    total_ohne_sprit = fix_sum + serv_sum
    total_mit_sprit = total_ohne_sprit + sprit_sum
    
    st.write("---")
    st.markdown(f"### ⚙️ Kosten Service: **CHF {serv_sum:,.2f}**")
    st.write("---")
    
    col1, col2 = st.columns(2)
    col1.metric("TOTAL OHNE BENZIN", f"CHF {total_ohne_sprit:,.2f}")
    col2.metric("GESAMTKOSTEN INKL. BENZIN", f"CHF {total_mit_sprit:,.2f}")
    
    st.info(f"⛽ Davon reine Benzinkosten: CHF {sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
