import streamlit as st
import os

# --- PREMIUM SETUP ---
st.set_page_config(page_title="Truelove App", layout="wide")

# Styling: Dunkler Hintergrund mit Blau-Akzenten für bessere Lesbarkeit
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255,255,255,0.05); 
        border-radius: 5px 5px 0 0; 
        padding: 10px 20px;
        color: white !important;
    }
    .stMetric { background: rgba(0, 212, 255, 0.1); border-radius: 10px; padding: 10px; }
    h1, h2 { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITEL ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Sucht Logo in allen Varianten
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_title:
    st.title("TRUELOVE - Crownline 286 SC")

# --- REITER (TABS) ERSTELLEN ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "🔧 Wartung", "⚙️ Motor", "💰 Kosten", "📖 Fahrtenbuch"])

with tab1:
    st.header("Sprit & Reichweite")
    col1, col2 = st.columns(2)
    with col1:
        dist = st.number_input("Distanz (nm)", value=25.0)
        liter = (dist / 22) * 60 # V8 Kalkulation
        st.metric("Spritbedarf", f"{liter:.1f} L")
        st.metric("Kosten", f"CHF {liter * 2.15:.2f}")
    with col2:
        if os.path.exists("tanken.jpg"):
            st.image("tanken.jpg", caption="Tanken der Truelove", use_container_width=True)

with tab2:
    st.header("Service & Pflege")
    if os.path.exists("wartung.jpg"):
        st.image("wartung.jpg", caption="Wartungsarbeiten", use_container_width=True)
    st.write("---")
    st.info("Nächster Ölwechsel: In 45 Betriebsstunden")
    st.checkbox("Unterwasseranstrich geprüft")
    st.checkbox("Anoden kontrolliert")

with tab3:
    st.header("Mercruiser V8 496 MAG")
    if os.path.exists("motor.jpg"):
        st.image("motor.jpg", caption="317 KW Kraftpaket", use_container_width=True)
    st.write("**Technische Daten:**")
    st.write("- Leistung: 431 PS")
    st.write("- Hubraum: 8.2 Liter")
    st.progress(0.9, text="Betriebsbereit")

with tab4:
    st.header("Budget (CHF)")
    v = st.number_input("Versicherung/Jahr", value=1150)
    s = st.number_input("Steuer/Jahr", value=350)
    w = st.number_input("Winterlager", value=2300)
    total = v + s + w
    st.metric("Total Fixkosten", f"CHF {total:,.2f}")
    st.write(f"Monatlich beiseitelegen: **CHF {total/12:.2f}**")

with tab5:
    st.header("Logbuch")
    st.text_input("Heutiges Ziel")
    st.text_area("Besatzung & Wetter")
    if st.button("Fahrt speichern"):
        st.success("Törn wurde im Fahrtenbuch archiviert!")
    
    # Platzhalter für das Hauptbild ganz unten im Fahrtenbuch
    if os.path.exists("boot_gross.jpg"):
        st.image("boot_gross.jpg", width=400, caption="Truelove in voller Fahrt")

st.write("---")
st.caption("Truelove Fleet v8.0 | Crownline Exclusive")
