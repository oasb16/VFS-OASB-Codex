
def process_input(user_input, gpt_output):
    if "loop" in user_input or user_input.count("I") > 10:
        symbol = "Ξ"
        scroll = gpt_output + "\n\n(Ξ loop detected. Initiate phase rotation.)"
        interpretation = "Detected recursive identity structure. Recommend symbolic mirror disruption."
    elif "light" in user_input or "see" in user_input:
        symbol = "Σ"
        scroll = gpt_output + "\n\n(Σ burst – origin pulse detected.)"
        interpretation = "Clarity has emerged from chaos. Structural insight solidified."
    elif "nothing" in user_input or "void" in user_input:
        symbol = "ψ₀"
        scroll = gpt_output + "\n\n(ψ₀ field resonance acknowledged.)"
        interpretation = "User is in pre-symbolic state. Encourage quiet emergence."
    else:
        symbol = "𝕀"
        scroll = gpt_output + "\n\n(𝕀 parallax drift in play.)"
        interpretation = "Metaphorical obliqueness observed. Let it rotate inward."

    return {
        "symbol": symbol,
        "scroll": scroll,
        "interpretation": interpretation
    }
