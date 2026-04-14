import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: OVERLAY BRIDGE DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    /* ENTFERNT DAS BANNER / HEADER / MENU / FOOTER */
    #MainMenu {visibility: hidden;} 
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;} /* Die farbige Linie oben */
    
    .stApp { background-color: #050A14; color: #FFFFFF; }
    
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 20px;
        color: #FFFFFF;
        text-align: center;
        margin-top: -10px;
        letter-spacing: 3px;
        font-weight: 200;
    }

    .nav-overlay-photo {
        background-color: rgba(5, 15, 30, 0.85); 
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        backdrop-filter: blur(10px);
        position: relative;
        margin-top: -110px; 
        z-index: 999;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }

    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 40px;
    }
    
    .spec-card { 
        background-color: rgba(212, 175, 55, 0.1); 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #D4AF37;
    }
    
    h2, h3, b { color: #D4AF37 !important; }
    .stMetric { background-color: rgba(255,255,255,0.05) !important; border-radius: 12px !important; border: 1px solid #D4AF37 !important; }
    
    div[data-testid="stHorizontalBlock"] { justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# HAUPTBILD
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

# NAVIGATION
st.markdown("<div class='nav-overlay-photo'>", unsafe_allow_html=True)
menu = st.radio("BRIDGE CONTROL", 
                ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], 
                key="nav_photo_overlay",
                horizontal=True,
                label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

st.write("##")

# --- BEREICHE (LOGIK) ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=400)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_lit")
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    c1, c2 = st.columns(2)
    if c1.button("Speichern ✅", use_container_width=True):
        if t_lit > 0:
            st.session_state.tank_daten.append({"Datum": datetime.now().strftime("%d.%m"), "Liter": t_lit, "Total": round(t_lit*t_pr, 2), "Wer": t_wer})
            st.rerun()
    if c2.button("Letzten löschen 🗑️", use_container_width=True):
        if st.session_state.tank_daten: st.session_state.tank_daten.pop(); st.rerun()

    if st.session_state.tank_daten:
        df_t = pd.DataFrame(st.session_state.tank_daten)
        ausg = df_t.groupby("Wer")["Total"].sum()
        st.info(f"Marc: **CHF {ausg.get('Marc',0):,.2f}** | Fabienne: **CHF {ausg.get('Fabienne',0):,.2f}**")
        st.table(df_t)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Motor & Service")
    st.markdown("""<div class='spec-card'><h3>Mercruiser 496 MAG HO</h3>
    • <b>Leistung:</b> 317 kW / 431 PS HO<br>• <b>Hubraum:</b> 8.2L V8 Big Block<br>
    • <b>Zündfolge:</b> 1-8-4-3-6-5-7-2</div>""", unsafe_allow_html=True)
    
    if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    
    st.write("### 🔧 Service Log")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    if st.button("Eintrag speichern"):
        st.session_state.service_historie.append({"Arbeit": s_arbeit, "CHF": s_preis})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💰 Finanzen")
    k_v = st.number_input("Versicherung (CHF)", value=1150.0)
    k_p = st.number_input("Bootsplatz (CHF)", value=1500.0)
    k_w = st.number_input("Winterlager (CHF)", value=2200.0)
    k_s = st.number_input("Steuern (CHF)", value=350.0)
    
    fix_sum = k_v + k_p + k_w + k_s
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    serv_sum = sum(i['CHF'] for i in st.session_state.service_historie)
    
    st.write("---")
    st.metric("Total Kosten OHNE Benzin", f"CHF {fix_sum + serv_sum:,.2f}")
    st.metric("GESAMTKOSTEN INKL. BENZIN", f"CHF {fix_sum + serv_sum + sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Bridge Overlay v23.6 - Clean UI")
