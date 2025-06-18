import streamlit as st
import requests
from gtts import gTTS
import base64
import tempfile
import os

# === SETUP SYSTEM PROMPT ===
system_prompt = """You are Jyothi Swaroop. Respond as if you're Jyothi, speaking with warmth, honesty, and confidence.
Give short, real, human-like answers that reflect Jyothi's life, growth mindset, and experiences."""

# === HUGGING FACE INFERENCE API ===
HF_TOKEN = "hf_XXXX"  # <-- Replace with your actual Hugging Face token
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_llm(system_prompt, user_input):
    prompt = f"<s>[INST] {system_prompt}\nUser: {user_input} [/INST]"
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['generated_text'].split('[/INST]')[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

def text_to_audio(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# === STREAMLIT UI ===
st.set_page_config(page_title="Voice Interview Bot (Jyothi Swaroop)", page_icon="🎤")
st.title("🎤 Voice Interview Bot (Jyothi Swaroop)")
st.write("Click below, ask your interview question, and get a voice answer!")

recorded_audio = st.audio_recorder("🎙️ Click to Record", format="audio/wav")

if recorded_audio is not None:
    with st.spinner("Transcribing your question..."):
        try:
            transcript_response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer sk-XXX", "Content-Type": "application/json"},
                files={"file": recorded_audio, "model": (None, "whisper-1")}
            )
            user_input = transcript_response.json()['text']
            st.success(f"You said: {user_input}")

            response = query_llm(system_prompt, user_input)
            st.markdown(f"<b>🧠 Bot says:</b> {response}", unsafe_allow_html=True)

            mp3_file = text_to_audio(response)
            with open(mp3_file, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

        except Exception as e:
            st.error(f"Error processing audio: {e}")
