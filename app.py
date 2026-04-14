import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Business", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; color: #1E293B; }
    div[data-testid="stMetric"] { background-color: #FFFFFF !important; border: 2px solid #005A9C !important; border-radius: 12px !important; }
    .cost-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .total-box { background-color: #005A9C; color: white; padding: 20px; border-radius: 12px; text-align: center; }
    h1, h2, h3 { color: #005A9C !important; }
    b { color: #005A9C; }
    </style>
    """, unsafe_allow_html=True)

if 'tank_daten' not in st.session_state:
    st.session_state.tank_daten = []
if 'zubehoer_daten' not in st.session_state:
    st.session_state.zubehoer_daten = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE | Skipper Zentrale")
    st.write(f"**Crownline 286 SC** | Mercruiser 496 MAG HO | Saison {datetime.now().year}")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "🔧 Wartung & Zubehör", "⚙️ Motor-Specs", "💰 Kosten-Check", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Abrechnung")
    # Bild ist hier IMMER sichtbar
    if os.path.exists("tanken.jpg"):
        st.image("tanken.jpg", use_container_width=True)
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("CHF / L", value=2.15)
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            if st.button("Tanken speichern"):
                st.session_state.tank_daten.append({"Datum": t_datum.strftime("%d.%m.%Y"), "Liter": t_liter, "Total CHF": round(t_liter * t_preis, 2), "Zahler": t_wer})
                st.rerun()
    
    with col_res:
        if st.session_state.tank_daten:
            df_tank = pd.DataFrame(st.session_state.tank_daten)
            st.metric("Total Benzin Saison", f"CHF {df_tank['Total CHF'].sum():,.2f}")
            st.table(df_tank)

with tab2:
    st.subheader("🔧 Wartung & Zubehör")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if os.path.exists("wartung.jpg"):
            st.image("wartung.jpg", use_container_width=True)
        st.info("Hier Zubehör oder Reparaturen eintragen:")
        zub_name = st.text_input("Was wurde gekauft/repariert?")
        zub_preis = st.number_input("Kosten Zubehör (CHF)", min_value=0.0)
        if st.button("Zubehör speichern"):
            st.session_state.zubehoer_daten.append({"Teil": zub_name, "Kosten": zub_preis})
            st.rerun()
    with col_w2:
        if st.session_state.zubehoer_daten:
            df_zub = pd.DataFrame(st.session_state.zubehoer_daten)
            st.write("### Gekauftes Zubehör")
            st.table(df_zub)
            st.metric("Total Zubehör", f"CHF {df_zub['Kosten'].sum():,.2f}")

with tab3:
    st.subheader("⚙️ Motor-Specs")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        st.markdown("<div class='spec-card'><b>Typ:</b> Mercruiser 496 MAG HO<br><b>Leistung:</b> 317 kW / 431 PS<br><b>Hubraum:</b> 8.2L V8<br><b>Kühlung:</b> Zweikreis</div>", unsafe_allow_html=True)

with tab4:
    st.subheader("💰 Kosten-Management")
    if os.path.exists("kosten.jpg"):
        st.image("kosten.jpg", use_container_width=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("### Fixkosten")
        # AXA Logo Integration (Platzhalter)
        st.image("https://wikimedia.org", width=60)
        k_axa = st.number_input("AXA Versicherung (CHF/Jahr)", value=1150.0)
        k_lager = st.number_input("Winterlager (CHF/Jahr)", value=2200.0)
        k_platz = st.number_input("Bootsplatz (CHF/Jahr)", value=1500.0)
        k_steuer = st.number_input("Steuern (CHF/Jahr)", value=350.0)
        
        fix_total = k_axa + k_lager + k_platz + k_steuer
        zubehör_summe = sum(item['Kosten'] for item in st.session_state.zubehoer_daten)
        sprit_summe = sum(item['Total CHF'] for item in st.session_state.tank_daten)
        
    with col_f2:
        st.markdown("### Zusammenfassung")
        st.metric("Fixkosten (ohne Benzin)", f"CHF {fix_total:,.2f}")
        st.metric("Zubehör & Reparaturen", f"CHF {zubehör_summe:,.2f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='total-box'><h2>GESAMTKOSTEN SAISON</h2><h1>CHF {fix_total + zubehör_summe + sprit_summe:,.2f}</h1><p>(Inkl. Benzin & Zubehör)</p></div>", unsafe_allow_html=True)

with tab5:
    st.header("Logbuch")
    st.text_input("Ziel")
    st.button("Törn speichern")

st.write("---")
st.caption("Truelove Fleet v15.0 | Premium Finance Edition")
