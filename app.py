import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# Nautisches Design (Heller Hintergrund, Navy Text)
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; color: #002347; }
    div[data-testid="stMetric"] { background-color: #ffffff !important; border-left: 5px solid #d4af37 !important; border-radius: 8px; }
    .spec-card { background-color: #002347; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; color: white; }
    .total-box { background: #002347; color: white !important; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #d4af37; }
    h1, h2, h3 { color: #002347 !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
st.title("⚓ TRUELOVE Skipper Zentrale")
st.write("Crownline 286 SC • **V8 496 MAG HO (317 kW)**")

# --- REITER ---
tab1, tab2, tab3, tab4 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=400)
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_dat = st.date_input("Datum", datetime.now(), key="date_fix")
            t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="lit_fix")
            t_pr = st.number_input("CHF/L", value=2.15, key="price_fix")
            t_w = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="who_fix")
            if st.button("Speichern ✅", key="save_fix"):
                if t_lit > 0:
                    st.session_state.tank_daten.append({"Datum": t_dat.strftime("%d.%m.%Y"), "Liter": t_lit, "CHF": round(t_lit * t_pr, 2), "Wer": t_w})
                    st.rerun()
            if st.button("Letzten löschen 🗑️", key="del_fix"):
                if st.session_state.tank_daten: 
                    st.session_state.tank_daten.pop()
                    st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df_t = pd.DataFrame(st.session_state.tank_daten)
            st.table(df_t)

with tab2:
    st.subheader("⚙️ Motor & Service")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="spec-card"><b>Mercruiser 496 MAG HO</b><br>
        • Leistung: 317 kW / 431 PS<br>• Hubraum: 8.2 Liter<br>• Zylinder: V8 Big Block<br>
        • Kühlung: Zweikreissystem<br>• WOT: 4600-5000 RPM<br>• Öl: 8.5 L</div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("**🔧 Service-Eintrag**")
            s_arbeit = st.text_input("Was wurde gemacht?", key="s_work_fix")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_price_fix")
            if st.button("Service speichern", key="s_save_fix"):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
        if st.session_state.service_kosten: st.table(pd.DataFrame(st.session_state.service_kosten))

with tab3:
    st.subheader("💰 Kostenübersicht")
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        k_axa = st.number_input("AXA 🛡️", value=1150.0, key="axa_fix")
        k_pl = st.number_input("Platz ⚓", value=1500.0, key="pl_fix")
        k_wi = st.number_input("Winter ❄️", value=2200.0, key="wi_fix")
        k_st = st.number_input("Steuer 📜", value=350.0, key="st_fix")
    with c_k2:
        sprit_sum = sum(i['CHF'] for i in st.session_state.tank_daten)
        serv_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_axa + k_pl + k_wi + k_st
        st.metric("Basis Fixkosten", f"CHF {fix:,.2f}")
        st.metric("Service Kosten", f"CHF {serv_sum:,.2f}")
        st.metric("Benzin Saison", f"CHF {sprit_sum:,.2f}")
        st.write("---")
        total = fix + serv_sum + sprit_sum
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN</h3><h1>CHF {total:,.2f}</h1></div>", unsafe_allow_html=True)

with tab4:
    st.header("📖 Logbuch")
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Zielort 📍", key="log_fix")

st.write("---")
st.caption("Truelove Fleet v20.2 | Stable Build")
