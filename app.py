import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- APP SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif; font-size: 45px; font-weight: bold;
        color: #D4AF37; text-align: center; letter-spacing: 5px; margin-bottom: 0px;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif; font-size: 16px;
        text-align: center; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border: 1px solid #D4AF37; margin-top: 20px;
    }
    h3 { color: #D4AF37 !important; }
    .stButton>button {
        background-color: #8B6914 !important; color: white !important;
        border: 1px solid #D4AF37 !important; width: 100%;
    }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS VERBINDUNG ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(worksheet):
    try:
        # Liest das Blatt und entfernt komplett leere Zeilen
        return conn.read(worksheet=worksheet).dropna(how="all")
    except Exception:
        # Falls Blatt leer oder Fehler: Erstelle leere Tabelle mit passenden Spalten
        if worksheet == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_and_refresh(df, worksheet):
    conn.update(worksheet=worksheet, data=df)
    st.cache_data.clear()
    st.success("Daten erfolgreich synchronisiert! ✅")

# Daten initial laden
df_tanken = load_data("tanken")
df_service = load_data("service")

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036))
menu = st.radio("NAVIGATION", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True)

# --- SEITE: TANKEN ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tankstopp {auswahl_jahr}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    t_lit = col1.number_input("Liter", min_value=0.0, step=0.1)
    t_pr = col2.number_input("CHF / L", value=2.15, step=0.01)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime("%d.%m.%Y"),
            "Liter": t_lit, "CHF/L": t_pr,
            "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer
        }])
        df_tanken = pd.concat([df_tanken, new_row], ignore_index=True)
        save_and_refresh(df_tanken, "tanken")
        st.rerun()
    
    if not df_tanken.empty:
        st.write("### Historie")
        st.dataframe(df_tanken, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SEITE: SERVICE ---
elif menu == "⚙️ Service":
    st.markdown(f"<div class='card'><h3>⚙️ Wartung & Log</h3>", unsafe_allow_html=True)
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=1.0)
    
    if st.button("Service-Eintrag speichern"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime("%d.%m.%Y"),
            "Arbeit": s_arbeit, "CHF": s_preis
        }])
        df_service = pd.concat([df_service, new_row], ignore_index=True)
        save_and_refresh(df_service, "service")
        st.rerun()
    
    if not df_service.empty:
        st.write("### Service-Historie")
        st.dataframe(df_service, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SEITE: FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Kostenübersicht</h3>", unsafe_allow_html=True)
    
    # Summen berechnen (Sicherstellen, dass es Zahlen sind)
    t_sum = pd.to_numeric(df_tanken["Total CHF"], errors='coerce').sum()
    s_sum = pd.to_numeric(df_service["CHF"], errors='coerce').sum()
    
    st.metric("Benzinkosten Total", f"CHF {t_sum:,.2f}")
    st.metric("Servicekosten Total", f"CHF {s_sum:,.2f}")
    st.divider()
    st.metric("GESAMTKOSTEN", f"CHF {t_sum + s_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
