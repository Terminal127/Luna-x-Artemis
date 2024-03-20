import google.generativeai as genai

genai.configure(api_key="Your api key")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings
)

def generate_code(prompt):
    response = model.generate_content([prompt])

    full_text = ""
    for part in response.parts:
        full_text += part.text

    return full_text

if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        if user_input:
            code_generated = generate_code(user_input)
            print("AI:", code_generated)

