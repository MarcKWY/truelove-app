import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- SETUP ---
st.set_page_config(page_title="Truelove Master", layout="centered")

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title {
        font-family: 'Georgia', serif; font-size: 45px; font-weight: bold;
        color: #D4AF37; text-align: center; letter-spacing: 5px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; margin-top: 10px;
    }
    h3 { color: #D4AF37 !important; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- VERBINDUNG ZU GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet):
    try:
        # Versucht Daten zu lesen, falls leer -> leeres DataFrame mit Spalten erstellen
        df = conn.read(worksheet=sheet)
        return df.dropna(how="all")
    except:
        if sheet == "tanken":
            return pd.DataFrame(columns=["Datum", "Liter", "CHF/L", "Total CHF", "Wer"])
        else:
            return pd.DataFrame(columns=["Datum", "Arbeit", "CHF"])

def save_data(df, sheet):
    conn.update(worksheet=sheet, data=df)
    st.cache_data.clear()

# --- DATEN LADEN ---
df_tanken = load_data("tanken")
df_service = load_data("service")

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
st.write("---")

auswahl_jahr = st.selectbox("📅 Saison", options=range(2025, 2030))
menu = st.radio("MENÜ", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True)

# --- TANKEN ---
if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>Tankstopp erfassen</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    lit = col1.number_input("Liter", min_value=0.0)
    preis = col2.number_input("CHF/L", value=2.15)
    wer = st.radio("Wer zahlt?", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern"):
        neuer_eintrag = pd.DataFrame([{
            "Datum": datetime.now().strftime("%d.%m.%Y"),
            "Liter": lit, "CHF/L": preis,
            "Total CHF": round(lit * preis, 2), "Wer": wer
        }])
        df_tanken = pd.concat([df_tanken, neuer_eintrag], ignore_index=True)
        save_data(df_tanken, "tanken")
        st.success("Erfolgreich gespeichert!")
        st.rerun()
    
    st.write("### Historie")
    st.dataframe(df_tanken)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SERVICE ---
elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>Service-Log</h3>", unsafe_allow_html=True)
    arbeit = st.text_input("Was wurde gemacht?")
    kosten = st.number_input("Kosten in CHF", min_value=0.0)
    
    if st.button("Service speichern"):
        neuer_service = pd.DataFrame([{
            "Datum": datetime.now().strftime("%d.%m.%Y"),
            "Arbeit": arbeit, "CHF": kosten
        }])
        df_service = pd.concat([df_service, neuer_service], ignore_index=True)
        save_data(df_service, "service")
        st.success("Service gespeichert!")
        st.rerun()
    
    st.write("### Bisherige Arbeiten")
    st.dataframe(df_service)
    st.markdown("</div>", unsafe_allow_html=True)

# --- FINANZEN ---
elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>Kostenübersicht</h3>", unsafe_allow_html=True)
    t_sum = pd.to_numeric(df_tanken["Total CHF"]).sum() if not df_tanken.empty else 0
    s_sum = pd.to_numeric(df_service["CHF"]).sum() if not df_service.empty else 0
    st.metric("Gesamtkosten Benzin", f"CHF {t_sum:,.2f}")
    st.metric("Gesamtkosten Service", f"CHF {s_sum:,.2f}")
    st.metric("TOTAL", f"CHF {t_sum + s_sum:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
