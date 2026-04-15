import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- SETUP: PRO-APP DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif !important;
        font-size: 45px !important;
        font-weight: bold !important;
        color: #D4AF37 !important;
        text-align: center !important;
        margin-bottom: 0px !important;
        letter-spacing: 5px !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
        display: block !important;
    }
    .crownline-subtitle {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px;
        text-align: center;
        margin-top: -5px;
        color: #FFFFFF;
        opacity: 0.8;
        letter-spacing: 3px;
    }
    label, p, span { color: #FFFFFF !important; font-size: 20px !important; }
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    .spec-card {
        background-color: rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #D4AF37;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS VERBINDUNG ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(worksheet_name):
    try:
        return conn.read(worksheet=worksheet_name).dropna(how="all")
    except:
        return pd.DataFrame()

def save_data(df, worksheet_name):
    conn.update(worksheet=worksheet_name, data=df)
    st.cache_data.clear()

# Daten laden
df_tanken = load_data("tanken")
df_service = load_data("service")

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036), index=0)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# --- FILTER LOGIK ---
def filter_nach_jahr(df, jahr):
    if df.empty: return df
    return df[df['Datum'].astype(str).str.contains(str(jahr))]

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tanken Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    
    t_lit = st.number_input("Liter", min_value=0.0, step=0.01)
    t_pr = st.number_input("CHF / L", value=2.15)
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime(f"%d.%m.{auswahl_jahr}"),
            "Liter": t_lit, "CHF/L": t_pr,
            "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer
        }])
        df_tanken = pd.concat([df_tanken, new_row], ignore_index=True)
        save_data(df_tanken, "tanken")
        st.success("Gespeichert!")
        st.rerun()
    
    tank_jahr = filter_nach_jahr(df_tanken, auswahl_jahr)
    if not tank_jahr.empty:
        st.table(tank_jahr)
        ausg = tank_jahr.groupby("Wer")["Total CHF"].sum()
        st.info(f"Marc: CHF {ausg.get('Marc', 0.0):.2f} | Fabienne: CHF {ausg.get('Fabienne', 0.0):.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown(f"<div class='card'><h3>⚙️ Service Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='spec-card'><b>Motor:</b> Mercruiser 496 MAG HO | 8.1L V8</div>", unsafe_allow_html=True)
    
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0)
    
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime(f"%d.%m.{auswahl_jahr}"),
            "Arbeit": s_arbeit, "CHF": s_preis
        }])
        df_service = pd.concat([df_service, new_row], ignore_index=True)
        save_data(df_service, "service")
        st.success("Service geloggt!")
        st.rerun()
    
    service_jahr = filter_nach_jahr(df_service, auswahl_jahr)
    if not service_jahr.empty:
        st.table(service_jahr)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown(f"<div class='card'><h3>💰 Finanzen Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    f_winter = st.number_input("❄️ Winterlager", value=2200.0)
    f_platz = st.number_input("⚓ Bootsplatz", value=1500.0)
    
    tank_jahr = filter_nach_jahr(df_tanken, auswahl_jahr)
    serv_jahr = filter_nach_jahr(df_service, auswahl_jahr)
    
    sprit_sum = tank_jahr["Total CHF"].sum() if not tank_jahr.empty else 0
    serv_sum = serv_jahr["CHF"].sum() if not serv_jahr.empty else 0
    
    st.metric("GESAMTKOSTEN SAISON", f"CHF {(f_winter + f_platz + sprit_sum + serv_sum):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
