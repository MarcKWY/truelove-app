import streamlit as st
import os
import pandas as pd
from datetime import datetime

# --- MASTER SETUP ---
st.set_page_config(page_title="Truelove Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1A1C1E; }
    div[data-testid="stMetric"] { background-color: #F0F7FF !important; border: 1px solid #005A9C !important; border-radius: 10px; }
    .spec-card { background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; }
    .total-box { background-color: #005A9C; color: white; padding: 15px; border-radius: 10px; text-align: center; }
    .zahler-box { background-color: #E1EFFE; padding: 10px; border-radius: 8px; border-left: 5px solid #005A9C; margin-bottom: 5px; color: #1A1C1E; }
    h1, h2, h3 { color: #005A9C !important; }
    </style>
    """, unsafe_allow_html=True)

# Daten-Speicher (Session)
if 'tank_daten' not in st.session_state: st.session_state.tank_daten = []
if 'zubehoer' not in st.session_state: st.session_state.zubehoer = []

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    for ext in ["png", "jpg", "jpeg"]:
        if os.path.exists(f"logo.{ext}"):
            st.image(f"logo.{ext}", width=100)
            break
with col_r:
    st.title("⚓ TRUELOVE Skipper Zentrale")
    st.write(f"Crownline 286 SC | **V8 496 MAG HO (317 kW)**")

# --- REITER-STRUKTUR ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛽ Tanken", "⚙️ Motor & Rechnungen", "🔧 Service & Zubehör", "💰 Kosten", "📖 Logbuch"])

# TAB 1: TANKEN
with tab1:
    st.subheader("⛽ Tank-Management")
    if os.path.exists("tanken.jpg"): 
        st.image("tanken.jpg", width=450)
    
    col_in, col_res = st.columns(2)
    with col_in:
        with st.container(border=True):
            t_datum = st.date_input("Datum", datetime.now(), key="tank_date")
            t_liter = st.number_input("Liter (L)", min_value=0.0, step=10.0, key="tank_lit")
            t_preis = st.number_input("CHF / L", value=2.15, key="tank_price")
            t_wer = st.radio("Zahler", ["Marc", "Fabienne"], horizontal=True, key="tank_who")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Speichern ✅", use_container_width=True):
                    if t_liter > 0:
                        st.session_state.tank_daten.append({
                            "Datum": t_datum.strftime("%d.%m.%Y"), 
                            "Liter": t_liter, 
                            "Total": round(t_liter * t_preis, 2), 
                            "Zahler": t_wer
                        })
                        st.rerun()
            with c_btn2:
                if st.button("Letzten löschen 🗑️", use_container_width=True):
                    if st.session_state.tank_daten:
                        st.session_state.tank_daten.pop()
                        st.rerun()
    with col_res:
        if st.session_state.tank_daten:
            df = pd.DataFrame(st.session_state.tank_daten)
            st.metric("Total Benzin Saison", f"CHF {df['Total'].sum():,.2f}")
            
            st.write("### 👥 Abrechnung")
            # Sicherer Check für die Summen
            ausgaben = df.groupby("Zahler")["Total"].sum()
            val_marc = ausgaben.get('Marc', 0.0)
            val_fabi = ausgaben.get('Fabienne', 0.0)
            
            c_m, c_f = st.columns(2)
            with c_m:
                st.markdown(f"<div class='zahler-box'><b>Marc:</b><br>CHF {val_marc:,.2f}</div>", unsafe_allow_html=True)
            with c_f:
                st.markdown(f"<div class='zahler-box'><b>Fabienne:</b><br>CHF {val_fabi:,.2f}</div>", unsafe_allow_html=True)
            
            st.write("### Details")
            st.table(df)

# TAB 2: MOTOR & RECHNUNGEN
with tab2:
    st.subheader("⚙️ Motor-Daten & Rechnungs-Upload")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div class="spec-card">
        <h3>Mercruiser 496 MAG HO</h3>
        <ul>
            <li><b>Leistung:</b> 317 kW / 431 PS</li>
            <li><b>Hubraum:</b> 8.2 Liter</li>
            <li><b>Kühlung:</b> Zweikreissystem</li>
            <li><b>WOT:</b> 4600 - 5000 RPM</li>
            <li><b>Ölkapazität:</b> 8.5 Liter</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists("motor.jpg"): st.image("motor.jpg", use_container_width=True)
    with col_m2:
        st.write("### 📂 Service-Rechnungen")
        uploaded_file = st.file_uploader("Rechnung/Foto hochladen", type=['jpg', 'jpeg', 'png'], key="file_up")
        if uploaded_file: st.image(uploaded_file, caption="Aktuelle Rechnung", use_container_width=True)

# TAB 3: SERVICE & ZUBEHÖR
with tab3:
    st.subheader("🔧 Service & Zubehör")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("### Service-Eintrag")
        s_text = st.text_area("Arbeiten", key="serv_text")
        if st.button("Service speichern"): st.success("Eintrag gemerkt")
    with col_s2:
        st.write("### Zubehör")
        zub_n = st.text_input("Teil", key="zub_name")
        zub_p = st.number_input("Preis CHF", min_value=0.0, key="zub_price")
        if st.button("Zubehör speichern"):
            st.session_state.zubehoer.append({"Teil": zub_n, "Preis": zub_p})
            st.rerun()

# TAB 4: KOSTEN
with tab4:
    st.subheader("💰 Kostenübersicht")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.image("https://wikimedia.org", width=50)
        k_axa = st.number_input("AXA Versicherung", value=1150.0, key="axa_val")
        k_platz = st.number_input("Bootsplatz & Winter", value=3700.0, key="platz_val")
        k_steuer = st.number_input("Steuer", value=350.0, key="tax_val")
    with col_k2:
        sprit_sum = sum(i['Total'] for i in st.session_state.tank_daten)
        zub_sum = sum(i['Preis'] for i in st.session_state.zubehoer)
        fix = k_axa + k_platz + k_steuer
        st.metric("Fixkosten", f"CHF {fix:,.2f}")
        st.markdown(f"<div class='total-box'><h3>GESAMTKOSTEN SAISON</h3><h1>CHF {fix + sprit_sum + zub_sum:,.2f}</h1></div>", unsafe_allow_html=True)

# TAB 5: LOGBUCH
with tab5:
    st.header("📖 Fahrtenbuch")
    if os.path.exists("boot_gross.jpg"): st.image("boot_gross.jpg", width=400)
    st.text_input("Törn-Ziel", key="log_dest")

st.write("---")
st.caption("Truelove Fleet v19.1 | Fixed Build")
