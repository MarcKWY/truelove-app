import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Truelove Master", layout="centered", page_icon="⚓")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2MXh0XJXUp_f5shaxFXC-MfNvOw43pTcjgkKF3bKzQiztWjViKpRHq26cUjgjFUqtxQ/exec"

# -----------------------
# LOAD DATA (NO CACHE HERE FOR FIXKOSTEN!)
# -----------------------
def load(sheet):
    try:
        return requests.get(f"{SCRIPT_URL}?sheet={sheet}", timeout=10).json()
    except:
        return []

def load_fixkosten():
    data = load("fixkosten")

    # 🔥 wichtig: Header + Safety
    for row in data:
        if isinstance(row, list) and len(row) >= 4:
            try:
                vals = [float(x) for x in row[:4]]
                if all(v >= 0 for v in vals):
                    return vals
            except:
                continue

    return [2200.0, 350.0, 1150.0, 1500.0]


# -----------------------
# SESSION STATE (WICHTIG: KEIN FIXIERTER INITIAL BLOCK MEHR!)
# -----------------------
st.session_state.fix_vals = load_fixkosten()

# -----------------------
# SYNC
# -----------------------
def fast_sync(payload):
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=5)
    except:
        pass


# -----------------------
# UI
# -----------------------
st.title("TRUELOVE ⚓")

tab1, tab2, tab3 = st.tabs(["Übersicht", "Fixkosten", "Debug"])

# -----------------------
# FIXKOSTEN
# -----------------------
with tab2:
    v = st.session_state.fix_vals

    n1 = st.number_input("Überwintern", value=v[0])
    n2 = st.number_input("Steuern", value=v[1])
    n3 = st.number_input("Versicherung", value=v[2])
    n4 = st.number_input("Bootsplatz", value=v[3])

    if st.button("Speichern"):
        new_vals = [n1, n2, n3, n4]

        st.session_state.fix_vals = new_vals

        fast_sync({
            "sheet": "fixkosten",
            "method": "update",
            "values": new_vals
        })

    st.write("TOTAL:", sum(v))


# -----------------------
# DEBUG (WICHTIG!)
# -----------------------
with tab3:
    st.write("RAW DATA:")
    st.write(load("fixkosten"))

    st.write("PARSED FIXKOSTEN:")
    st.write(st.session_state.fix_vals)
