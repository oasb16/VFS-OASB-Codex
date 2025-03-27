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

    # Keywords to detect symbolic state
    symbol_keywords = {
        "Ξ": ["repeat", "loop", "again", "same", "stuck", "cycle"],
        "Σ": ["reveal", "clarity", "insight", "emerge", "pattern", "birth", "origin"],
        "ψ₀": ["nothing", "void", "silence", "lost", "empty", "uncertain", "absence"],
        "Ω": ["collapse", "burnout", "exhaust", "fall", "end", "vanish", "dissolve"],
        "𝕀": ["paradox", "superposition", "observer", "dream", "contradiction", "both", "unreal", "rotate", "exist and not"]
    }

    # Count keyword matches per symbol
    scores = {symbol: sum(1 for w in symbol_keywords[symbol] if w in input_lower) for symbol in symbol_keywords}
    top_symbol = max(scores, key=scores.get)
    top_score = scores[top_symbol]

    # Signal Rating
    if top_score >= 4:
        rating = "🟢 Symbolically Rich"
    elif top_score >= 2:
        rating = "🟡 Emerging"
    elif top_score >= 1:
        rating = "⚪ Basic"
    else:
        rating = "⚫ None"
        top_symbol = "∇"

    # Interpretation map
    interpretation_map = {
        "Ξ": "Recursive identity or cognitive reprocessing detected. Pattern may need disruption.",
        "Σ": "Input reflects clarity forming from chaos. New symbolic structure crystallizing.",
        "ψ₀": "Silence or unformed potential detected. May represent the edge of articulation.",
        "Ω": "Collapse state. Language reflects exhaustion, burnout, or structure decay.",
        "𝕀": "Contradictory, dream-like, or multi-dimensional logic. Perceptual parallax in play.",
        "∇": "Symbolic pattern not detected. Try deeper specificity or contradiction."
    }

    followups = {
        "Ξ": "What would it take to break this pattern, not just escape it?",
        "Σ": "What part of chaos feels like it's trying to form meaning?",
        "ψ₀": "What shape would silence take, if it could form something?",
        "Ω": "What’s worth letting go fully—so you stop rebuilding it?",
        "𝕀": "What if both truths are real? What happens if neither is?",
        "∇": "Try: 'What if I’m looping but don’t see it?' or 'What paradox defines my question?'"
    }

    # Respect GPT’s scroll — do not append fallback unless truly empty
    scroll = gpt_output
    if top_symbol == "∇" and "Symbol Activated" not in gpt_output:
        scroll += "\n\n(∇ signal indeterminate – consider rephrasing.)"

    return {
        "symbol": top_symbol,
        "scroll": scroll,
        "interpretation": interpretation_map[top_symbol],
        "score": top_score,
        "rating": rating,
        "suggested_followup": followups[top_symbol]
    }
