import streamlit as st
import os

# --- PREMIUM SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# CSS für den "High-End" Look
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #050a14 0%, #0a1428 100%); color: white; }
    .stMetric { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 15px; border: 1px solid #00d4ff; }
    h1 { color: #00d4ff; font-family: 'Arial Black'; letter-spacing: 2px; }
    .stButton>button { background-color: #00d4ff; color: #050a14; font-weight: bold; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER LOGO-CHECK ---
col_l, col_r = st.columns([1, 3])
with col_l:
    # Prüft verschiedene Schreibweisen für das Logo
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    elif os.path.exists("Logo.png"): st.image("Logo.png", width=150)
    elif os.path.exists("logo.jpg"): st.image("logo.jpg", width=150)
    else: st.write("⚓ [Logo hochladen]")

with col_r:
    st.title("TRUELOVE")
    st.write("Crownline 286 SC | 8.2L V8 496 MAG")

# --- HAUPTBILD ---
if os.path.exists("boot.jpg"):
    st.image("boot.jpg", use_container_width=True)
elif os.path.exists("boot.jpeg"):
    st.image("boot.jpeg", use_container_width=True)

st.write("---")

# --- NEUE FUNKTIONEN: TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Reise", "💰 Kosten", "🔧 Wartung", "🏆 Records"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        dist = st.number_input("Distanz (nm)", value=20.0)
        speed = st.slider("Speed (kn)", 5, 50, 24)
    with c2:
        # V8 496 MAG braucht bei ca. 3500-4000 RPM etwa 55-65 L/h
        liter = (dist / speed) * 60 
        st.metric("Spritbedarf", f"{liter:.1f} L")
        st.metric("Kosten (CHF)", f"{liter * 2.15:.2f}")

with tab2:
    st.subheader("Jährliche Fixkosten (CHF)")
    v = st.number_input("Versicherung", value=1150)
    s = st.number_input("Steuer", value=350)
    w = st.number_input("Winterlager & Service", value=2400)
    total = v + s + w
    st.metric("Total pro Jahr", f"CHF {total:,.2f}")
    st.write(f"Monatliche Rücklage: **CHF {total/12:.2f}**")

with tab3:
    st.subheader("V8 Service-Heft")
    st.info("Letzter Ölwechsel: Juni 2023")
    st.write("✅ Impeller: Neu (2023)")
    st.write("✅ Zündkerzen: Geprüft")
    st.progress(0.8, text="Nächster Service in ca. 40h")

with tab4:
    st.subheader("Persönliche Bestwerte")
    st.metric("Top Speed (GPS)", "44.2 kn", delta="V8 Peak")
    st.write("Datum: 15.08.2023 | Ort: Vierwaldstättersee")

st.write("---")
st.caption("Truelove Fleet Management v4.0")
