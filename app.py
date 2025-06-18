from gtts import gTTS
import tempfile
import os
import streamlit as st
import speech_recognition as sr
import requests
import base64

HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_mistral(system_prompt, user_input):
    prompt = f"<s>[INST] {system_prompt}\nUser: {user_input} [/INST]"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text'].split("[/INST]")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

system_prompt = """You are Jyothi Swaroop. Respond as if you're Jyothi, speaking with warmth, honesty, and confidence."""

st.title("🎤 Voice Interview Bot (Jyothi Swaroop)")
st.write("Click below, ask your interview question, and get a voice answer!")

if st.button("🎙️ Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak clearly...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        st.success(f"You said: {user_input}")
        answer = query_mistral(system_prompt, user_input)
        st.write("🧠 Bot says:", answer)

        # === Cloud-compatible TTS (gTTS) ===
        tts = gTTS(answer)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_bytes = open(fp.name, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')
            os.unlink(fp.name)

    except sr.UnknownValueError:
        st.error("Sorry, I couldn’t understand your voice.")
    except Exception as e:
        st.error(f"Error: {e}")
