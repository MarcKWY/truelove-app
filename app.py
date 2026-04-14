import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: MODERN & VOLLSTÄNDIG ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: #ffffff; }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    .spec-card { background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; color: white; border-left: 5px solid #D4AF37; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; letter-spacing: 2px; }
    b { color: #D4AF37; }
    .stMetric { background-color: rgba(255,255,255,0.05) !important; border-radius: 10px !important; padding: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_historie' not in st.session_state: st.session_state.service_historie = []

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>TRUELOVE</h1>", unsafe_allow_html=True)
if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True, caption="Crownline 286 SC")

st.write("---")

# --- NAVIGATION ---
menu = st.radio("Bereich wählen", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten & Finanzen"], horizontal=True)

if menu == "⛽ Tanken":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=400)
    
    with st.container():
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
        st.write("### Abrechnung Marc & Fabienne")
        ausg = df_t.groupby("Wer")["Total"].sum()
        st.write(f"Marc: **CHF {ausg.get('Marc',0):,.2f}** | Fabienne: **CHF {ausg.get('Fabienne',0):,.2f}**")
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
        
    st.write("### 📂 Rechnungs-Upload")
    up = st.file_uploader("Foto der Rechnung", type=['jpg', 'jpeg', 'png'])
    if up: st.image(up, caption="Hochgeladenes Dokument", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Kosten & Finanzen":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### Fixkosten & Saison-Total")
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

st.caption("Truelove Master Build v23.0")
