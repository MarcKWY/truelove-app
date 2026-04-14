import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- NAUTIC DESIGN SETUP ---
st.set_page_config(page_title="Truelove Skipper", layout="wide")

st.markdown("""
    <style>
    /* Hintergrund & Grundschrift */
    .stApp { background-color: #F4F7F9; color: #001F3F; }
    
    /* Nautische Header-Boxen (Metrics) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-left: 6px solid #D4AF37 !important; /* Goldkante */
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Kompakter Technik-Kasten */
    .spec-card {
        background-color: #001F3F;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #D4AF37;
        color: white;
        font-size: 0.9em;
    }
    .spec-card b { color: #D4AF37; }
    
    /* Captains-Kosten-Boxen */
    .cost-box-fix { 
        background: linear-gradient(135deg, #003366 0%, #001F3F 100%);
        color: white !important; padding: 15px; border-radius: 12px; text-align: center;
        border: 1px solid #D4AF37; margin-bottom: 10px;
    }
    .cost-box-full { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: white !important; padding: 15px; border-radius: 12px; text-align: center;
        border: 1px solid #001F3F;
    }
    .cost-box-fix h2, .cost-box-full h2 { color: white !important; margin: 0; font-size: 1.8em; }
    .cost-box-fix p, .cost-box-full p { color: #f0f0f0 !important; margin: 0; text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px; }

    /* Tabs kompakter gestalten */
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { 
        padding: 8px 12px; 
        font-size: 16px;
        background-color: #e6ebf0;
        border-radius: 5px 5px 0 0;
    }
    
    h1, h2, h3 { color: #001F3F !important; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=80)
            break
with col_title:
    st.markdown("<h2 style='margin:0;'>⚓ TRUELOVE | Skipper Zentrale</h2>", unsafe_allow_html=True)
    st.write("Crownline 286 SC • **V8 496 MAG HO**")

# --- KOMPAKTE REITER ---
tab1, tab2, tab3 = st.tabs(["⛽ Tanken", "⚙️ Technik & Service", "💰 Kosten"])

# TAB 1: TANKEN
with tab1:
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=400)
    col_in, col_res = st.columns([1, 1.2])
    with col_in:
        with st.container(border=True):
            t_dat = st.date_input("Datum", datetime.now(), key="t_d_20")
            t_lit = st.number_input("Liter", min_value=0.0, step=10.0, key="t_l_20")
            t_pr = st.number_input("CHF/L", value=2.15, key="t_p_20")
            t_w = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="t_w_20")
            c1, c2 = st.columns(2)
            if c1.button("Sichern ✅", use_container_width=True):
                if t_lit > 0:
                    st.session_state.tank_daten.append({"Datum": t_dat.strftime("%d.%m"), "Liter": t_lit, "CHF": round(t_lit * t_pr, 2), "Wer": t_w})
                    st.rerun()
            if c2.button("Löschen 🗑️", use_container_width=True):
                if st.session_state.tank_daten: st.session_state.tank_daten.pop(); st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df_t = pd.DataFrame(st.session_state.tank_daten)
            ausg = df_t.groupby("Wer")["CHF"].sum()
            st.markdown(f"**Marc:** CHF {ausg.get('Marc',0):,.2f} | **Fabienne:** CHF {ausg.get('Fabienne',0):,.2f}")
            st.dataframe(df_t, use_container_width=True, hide_index=True)

# TAB 2: TECHNIK & SERVICE
with tab2:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""<div class="spec-card"><b>V8 496 MAG HO Specs:</b><br>
        • 317 kW / 431 PS<br>• 8.2L Big Block<br>• Zweikreis-Kühlung<br>• WOT: 4600-5000 RPM</div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        with st.container(border=True):
            st.write("**🔧 Service-Eintrag**")
            s_arbeit = st.text_input("Arbeit", key="s_a_20")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_c_20")
            cs1, cs2 = st.columns(2)
            if cs1.button("Speichern", use_container_width=True):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
            if cs2.button("Löschen", use_container_width=True):
                if st.session_state.service_kosten: st.session_state.service_kosten.pop(); st.rerun()
        if st.session_state.service_kosten:
            st.table(pd.DataFrame(st.session_state.service_kosten))

# TAB 3: KOSTEN
with tab3:
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        k_vers = st.number_input("Versicherung 🛡️", value=1150.0, key="k_v_20")
        k_pl = st.number_input("Bootsplatz ⚓", value=1500.0, key="k_p_20")
        k_wi = st.number_input("Winterlager ❄️", value=2200.0, key="k_w_20")
        k_st = st.number_input("Steuern 📜", value=350.0, key="k_s_20")
    with c_k2:
        s_sum = sum(i['CHF'] for i in st.session_state.tank_daten)
        m_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_vers + k_pl + k_wi + k_st
        
        st.markdown(f"<div class='cost-box-fix'><p>Total ohne Benzin</p><h2>CHF {fix + m_sum:,.2f}</h2></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='cost-box-full'><p>Total inkl. Benzin</p><h2>CHF {fix + m_sum + s_sum:,.2f}</h2></div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Skipper v20.0 | Nautical Master Build")
