import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Skipper App", layout="wide")

# Nautisches CSS Design (Navy, Gold, Weiss)
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; color: #002347; }
    
    /* Metrics im Marine-Look */
    div[data-testid="stMetric"] { 
        background-color: #ffffff !important; 
        border-left: 5px solid #d4af37 !important; 
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Kompakter Tech-Kasten */
    .spec-card { 
        background-color: #002347; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #d4af37; 
        color: white;
        font-size: 14px;
    }
    .spec-card b { color: #d4af37; }
    
    /* Blauer Captains-Balken */
    .total-box { 
        background: linear-gradient(135deg, #002347 0%, #004080 100%);
        color: white !important; 
        padding: 15px; 
        border-radius: 12px; 
        text-align: center; 
        border: 2px solid #d4af37;
    }
    .total-box h1, .total-box h3 { color: white !important; margin: 0; }

    /* Tabs kompakter */
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] { 
        padding: 8px 12px; 
        font-size: 16px;
        background-color: #e6eef5;
        border-radius: 5px 5px 0 0;
    }
    
    h1, h2, h3 { color: #002347 !important; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Initialisierung
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'service_kosten' not in st.session_state: st.session_state.service_kosten = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=90)
            break
with col_r:
    st.markdown("<h2 style='margin:0;'>⚓ TRUELOVE | Skipper Zentrale</h2>", unsafe_allow_html=True)
    st.write("Crownline 286 SC • **V8 496 MAG HO**")

# --- KOMPAKTE REITER ---
tab1, tab2, tab3, tab4 = st.tabs(["⛽ Tanken", "⚙️ Technik", "💰 Kosten", "📖 Log"])

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
            st.markdown(f"**Marc:** CHF {ausg.get('Marc',0):,.20} | **Fabienne:** CHF {ausg.get('Fabienne',0):,.20}")
            st.dataframe(df_t, use_container_width=True, hide_index=True)

# TAB 2: TECHNIK & SERVICE
with tab2:
    c_m1, c_m2 = st.columns([1, 1])
    with c_m1:
        st.markdown("""<div class="spec-card"><b>V8 496 MAG HO Specs:</b><br>
        • 317 kW / 431 PS HO<br>• 8.2L Big Block<br>• Zweikreis-Kühlung<br>• WOT: 4600-5000 RPM<br>• Zündfolge: 1-8-4-3-6-5-7-2</div>""", unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with c_m2:
        with st.container(border=True):
            st.write("**🔧 Service-Eintrag**")
            s_arbeit = st.text_input("Arbeit", key="s_a_20")
            s_chf = st.number_input("Kosten (CHF)", min_value=0.0, key="s_c_20")
            if st.button("Speichern", use_container_width=True):
                st.session_state.service_kosten.append({"Datum": datetime.now().strftime("%d.%m"), "Arbeit": s_arbeit, "CHF": s_chf})
                st.rerun()
        if st.session_state.service_kosten:
            st.table(pd.DataFrame(st.session_state.service_kosten))

# TAB 3: KOSTEN
with tab3:
    c_k1, c_k2 = st.columns(2)
    with c_k1:
        st.image("https://wikimedia.org", width=40)
        k_axa = st.number_input("AXA 🛡️", value=1150.0, key="k_a_20")
        k_pl = st.number_input("Platz ⚓", value=1500.0, key="k_p_20")
        k_wi = st.number_input("Winter ❄️", value=2200.0, key="k_w_20")
        k_st = st.number_input("Steuer 📜", value=350.0, key="k_s_20")
    with c_k2:
        s_sum = sum(i['CHF'] for i in st.session_state.tank_daten)
        m_sum = sum(i['CHF'] for i in st.session_state.service_kosten)
        fix = k_axa + k_pl + k_wi + k_st
        st.metric("Fixkosten 🏗️", f"CHF {fix:,.20}")
        st.metric("Service 🛠️", f"CHF {m_sum:,.20}")
        st.metric("Sprit ⛽", f"CHF {s_sum:,.20}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN SAISON</h3><h1>CHF {fix + s_sum + m_sum:,.20}</h1></div>", unsafe_allow_html=True)

# TAB 4: LOGBUCH
with tab4:
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=350)
    st.text_input("Zielort 📍", key="l_d_20")

st.write("---")
st.caption("Truelove v20.0 | Nautical Edition")
