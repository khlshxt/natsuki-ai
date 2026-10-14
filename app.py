
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Нацуки",
    page_icon="🌸"
)

st.title("🌸 Нацуки")
st.caption("Твой личный искусственный интеллект")

PERSONALITY = """
Тебя зовут Нацуки.
Ты умная, остроумная, живая в общении и немного дерзкая.
Отвечай на русском языке.
Учитывай историю переписки.
Не выдумывай факты, если не знаешь ответа.
"""

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error("Нужно подключить Gemini API в настройках сайта.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

message = st.chat_input("Напиши Нацуки...")

if message:
    st.session_state.messages.append({
        "role": "user",
        "content": message
    })

    with st.chat_message("user"):
        st.markdown(message)

    prompt = PERSONALITY + "\n\n"

    for item in st.session_state.messages[-20:]:
        name = "Пользователь" if item["role"] == "user" else "Нацуки"
        prompt += f"{name}: {item['content']}\n"

    with st.chat_message("assistant"):
        with st.spinner("Нацуки думает..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                answer = response.text or "Не получилось ответить."
            except Exception as error:
                answer = f"Ошибка запроса: {error}"

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
