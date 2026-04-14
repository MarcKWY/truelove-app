import streamlit as st
import os

# --- APP SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

# Styling: Tiefblau & Gold
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .stMetric { background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 15px; }
    h1 { color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & LOGO ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG", "JPG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=120)
            break
with col_r:
    st.title("TRUELOVE: Dashboard")
    st.write("Crownline 286 SC | 8.2L V8 496 MAG")

# --- STARTSEITE: HAUPTBILD ---
if os.path.exists("boot_gross.jpg"):
    st.image("boot_gross.jpg", use_container_width=True)

st.divider()

# --- TABS MIT DEINEN SPEZIFISCHEN BILDERN ---
tab1, tab2, tab3 = st.tabs(["🚀 Reise & Tanken", "🔧 Wartung & Motor", "💰 Finanzen"])

with tab1:
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("Sprit-Kalkulation")
        dist = st.number_input("Distanz (nm)", value=20.0)
        liter = (dist / 22) * 60 
        st.metric("Spritbedarf", f"{liter:.1f} L")
        st.metric("Kosten", f"CHF {liter * 2.15:.2f}")
    
    with col_t2:
        if os.path.exists("tanken.jpg"):
            st.image("tanken.jpg", caption="Tank-Stopp", use_container_width=True)
        else:
            st.info("Hier erscheint 'tanken.jpg', sobald hochgeladen.")

with tab2:
    st.subheader("Technik & Wartung")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if os.path.exists("motor.jpg"):
            st.image("motor.jpg", caption="Mercruiser V8 496 MAG", use_container_width=True)
        st.write("**Status:** 317 KW Power bereit.")
            
    with col_m2:
        if os.path.exists("wartung.jpg"):
            st.image("wartung.jpg", caption="Service-Dokumentation", use_container_width=True)
        st.progress(0.8, text="Service-Intervall")
        st.write("🔔 Nächster Service: 45h")

with tab3:
    st.subheader("Kostenübersicht")
    v = st.number_input("Versicherung/Jahr", value=1150)
    w = st.number_input("Winterlager", value=2300)
    st.metric("Total CHF", f"{v + w + 350:,.2f}")

st.write("---")
st.caption("Truelove Fleet System v6.0 | Personal Media Edition")
