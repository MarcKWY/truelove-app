import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Skipper", layout="wide")

# Nautisches Design: Rein programmiertes Wellen-Muster (SVG)
st.markdown("""
    <style>
    /* Sicherer nautischer Hintergrund (Wellen-Muster programmiert) */
    .stApp {
        background-color: #f0f4f8;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' width='80' height='40' viewBox='0 0 80 40'%3E%3Cpath d='M0 40 C10 35 10 25 20 25 C30 25 30 35 40 40 C50 35 50 25 60 25 C70 25 70 35 80 40' fill='none' stroke='%23002d5a' stroke-width='1' stroke-opacity='0.1'/%3E%3C/svg%3E");
        background-attachment: fixed;
    }
    
    /* Inhalts-Boxen mit Glas-Effekt */
    div[data-testid="stMetric"], .stTabs, div[data-testid="stExpander"], .stTable, .stDataFrame {
        background-color: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(5px);
        border-radius: 12px !important;
        border: 1px solid rgba(0, 45, 90, 0.1) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }

    div[data-testid="stMetric"] { border-left: 6px solid #D4AF37 !important; }
    
    .motor-card {
        background-color: #002d5a;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #D4AF37;
        color: white;
    }
    .motor-card b { color: #D4AF37; }
    
    .nav-box { 
        background: #002d5a; color: white !important; padding: 15px; 
        border-radius: 12px; text-align: center; border: 2px solid #D4AF37;
    }
    .gold-box { 
        background: #D4AF37; color: #002d5a !important; padding: 15px; 
        border-radius: 12px; text-align: center; border: 2px solid #002d5a; font-weight: bold;
    }
    
    h1, h2, h3 { color: #002d5a !important; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Initialisierung
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=80)
            break
with col_title:
    st.markdown("<h2 style='margin:0;'>⚓ TRUELOVE | Skipper Zentrale</h2>", unsafe_allow_html=True)
    st.write("Crownline 286 SC • **V8 496 MAG HO**")

# --- REITER ---
tab1, tab2, tab3 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten"])

with tab1:
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=350)
    c_in, c_res = st.columns([1, 1.2])
    with c_in:
        with st.container(border=True):
            t_dat = st.date_input("Datum", datetime.now(), key="t_d_24")
            t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_l_24")
            t_pr = st.number_input("CHF/L", value=2.15, key="t_p_24")
            t_w = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="t_w_24")
            c1, c2 = st.columns(2)
            if c1.button("Sichern ✅", use_container_width=True, key="s_t_24"):
                if t_lit > 0:
                    st.session_state.tank_daten.append({"Datum": t_dat.strftime("%d.%m"), "Liter": t_lit, "CHF": round(t_lit * t_pr, 2), "Wer": t_w})
                    st.rerun()
            if c2.button("Löschen 🗑️", use_container_width=True, key="d_t_24"):
                if st.session_state.tank_daten: st.session_state.tank_daten.pop(); st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df_t = pd.DataFrame(st.session_state.tank_daten)
            ausg = df_t.groupby("Wer")["CHF"].sum()
            st.write(f"**Marc:** CHF {ausg.get('Marc',0):,.2f} | **Fabienne:** CHF {ausg.get('Fabienne',0):,.2f}")
            st.dataframe(df_t, use_container_width=True, hide_index=True)

with tab2:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="motor-card">
        <h3>⚙️ Mercruiser 496 MAG HO</h3>
        • <b>Leistung:</b> 317 kW / 431 PS HO<br>
        • <b>Hubraum:</b> 8.2L Big Block (496 cid)<br>
        • <b>Zylinder:</b> V8<br>
        • <b>Kühlung:</b> Zweikreissystem (Closed)<br>
        • <b>WOT:</b> 4600 - 5000 RPM<br>
        • <b>Einspritzung:</b> Multi-Point (MPI)<br>
        • <b>Zündfolge:</b> 1-8-4-3-6-5-7-2<br>
        • <b>Ölkapazität:</b> 8.5 Liter
        </div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("**🔧 Service-Eintrag**")
            s_arbeit = st.text_input("Arbeit", key="s_a_24")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_c_24")
            if st.button("Speichern", key="s_s_24"):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
            if st.button("Löschen", key="s_l_24"):
                if st.session_state.service_kosten: st.session_state.service_kosten.pop(); st.rerun()
        if st.session_state.service_kosten:
            st.table(pd.DataFrame(st.session_state.service_kosten))

with tab3:
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        k_vers = st.number_input("Versicherung 🛡️", value=1150.0, key="k_v_24")
        k_pl = st.number_input("Bootsplatz ⚓", value=1500.0, key="k_p_24")
        k_wi = st.number_input("Winterlager ❄️", value=2200.0, key="k_w_24")
        k_st = st.number_input("Steuern 📜", value=350.0, key="k_s_24")
    with c_k2:
        s_sum = sum(i['CHF'] for i in st.session_state.tank_daten)
        m_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_vers + k_pl + k_wi + k_st
        st.markdown(f"<div class='nav-box'><small>Fixkosten + Service</small><br><h2>CHF {fix + m_sum:,.2f}</h2></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='gold-box'><small>Gesamtkosten inkl. Benzin</small><br><h2>CHF {fix + m_sum + s_sum:,.2f}</h2></div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Skipper v20.4 | Safe Nautical Edition")
