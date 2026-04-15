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

    label, .stRadio label, p, span {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stRadio"] label { font-size: 45px !important; }
    input { color: #000000 !important; font-size: 18px !important; }
    img { border: 2px solid #D4AF37 !important; border-radius: 15px !important; }
    
    .stButton>button {
        background-color: #8B6914 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
        width: 100%;
    }

    div[data-testid="stRadio"] > div {
        background-color: rgba(5, 15, 30, 0.85);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #D4AF37;
        margin-top: 10px;
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
        line-height: 1.6;
    }
    h2, h3, b { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    
    [data-testid="stTable"] {
        background-color: #0A1E3C !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS VERBINDUNG ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(worksheet):
    try:
        df = conn.read(worksheet=worksheet)
        return df.dropna(how="all")
    except:
        if worksheet == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_data(df, worksheet):
    conn.update(worksheet=worksheet, data=df)
    st.cache_data.clear()

# Daten initial laden
df_tanken = load_data("tanken")
df_service = load_data("service")

# --- HEADER ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.markdown("<p class='crownline-subtitle'>CROWNLINE 286 SC</p>", unsafe_allow_html=True)

auswahl_jahr = st.selectbox("📅 Saison wählen", options=range(2025, 2036), index=0)

if os.path.exists("boot_gross.jpg"): 
    st.image("boot_gross.jpg", use_container_width=True)

menu = st.radio("BRIDGE CONTROL", ["⛽ Tanken", "⚙️ Motor & Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

# Filter Logik
def filter_nach_jahr(df, jahr):
    if df.empty: return df
    return df[df['Datum'].astype(str).str.contains(str(jahr))]

# --- BEREICHE ---
if menu == "⛽ Tanken":
    st.markdown(f"<div class='card'><h3>⛽ Tanken Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("tanken.jpg"): st.image("tanken.jpg", width=300)
    
    col1, col2 = st.columns(2)
    t_lit = col1.number_input("Liter", min_value=0.0, step=0.01, format="%.2f")
    t_pr = col2.number_input("CHF / L", value=2.15, format="%.2f")
    t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime(f"%d.%m.%Y"), 
            "Liter": t_lit, "CHF/L": t_pr,
            "Total CHF": round(t_lit * t_pr, 2), "Wer": t_wer
        }])
        df_tanken = pd.concat([df_tanken, new_row], ignore_index=True)
        save_data(df_tanken, "tanken")
        st.rerun()

    tank_jahr = filter_nach_jahr(df_tanken, auswahl_jahr)
    if not tank_jahr.empty:
        st.table(tank_jahr)
        ausg = tank_jahr.groupby("Wer")["Total CHF"].sum()
        st.info(f"Marc: **CHF {ausg.get('Marc', 0.0):,.2f}** | Fabienne: **CHF {ausg.get('Fabienne', 0.0):,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Motor & Service":
    st.markdown(f"<div class='card'><h3>⚙️ Service Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    if os.path.exists("motor.jpg"): st.image("motor.jpg", width=300)
    
    st.markdown(f"""<div class='spec-card'>
    <b>Modell:</b> Mercruiser 496 MAG HO<br>
    <b>Leistung:</b> 425 HP | <b>Hubraum:</b> 8.1 Liter V8<br>
    <b>Öl:</b> 8.5 Liter SAE 25W-40 Synthetic Blend</div>""", unsafe_allow_html=True)
    
    s_arbeit = st.text_input("Was wurde gemacht?")
    s_preis = st.number_input("Kosten CHF", min_value=0.0, step=0.01, format="%.2f")
    
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame([{
            "Datum": datetime.now().strftime(f"%d.%m.%Y"), 
            "Arbeit": s_arbeit, "CHF": s_preis
        }])
        df_service = pd.concat([df_service, new_row], ignore_index=True)
        save_data(df_service, "service")
        st.rerun()
    
    service_jahr = filter_nach_jahr(df_service, auswahl_jahr)
    if not service_jahr.empty:
        st.table(service_jahr)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💰 Finanzen":
    st.markdown(f"<div class='card'><h3>💰 Finanzen Saison {auswahl_jahr}</h3>", unsafe_allow_html=True)
    f_winter = st.number_input("❄️ Winterlager (CHF)", value=2200.0)
    f_platz = st.number_input("⚓ Bootsplatz (CHF)", value=1500.0)
    
    tank_jahr = filter_nach_jahr(df_tanken, auswahl_jahr)
    serv_jahr = filter_nach_jahr(df_service, auswahl_jahr)
    
    sprit_sum = pd.to_numeric(tank_jahr["Total CHF"]).sum() if not tank_jahr.empty else 0
    serv_sum = pd.to_numeric(serv_jahr["CHF"]).sum() if not serv_jahr.empty else 0
    
    st.metric("GESAMTKOSTEN SAISON", f"CHF {(f_winter + f_platz + sprit_sum + serv_sum):,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
