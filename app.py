import streamlit as st
from gtts import gTTS
import os

# 1. UI Header - Making it look professional
st.set_page_config(page_title="PraxisPages AI", page_icon="🎧")
st.title("🎧 AI Study Notes to Speech")
st.markdown("### Build by Dipak | Student Code: [Your Code]")

# 2. Input Section
st.write("Paste your notes below to convert them into a human-like voice.")
user_input = st.text_area("Enter Study Notes:", placeholder="Type or paste here...", height=200)

# 3. Speed Control (An 'AI Feature')
speed = st.select_slider("Select Speaking Speed", options=['Slow', 'Normal', 'Fast'], value='Normal')
is_slow = True if speed == 'Slow' else False

# 4. The Conversion Logic
if st.button("Convert to Audio"):
    if user_input:
        with st.spinner("AI is synthesizing speech..."):
            # Using Google Text-to-Speech AI
            tts = gTTS(text=user_input, lang='en', slow=is_slow)
            tts.save("speech.mp3")
            
            # Displaying the Result
            st.success("Done! You can now listen or download.")
            audio_file = open("speech.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            
            # Download Button for 'Walking & Learning'
            st.download_button(
                label="Download MP3 for offline study",
                data=audio_bytes,
                file_name="study_notes.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Please enter some text first!")
