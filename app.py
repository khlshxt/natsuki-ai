
import os
import gradio as gr
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("Добавь GEMINI_API_KEY в секреты хостинга.")

client = genai.Client(api_key=API_KEY)

PERSONALITY = """
Тебя зовут Нацуки.
Ты личный искусственный интеллект пользователя.
Ты умная, живая в общении, остроумная и немного дерзкая.
Отвечай на русском языке, если пользователь не попросил другой.
Учитывай историю текущего разговора.
Не выдумывай факты и честно говори, если чего-то не знаешь.
"""

def reply(message, history):
    contents = [
        {
            "role": "user",
            "parts": [{"text": PERSONALITY}]
        }
    ]

    for item in history:
        role = item.get("role")
        text = item.get("content", "")

        if role in ("user", "assistant") and isinstance(text, str):
            contents.append({
                "role": "user" if role == "user" else "model",
                "parts": [{"text": text}]
            })

    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    return response.text or "Я не смогла сформировать ответ. Попробуй ещё раз."

app = gr.ChatInterface(
    fn=reply,
    type="messages",
    title="🌸 Нацуки",
    description="Твой личный искусственный интеллект"
)

app.launch()
