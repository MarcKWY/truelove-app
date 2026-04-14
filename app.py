import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; }
    div[data-testid="stMetric"] { background-color: #F0F7FF !important; border: 1px solid #005A9C !important; border-radius: 10px; }
    .spec-card { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    
    /* Kosten-Boxen Styling */
    .total-box-blue { 
        background-color: #005A9C !important; 
        color: white !important; 
        padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;
    }
    .total-box-petrol { 
        background-color: #008080 !important; 
        color: white !important; 
        padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;
    }
    .total-box-blue h2, .total-box-blue h4, .total-box-petrol h2, .total-box-petrol h4 { color: white !important; margin: 0; }
    
    .zahler-box { background-color: #E1EFFE; padding: 10px; border-radius: 8px; border-left: 5px solid #005A9C; margin-bottom: 5px; color: #1A1C1E; }
    h1, h2, h3 { color: #005A9C !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialisierung der Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write(f"Crownline 286 SC | **V8 496 MAG HO (317 kW)**")

# --- REITER-STRUKTUR (Jetzt 3 Reiter) ---
tab1, tab2, tab3 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten"])

# TAB 1: TANKEN
with tab1:
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=550)
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now(), key="t_date_v199")
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0, key="t_lit_v199")
            t_preis = st.number_input("CHF / L", value=2.15, key="t_price_v199")
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="t_who_v199")
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Speichern ✅", use_container_width=True, key="btn_save_v199"):
                    if t_liter > 0:
                        st.session_state.tank_daten.append({"Datum": t_datum.strftime("%d.%m.%Y"), "Liter": t_liter, "Total": round(t_liter * t_preis, 2), "Zahler": t_wer})
                        st.rerun()
            with c_btn2:
                if st.button("Eintrag löschen 🗑️", use_container_width=True, key="btn_del_v199"):
                    if st.session_state.tank_daten: st.session_state.tank_daten.pop(); st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df_t = pd.DataFrame(st.session_state.tank_daten)
            st.metric("Benzin Saison (CHF)", f"{df_t['Total'].sum():,.2f}")
            ausg = df_t.groupby("Zahler")["Total"].sum()
            cm, cf = st.columns(2)
            with cm: st.markdown(f"<div class='zahler-box'><b>Marc:</b><br>CHF {ausg.get('Marc', 0.0):,.2f}</div>", unsafe_allow_html=True)
            with cf: st.markdown(f"<div class='zahler-box'><b>Fabienne:</b><br>CHF {ausg.get('Fabienne', 0.0):,.2f}</div>", unsafe_allow_html=True)
            st.table(df_t)

# TAB 2: MOTOR & SERVICE
with tab2:
    st.subheader("⚙️ Motor-Daten & Service-Historie")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="spec-card"><h3>Mercruiser 496 MAG HO</h3><ul><li><b>Leistung:</b> 317 kW / 431 PS</li><li><b>Hubraum:</b> 8.2 Liter</li><li><b>Kühlung:</b> Zweikreissystem</li><li><b>WOT:</b> 4600-5000 RPM</li><li><b>Ölkapazität:</b> 8.5 L</li><li><b>Zündfolge:</b> 1-8-4-3-6-5-7-2</li></ul></div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("### 🔧 Service eintragen")
            s_datum = st.date_input("Datum", datetime.now(), key="s_date_v199")
            s_arbeit = st.text_input("Was wurde gemacht?", key="s_work_v199")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_price_v199")
            cs1, cs2 = st.columns(2)
            with cs1:
                if st.button("Speichern ✅", use_container_width=True, key="btn_s_v199"):
                    st.session_state.service_kosten.append({"Datum": s_datum.strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_chf})
                    st.rerun()
            with cs2:
                if st.button("Löschen 🗑️", use_container_width=True, key="btn_s_del"):
                    if st.session_state.service_kosten: st.session_state.service_kosten.pop(); st.rerun()
        st.write("---")
        up = st.file_uploader("Rechnung hochladen", type=['jpg', 'jpeg', 'png'], key="f_up_v199")
        if up: st.image(up, caption="Service Dokument", use_container_width=True)
        if st.session_state.service_kosten:
            st.table(pd.DataFrame(st.session_state.service_kosten))

# TAB 3: KOSTEN
with tab3:
    st.subheader("💰 Gesamtkosten Truelove")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        k_versicherung = st.number_input("Versicherung 🛡️", value=1150.0, key="k_vers_v199")
        k_platz = st.number_input("Bootsplatz ⚓", value=1500.0, key="k_platz_v199")
        k_winter = st.number_input("Winterlager ❄️", value=2200.0, key="k_winter_v199")
        k_steuer = st.number_input("Steuern 📜", value=350.0, key="k_tax_v199")
        
    with col_k2:
        sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
        serv_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix_basis = k_versicherung + k_platz + k_winter + k_steuer
        
        st.markdown(f"""
            <div class='total-box-petrol'>
                <h4>TOTAL OHNE BENZIN</h4>
                <h2>CHF {fix_basis + serv_sum:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='total-box-blue'>
                <h4>TOTAL MIT BENZIN</h4>
                <h2>CHF {fix_basis + serv_sum + sprit_sum:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Fleet v19.9 | Final Master Build")
