import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Skipper App", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; color: #002347; }
    div[data-testid="stMetric"] { background-color: #ffffff !important; border-left: 5px solid #d4af37 !important; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .spec-card { background-color: #002347; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; color: white; }
    .spec-card b { color: #d4af37; }
    .total-box { background: linear-gradient(135deg, #002347 0%, #004080 100%); color: white !important; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #d4af37; }
    .total-box h1, .total-box h3 { color: white !important; margin: 0; }
    h1, h2, h3 { color: #002347 !important; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

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
    st.markdown("<h2 style='margin:0;'>⚓ TRUELOVE | Skipper Zentrale</h2>", unsafe_allow_html=True)
    st.write("Crownline 286 SC • **V8 496 MAG HO (317 kW)**")

# --- REITER-STRUKTUR ---
tab1, tab2, tab3, tab4 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=600)
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_dat = st.date_input("Datum", datetime.now(), key="t_d_21")
            t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_l_21")
            t_pr = st.number_input("CHF/L", value=2.15, key="t_p_21")
            t_w = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="t_w_21")
            c1, c2 = st.columns(2)
            if c1.button("Sichern ✅", use_container_width=True, key="s_t_21"):
                if t_lit > 0:
                    st.session_state.tank_daten.append({"Datum": t_dat.strftime("%d.%m.%Y"), "Liter": t_lit, "CHF": round(t_lit * t_pr, 2), "Wer": t_w})
                    st.rerun()
            if c2.button("Löschen 🗑️", use_container_width=True, key="d_t_21"):
                if st.session_state.tank_daten: st.session_state.tank_daten.pop(); st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df_t = pd.DataFrame(st.session_state.tank_daten)
            ausg = df_t.groupby("Wer")["CHF"].sum()
            st.markdown(f"**Marc:** CHF {ausg.get('Marc',0):,.2f} | **Fabienne:** CHF {ausg.get('Fabienne',0):,.2f}")
            st.table(df_t)

with tab2:
    st.subheader("⚙️ Motor-Daten & Service")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="spec-card"><h3>Mercruiser 496 MAG HO</h3><ul>
        <li><b>Leistung:</b> 317 kW / 431 PS</li>
        <li><b>Hubraum:</b> 8.2 Liter</li>
        <li><b>Zylinder:</b> V8 Big Block</li>
        <li><b>Kühlung:</b> Zweikreissystem</li>
        <li><b>WOT:</b> 4600-5000 RPM</li>
        <li><b>Zündfolge:</b> 1-8-4-3-6-5-7-2</li>
        <li><b>Ölkapazität:</b> 8.5 L</li></ul></div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("**🔧 Service-Eintrag**")
            s_arbeit = st.text_input("Was wurde gemacht?", key="s_a_21")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_c_21")
            if st.button("Service speichern", use_container_width=True, key="s_s_21"):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
        st.write("---")
        up = st.file_uploader("Rechnung hochladen", type=['jpg', 'jpeg', 'png'], key="f_u_21")
        if up: st.image(up, caption="Service Dokument", use_container_width=True)
        if st.session_state.service_kosten: st.table(pd.DataFrame(st.session_state.service_kosten))

with tab3:
    st.subheader("💰 Kostenübersicht")
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        st.image("https://wikimedia.org", width=50)
        k_axa = st.number_input("AXA Versicherung 🛡️", value=1150.0, key="k_a_21")
        k_pl = st.number_input("Bootsplatz ⚓", value=1500.0, key="k_p_21")
        k_wi = st.number_input("Winterlager ❄️", value=2200.0, key="k_w_21")
        k_st = st.number_input("Steuern 📜", value=350.0, key="k_s_21")
    with c_k2:
        sprit_sum = sum(i['CHF'] for i in st.session_state.tank_daten)
        serv_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_axa + k_pl + k_wi + k_st
        st.metric("Fixkosten (Basis) 🏗️", f"CHF {fix:,.2f}")
        st.metric("Service & Reparaturen 🛠️", f"CHF {serv_sum:,.2f}")
        st.metric("Benzin Saison ⛽", f"CHF {sprit_sum:,.2f}")
        st.write("---")
        st.write(f"**Total ohne Benzin:** CHF {fix + serv_sum:,.2f}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN (Inkl. Benzin)</h3><h1>CHF {fix + serv_sum + sprit_sum:,.2f}</h1></div>", unsafe_allow_html=True)

with tab4:
    st.header("📖 Fahrtenbuch")
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Törn-Ziel 📍", key="l_d_21")

st.write("---")
st.caption("Truelove Fleet v20.1 | Stable Master Build")
