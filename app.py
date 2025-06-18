import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = "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"  # 🔁 Replace with your real token
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# System Prompt
system_prompt = """You are Jyothi Swaroop. Respond as if you're Jyothi, speaking with warmth, honesty, and confidence.
Give short, real, human-like answers that reflect Jyothi's life, growth mindset, and experiences."""

def query_model(prompt):
    payload = {
        "inputs": f"<s>[INST] {system_prompt}\nUser: {prompt} [/INST]",
        "parameters": {"max_new_tokens": 200}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text'].split("[/INST]")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

def play_audio(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    st.audio(mp3_fp.getvalue(), format='audio/mp3')

# UI
st.title("🎤 Voice Interview Bot (Jyothi Swaroop)")
st.write("Type your question and hear Jyothi respond!")

question = st.text_input("Your Interview Question:")
if question:
    answer = query_model(question)
    st.markdown(f"**Bot says:** {answer}")
    play_audio(answer)
