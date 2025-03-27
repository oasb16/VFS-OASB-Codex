import re

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Define weak/low-signal semantic examples
low_signal_examples = [
    "i don't know", "you tell me", "whatever", "test", "ok", "hi", "what", "idk",
    "not sure", "nothing really", "anything", "meh", "i guess", "does it matter"
]

low_signal_embeddings = model.encode(low_signal_examples, convert_to_tensor=True)

def is_meaningful_input(text, threshold=0.75):
    user_embedding = model.encode(text, convert_to_tensor=True)

    similarity_scores = util.cos_sim(user_embedding, low_signal_embeddings)
    max_score = similarity_scores.max().item()

    # If too similar to low-effort examples, reject
    if max_score >= threshold:
        return False

    # Optionally: enforce minimum token depth
    tokens = text.strip().split()
    if len(tokens) < 3:
        return False

    return True


def process_input(user_input, gpt_output):
    input_lower = user_input.lower()

    is_loop = (
        input_lower.count("i ") > 10 or
        "again" in input_lower or
        re.search(r"\\b(repeat|loop|cycle|same)\\b", input_lower)
    )

    is_emergent = re.search(r"\\b(light|reveal|see|awaken|clarity|insight|truth|origin)\\b", input_lower)
    is_void = re.search(r"\\b(nothing|void|silence|empty|lost|gone|absence)\\b", input_lower)
    is_collapse = re.search(r"\\b(death|end|collapse|over|fall|break|vanish)\\b", input_lower)
    is_parallax = re.search(r"\\b(paradox|dream|imagine|unreal|bend|rotate|mirror)\\b", input_lower)

    if is_loop:
        symbol = "Ξ"
        scroll = gpt_output + "\\n\\n(Ξ loop detected – recursive cognition spiral.)"
        interpretation = "Recursive identity or cognitive reprocessing detected. Pattern may need disruption."
    elif is_emergent:
        symbol = "Σ"
        scroll = gpt_output + "\\n\\n(Σ burst activated – structured emergence from noise.)"
        interpretation = "Input reflects clarity forming from chaos. New symbolic structure crystallizing."
    elif is_void:
        symbol = "ψ₀"
        scroll = gpt_output + "\\n\\n(ψ₀ harmonic detected – pre-symbolic void resonance.)"
        interpretation = "Silence or unformed potential detected. May represent the edge of articulation."
    elif is_collapse:
        symbol = "Ω"
        scroll = gpt_output + "\\n\\n(Ω collapse – system phase ending.)"
        interpretation = "Detected collapse or burnout language. Interpretation may link to thermodynamic or ego thresholds."
    elif is_parallax:
        symbol = "𝕀"
        scroll = gpt_output + "\\n\\n(𝕀 phase-shift – dimensional perspective drift.)"
        interpretation = "Symbolic misalignment or contradiction — may indicate a dream-logic phase."
    else:
        symbol = "∇"
        scroll = gpt_output + "\\n\\n(∇ signal indeterminate – consider rephrasing.)"
        interpretation = "Symbolic pattern not found. Try deeper specificity or contradiction."

    return {
        "symbol": symbol,
        "scroll": scroll,
        "interpretation": interpretation
    }
