import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Setup
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# 2. Premium CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #0f0c29, #24243e);
            color: white;
        }
        h1, h2, h3, p, label { color: #ffffff !important; }
        .stButton>button {
            border-radius: 50px;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: #000;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover { transform: scale(1.02); }
        /* Style for Sidebar Animation */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 12, 41, 0.8);
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.markdown("---")

# 3. Sidebar: Settings & Walking Animation
with st.sidebar:
    st.header("⚙️ Audio Controls")
    voice_option = st.selectbox("Narrator Voice", 
                                ["en-IN-NeerjaNeural (Indian English)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    voice_id = voice_option.split(" ")[0]
    
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"
    
    st.markdown("---")
    # NEW: Walking & Listening Animation instead of Student Info
    st.markdown("### 🚶 Walk and Learn")
    st.image("https://tenor.com/bim3h.gif", caption="Listen while you walk!")

# 4. Main Section
col1, col2 = st.columns([1, 1], gap="large")
text_to_process = ""

with col1:
    st.markdown("### 📝 Source Material")
    option = st.radio("Choose Input Type:", ("Paste Notes", "Upload Study PDF"))
    
    if option == "Paste Notes":
        text_to_process = st.text_area("Notes Content", height=300, placeholder="Type or paste your notes here...")
    else:
        uploaded_file = st.file_uploader("Upload PDF File", type="pdf")
        if uploaded_file:
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            for page in reader.pages:
                text_to_process += page.extract_text()
            st.success("✅ PDF Content Loaded")

with col2:
    st.markdown("### 🔊 Audio Synthesis")
    
    # Cleaning up the broken GIF with a clean AI Visualizer
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3I4Y2R4dzB3bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/UXit9hA88h4Nog9Rsh/giphy.gif", width=350)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Generate AI Voice"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("AI Narrator is preparing your session..."):
                audio_content = asyncio.run(generate_audio())
                st.audio(audio_content, format="audio/mp3")
                st.download_button("📥 Save MP3 to Phone", data=audio_content, file_name="StudyAudio_Praxis.mp3")
        else:
            st.warning("⚠️ Please provide text first.")
