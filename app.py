import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; }
    div[data-testid="stMetric"] { background-color: #F0F7FF !important; border: 1px solid #005A9C !important; border-radius: 10px; }
    .spec-card { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .total-box { background-color: #005A9C; color: white; padding: 15px; border-radius: 10px; text-align: center; }
    h1, h2, h3 { color: #005A9C !important; }
    </style>
    """, unsafe_allow_html=True)

# Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'zubehoer' not in st.session_state: st.session_state.zubehoer = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg"]:
        if os.path.exists(f"logo.{ext}"): st.image(f"logo.{ext}", width=100)
with col_r:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write(f"Crownline 286 SC | **V8 496 MAG HO (317 kW)**")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "⚙️ Motor & Rechnungen", "🔧 Service & Zubehör", "💰 Kosten", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("CHF / L", value=2.15)
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Speichern ✅", use_container_width=True):
                    st.session_state.tank_daten.append({"Datum": t_datum.strftime("%d.%m.%Y"), "Liter": t_liter, "Total": round(t_liter * t_preis, 2), "Zahler": t_wer})
                    st.rerun()
            with c_btn2:
                if st.button("Letzten löschen 🗑️", use_container_width=True):
                    if st.session_state.tank_daten:
                        st.session_state.tank_daten.pop()
                        st.rerun()
    
    with col_res:
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            st.metric("Total Benzin", f"CHF {df['Total'].sum():,.2f}")
            st.table(df)

with tab2:
    st.subheader("⚙️ Motor-Daten & Rechnungs-Upload")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class="spec-card">
        <h3>Mercruiser 496 MAG HO</h3>
        <ul>
            <li><b>Leistung:</b> 317 kW / 431 PS</li>
            <li><b>Hubraum:</b> 8.2 Liter</li>
            <li><b>Kühlung:</b> Zweikreissystem</li>
            <li><b>Ölkapazität:</b> 8.5 Liter</li>
            <li><b>WOT:</b> 4600 - 5000 RPM</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
        
    with col_m2:
        st.write("### 📂 Service-Rechnungen")
        uploaded_file = st.file_uploader("Rechnung als Foto hochladen", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Hochgeladene Rechnung", use_container_width=True)
            st.success("Rechnung für diese Sitzung geladen!")

with tab3:
    st.subheader("🔧 Service-Einträge")
    s_datum = st.date_input("Service am", datetime.now())
    s_was = st.text_area("Arbeiten")
    if st.button("Service speichern"): st.success("Eintrag gespeichert!")

with tab4:
    st.subheader("💰 Kosten")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.image("https://wikimedia.org", width=50)
        k_axa = st.number_input("AXA Versicherung", value=1150.0)
        k_platz = st.number_input("Bootsplatz & Winter", value=3700.0)
        k_steuer = st.number_input("Steuern", value=350.0)
    with col_k2:
        sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
        total = k_axa + k_platz + k_steuer + sprit_sum
        st.metric("Fixkosten", f"CHF {k_axa + k_platz + k_steuer:,.2f}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN</h3><h1>CHF {total:,.2f}</h1></div>", unsafe_allow_html=True)

with tab5:
    st.header("📖 Logbuch")
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Ziel")

st.write("---")
st.caption("Truelove v17.0 | Marc & Fabienne Edition")
