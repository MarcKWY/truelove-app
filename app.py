import streamlit as st
import os

# --- SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# CSS für den edlen Look
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1 { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- BILDER LADEN (LOKAL AUS GITHUB) ---
col1, col2 = st.columns([1, 3])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        st.write("⚓ LOGO FEHLT")

with col2:
    st.title("TRUELOVE: CROWNLINE 286 SC")
    st.write("V8 496 MAG Power Dashboard")

# DAS HAUPTBILD (DIREKT AUS DEINEM ORDNER)
if os.path.exists("boot.jpg"):
    st.image("boot.jpg", caption="Deine Truelove", use_container_width=True)
else:
    st.warning("⚠️ Bitte lade ein Foto namens 'boot.jpg' in dein GitHub-Repo hoch!")

st.write("---")

# --- FUNKTIONEN ---
tab1, tab2 = st.tabs(["🚀 Reise-Planer", "💰 Kosten (CHF)"])

with tab1:
    st.subheader("Sprit-Kalkulation")
    dist = st.number_input("Distanz (nm)", value=20.0)
    # 55 Liter pro Stunde für den V8 496 MAG bei Gleitfahrt
    verbrauch = (dist / 24) * 55 
    st.metric("Spritbedarf", f"{verbrauch:.1f} Liter")
    st.metric("Kosten", f"CHF {verbrauch * 2.15:.2f}")

with tab2:
    st.subheader("Fixkosten (CHF)")
    v = st.number_input("Versicherung", value=1150)
    w = st.number_input("Winterlager", value=2300)
    st.metric("Total Jahr", f"CHF {v + w + 350:,.2f}")
