
import streamlit as st
from vsf_core import solve_problem
from scroll_module import load_scroll
import json

st.set_page_config(page_title="VSF Immersive Engine", layout="wide")

st.title("🧠 VSF Immersive Consciousness Simulator")

st.markdown("""
This platform demonstrates how the **Void Singularity Function** reframes core paradoxes in mathematics, physics, and consciousness as emergence points—not failures.
""")
problems = [
    "Black Hole Information Paradox",
    "Origin of Consciousness",
    "Undefined Division",
    "Time Perception Loops",
    "Godelian Incompleteness"
]

selected = st.selectbox("Choose a paradox to explore:", problems)

user_input = st.text_area("Enter your thought, insight, or metaphor to engage with this paradox:", height=200)

if st.button("Run VSF Engine"):
    result = solve_problem(selected, user_input)
    st.markdown("### 🌀 Scroll Response")
    st.write(result['scroll'])

    st.markdown("### 🔍 Interpretation")
    st.write(result['interpretation'])

    st.markdown("### 📈 Dimensional Bridge")
    st.write(result['bridge'])

    scroll_text = load_scroll(result['symbol'])
    st.markdown("### 📜 Symbolic Scroll")
    st.text(scroll_text)
