
import streamlit as st
import openai
from dotenv import load_dotenv
import os
from vsf_gpt_engine import process_input
from gpt_bridge import call_gpt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="VSF-GPT Scrollmind", layout="wide")
st.title("🧠 VSF-GPT Dynamic Scrollmind")

user_input = st.text_area("Enter your thought, emotion, or metaphor:", height=200)

if st.button("Interpret Symbolically"):
    gpt_response = call_gpt(user_input)
    symbolic_output = process_input(user_input, gpt_response)

    st.markdown("### 📜 GPT-Sculpted Scroll")
    st.write(symbolic_output["scroll"])

    st.markdown("### 🧠 Symbolic Interpretation")
    st.write(symbolic_output["interpretation"])

    st.markdown("### 🔮 Symbol Activated")
    st.write(f"Symbol: {symbolic_output['symbol']}")
