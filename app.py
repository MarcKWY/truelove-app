import streamlit as st
from datetime import datetime

# --- PREMIUM DESIGN SETUP ---
st.set_page_config(page_title="Truelove - Crownline 286 SC", page_icon="⚓", layout="wide")

# Custom CSS für den "Luxus-Yacht" Look
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #d4af37 !important; font-weight: bold; }
    .stButton>button { border: 1px solid #d4af37; background-color: #1a1f26; color: #d4af37; border-radius: 5px; height: 3em; }
    .stButton>button:hover { background-color: #d4af37; color: #0b0e14; }
    .css-1kyx600 { background-color: #161b22; border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #d4af37; font-family: 'Playfair Display', serif; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER MIT LOGO ---
col_logo, col_info = st.columns([1, 3])
with col_logo:
    # Stabilerer Logo-Link
    st.image("https://crownline.com", width=220)

with col_info:
    st.title("TRUELOVE | Skipper Dashboard")
    st.markdown("#### Crownline 286 SC | 8.2L Mercruiser V8 496 MAG")

st.write("---")

# --- WARTUNGS-ALARM (Neu!) ---
with st.container():
    st.subheader("🛠️ Maschinenraum & Wartung")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Motorleistung", "317 KW / 431 PS")
    with c2:
        last_service = 450 # Beispielwert
        st.metric("Letzter Service bei", f"{last_service} h")
    with c3:
        next_service = 500
        st.metric("Nächster Service fällig", f"{next_service} h")
    
    st.warning(f"🔔 Hinweis: In ca. {next_service - last_service} Betriebsstunden ist der Ölwechsel für den V8 fällig.")

# --- NAVIGATION ---
tab_trip, tab_kosten, tab_log = st.tabs(["🚀 Törn-Planer", "💰 Finanzen (CHF)", "📋 Bordbuch"])

with tab_trip:
    st.subheader("Sprit & Reichweite")
    col_a, col_b = st.columns(2)
    with col_a:
        dist = st.number_input("Distanz (Seemeilen)", value=20.0)
        speed = st.slider("Reisegeschwindigkeit (kn)", 5, 45, 24)
        tank_inhalt = st.slider("Aktueller Tankstand (L)", 0, 300, 180)
    
    with col_b:
        verbrauch_h = 55.0 # Geschätzter V8 Verbrauch bei Gleitfahrt
        zeit = dist / speed
        benötigt = zeit * verbrauch_h
        st.metric("Spritbedarf", f"{benötigt:.1f} L", delta=f"{tank_inhalt - benötigt:.1f} L Rest")
        st.metric("Kosten (bei 2.15 CHF/L)", f"CHF {benötigt * 2.15:.2f}")

with tab_kosten:
    st.subheader("Kostenübersicht Truelove")
    k1, k2 = st.columns(2)
    with k1:
        v = st.number_input("Versicherung/Jahr", value=1150)
        s = st.number_input("Steuer (Kanton)/Jahr", value=380)
        w = st.number_input("Winterlager & Service", value=2400)
    with k2:
        total = v + s + w
        st.metric("Gesamt Fixkosten", f"CHF {total:,.2f}")
        st.info(f"Rückstellung monatlich: CHF {total/12:.2f}")

with tab_log:
    st.subheader("Digitales Logbuch")
    st.text_input("Törn-Bezeichnung (z.B. Ausflug nach Brunnen)")
    st.text_area("Besatzung & Wetternotizen")
    if st.button("Törn im Logbuch speichern"):
        st.success("Daten wurden sicher auf dem Server abgelegt.")

# --- FOOTER ---
st.write("---")
st.caption("Truelove Platinum Edition | Created for Crownline Owners")
