import re
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def is_meaningful_input(text):
    stripped = text.strip().lower()
    if len(stripped) < 10 or stripped in {"asd", "test", "ok", "hello", "hi", "hmm", "..."}:
        return False
    if not any(char.isalpha() for char in stripped):
        return False

    tokens = word_tokenize(stripped)
    tags = pos_tag(tokens)

    # Check if there's at least 2 content-carrying POS tokens
    content_tags = {"NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "JJ", "RB"}
    content_words = [word for word, tag in tags if tag in content_tags]

    return len(content_words) >= 2


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
