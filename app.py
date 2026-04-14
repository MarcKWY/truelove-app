import streamlit as st
from datetime import datetime

# --- SETUP & MARITIMES DESIGN ---
st.set_page_config(page_title="Truelove Dashboard", page_icon="🛥️", layout="wide")

# CSS für Hintergrundbild, Transparenz und Farben
st.markdown("""
    <style>
    /* Hintergrundbild (Wasser-Textur) */
    .stApp {
        background-image: url("https://unsplash.com");
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Boxen halbdurchsichtig (Frosted Glass Effekt) */
    div.stMetric, div[data-testid="stExpander"], div.stTabs, .st-emotion-cache-1kyx600 {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        color: #002d5a !important;
    }
    
    /* Texte anpassen */
    h1, h2, h3 { color: #ffffff !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    p, label { color: #002d5a !important; font-weight: bold; }
    
    /* Tabs Design */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0, 45, 90, 0.8); border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_title = st.columns([1, 2])
with col_logo:
    st.image("https://crownline.com", width=220)

with col_title:
    st.title("⚓ TRUELOVE: Crownline 286 SC")
    st.markdown("<p style='color:white; font-size:1.2em;'>V8 496 MAG Power Dashboard</p>", unsafe_allow_html=True)

# --- BILDER-GALERIE (Macht es lebendig) ---
col_img1, col_img2 = st.columns(2)
with col_img1:
    st.image("https://boats.com", caption="Crownline SC Series", use_container_width=True)
with col_img2:
    st.image("https://pboat.com", caption="8.2L Mercruiser V8", use_container_width=True)

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🚀 Reise-Planer", "💰 Kosten (CHF)", "📋 Bordbuch & Technik"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Fahrt-Kalkulation")
        distanz = st.number_input("Distanz (nm)", value=15.0)
        speed = st.slider("Speed (kn)", 5, 45, 22)
    with c2:
        sprit_preis = 2.15
        verbrauch_h = 55.0
        zeit = distanz / speed
        liter = zeit * verbrauch_h
        st.metric("Spritbedarf", f"{liter:.1f} Liter")
        st.metric("Kosten", f"CHF {liter * sprit_preis:.2f}")

with tab2:
    st.subheader("Finanzen")
    v = st.number_input("Versicherung/Jahr (CHF)", value=1100)
    s = st.number_input("Steuern (CHF)", value=350)
    w = st.number_input("Winterlager (CHF)", value=2200)
    total = v + s + w
    st.metric("Total Fixkosten", f"CHF {total:,.2f}")
    st.metric("Monatliche Sparrate", f"CHF {total/12:.2f}")

with tab3:
    st.subheader("Wartungs-Check")
    st.info("Nächster Service: In 45 Betriebsstunden fällig.")
    st.checkbox("Motoröl-Stand okay")
    st.checkbox("Batterien geladen")
    st.checkbox("Kühlwasser-Check")
    st.button("Törn im Logbuch speichern")

st.write("---")
st.caption(f"Truelove Cloud v3.0 | {datetime.now().year} | Design: Ocean-Blue")
