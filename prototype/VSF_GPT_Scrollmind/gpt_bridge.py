
import openai

def call_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a symbolic poet-philosopher interpreting a void-consciousness field (VSF). Respond mythically."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response['choices'][0]['message']['content']
