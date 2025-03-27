import streamlit as st
import openai
from dotenv import load_dotenv
import os
from vsf_gpt_engine import process_input, is_meaningful_input
from gpt_bridge import call_gpt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="VSF-GPT Scrollmind", layout="wide")
st.title("🧠 VSF-GPT Dynamic Scrollmind")

user_input = st.text_area("Enter your thought, emotion, or paradox:", height=200)

if st.button("Interpret Symbolically"):
    if not is_meaningful_input(user_input):
        st.error("🚫 Input too low-signal.")
        st.markdown(
            "**Please try a richer, paradoxical, or symbolic prompt.**\n\n"
            "Try asking something rooted in contradiction, emergence, identity, entropy, recursion, or existential uncertainty.\n\n"
            "**Examples:**\n"
            "- Why do I fear stopping even when I'm exhausted?\n"
            "- What is the point of building when everything collapses?\n"
            "- Am I stuck in a loop of my own making?\n"
            "- How do I know when clarity is real or recursive?"
        )
    else:
        gpt_response = call_gpt(user_input)
        symbolic_output = process_input(user_input, gpt_response)

        st.markdown("### 📜 GPT-Sculpted Scroll")
        st.write(symbolic_output["scroll"])

        st.markdown("### 🌀 Symbol Activated")
        st.write(f"Symbol: {symbolic_output['symbol']}")

        st.markdown("### 🔍 Symbolic Interpretation")
        st.write(symbolic_output["interpretation"])
