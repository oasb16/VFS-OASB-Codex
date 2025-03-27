import re

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Examples of low-value inputs to compare against
low_signal_prompts = [
    "i don't know", "you tell me", "idk", "whatever", "help", "test", "meh", "ok", "nothing", "nah"
]

# Fetch OpenAI embeddings
def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Cosine similarity
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a**2 for a in vec1) ** 0.5
    norm2 = sum(b**2 for b in vec2) ** 0.5
    return dot / (norm1 * norm2)

# Master check
def is_meaningful_input(user_input, threshold=0.80):
    user_vec = get_embedding(user_input)

    for example in low_signal_prompts:
        example_vec = get_embedding(example)
        score = cosine_similarity(user_vec, example_vec)
        if score > threshold:
            return False

    # Extra check for word count
    return len(user_input.strip().split()) >= 3


def process_input(user_input, gpt_output):
    input_lower = user_input.lower()

    # Clean regex, meaningful keywords
    is_loop = (
        input_lower.count("i ") > 10 or
        "again" in input_lower or
        re.search(r"\b(repeat|loop|cycle|same)\b", input_lower)
    )

    is_emergent = re.search(r"\b(light|reveal|see|awaken|clarity|insight|truth|origin|emerge)\b", input_lower)
    is_void = re.search(r"\b(nothing|void|silence|empty|lost|gone|absence)\b", input_lower)
    is_collapse = re.search(r"\b(death|end|collapse|over|fall|break|burnout|vanish|dissolve)\b", input_lower)
    is_parallax = re.search(r"\b(paradox|dream|contradiction|imagine|unreal|superposition|exist and not|mirror|observer|rotate|bend)\b", input_lower)

    symbol = None
    if is_loop:
        symbol = "Ξ"
    elif is_emergent:
        symbol = "Σ"
    elif is_void:
        symbol = "ψ₀"
    elif is_collapse:
        symbol = "Ω"
    elif is_parallax:
        symbol = "𝕀"

    if symbol:
        interpretation_map = {
            "Ξ": "Recursive identity or cognitive reprocessing detected. Pattern may need disruption.",
            "Σ": "Input reflects clarity forming from chaos. New symbolic structure crystallizing.",
            "ψ₀": "Silence or unformed potential detected. May represent the edge of articulation.",
            "Ω": "Detected collapse or burnout language. Interpretation may link to thermodynamic or ego thresholds.",
            "𝕀": "Symbolic misalignment or contradiction — may indicate a dream-logic phase."
        }
        interpretation = interpretation_map[symbol]
        scroll = gpt_output  # do not append noise — GPT already explained this
    else:
        symbol = "∇"
        scroll = gpt_output + "\n\n(∇ signal indeterminate – consider rephrasing.)"
        interpretation = "Symbolic pattern not found. Try deeper specificity or contradiction."

    return {
        "symbol": symbol,
        "scroll": scroll,
        "interpretation": interpretation
    }
