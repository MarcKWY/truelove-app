import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- APP SETUP ---
st.set_page_config(page_title="Truelove - V8 HO Edition", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .stMetric { background: rgba(0, 212, 255, 0.1); border-radius: 15px; border: 1px solid #00d4ff; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    h1, h2 { color: #00d4ff; }
    b { color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-SIMULATION (Tankbuch) ---
# In einer echten App würden wir hier eine CSV-Datei laden
if 'tank_daten' not in st.session_state:
    st.session_state.tank_daten = []

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_title:
    st.title("TRUELOVE | Skipper Dashboard")
    st.write(f"Saison {datetime.now().year} | Mercruiser 496 MAG HO")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken & Log", "🔧 Wartung", "⚙️ Motor-Specs", "💰 Fixkosten", "📖 Fahrtenbuch"])

with tab1:
    st.header("⛽ Tankbuch & Kalkulation")
    
    col_input, col_img = st.columns([2, 1])
    
    with col_input:
        with st.expander("➕ Neuen Tankstopp eintragen", expanded=True):
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("Preis pro Liter (CHF)", min_value=0.0, value=2.15)
            t_wer = st.selectbox("Bezahlt durch", ["Marc", "Fabienne"])
            
            if st.button("Eintrag speichern"):
                neuer_eintrag = {
                    "Datum": t_datum.strftime("%d.%m.%Y"),
                    "Liter": t_liter,
                    "CHF/L": t_preis,
                    "Total CHF": round(t_liter * t_preis, 2),
                    "Zahler": t_wer
                }
                st.session_state.tank_daten.append(neuer_eintrag)
                st.success("Tanken erfolgreich registriert!")

    with col_img:
        if os.path.exists("tanken.jpg"):
            st.image("tanken.jpg", use_container_width=True)

    # Auswertung
    if st.session_state.tank_daten:
        df = pd.DataFrame(st.session_state.tank_daten)
        st.write("### Aktuelle Saisonübersicht")
        st.dataframe(df, use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Liter", f"{df['Liter'].sum():.1f} L")
        with c2:
            st.metric("Total Kosten", f"CHF {df['Total CHF'].sum():,.2f}")
        with c3:
            st.metric("Einträge", len(df))
            
        # Wer hat wie viel bezahlt?
        st.write("**Wer hat wie viel bezahlt?**")
        ausgaben = df.groupby("Zahler")["Total CHF"].sum()
        st.write(ausgaben)
        
        if st.button("🚨 Saison abschliessen & Daten löschen"):
            st.session_state.tank_daten = []
            st.rerun()
    else:
        st.info("Noch keine Tankeinträge für diese Saison vorhanden.")

with tab2:
    st.header("Service & Wartung")
    if os.path.exists("wartung.jpg"):
        st.image("wartung.jpg", use_container_width=True)

with tab3:
    st.header("⚙️ 496 MAG HO Specs")
    if os.path.exists("motor.jpg"):
        st.image("motor.jpg", width=400)
    st.markdown("- **Leistung:** 317 kW / 431 PS\n- **Hubraum:** 8.2L V8 Big Block\n- **Zweikreiskühlung**")

with tab4:
    st.header("Fixkosten")
    if os.path.exists("kosten.jpg"):
        st.image("kosten.jpg", width=400)
    v = st.number_input("Versicherung (CHF)", value=1150)
    w = st.number_input("Winterlager (CHF)", value=2400)
    st.metric("Total Jahr", f"CHF {v + w + 350:,.2f}")

with tab5:
    st.header("Fahrtenbuch")
    st.text_input("Heutiger Törn")
    st.button("Speichern")

st.write("---")
st.caption(f"Truelove Fleet v10.0 | Tank-Tracker Aktiv")
