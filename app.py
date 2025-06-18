import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import threading

# === HUGGING FACE TOKEN ===
HF_TOKEN = "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"  # Replace with your token

# === STREAMLIT SETUP ===
st.set_page_config(page_title="Voice Interview Bot", layout="centered")
st.title("🎤 Voice Interview Bot (Jyothi Swaroop)")
st.write("Click below, ask your interview question, and get a voice answer!")

# === TTS SETUP ===
engine = pyttsx3.init()

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# === SYSTEM INSTRUCTION ===
system_prompt = """You are Jyothi Swaroop. Respond as if you're Jyothi, speaking with warmth, honesty, and confidence.
Give short, real, human-like answers that reflect Jyothi's life, growth mindset, and experiences."""

# === HUGGING FACE ZEHPYR MODEL ===
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_zephyr(system_prompt, user_input):
    prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_input}</s>\n<|assistant|>"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()[0]["generated_text"]
        return result.split("<|assistant|>")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# === RECORD & RESPOND ===
if st.button("🎙️ Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak your question clearly...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        st.success(f"You said: {user_input}")

        answer = query_zephyr(system_prompt, user_input)
        st.write("🧠 Bot says:", answer)
        speak(answer)

    except sr.UnknownValueError:
        st.error("Sorry, I couldn’t understand your voice.")
    except Exception as e:
        st.error(f"Error: {e}")
