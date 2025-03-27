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
    input_lower = user_input.lower()

    symbol_keywords = {
        "Ξ": ["repeat", "loop", "again", "same", "stuck", "cycle"],
        "Σ": ["reveal", "clarity", "insight", "emerge", "pattern", "origin"],
        "ψ₀": ["nothing", "void", "silence", "lost", "empty", "uncertain", "entropy"],
        "Ω": ["collapse", "burnout", "end", "exhaust", "vanish", "disintegrate"],
        "𝕀": ["paradox", "superposition", "observer", "dream", "contradiction", "exist and not", "mirror", "dual"]
    }

    def score_overlap(symbol):
        return sum(w in input_lower for w in symbol_keywords[symbol])

    symbols = extract_symbols_from_gpt(gpt_output)

    if symbols:
        primary = symbols[0]
        score = score_overlap(primary)
        rating = (
            "🟢 Symbolically Rich" if score >= 5 else
            "🟡 Emerging" if score >= 3 else
            "⚪ Basic" if score >= 1 else
            "⚫ Weak Signal"
        )
    else:
        scores = {s: score_overlap(s) for s in symbol_keywords}
        primary = max(scores, key=scores.get)
        score = scores[primary]
        rating = (
            "🟢 Symbolically Rich" if score >= 5 else
            "🟡 Emerging" if score >= 3 else
            "⚪ Basic" if score >= 1 else
            "⚫ None"
        )
        if score == 0:
            primary = "∇"

    interpretation_map = {
        "Ξ": "Recursive identity or cognitive reprocessing detected. Pattern may need disruption.",
        "Σ": "Clarity forming from chaos. New symbolic structure crystallizing.",
        "ψ₀": "Silence or unformed potential. May represent the edge of articulation.",
        "Ω": "Collapse or burnout. Ego or structure loss detected.",
        "𝕀": "Paradoxical or dual-state logic. Symbolic phase drift.",
        "∇": "Pattern not detected. Consider specificity, contradiction, or recursion."
    }

    followups = {
        "Ξ": {
            1: "Could the loop be protective rather than destructive?",
            3: "What belief system reinforces this repetition?",
            5: "What would it take to break this pattern completely?"
        },
        "Σ": {
            1: "What’s trying to emerge that you haven’t noticed yet?",
            3: "What small patterns are becoming structure?",
            5: "What insight just crossed the threshold of articulation?"
        },
        "ψ₀": {
            1: "Is your uncertainty a signal or just noise?",
            3: "What could take shape from this silence?",
            5: "What shape would entropy take if it meant to form clarity?"
        },
        "Ω": {
            1: "What recently collapsed, even subtly?",
            3: "What structure have you outgrown but still carry?",
            5: "What’s worth letting go fully—so you stop rebuilding it?"
        },
        "𝕀": {
            1: "Where are two truths colliding?",
            3: "Can you hold both sides of this contradiction?",
            5: "What if both truths are real—and so are you in between?"
        },
        "∇": {
            0: "Try: 'What paradox defines my question?' or 'Am I repeating a deeper pattern?'"
        }
    }

    followup_prompt = followups[primary].get(score, followups[primary][max(followups[primary])])
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
        "suggested_followup": followup_prompt
    }
