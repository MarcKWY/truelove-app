import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: HELL & FREUNDLICH ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# CSS für maximale Lesbarkeit (Heller Hintergrund, dunkle Schrift)
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; color: #1A1C1E; }
    
    /* Metrics: Hellweiss mit blauem Rand */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #005A9C !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    /* Tabelle: Kontrastreich */
    .stDataFrame, table { 
        background-color: white !important; 
        color: black !important; 
    }
    
    /* Reiter: Blau/Grau Design */
    .stTabs [data-baseweb="tab-list"] { background-color: #E1E8ED; border-radius: 10px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: #005A9C !important; font-weight: bold; font-size: 18px; }
    
    h1, h2, h3 { color: #005A9C !important; font-family: 'Helvetica Neue', sans-serif; }
    label { color: #1A1C1E !important; font-weight: bold !important; }
    
    /* Eingabefelder weiss machen */
    input { background-color: white !important; border: 1px solid #CED4DA !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-SPEICHER ---
if 'tank_daten' not in st.session_state:
    st.session_state.tank_daten = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=120)
            break
with col_r:
    st.title("⚓ TRUELOVE | Skipper Zentrale")
    st.markdown(f"**Crownline 286 SC** | Mercruiser 496 MAG HO | Saison {datetime.now().year}")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⛽ Tanken", "🔧 Wartung", "⚙️ Motor", "💰 Kosten", "📖 Logbuch"
])

with tab1:
    st.subheader("⛽ Tank-Management")
    col_in, col_res = st.columns([1, 2])
    
    with col_in:
        with st.container():
            st.write("### Neuer Eintrag")
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("CHF / L", value=2.15)
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            
            if st.button("Speichern 📥", use_container_width=True):
                if t_liter > 0:
                    st.session_state.tank_daten.append({
                        "Datum": t_datum.strftime("%d.%m.%Y"),
                        "Liter": t_liter,
                        "Preis": t_preis,
                        "Total CHF": round(t_liter * t_preis, 2),
                        "Zahler": t_wer
                    })
                    st.rerun()

        st.write("---")
        if st.session_state.tank_daten:
            if st.button("🗑️ Letzten Eintrag löschen"):
                st.session_state.tank_daten.pop()
                st.rerun()

    with col_res:
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            
            # Die Gesamtübersicht (Metric Cards)
            c1, c2 = st.columns(2)
            c1.metric("Gesamt Liter", f"{df['Liter'].sum():.1f} L")
            c2.metric("Gesamt Kosten", f"CHF {df['Total CHF'].sum():,.2f}")
            
            st.write("### Saison-Details")
            st.table(df) # table ist oft besser lesbar als dataframe

            # Wer hat wie viel bezahlt?
            st.write("### Verteilung")
            ausgaben = df.groupby("Zahler")["Total CHF"].sum()
            st.bar_chart(ausgaben)
        else:
            if os.path.exists("tanken.jpg"):
                st.image("tanken.jpg", use_container_width=True)

with tab2:
    st.subheader("🔧 Wartungshistorie")
    if os.path.exists("wartung.jpg"):
        st.image("wartung.jpg", width=600)
    st.info("**Hinweis:** Ölwechsel Mercruiser 496 fällig nach 50 Betriebsstunden.")

with tab3:
    st.subheader("⚙️ Triebwerk: 496 MAG HO")
    if os.path.exists("motor.jpg"):
        st.image("motor.jpg", width=500)
    st.markdown("""
    - **Hubraum:** 8.2 Liter V8
    - **Leistung:** 317 kW / 431 PS
    - **Kühlung:** Zweikreissystem
    """)

with tab4:
    st.subheader("💰 Jährliche Fixkosten")
    if os.path.exists("kosten.jpg"):
        st.image("kosten.jpg", width=500)
    # Kalkulations-Beispiel
    v = st.number_input("Versicherung/Jahr", value=1150)
    w = st.number_input("Winterlager", value=2300)
    st.metric("Total Kosten", f"CHF {v + w + 350:,.2f}")

with tab5:
    st.subheader("📖 Fahrtenbuch")
    st.text_input("Törn-Ziel (z.B. Vierwaldstättersee)")
    st.button("Logbuch-Eintrag erstellen")

st.write("---")
st.caption(f"Truelove Fleet v13.0 | Light Design for better visibility")
