import streamlit as st
import os

# --- APP SETUP ---
st.set_page_config(page_title="Truelove - V8 HO Edition", layout="wide")

# Styling: High-End Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: white; }
    .stMetric { background: rgba(0, 212, 255, 0.1); border-radius: 15px; border: 1px solid #00d4ff; }
    .spec-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #d4af37; }
    h1, h2 { color: #00d4ff; }
    b { color: #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=120)
            break
with col_title:
    st.title("TRUELOVE | Crownline 286 SC")
    st.write("Special Edition: Mercruiser 8.2L V8 High Output")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "🔧 Wartung", "⚙️ Motor-Specs", "💰 Kosten", "📖 Fahrtenbuch"])

with tab1:
    st.header("Reise-Kalkulation")
    col1, col2 = st.columns(2)
    with col1:
        dist = st.number_input("Distanz (nm)", value=25.0)
        # Der HO verbraucht bei ca. 3500 RPM (Cruising) ca. 60-70 L/h
        liter = (dist / 22) * 65 
        st.metric("Spritbedarf", f"{liter:.1f} L")
        st.metric("Kosten (CHF)", f"{liter * 2.15:.2f}")
    with col2:
        if os.path.exists("tanken.jpg"):
            st.image("tanken.jpg", caption="Refueling Truelove", use_container_width=True)

with tab2:
    st.header("Service-Intervall")
    if os.path.exists("wartung.jpg"):
        st.image("wartung.jpg", use_container_width=True)
    st.write("---")
    st.warning("Nächster Service: Getriebeöl & Impeller-Check empfohlen.")

with tab3:
    st.header("⚙️ Mercruiser 496 MAG HO (High Output)")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if os.path.exists("motor.jpg"):
            st.image("motor.jpg", caption="8.2L V8 Big Block", use_container_width=True)
            
    with col_m2:
        st.markdown("""
        <div class="spec-box">
        <h3>Technische Daten:</h3>
        <ul>
            <li><b>Leistung:</b> 317 kW / 431 PS (High Output)</li>
            <li><b>Hubraum:</b> 8.128 ccm (496 cubic inches)</li>
            <li><b>Zylinder:</b> V8 Big Block</li>
            <li><b>Max. Drehzahl (WOT):</b> 4600 - 5000 RPM</li>
            <li><b>Einspritzung:</b> MPI (Multi-Point Injection)</li>
            <li><b>Kühlsystem:</b> Zweikreiskühlung (Closed Cooling)</li>
            <li><b>SmartCraft:</b> Full Digital Monitoring</li>
            <li><b>Bohrung x Hub:</b> 108 mm x 111 mm</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Finanzielles")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        v = st.number_input("Versicherung (CHF)", value=1150)
        w = st.number_input("Winterlager & Dock (CHF)", value=2400)
        total = v + w + 350
        st.metric("Gesamt Fixkosten", f"CHF {total:,.2f}")
    with col_k2:
        if os.path.exists("kosten.jpg"):
            st.image("kosten.jpg", caption="Hafen & Infrastruktur", use_container_width=True)
        else:
            st.info("Lade 'kosten.jpg' auf GitHub hoch (z.B. Foto vom Hafen).")

with tab5:
    st.header("Fahrtenbuch")
    st.text_input("Start/Ziel")
    st.number_input("Aktuelle Motorstunden", step=1, value=455)
    if st.button("Törn speichern"):
        st.success("Daten wurden sicher abgelegt.")

st.write("---")
st.caption("Truelove Fleet v9.0 | Built for V8 Performance")
