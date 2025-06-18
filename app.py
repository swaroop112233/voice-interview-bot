import streamlit as st
import speech_recognition as sr
import requests
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import tempfile

# === YOUR HUGGING FACE TOKEN ===
HF_TOKEN = "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"  # Replace with your actual Hugging Face token

# === SYSTEM PROMPT ===
system_prompt = """You are Jyothi Swaroop. Respond as if you're Jyothi, speaking with warmth, honesty, and confidence.
Give short, real, human-like answers that reflect Jyothi's life, growth mindset, and experiences."""

# === HUGGING FACE INFERENCE API DETAILS ===
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


def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        sound = AudioSegment.from_mp3(fp.name)
        play(sound)
        os.remove(fp.name)


# === STREAMLIT UI ===
st.title("🎤 Voice Interview Bot (Jyothi Swaroop)")
st.write("Click below, ask your interview question, and get a voice answer!")

if st.button("🎙️ Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak your question clearly...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        st.success(f"You said: {user_input}")

        # Query the model
        answer = query_mistral(system_prompt, user_input)
        st.write("🧠 Bot says:", answer)

        # Speak the answer
        speak(answer)

    except sr.UnknownValueError:
        st.error("Sorry, I couldn’t understand your voice.")
    except Exception as e:
        st.error(f"Error: {e}")
