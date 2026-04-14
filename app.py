import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: LUXURY LIGHT DESIGN ---
st.set_page_config(page_title="Truelove Dashboard", layout="centered")

st.markdown("""
    <style>
    /* Heller, edler Hintergrund für maximale Lesbarkeit */
    .stApp { background-color: #F8FAFC; color: #0F172A; }
    
    /* Edle Serifenschrift für Truelove */
    .truelove-title {
        font-family: 'Georgia', serif;
        font-size: 65px;
        font-weight: bold;
        color: #002D5A;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: 4px;
    }
    
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 24px;
        color: #D4AF37;
        text-align: center;
        margin-top: -10px;
        font-weight: 300;
        letter-spacing: 2px;
    }

    /* Grössere Navigations-Schrift */
    div[data-testid="stWidgetLabel"] p {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #002D5A !important;
    }

    /* Karten-Design mit Kontrast */
    .card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }
    
    .spec-card { 
        background-color: #F1F5F9; 
        padding: 20px; 
        border-radius: 12px; 
        color: #0F172A; 
        border-left: 6px solid #D4AF37; 
        font-size: 1.1em;
    }
    
    b { color: #002D5A; }
    h2, h3 { color: #002D5A !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 class='truelove-title'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

# Erstes Bild etwas grösser (Nutzt volle Breite des Containers)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

st.write("##")

# --- NAVIGATION (GRÖSSER) ---
menu = st.radio("BEREICH WÄHLEN", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten & Finanzen"], horizontal=True)

st.write("---")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=450)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_lit")
    t_pr = st.number_input("CHF / L", value=2.15, key="t_pr")
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
        st.write("### Abrechnung")
        ausg = df_t.groupby("Wer")["Total"].sum()
        st.info(f"Marc: **CHF {ausg.get('Marc',0):,.2f}** | Fabienne: **CHF {ausg.get('Fabienne',0):,.2f}**")
        st.table(df_t)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""<div class='spec-card'><h3>Mercruiser 496 MAG HO</h3>
    • <b>Leistung:</b> 317 kW / 431 PS HO<br>• <b>Hubraum:</b> 8.2L V8 Big Block<br>
    • <b>Kühlung:</b> Zweikreissystem<br>• <b>WOT:</b> 4600 - 5000 RPM<br>
    • <b>Ölkapazität:</b> 8.5 Liter<br>• <b>Zündfolge:</b> 1-8-4-3-6-5-7-2</div>""", unsafe_allow_html=True)
    
    if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    
    st.write("### 🔧 Service & Reparatur")
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    if st.button("Eintrag speichern"):
        st.session_state.service_historie.append({"Arbeit": s_arbeit, "CHF": s_preis})
        st.rerun()
        
    st.write("### 📂 Dokumente")
    up = st.file_uploader("Rechnung hochladen", type=['jpg', 'jpeg', 'png'])
    if up: st.image(up, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Kosten & Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### Fixkosten")
    c1, c2 = st.columns(2)
    k_v = c1.number_input("Versicherung (CHF)", value=1150.0)
    k_p = c2.number_input("Bootsplatz (CHF)", value=1500.0)
    k_w = c1.number_input("Winterlager (CHF)", value=2200.0)
    k_s = c2.number_input("Steuern (CHF)", value=350.0)
    
    fix_sum = k_v + k_p + k_w + k_s
    sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
    serv_sum = sum(i['CHF'] for i in st.session_state.service_historie)
    
    st.write("---")
    st.metric("Total Kosten OHNE Benzin", f"CHF {fix_sum + serv_sum:,.2f}")
    st.metric("GESAMTKOSTEN INKL. BENZIN", f"CHF {fix_sum + serv_sum + sprit_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Truelove Management v23.1 | {datetime.now().year}")
