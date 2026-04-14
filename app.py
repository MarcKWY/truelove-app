import streamlit as st
import os
import pandas as pd
from datetime import datetime
from PIL import Image

# --- SETUP: BRIDGE CONTROL FINAL ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* GRUNDFARBEN */
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    /* TITEL: GOLDIG UND GROSS */
    .truelove-title {
        font-family: 'Georgia', serif; 
        font-size: 80px !important; 
        font-weight: bold;
        color: #D4AF37 !important; 
        text-align: center; 
        margin-bottom: 0px;
        letter-spacing: 8px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif; 
        font-size: 22px; 
        text-align: center; 
        margin-top: -10px;
        color: #FFFFFF;
        letter-spacing: 4px;
    }

    /* NAVIGATION: GOLDENER RAHMEN BÜNDIG ZUM BILD */
    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85);
        padding: 20px 10px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        margin-top: 15px;
        display: flex;
        justify-content: space-around;
        width: 100%;
    }

    /* ICONS: GROSS UND WEISS */
    div[data-testid="stRadio"] label {
        color: #FFFFFF !important;
        font-size: 45px !important;
        font-weight: bold;
    }

    /* UPLOAD BALKEN: DUNKELBLAU MIT GOLDRAND */
    [data-testid="stFileUploadDropzone"] {
        background-color: #0A1E3C !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
    }
    [data-testid="stFileUploadDropzone"] * {
        color: #FFFFFF !important;
        font-size: 18px !important;
    }

    /* INPUTS & BUTTONS */
    input { color: #000000 !important; font-size: 18px !important; }
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        font-size: 20px !important;
    }

    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 25px;
    }
    
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #D4AF37;
    }
    
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    
    [data-testid="stTable"] {
        background-color: #0A1E3C !important;
        border: 1px solid #D4AF37 !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Speicher initialisieren
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []
if 'rechnungs_bilder' not in st.session_state: st.session_state.rechnungs_bilder = {}

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    t_pr = st.number_input("CHF / L", value=2.15, format="%.2f")
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        if t_lit > 0:
            st.session_state.tank_daten.append({
                "Datum": datetime.now().strftime("%d.%m.%Y"), "Liter": f"{t_lit:.2f}", 
                "CHF/L": f"{t_pr:.2f}", "Total CHF": f"{(t_lit*t_pr):.2f}", "Wer": t_wer
            })
            st.rerun()
    
    if st.session_state.tank_daten:
        df_tank = pd.DataFrame(st.session_state.tank_daten)
        st.table(df_tank)
        st.write("### 📊 Abrechnung")
        df_tank["Total CHF"] = df_tank["Total CHF"].astype(float)
        ausg = df_tank.groupby("Wer")["Total CHF"].sum()
        st.info(f"Marc: **CHF {ausg.get('Marc', 0.0):,.2f}** | Fabienne: **CHF {ausg.get('Fabienne', 0.0):,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Vollständige Motordaten")
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown("""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO (High Output)<br>
    <b>Leistung:</b> 431 PS (317 kW) @ 4400-4800 RPM<br>
    <b>Hubraum:</b> 8.1 Liter V8 Big Block<br>
    <b>Ölkapazität:</b> 8.5 Liter SAE 25W-40<br>
    <b>Kühlung:</b> Zweikreiskühlung (Closed Cooling)</div>""", unsafe_allow_html=True)
    
    st.write("### 🔧 Service Log & Rechnung")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=0.01, format="%.2f")
    s_foto = st.file_uploader("Rechnung hochladen", type=['png', 'jpg', 'jpeg'])
    
    if st.button("Eintrag speichern"):
        if s_arbeit:
            id_gen = datetime.now().strftime("%H%M%S")
            st.session_state.service_historie.append({
                "ID": id_gen, "Datum": datetime.now().strftime("%d.%m.%Y"), 
                "Arbeit": s_arbeit, "CHF": f"{s_preis:.2f}", "Rechnung": "✅" if s_foto else "❌"
            })
            if s_foto: st.session_state.rechnungs_bilder[id_gen] = Image.open(s_foto)
            st.rerun()
    
    if st.session_state.service_historie:
        st.table(pd.DataFrame(st.session_state.service_historie).drop(columns=["ID"]))
        for img in st.session_state.rechnungs_bilder.values():
            st.image(img, width=400)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Fixkosten & Übersicht")
    f_winter = st.number_input("❄️ Winterlager (CHF)", value=2200.0, format="%.2f")
    f_platz = st.number_input("⚓ Bootsplatz (CHF)", value=1500.0, format="%.2f")
    f_steuer = st.number_input("📜 Steuern (CHF)", value=350.0, format="%.2f")
    f_vers = st.number_input("🛡️ Versicherung (CHF)", value=1150.0, format="%.2f")
    
    sprit_sum = sum(float(i['Total CHF']) for i in st.session_state.tank_daten)
    serv_sum = sum(float(i['CHF']) for i in st.session_state.service_historie)
    fix_sum = f_winter + f_platz + f_steuer + f_vers
    
    st.metric("Total ohne Benzin", f"CHF {(fix_sum + serv_sum):,.2f}")
    st.metric("Total inkl. Benzin", f"CHF {(fix_sum + serv_sum + sprit_sum):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
