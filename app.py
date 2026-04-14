import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: HELL & MAXIMALE LESBARKEIT ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; }
    div[data-testid="stMetric"] {
        background-color: #F0F7FF !important;
        border: 1px solid #005A9C !important;
        border-radius: 10px !important;
    }
    .spec-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        color: #1E293B;
    }
    .total-box {
        background-color: #005A9C;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }
    h1, h2, h3 { color: #005A9C !important; }
    b { color: #005A9C; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'zubehoer' not in st.session_state: st.session_state.zubehoer = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write(f"Crownline 286 SC | **Mercruiser 496 MAG HO (317 kW)**")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "⚙️ Motor-Daten", "🔧 Service & Zubehör", "💰 Kosten", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Management")
    # Bild ist jetzt kleiner
    if os.path.exists("tanken.jpg"):
        st.image("tanken.jpg", width=350, caption="Tanken")
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("CHF / L", value=2.15)
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            if st.button("Speichern"):
                st.session_state.tank_daten.append({"Datum": t_datum.strftime("%d.%m.%Y"), "Liter": t_liter, "Total": round(t_liter * t_preis, 2), "Zahler": t_wer})
                st.rerun()
    
    with col_res:
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            st.metric("Total Benzin", f"CHF {df['Total'].sum():,.2f}")
            st.write("**Abrechnung:**")
            ausgaben = df.groupby("Zahler")["Total"].sum()
            st.write(ausgaben)
            st.table(df)

with tab2:
    st.subheader("⚙️ Komplette Motor-Daten")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        st.markdown("""
        <div class="spec-card">
        <h3>Mercruiser 496 MAG HO</h3>
        <ul>
            <li><b>Leistung:</b> 317 kW / 431 PS</li>
            <li><b>Hubraum:</b> 8.2 Liter (496 cid)</li>
            <li><b>Zylinder:</b> V8 Big Block</li>
            <li><b>Kühlung:</b> Zweikreissystem (Closed Cooling)</li>
            <li><b>Drehzahl (WOT):</b> 4600 - 5000 RPM</li>
            <li><b>Einspritzung:</b> Multi-Point Injection (MPI)</li>
            <li><b>Zündfolge:</b> 1-8-4-3-6-5-7-2</li>
            <li><b>Ölkapazität:</b> ca. 8.5 Liter</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("🔧 Motor Service & Zubehör")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("### Motor Service Eintrag")
        s_datum = st.date_input("Service Datum", datetime.now())
        s_stunden = st.number_input("Betriebsstunden", value=450)
        s_was = st.text_area("Ausgeführte Arbeiten (z.B. Ölwechsel, Impeller)")
        if st.button("Service speichern"):
            st.success("Service-Eintrag erstellt!")
    with col_s2:
        if os.path.exists("wartung.jpg"): st.image("wartung.jpg", use_container_width=True)
        st.write("### Zubehör & Einkäufe")
        zub_name = st.text_input("Teil/Reparatur")
        zub_preis = st.number_input("Kosten (CHF)", min_value=0.0)
        if st.button("Zubehör erfassen"):
            st.session_state.zubehoer.append({"Teil": zub_name, "CHF": zub_preis})
            st.rerun()

with tab4:
    st.subheader("💰 Kosten-Übersicht")
    if os.path.exists("kosten.jpg"): st.image("kosten.jpg", width=400)
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.image("https://wikimedia.org", width=50)
        k_axa = st.number_input("AXA Versicherung", value=1150.0)
        k_platz = st.number_input("Bootsplatz / Winter", value=3700.0)
        k_steuer = st.number_input("Steuern", value=350.0)
    
    with col_k2:
        fix = k_axa + k_platz + k_steuer
        zub_sum = sum(i['CHF'] for i in st.session_state.zubehoer)
        sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
        
        st.metric("Fixkosten (Jahr)", f"CHF {fix:,.2f}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN SAISON</h3><h1>CHF {fix + zub_sum + sprit_sum:,.2f}</h1></div>", unsafe_allow_html=True)

with tab5:
    st.header("📖 Logbuch")
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Törn Ziel")
    st.button("Eintrag speichern")

st.write("---")
st.caption("Truelove v16.0 | Classic Bright Design")
