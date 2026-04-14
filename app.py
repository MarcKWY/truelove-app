import streamlit as st
import os

# --- APP CONFIG & LIFESTYLE DESIGN ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# Radikales Custom CSS für Hintergrundbild und Lesbarkeit
st.markdown("""
    <style>
    /* Hintergrundbild fixieren */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://githubusercontent.com");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glassmorphism Karten-Design */
    .stTabs, .st-emotion-cache-1kyx600, div[data-testid="stMetric"] {
        background: rgba(10, 25, 45, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* Schriften & Farben */
    h1, h2, h3 { color: #00d4ff !important; font-family: 'Segoe UI', sans-serif; text-transform: uppercase; }
    p, label, .stMarkdown { color: #ffffff !important; font-weight: 500; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255,255,255,0.1); 
        border-radius: 10px 10px 0 0; 
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Sucht Logo in allen Varianten
    for ext in ["png", "jpg", "jpeg"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=120)
            break

with col_title:
    st.markdown("<h1>TRUELOVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2em;'>CROWNLINE 286 SC | V8 496 MAG</p>", unsafe_allow_html=True)

st.write("##")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🚀 NAVIGATION", "🔧 TECHNIK", "💰 BUDGET"])

with tab1:
    st.subheader("Trip-Kalkulator")
    c1, c2 = st.columns(2)
    with c1:
        dist = st.number_input("Distanz (Seemeilen)", value=20.0)
        speed = st.slider("Geschwindigkeit (kn)", 5, 50, 24)
        
        zeit = dist / speed
        liter = zeit * 60 # V8 Verbrauch
        
        st.metric("Vorauss. Verbrauch", f"{liter:.1f} L")
        st.metric("Kosten", f"CHF {liter * 2.15:.2f}")

    with c2:
        if os.path.exists("tanken.jpg"):
            st.image("tanken.jpg", caption="Tanken", use_container_width=True)

with tab2:
    st.subheader("Maschinenraum")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if os.path.exists("motor.jpg"):
            st.image("motor.jpg", caption="8.2L Power", use_container_width=True)
    with col_m2:
        if os.path.exists("wartung.jpg"):
            st.image("wartung.jpg", caption="Service Check", use_container_width=True)
        st.info("Letzter Service: Juni 2023")
        st.progress(0.85, text="Service fällig in 45h")

with tab3:
    st.subheader("Kostenübersicht (CHF)")
    v = st.number_input("Versicherung", value=1150)
    w = st.number_input("Winterlager", value=2300)
    total = v + w + 350
    st.metric("Total pro Jahr", f"CHF {total:,.2f}")

st.write("---")
st.caption(f"Truelove Platinum v7.0 | {os.name}")
