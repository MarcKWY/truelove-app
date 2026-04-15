import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Truelove Master", layout="centered")
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhDxQNTjyCGLLR5hZwUo_7tQ5wEohouVXHrbn-FJzDKUPJ8c0MmbzfwfiOxUYDyRwE/exec"

st.markdown("""
    <style>
    .stApp { background-color: #050A14; color: #FFFFFF; }
    .truelove-title { font-family: 'Georgia', serif; font-size: 45px; font-weight: bold; color: #D4AF37; text-align: center; letter-spacing: 5px; }
    .card { background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; }
    .stButton>button { background-color: #8B6914 !important; color: white !important; border: 1px solid #D4AF37 !important; width: 100%; }
    h3 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TURBO-LADEN ---
def get_clean_df(sheet):
    try:
        r = requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=5)
        data = r.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            # DATUM FIX
            if 'Datum' in df.columns:
                df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.strftime('%d.%m.%Y')
            # ZAHLEN FIX (2 Stellen)
            for col in ['Liter', 'CHF/L', 'Total CHF', 'CHF']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').map('{:,.2f}'.format)
            return df
        return pd.DataFrame()
    except: return pd.DataFrame()

def post_data(row, sheet, method="append"):
    payload = {"sheet": sheet, "method": method, "values": row}
    requests.post(SCRIPT_URL, json=payload, timeout=5)

# --- UI ---
st.markdown("<div class='truelove-title'>TRUELOVE</div>", unsafe_allow_html=True)
menu = st.radio("MENU", ["⛽ Tanken", "⚙️ Service", "💰 Finanzen"], horizontal=True, label_visibility="collapsed")

if menu == "⛽ Tanken":
    st.markdown("<div class='card'><h3>⛽ Tanken</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lit = c1.number_input("Liter", step=0.01, format="%.2f")
    pr = c2.number_input("CHF/L", value=2.15, format="%.2f")
    wer = st.radio("Wer?", ["Marc", "Fabienne"], horizontal=True)
    
    if st.button("Speichern ✅"):
        post_data([datetime.now().strftime("%d.%m.%Y"), lit, pr, round(lit*pr, 2), wer], "tanken")
        st.cache_data.clear()
        st.rerun()

    df = get_clean_df("tanken")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        if st.button("Löschen 🗑️"):
            new_df = df.drop(df.index[-1])
            post_data([new_df.columns.tolist()] + new_df.values.tolist(), "tanken", "overwrite")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "⚙️ Service":
    st.markdown("<div class='card'><h3>⚙️ Service</h3>", unsafe_allow_html=True)
    arb = st.text_input("Arbeit")
    kost = st.number_input("Kosten", step=0.05)
    if st.button("Service speichern"):
        post_data([datetime.now().strftime("%d.%m.%Y"), arb, kost], "service")
        st.rerun()
    df_s = get_clean_df("service")
    if not df_s.empty:
        st.dataframe(df_s, use_container_width=True, hide_index=True)

elif menu == "💰 Finanzen":
    st.markdown("<div class='card'><h3>💰 Finanzen</h3>", unsafe_allow_html=True)
    df_t = get_clean_df("tanken")
    # Hier werden die bereinigten Strings wieder in Zahlen für die Summe umgewandelt
    sprit = df_t['Total CHF'].str.replace(',', '').astype(float).sum() if not df_t.empty else 0
    st.metric("Total Benzin", f"CHF {sprit:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
