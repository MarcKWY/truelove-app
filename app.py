import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- NAUTICAL STORY SETUP ---
st.set_page_config(page_title="Truelove Story", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #001F3F; }
    
    /* Story-Karten Design */
    .story-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #E6EBF0;
        margin-bottom: 20px;
    }
    
    .story-title {
        font-family: 'Georgia', serif;
        color: #001F3F;
        font-size: 24px;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    /* Captain's Highlight Box */
    .captain-box {
        background: linear-gradient(135deg, #001F3F 0%, #003366 100%);
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border-left: 8px solid #D4AF37;
    }
    
    h1 { font-family: 'Georgia', serif; letter-spacing: 2px; color: #001F3F; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher
if 't_story' not in st.session_state: st.session_state.t_story = []
if 's_story' not in st.session_state: st.session_state.s_story = []

# --- TITELBILD & LOGO ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if os.path.exists("logo.png"): st.image("logo.png", width=120)
st.title("Truelove Chronicles")
st.write("Crownline 286 SC | 8.2L V8 Power")
st.markdown("</div>", unsafe_allow_html=True)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

st.write("---")

# --- STORY NAVIGATION ---
menu = st.radio("Navigation", ["⚓ Übersicht", "⛽ Tank-Tagebuch", "⚙️ Maschinenraum", "💰 Finanzen"], horizontal=True)

if menu == "⚓ Übersicht":
    st.markdown("<div class='story-card'>", unsafe_allow_html=True)
    st.markdown("<div class='story-title'>Status-Bericht</div>", unsafe_allow_html=True)
    
    total_sprit = sum(i['CHF'] for i in st.session_state.t_story)
    total_serv = sum(i['CHF'] for i in st.session_state.s_story)
    
    st.write(f"Die **Truelove** ist bereit für die nächste Fahrt.")
    st.write(f"In dieser Saison wurden bereits **{sum(i['Liter'] for i in st.session_state.t_story):.1f} Liter** V8-Power verbraucht.")
    
    st.markdown(f"<div class='captain-box'><h3>Saison-Investition</h3><h2>CHF {total_sprit + total_serv + 5200:,.2f}</h2></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⛽ Tank-Tagebuch":
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", use_container_width=True)
    
    with st.form("tank_form", clear_on_submit=True):
        st.write("### Neuen Tankstopp festhalten")
        c1, c2 = st.columns(2)
        lit = c1.number_input("Liter", min_value=0.0)
        pr = c2.number_input("CHF/L", value=2.15)
        who = st.select_slider("Bezahlt von", options=["Marc", "Fabienne"])
        if st.form_submit_button("Logbuch aktualisieren"):
            st.session_state.t_story.append({"Datum": datetime.now().strftime("%d.%m"), "Liter": lit, "CHF": round(lit*pr, 2), "Wer": who})
            st.rerun()

    if st.session_state.t_story:
        for entry in reversed(st.session_state.t_story):
            st.markdown(f"**{entry['Datum']}**: {entry['Wer']} hat **{entry['Liter']}L** für **CHF {entry['CHF']}** getankt.")
        if st.button("Letzten Eintrag löschen"):
            st.session_state.t_story.pop()
            st.rerun()

elif menu == "⚙️ Maschinenraum":
    st.markdown("<div class='story-card'>", unsafe_allow_html=True)
    st.markdown("<div class='story-title'>V8 496 MAG HO Specs</div>", unsafe_allow_html=True)
    col_img, col_txt = st.columns([1, 1.2])
    with col_img:
        if os.path.exists("motor.jpg"): st.image("motor.jpg")
    with col_txt:
        st.write("**Kraft:** 317 kW / 431 PS")
        st.write("**Hubraum:** 8.2 Liter Big Block")
        st.write("**Kühlung:** Zweikreis (Closed)")
        st.write("**WOT:** 4600 - 5000 RPM")
    st.markdown("</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.write("### Service & Reparatur")
        s_txt = st.text_input("Was wurde gemacht?")
        s_chf = st.number_input("Kosten", min_value=0.0)
        if st.button("Eintrag speichern"):
            st.session_state.s_story.append({"Arbeit": s_txt, "CHF": s_chf})
            st.rerun()

elif menu == "💰 Finanzen":
    if os.path.exists("kosten.jpg"): st.image("kosten.jpg", use_container_width=True)
    st.markdown("<div class='story-card'>", unsafe_allow_html=True)
    st.markdown("<div class='story-title'>Fixe Kosten</div>", unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    v = k1.number_input("Versicherung", value=1150.0)
    p = k2.number_input("Bootsplatz", value=1500.0)
    w = k1.number_input("Winterlager", value=2200.0)
    s = k2.number_input("Steuern", value=350.0)
    
    fix_sum = v + p + w + s
    sprit_sum = sum(i['CHF'] for i in st.session_state.t_story)
    serv_sum = sum(i['CHF'] for i in st.session_state.s_story)
    
    st.write("---")
    st.markdown(f"**Basis-Kosten:** CHF {fix_sum + serv_sum:,.2f}")
    st.markdown(f"<div class='captain-box'><h3>Total inkl. Benzin</h3><h2>CHF {fix_sum + serv_sum + sprit_sum:,.2f}</h2></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.caption("Truelove Chronicles v21.0 | Story Edition")
