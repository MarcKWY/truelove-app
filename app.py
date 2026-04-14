import streamlit as st

# Setup & Dark-Theme Styling
st.set_page_config(page_title="Truelove App", page_icon="🛥️")

st.markdown("""
    <style>
    /* Hintergrund und Textfarben für den Premium-Look */
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1c212b; border: 1px solid #002d5a; padding: 15px; border-radius: 15px; }
    div[data-testid="stExpander"] { background-color: #1c212b; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #002d5a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.image("https://crownline.com", width=180)
st.title("Truelove Dashboard ⚓")

# --- TANK ANZEIGE (Neu!) ---
st.subheader("⛽ Treibstoff-Status")
tank_kapazitaet = 300  # Liter (Schätzung für 286 SC)
aktueller_stand = st.slider("Aktueller Tankinhalt (Liter)", 0, tank_kapazitaet, 220)
verbrauch_prozent = (aktueller_stand / tank_kapazitaet) * 100

if verbrauch_prozent > 20:
    st.progress(verbrauch_prozent / 100)
    st.write(f"Dein Tank ist noch zu {verbrauch_prozent:.0f}% voll ({aktueller_stand}L).")
else:
    st.error(f"⚠️ RESERVE! Nur noch {verbrauch_prozent:.0f}% im Tank.")

# --- BERECHNUNG ---
with st.expander("🚀 Fahrt-Kalkulator & Kosten", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        distanz = st.number_input("Distanz (nm)", value=15.0)
        speed = st.slider("Speed (kn)", 1, 45, 24)
        liter_preis = st.number_input("Preis CHF/L", value=2.10)
    
    # Kalkulation
    zeit = distanz / speed
    verbrauch = zeit * 50 # Annahme 50L/h für den V8
    kosten = verbrauch * liter_preis
    
    with col2:
        st.metric("Verbrauch Trip", f"{verbrauch:.1f} L")
        st.metric("Kosten Trip", f"CHF {kosten:.2f}")

# --- KOSTEN ZUSAMMENFASSUNG ---
with st.expander("💰 Fixkosten Übersicht (CHF)"):
    v = st.number_input("Versicherung/Jahr", value=1100)
    s = st.number_input("Steuer/Jahr", value=350)
    w = st.number_input("Winterlager", value=2200)
    total = v + s + w
    st.metric("Gesamtkosten Jahr", f"CHF {total}")
    st.caption(f"Das sind CHF {total/12:.2f} pro Monat.")

# --- LOGBUCH QUICK-ENTRY ---
st.subheader("📝 Quick-Log")
st.text_input("Wohin geht's heute?")
if st.button("Törn starten"):
    st.success("Fahrt wurde im Logbuch gespeichert!")

st.write("---")
st.caption("Truelove Crownline Edition | V8 Power")
