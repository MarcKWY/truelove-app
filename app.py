import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
from datetime import datetime

# --- SETUP: PRO-APP DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important; font-weight: bold !important;
        color: #D4AF37 !important; text-align: center !important;
        letter-spacing: 5px !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px; text-align: center; margin-top: -5px; color: #FFFFFF; opacity: 0.8; letter-spacing: 3px;
    }
    label, .stRadio label, p, span { color: #FFFFFF !important; font-size: 20px !important; font-weight: 500 !important; }
    input { color: #000000 !important; font-size: 18px !important; }
    .stButton>button {
        background-color: #8B6914 !important; color: white !important;
        border: 1px solid #D4AF37 !important; border-radius: 10px !important; width: 100%;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 20px;
    }
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1); padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; line-height: 1.6;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    [data-testid="stTable"] { background-color: #0A1E3C !important; border: 1px solid #D4AF37 !important; border-radius: 10px !important; }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS VERBINDUNG ---
SHEET_ID = "17cBCWZz_oFuPHVjbRkxGFLzkRVthK_2_cqFZY6vQ9Bo"
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(worksheet):
    try:
        return conn.read(spreadsheet=SHEET_ID, worksheet=worksheet).dropna(how="all")
    except Exception as e:
        st.error(f"Fehler beim Laden von {worksheet}: {e}")
        if worksheet == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_data(df, worksheet):
    try:
        # Hier probieren wir das Update
        conn.update(spreadsheet=SHEET_ID, worksheet=worksheet, data=df)
        st.cache_data.clear()
        st.success(f"Erfolgreich in {worksheet} gespeichert!")
        return True
    except Exception as e:
        # Falls es knallt, zeigen wir den Fehler GROSS an
        st.error(f"🚨 SPEICHERFEHLER in {worksheet}:")
        st.code(str(e))
        return False

# Daten laden
df_tanken = load_data("tanken")
df_service = load_data("service")

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036))

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

def filter_nach_jahr(df, jahr):
    if df.empty: return df
    df['Datum'] = df['Datum'].astype(str)
    return df[df['Datum'].str.contains(str(jahr))]

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tanken Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime(f"%d.%m.%Y"), "Liter": t_lit, "CHF/L": t_pr, "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer}])
        neuer_df = pd.concat([df_tanken, new_row], ignore_index=True)
        if save_data(neuer_df, "tanken"):
             st.info("App wird in 2 Sek. aktualisiert...")
             # st.rerun() entfernt, damit du den Fehler lesen kannst!

    tank_jahr = filter_nach_jahr(df_tanken, auswahl_jahr)
    if not tank_jahr.empty:
        st.table(tank_jahr)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown(f"<div class='card'><h3>⚙️ Service Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    st.markdown(f"""<div class='spec-card'><b>Modell:</b> Mercruiser 496 MAG HO<br><b>Leistung:</b> 317 kW (425 HP)<br><b>Hubraum:</b> 8.1 Liter V8</div>""", unsafe_allow_html=True)
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame([{"Datum": datetime.now().strftime(f"%d.%m.%Y"), "Arbeit": s_arbeit, "CHF": s_preis}])
        neuer_df_s = pd.concat([df_service, new_row], ignore_index=True)
        if save_data(neuer_df_s, "service"):
            st.info("App wird aktualisiert...")
    
    service_jahr = filter_nach_jahr(df_service, auswahl_jahr)
    if not service_jahr.empty:
        st.table(service_jahr)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown(f"<div class='card'><h3>💰 Finanzen Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    sprit_sum = pd.to_numeric(df_tanken["Total CHF"], errors='coerce').sum() if not df_tanken.empty else 0
    serv_sum = pd.to_numeric(df_service["CHF"], errors='coerce').sum() if not df_service.empty else 0
    st.metric("TOTAL INKL. BENZIN", f"CHF {(3700 + serv_sum + sprit_sum):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
