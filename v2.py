import streamlit as st
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import os

# Load model and tokenizer once
tokenizer = AutoTokenizer.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")

# Step 1: Speech Recognition
def recognize_speech_from_video(video_path):
    recognizer = sr.Recognizer()
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    video.close()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    os.remove(audio_path)
    return text

# Step 2: Language Translation
def translate_text(text, src_lang, tgt_lang):
    language_mapping = {
        "en": "en_XX",
        "fr": "fr_XX",
        "es": "es_XX",
        "de": "de_DE",
        "zh": "zh_CN",
        "ja": "ja_XX",
        "hi": "hi_IN",
        "ru": "ru_RU",
        "pt": "pt_XX",
        "it": "it_IT",
    }

    src_lang_token = language_mapping.get(src_lang)
    tgt_lang_token = language_mapping.get(tgt_lang)
    
    if not src_lang_token or not tgt_lang_token:
        st.error("Unsupported language")
        return None

    tokenizer.src_lang = src_lang_token
    tokenizer.tgt_lang = tgt_lang_token

    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang_token])
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

# Step 3: Speech Synthesis
def text_to_speech(text, lang):
    tts = gTTS(text, lang=lang)
    audio_path = "translated_audio.mp3"
    tts.save(audio_path)
    return audio_path

# Step 4: Video Editing
def replace_audio_in_video(video_path, new_audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)
    video = video.set_audio(new_audio)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')
    video.close()
    new_audio.close()

# Main Function
def translate_video_language(video_path, output_path, src_lang, tgt_lang):
    st.write("Recognizing speech...")
    text = recognize_speech_from_video(video_path)
    st.write(f"Recognized text: {text}")
    
    st.write("Translating text...")
    translated_text = translate_text(text, src_lang, tgt_lang)
    if translated_text is None:
        return
    st.write(f"Translated text: {translated_text}")
    
    st.write("Converting text to speech...")
    translated_audio_path = text_to_speech(translated_text, tgt_lang)
    
    st.write("Replacing audio in video...")
    replace_audio_in_video(video_path, translated_audio_path, output_path)
    os.remove(translated_audio_path)
    st.write(f"Output video saved to: {output_path}")

# Streamlit App
st.title("Video Language Translator")
st.write("Upload a video, and we'll translate its audio to a different language.")

uploaded_video = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

# Language options
languages = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
}

src_lang = st.selectbox("Source language", list(languages.keys()))
tgt_lang = st.selectbox("Target language", list(languages.keys()))

if st.button("Translate Video"):
    if uploaded_video is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_video.read())
        
        output_video_path = "translated_video.mp4"
        translate_video_language("temp_video.mp4", output_video_path, languages[src_lang], languages[tgt_lang])
        
        with open(output_video_path, "rb") as f:
            btn = st.download_button(
                label="Download Translated Video",
                data=f,
                file_name="translated_video.mp4",
                mime="video/mp4"
            )
        
        os.remove("temp_video.mp4")
        os.remove(output_video_path)
    else:
        st.write("Please upload a video file first.")
