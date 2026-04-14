import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- STABILER SETUP (HELL & KLAR) ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; }
    div[data-testid="stMetric"] { background-color: #F0F7FF !important; border: 1px solid #005A9C !important; border-radius: 10px; }
    .spec-card { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .total-box { background-color: #005A9C; color: white !important; padding: 15px; border-radius: 10px; text-align: center; }
    .total-box h1, .total-box h3 { color: white !important; margin: 0; }
    .zahler-box { background-color: #E1EFFE; padding: 10px; border-radius: 8px; border-left: 5px solid #005A9C; margin-bottom: 5px; color: #1A1C1E; }
    h1, h2, h3 { color: #005A9C !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher initialisieren
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
col_l, col_r = st.columns()
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write(f"Crownline 286 SC | **V8 496 MAG HO (317 kW)**")

# --- REITER ---
tab1, tab2, tab3, tab4 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten", "📖 Logbuch"])

# TAB 1: TANKEN
with tab1:
    if os.path.exists("tanken.jpg"): 
        st.image("tanken.jpg", width=450)
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now(), key="t_date_s")
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0, key="t_lit_s")
            t_preis = st.number_input("CHF / L", value=2.15, key="t_price_s")
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="t_who_s")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Speichern ✅", use_container_width=True, key="s_t_s"):
                    if t_liter > 0:
                        st.session_state.tank_daten.append({"Datum": t_datum.strftime("%d.%m.%Y"), "Liter": t_liter, "Total": round(t_liter * t_preis, 2), "Zahler": t_wer})
                        st.rerun()
            with c_btn2:
                if st.button("Letzten löschen 🗑️", use_container_width=True, key="d_t_s"):
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
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="spec-card"><h3>Mercruiser 496 MAG HO</h3><ul><li><b>Leistung:</b> 317 kW / 431 PS</li><li><b>Hubraum:</b> 8.2 Liter</li><li><b>Kühlung:</b> Zweikreissystem</li><li><b>Drehzahl (WOT):</b> 4600-5000 RPM</li><li><b>Zündfolge:</b> 1-8-4-3-6-5-7-2</li><li><b>Ölkapazität:</b> 8.5 L</li></ul></div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("### 🔧 Service eintragen")
            s_arbeit = st.text_input("Was wurde gemacht?", key="s_w_s")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_c_s")
            if st.button("Service speichern", key="s_b_s"):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
        st.write("---")
        up = st.file_uploader("Rechnung hochladen", type=['jpg', 'jpeg', 'png'], key="f_u_s")
        if up: st.image(up, caption="Service Dokument", use_container_width=True)
        if st.session_state.service_kosten: st.table(pd.DataFrame(st.session_state.service_kosten))

# TAB 3: KOSTEN
with tab3:
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.image("https://wikimedia.org", width=50)
        k_axa = st.number_input("AXA Versicherung 🛡️", value=1150.0, key="k_a_s")
        k_platz = st.number_input("Bootsplatz ⚓", value=1500.0, key="k_p_s")
        k_winter = st.number_input("Winterlager ❄️", value=2200.0, key="k_w_s")
        k_steuer = st.number_input("Steuern 📜", value=350.0, key="k_s_s")
        
    with col_k2:
        sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
        serv_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_axa + k_platz + k_winter + k_steuer
        st.metric("Fixkosten (Basis) 🏗️", f"CHF {fix:,.2f}")
        st.metric("Service & Benzin 🛠️", f"CHF {serv_sum + sprit_sum:,.2f}")
        st.write("---")
        st.write(f"**Total ohne Benzin:** CHF {fix + serv_sum:,.2f}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN (Inkl. Benzin)</h3><h1>CHF {fix + serv_sum + sprit_sum:,.2f}</h1></div>", unsafe_allow_html=True)

# TAB 4: LOGBUCH
with tab4:
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Törn-Ziel 📍", key="l_d_s")

st.write("---")
st.caption("Truelove Fleet v19.3-Stable | Zurück auf bewährte Version")
