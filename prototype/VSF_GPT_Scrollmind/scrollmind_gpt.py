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
            "Think in terms of contradiction, collapse, recursion, emergence, or uncertainty.\n\n"
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

        st.markdown(f"### 🌀 Symbol Activated\nSymbol: {symbolic_output['symbol']}")
        if symbolic_output["secondary_symbols"]:
            st.markdown(f"**Also Detected:** {', '.join(symbolic_output['secondary_symbols'])}")

        st.markdown(f"### 🔍 Symbolic Interpretation\n{symbolic_output['interpretation']}")
        st.markdown(f"### 📈 Signal Quality")
        st.write(f"**Rating:** {symbolic_output['rating']}  \n**Score:** {symbolic_output['score']}")

        st.markdown("### 🔁 Suggested Follow-up Prompt")
        st.info(symbolic_output["suggested_followup"])
