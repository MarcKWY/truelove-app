import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# Nautisches Design: Wellen-Muster & Navy-Farben
st.markdown("""
    <style>
    /* Sicherer nautischer Hintergrund */
    .stApp {
        background-color: #f0f4f8;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://w3.org' width='80' height='40' viewBox='0 0 80 40'%3E%3Cpath d='M0 40 C10 35 10 25 20 25 C30 25 30 35 40 40' fill='none' stroke='%23002d5a' stroke-width='1' stroke-opacity='0.1'/%3E%3C/svg%3E");
    }
    
    /* Weisse Boxen für gute Lesbarkeit */
    div[data-testid="stMetric"], .stTabs, .stTable, .stDataFrame {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: 1px solid #ddd !important;
    }

    div[data-testid="stMetric"] { border-left: 6px solid #D4AF37 !important; }
    
    /* Maschinenraum-Karte */
    .motor-card {
        background-color: #002d5a;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #D4AF37;
        color: white;
    }
    
    /* Kosten-Boxen */
    .nav-box { 
        background: #002d5a; color: white !important; padding: 15px; 
        border-radius: 12px; text-align: center; border: 1px solid #D4AF37;
    }
    .gold-box { 
        background: #D4AF37; color: #002d5a !important; padding: 15px; 
        border-radius: 12px; text-align: center; font-weight: bold;
    }
    h1, h2, h3 { color: #002d5a !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_v20' not in st.session_state: st.session_state.tank_v20 = []
if 'serv_v20' not in st.session_state: st.session_state.serv_v20 = []

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=80)
            break
with col_title:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write("Crownline 286 SC • **V8 496 MAG HO**")

# --- REITER ---
t1, t2, t3 = st.tabs(["⛽ Tanken", "⚙️ Motor & Service", "💰 Kosten"])

with t1:
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=350)
    c_in, c_res = st.columns(2)
    with c_in:
        with st.container(border=True):
            d_t = st.date_input("Datum", datetime.now(), key="k_dat_t")
            l_t = st.number_input("Liter", min_value=0.0, step=10.0, key="k_lit_t")
            p_t = st.number_input("CHF/L", value=2.15, key="k_pri_t")
            w_t = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="k_who_t")
            if st.button("Speichern ✅", key="k_btn_s_t"):
                if l_t > 0:
                    st.session_state.tank_v20.append({"Datum": d_t.strftime("%d.%m"), "Liter": l_t, "CHF": round(l_t * p_t, 2), "Wer": w_t})
                    st.rerun()
            if st.button("Löschen 🗑️", key="k_btn_d_t"):
                if st.session_state.tank_v20: st.session_state.tank_v20.pop(); st.rerun()
    with c_res:
        if st.session_state.tank_v20:
            df = pd.DataFrame(st.session_state.tank_v20)
            st.table(df)

with t2:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="motor-card">
        <h3>⚙️ 496 MAG HO</h3>
        • 317 kW / 431 PS<br>• 8.2L V8 Big Block<br>• Zweikreiskühlung<br>• WOT: 4600-5000<br>• Öl: 8.5 L
        </div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("**🔧 Service**")
            s_a = st.text_input("Was wurde gemacht?", key="k_ser_a")
            s_c = st.number_input("Kosten (CHF)", min_value=0.0, key="k_ser_c")
            if st.button("Service speichern", key="k_btn_s_s"):
                st.session_state.serv_v20.append({"Arbeit": s_a, "CHF": s_c})
                st.rerun()
        if st.session_state.serv_v20: st.table(pd.DataFrame(st.session_state.serv_v20))

with t3:
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        k_v = st.number_input("Versicherung 🛡️", value=1150.0, key="k_fix_v")
        k_p = st.number_input("Platz ⚓", value=1500.0, key="k_fix_p")
        k_w = st.number_input("Winter ❄️", value=2200.0, key="k_fix_w")
        k_s = st.number_input("Steuer 📜", value=350.0, key="k_fix_s")
    with c_k2:
        sum_t = sum(i['CHF'] for i in st.session_state.tank_v20)
        sum_s = sum(i['CHF'] for i in st.session_state.serv_v20)
        fix = k_v + k_p + k_w + k_s
        st.metric("Fixkosten + Service", f"CHF {fix + sum_s:,.2f}")
        st.markdown(f"<div class='nav-box'><small>Basis + Service</small><br><h2>CHF {fix + sum_s:,.2f}</h2></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='gold-box'><small>Total inkl. Benzin</small><br><h2>CHF {fix + sum_s + sum_t:,.2f}</h2></div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Fleet v20.5 | Final Stable Version")
