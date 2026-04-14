import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- SETUP: HELL & LESBAR ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; color: #1E293B; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 2px solid #005A9C !important;
        border-radius: 12px !important;
    }
    .spec-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .zahler-box {
        background-color: #E0F2FE;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0369A1;
        margin-top: 10px;
    }
    h1, h2, h3 { color: #005A9C !important; }
    b { color: #0369A1; }
    </style>
    """, unsafe_allow_html=True)

if 'tank_daten' not in st.session_state:
    st.session_state.tank_daten = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg", "PNG"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE | Skipper Zentrale")
    st.write(f"**Crownline 286 SC** | Mercruiser 496 MAG HO | Saison {datetime.now().year}")

# --- REITER ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "🔧 Wartung", "⚙️ Motor-Specs", "💰 Kosten", "📖 Logbuch"])

with tab1:
    st.subheader("⛽ Tank-Abrechnung")
    col_in, col_res = st.columns([1, 2])
    
    with col_in:
        with st.container(border=True):
            st.write("**Neuer Stopp**")
            t_datum = st.date_input("Datum", datetime.now())
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0)
            t_preis = st.number_input("CHF / L", value=2.15)
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True)
            if st.button("Speichern 📥", use_container_width=True):
                if t_liter > 0:
                    st.session_state.tank_daten.append({
                        "Datum": t_datum.strftime("%d.%m.%Y"),
                        "Liter": t_liter,
                        "Preis": t_preis,
                        "Total CHF": round(t_liter * t_preis, 2),
                        "Zahler": t_wer
                    })
                    st.rerun()
        
        if st.session_state.tank_daten:
            st.write("---")
            if st.button("🗑️ Letzten Eintrag löschen"):
                st.session_state.tank_daten.pop()
                st.rerun()

    with col_res:
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            
            # Gesamt-Metrics
            m1, m2 = st.columns(2)
            m1.metric("Gesamt Liter", f"{df['Liter'].sum():.1f} L")
            m2.metric("Gesamt Kosten", f"CHF {df['Total CHF'].sum():,.2f}")
            
            # NEU: Abrechnung Marc & Fabienne
            st.write("### 👥 Wer hat bezahlt?")
            ausgaben = df.groupby("Zahler")["Total CHF"].sum()
            
            c_marc, c_fab = st.columns(2)
            with c_marc:
                betrag_m = ausgaben.get("Marc", 0.0)
                st.markdown(f"<div class='zahler-box'><b>Marc:</b><br>CHF {betrag_m:,.2f}</div>", unsafe_allow_html=True)
            with c_fab:
                betrag_f = ausgaben.get("Fabienne", 0.0)
                st.markdown(f"<div class='zahler-box'><b>Fabienne:</b><br>CHF {betrag_f:,.2f}</div>", unsafe_allow_html=True)
            
            st.write("### Details")
            st.table(df)
        else:
            if os.path.exists("tanken.jpg"):
                st.image("tanken.jpg", use_container_width=True)

with tab2:
    st.subheader("🔧 Wartung")
    if os.path.exists("wartung.jpg"):
        st.image("wartung.jpg", width=600)
    st.info("Checkliste: Impeller, Getriebeöl, Anoden (Saison 2024)")

with tab3:
    st.subheader("⚙️ Motor-Spezifikationen")
    col_m_img, col_m_data = st.columns([1, 1])
    with col_m_img:
        if os.path.exists("motor.jpg"):
            st.image("motor.jpg", use_container_width=True)
    with col_m_data:
        st.markdown(f"""
        <div class="spec-card">
        <h3>Mercruiser 496 MAG HO</h3>
        <ul>
            <li><b>Leistung:</b> 317 kW / 431 PS</li>
            <li><b>Typ:</b> V8 Big Block (8.2 Liter)</li>
            <li><b>Kühlung:</b> Zweikreissystem (Closed)</li>
            <li><b>Drehzahl (WOT):</b> 4600 - 5000 RPM</li>
            <li><b>Einspritzung:</b> Multi-Point Injection (MPI)</li>
            <li><b>Hubraum:</b> 496 cubic inches</li>
            <li><b>Antrieb:</b> Kompatibel mit Bravo One/Two/Three</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("💰 Kosten")
    if os.path.exists("kosten.jpg"):
        st.image("kosten.jpg", width=500)
    v = st.number_input("Versicherung (CHF)", value=1150)
    w = st.number_input("Winterlager (CHF)", value=2400)
    st.metric("Total Fixkosten", f"CHF {v + w + 350:,.2f}")

with tab5:
    st.subheader("📖 Logbuch")
    st.text_input("Zielort")
    st.button("Törn speichern")

st.write("---")
st.caption("Truelove Fleet v14.0 | Marc & Fabienne Edition")
