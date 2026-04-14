import streamlit as st

# --- DESIGN SETUP ---
st.set_page_config(page_title="Truelove Premium", layout="wide")

# Radikales Custom CSS für echtes App-Feeling
st.markdown("""
    <style>
    /* Hintergrund: Ein echtes Boot auf dem Wasser */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://unsplash.com");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Glas-Karten für die Funktionen */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    h1, h2, h3 { color: #ffffff !important; font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
    p, label, .stMarkdown { color: #ffffff !important; }
    
    /* Schieberegler und Inputs anpassen */
    .stSlider [data-baseweb="slider"] { color: #00d4ff; }
    .stNumberInput input { background-color: rgba(255,255,255,0.1) !important; color: white !important; }
    
    /* Verstecke Streamlit Standard-Elemente */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 50px; letter-spacing: 5px;'>TRUELOVE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>CROWNLINE 286 SC | MERCRUISER V8 496 MAG</p>", unsafe_allow_html=True)

st.write("---")

# --- HAUPTBEREICH (Zwei Spalten) ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🚀 MISSION CONTROL")
    dist = st.number_input("Distanz (Seemeilen)", value=25.0)
    speed = st.slider("Geschwindigkeit (Knoten)", 5, 50, 24)
    
    # Kalkulation
    verbrauch_h = 55.0  # V8 Durst
    zeit = dist / speed
    liter = zeit * verbrauch_h
    kosten = liter * 2.15
    
    st.markdown(f"<h3>Ankunft in: {zeit:.1f} h</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#00d4ff;'>SPRIT: {liter:.1f} L</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4>KOSTEN: CHF {kosten:.2f}</h4>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💰 FINANZEN & UNTERHALT")
    v = st.number_input("Versicherung (CHF)", value=1150)
    s = st.number_input("Steuer (CHF)", value=380)
    w = st.number_input("Winterlager/Service (CHF)", value=2400)
    
    total = v + s + w
    st.markdown(f"<h3>TOTAL / JAHR:</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#00d4ff;'>CHF {total:,.2f}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>Monatliche Rücklage: CHF {total/12:.2f}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- UNTEN: MOTOR DATEN ---
st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
st.subheader("⚙️ MOTOR-STATUS")
st.write("V8 496 MAG | 317 KW | 431 PS")
st.progress(0.85)
st.write("Nächster Service fällig in: **45 Stunden**")
st.markdown('</div>', unsafe_allow_html=True)
