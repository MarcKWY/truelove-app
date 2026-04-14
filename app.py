import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- APP SETUP ---
st.set_page_config(page_title="Truelove - Tank-Management", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .stMetric { background: rgba(0, 212, 255, 0.1); border-radius: 15px; border: 1px solid #00d4ff; }
    h1, h2 { color: #00d4ff; }
    /* Tabelle lesbar machen */
    .stDataFrame { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN-SPEICHER ---
if 'tank_daten' not in st.session_state:
    st.session_state.tank_daten = []

# --- HEADER ---
st.title("⚓ TRUELOVE | Tank-Zentrale")
st.write(f"Saison {datetime.now().year} | Mercruiser 496 MAG HO")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "🔧 Wartung", "⚙️ Motor", "💰 Kosten", "📖 Fahrtenbuch"])

with tab1:
    col_in, col_list = st.columns([1, 2])
    
    with col_in:
        st.subheader("➕ Eintrag hinzufügen")
        t_datum = st.date_input("Datum", datetime.now())
        t_liter = st.number_input("Liter (L)", min_value=0.0, step=5.0)
        t_preis = st.number_input("Preis CHF/L", min_value=0.0, value=2.15)
        t_wer = st.selectbox("Bezahlt durch", ["Marc", "Fabienne"])
        
        if st.button("Speichern"):
            if t_liter > 0:
                neuer_eintrag = {
                    "Datum": t_datum.strftime("%d.%m.%Y"),
                    "Liter": t_liter,
                    "CHF/L": t_preis,
                    "Total CHF": round(t_liter * t_preis, 2),
                    "Zahler": t_wer
                }
                st.session_state.tank_daten.append(neuer_eintrag)
                st.success("Gespeichert!")
                st.rerun()
            else:
                st.error("Bitte Liter eingeben!")

        st.write("---")
        st.subheader("🗑️ Korrektur")
        if st.session_state.tank_daten:
            if st.button("Letzten Eintrag löschen"):
                st.session_state.tank_daten.pop()
                st.warning("Letzter Eintrag entfernt.")
                st.rerun()
            
            del_index = st.number_input("Eintrag Nr. zum Löschen", min_value=0, max_value=len(st.session_state.tank_daten)-1, step=1)
            if st.button(f"Eintrag Nr. {del_index} löschen"):
                st.session_state.tank_daten.pop(del_index)
                st.rerun()

    with col_list:
        st.subheader("📋 Tank-Übersicht")
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            # Tabelle mit Index anzeigen, damit man weiss, welche Nummer man löschen muss
            st.table(df)
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Gesamt Liter", f"{df['Liter'].sum():.1f} L")
            with c2:
                st.metric("Gesamt Kosten", f"CHF {df['Total CHF'].sum():,.2f}")
            
            # Auswertung pro Person
            st.write("**Verteilung Marc & Fabienne:**")
            st.bar_chart(df.groupby("Zahler")["Total CHF"].sum())
        else:
            st.info("Noch keine Daten vorhanden.")
            if os.path.exists("tanken.jpg"):
                st.image("tanken.jpg", use_container_width=True)

# (Die restlichen Reiter bleiben wie gehabt)
with tab2:
    if os.path.exists("wartung.jpg"): st.image("wartung.jpg", use_container_width=True)
with tab3:
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=400)
    st.write("317 KW / 431 PS HO Power")
with tab4:
    if os.path.exists("kosten.jpg"): st.image("kosten.jpg", width=400)
with tab5:
    st.header("Fahrtenbuch")
    st.text_input("Heutiger Törn")

st.write("---")
st.caption("Truelove Fleet v11.0 | Edit & Delete Mode")
