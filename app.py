import streamlit as st

# --- HIGH-END UI SETUP ---
st.set_page_config(page_title="Truelove Premium", layout="wide")

# CSS für das "App-Gefühl" (inspiriert von den Mockups oben)
st.markdown("""
    <style>
    /* Hintergrund: Dunkles Marine-Blau mit Verlauf */
    .stApp {
        background: linear-gradient(180deg, #041021 0%, #0b1e3b 100%);
        color: #ffffff;
    }
    
    /* Karten-Design (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons stylen */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff 0%, #005f73 100%);
        border: none;
        color: white;
        border-radius: 30px;
        padding: 10px 25px;
        font-weight: bold;
        width: 100%;
    }

    /* Tabs verstecken/stylen */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #888; font-size: 18px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00d4ff; border-bottom-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- APP STRUKTUR ---
st.image("https://crownline.com", width=180)
st.markdown("<h1 style='text-align: center; margin-top:-50px;'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00d4ff;'>CROWNLINE 286 SC | V8 496 MAG</p>", unsafe_allow_html=True)

# Top Status Bar (wie in einer echten App)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="metric-card"><div class="metric-value">220 L</div><div class="metric-label">Tankinhalt</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-value">42.8 kn</div><div class="metric-label">Top Speed</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-value">45 h</div><div class="metric-label">Bis Service</div></div>', unsafe_allow_html=True)

st.write("##")

# Hauptbereich
tabs = st.tabs(["Navigation", "Finanzen", "Checkliste"])

with tabs[0]:
    col_left, col_right = st.columns([2,1])
    with col_left:
        st.markdown("### Reise-Kalkulation")
        dist = st.slider("Distanz (nm)", 0, 100, 25)
        speed = st.slider("Speed (kn)", 5, 50, 24)
        
    with col_right:
        verbrauch = (dist / speed) * 55
        st.markdown(f"""
            <div class="metric-card" style="background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff;">
                <div class="metric-label">Vorauss. Verbrauch</div>
                <div class="metric-value" style="color: #ffffff;">{verbrauch:.1f} L</div>
                <div class="metric-label" style="margin-top:10px;">Kosten</div>
                <div class="metric-value" style="color: #ffffff;">CHF {verbrauch*2.10:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### Kostenübersicht (CHF)")
    k1, k2 = st.columns(2)
    with k1:
        v = st.number_input("Versicherung", value=1100)
        w = st.number_input("Winterlager", value=2200)
    with k2:
        total = v + w + 350
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total / Jahr</div><div class="metric-value">CHF {total}</div></div>', unsafe_allow_html=True)

with tabs[2]:
    st.checkbox("Motorraum-Check (V8)")
    st.checkbox("Batterie-Hauptschalter EIN")
    st.checkbox("Mercruiser App synchronisiert")
    if st.button("Törn im Logbuch speichern"):
        st.balloons()
