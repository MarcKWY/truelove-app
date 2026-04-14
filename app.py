import streamlit as st

# --- DESIGN & LIFESTYLE SETUP ---
st.set_page_config(page_title="Truelove Dashboard", page_icon="🛥️", layout="wide")

# CSS für den "High-End" Look (Dark Mode mit Glas-Effekt)
st.markdown("""
    <style>
    .stApp {
        background-color: #050a14;
        color: #ffffff;
    }
    /* Die Karten für die Funktionen */
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    h1, h2 { color: #00d4ff !important; font-family: 'Trebuchet MS', sans-serif; }
    label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BILDER-BEREICH (BOOT & LOGO) ---
# Hier laden wir die Bilder direkt
col_logo, col_text = st.columns([1, 3])
with col_logo:
    # Das Crownline Logo
    st.image("https://logovector.net", width=180)

with col_text:
    st.title("⚓ TRUELOVE | Skipper App")
    st.write("Crownline 286 SC • Mercruiser V8 496 MAG (317 KW)")

# DAS HAUPTBILD DEINES BOOTES (Crownline 286 SC)
st.image("https://boats.com", 
         caption="DEINE TRUELOVE - CROWNLINE 286 SC", 
         use_container_width=True)

st.write("---")

# --- FUNKTIONEN ---
tab1, tab2, tab3 = st.tabs(["🚀 Navigation", "💰 Kosten (CHF)", "⚙️ Motor & Technik"])

with tab1:
    st.subheader("Sprit-Kalkulator")
    c1, c2 = st.columns(2)
    with c1:
        dist = st.number_input("Distanz (nm)", value=15.0)
        speed = st.slider("Speed (kn)", 5, 45, 24)
    with c2:
        verbrauch = (dist / speed) * 55 # V8 Verbrauch
        st.metric("Spritbedarf", f"{verbrauch:.1f} Liter", delta="Reservetank prüfen")
        st.metric("Kosten Trip", f"CHF {verbrauch * 2.15:.2f}")

with tab2:
    st.subheader("Finanzen")
    k1, k2 = st.columns(2)
    with k1:
        v = st.number_input("Versicherung/Jahr", value=1150)
        w = st.number_input("Winterlager", value=2200)
    with k2:
        total = v + w + 380
        st.metric("Total pro Jahr", f"CHF {total:,.2f}")
        st.info(f"Rückstellung: CHF {total/12:.2f} / Monat")

with tab3:
    st.subheader("Motorraum (V8 496 MAG)")
    # Bild vom Motor
    st.image("https://pboat.com", width=400, caption="Der Herzschlag deiner Truelove")
    st.progress(0.9)
    st.write("✅ Ölstand & Kühlung: OK")
    st.write("🔔 Service in 45 Stunden")

st.write("---")
st.caption("Truelove Premium System | Swiss Edition")
