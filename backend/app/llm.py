import os
import requests

API_KEY = os.getenv("GROQ_API_KEY", "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")
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def get_ai_response(user_message: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that asks clarifying questions when needed."},
            {"role": "user", "content": user_message}
        ]
    }
    res = requests.post(ENDPOINT, json=payload, headers=headers)
    if res.status_code != 200:
        return "Sorry, something went wrong with the AI layer."
    data = res.json()
    return data["choices"][0]["message"]["content"]
