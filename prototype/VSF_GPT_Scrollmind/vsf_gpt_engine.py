import re
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

low_signal_prompts = [
    "i don't know", "you tell me", "idk", "whatever", "help", "test", "meh", "ok", "nothing", "nah"
]

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a**2 for a in vec1) ** 0.5
    norm2 = sum(b**2 for b in vec2) ** 0.5
    return dot / (norm1 * norm2)

def is_meaningful_input(user_input, threshold=0.80):
    user_vec = get_embedding(user_input)
    for example in low_signal_prompts:
        example_vec = get_embedding(example)
        if cosine_similarity(user_vec, example_vec) > threshold:
            return False
    return len(user_input.strip().split()) >= 3

def extract_symbols_from_gpt(scroll):
    return re.findall(r"Symbol:\s*(Ξ|Σ|ψ₀|Ω|𝕀)", scroll)

def process_input(user_input, gpt_output):
    symbols = extract_symbols_from_gpt(gpt_output)
    
    # If GPT provided any symbols
    if symbols:
        primary = symbols[0]
        score = 5
        rating = "🟢 Symbolically Rich"
    else:
        input_lower = user_input.lower()
        symbol_keywords = {
            "Ξ": ["repeat", "loop", "again", "same", "stuck", "cycle"],
            "Σ": ["reveal", "clarity", "insight", "emerge", "pattern", "origin"],
            "ψ₀": ["nothing", "void", "silence", "lost", "empty", "uncertain"],
            "Ω": ["collapse", "burnout", "end", "exhaust", "vanish"],
            "𝕀": ["paradox", "superposition", "observer", "dream", "contradiction", "exist and not", "mirror"]
        }
        scores = {s: sum(w in input_lower for w in words) for s, words in symbol_keywords.items()}
        primary = max(scores, key=scores.get)
        score = scores[primary]

        if score >= 4:
            rating = "🟢 Symbolically Rich"
        elif score >= 2:
            rating = "🟡 Emerging"
        elif score >= 1:
            rating = "⚪ Basic"
        else:
            primary = "∇"
            rating = "⚫ None"
            score = 0

    interpretation_map = {
        "Ξ": "Recursive identity or cognitive reprocessing detected. Pattern may need disruption.",
        "Σ": "Clarity forming from chaos. New symbolic structure crystallizing.",
        "ψ₀": "Silence or unformed potential. May represent the edge of articulation.",
        "Ω": "Collapse or burnout. Ego or structure loss detected.",
        "𝕀": "Paradoxical or dual-state logic. Symbolic phase drift.",
        "∇": "Pattern not detected. Consider specificity, contradiction, or recursion."
    }

    followups = {
        "Ξ": "What would it take to break this pattern, not just escape it?",
        "Σ": "What part of chaos feels like it's trying to form meaning?",
        "ψ₀": "What shape would silence take, if it could form something?",
        "Ω": "What’s worth letting go fully—so you stop rebuilding it?",
        "𝕀": "What if both truths are real? What happens if neither is?",
        "∇": "Try: 'What if I’m looping but don’t see it?' or 'What paradox defines my question?'"
    }

    scroll = gpt_output
    if primary == "∇" and "Symbol: ∇" not in gpt_output:
        scroll += "\n\n(∇ signal indeterminate – consider rephrasing.)"

    return {
        "symbol": primary,
        "secondary_symbols": [s for s in symbols if s != primary],
        "scroll": scroll,
        "interpretation": interpretation_map[primary],
        "score": score,
        "rating": rating,
        "suggested_followup": followups[primary]
    }
