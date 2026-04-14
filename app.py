import streamlit as st
import os
import pandas as pd
from datetime import datetime
from PIL import Image

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
    
    /* FARBANPASSUNG UPLOAD-FELD (Helleres Gold & Schwarze Schrift) */
    [data-testid="stFileUploadDropzone"] {
        background-color: #D4AF37 !important;
        border: 2px dashed #FFFFFF !important;
        border-radius: 15px !important;
    }
    /* Text innerhalb der Dropzone auf Schwarz setzen */
    [data-testid="stFileUploadDropzone"] div div span, 
    [data-testid="stFileUploadDropzone"] div div small {
        color: #000000 !important;
        font-weight: bold !important;
    }

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
    
    [data-testid="stTable"] {
        background-color: #0A1E3C !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: white !important;
        text-align: left !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []
if 'rechnungs_bilder' not in st.session_state: st.session_state.rechnungs_bilder = {}

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
    
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    t_pr = st.number_input("CHF / L", value=2.15, format="%.2f")
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    c1, c2 = st.columns(2)
    if c1.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({
                "Datum": datetime.now().strftime("%d.%m.%Y"), 
                "Liter": f"{t_lit:.2f}", 
                "CHF/L": f"{t_pr:.2f}",
                "Total CHF": f"{(t_lit*t_pr):.2f}", 
                "Wer": t_wer
            })
            st.rerun()
    if c2.button("Löschen 🗑️"):
        if st.session_state.tank_daten:
            st.session_state.tank_daten.pop()
            st.rerun()
    
    if st.session_state.tank_daten:
        df_tank = pd.DataFrame(st.session_state.tank_daten)
        st.table(df_tank)
        st.write("### 📊 Abrechnung Benzin")
        df_tank["Total CHF"] = df_tank["Total CHF"].astype(float)
        ausg = df_tank.groupby("Wer")["Total CHF"].sum()
        st.info(f"Marc hat bezahlt: **CHF {ausg.get('Marc', 0.00):,.2f}**")
        st.info(f"Fabienne hat bezahlt: **CHF {ausg.get('Fabienne', 0.00):,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Vollständige Motordaten")
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown("""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO (High Output)<br>
    <b>Leistung:</b> 431 PS (317 kW) @ 4400-4800 RPM<br>
    <b>Hubraum:</b> 8.1 Liter V8 Big Block<br>
    <b>Kühlung:</b> Zweikreiskühlung (Closed Cooling)</div>""", unsafe_allow_html=True)
    
    st.write("### 🔧 Service Log & Rechnung")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=0.01, format="%.2f")
    
    s_foto = st.file_uploader("Rechnung hochladen", type=['png', 'jpg', 'jpeg'])
    
    c3, c4 = st.columns(2)
    if c3.button("Eintrag speichern"):
        if s_arbeit:
            eintrag_id = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state.service_historie.append({
                "ID": eintrag_id,
                "Datum": datetime.now().strftime("%d.%m.%Y"), 
                "Arbeit": s_arbeit, 
                "CHF": f"{s_preis:.2f}",
                "Rechnung": "✅" if s_foto else "❌"
            })
            if s_foto:
                st.session_state.rechnungs_bilder[eintrag_id] = Image.open(s_foto)
            st.rerun()
    if c4.button("Löschen 🗑️"):
        if st.session_state.service_historie:
            st.session_state.service_historie.pop()
            st.rerun()
    
    if st.session_state.service_historie:
        df_service = pd.DataFrame(st.session_state.service_historie)
        st.table(df_service.drop(columns=["ID"])) # ID in Tabelle verstecken
        
        # Galerie der hochgeladenen Rechnungen
        if st.session_state.rechnungs_bilder:
            st.write("### 📸 Hochgeladene Rechnungen")
            for key in st.session_state.rechnungs_bilder:
                st.image(st.session_state.rechnungs_bilder[key], caption=f"Rechnung für Eintrag {key}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Fixkosten & Übersicht")
