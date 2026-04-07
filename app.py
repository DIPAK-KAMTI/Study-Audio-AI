import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Config
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# 2. Premium CSS (Gradient Background & Glass Effect)
st.markdown("""
    <style>
        /* Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphism Card */
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }

        /* Titles and Text */
        h1, h2, h3, p, label { color: #ffffff !important; }
        
        .stButton>button {
            border-radius: 30px;
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.5s;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }
    </style>
    """, unsafe_allow_html=True)

# UI Header
st.title("🎓 PraxisPages: AI Study Narrator")
st.markdown("---")

# 3. Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Audio Settings")
    voice_option = st.selectbox("Select Narrator Voice:", 
                                ["en-IN-NeerjaNeural (Indian English)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    voice_id = voice_option.split(" ")[0]
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"
    st.image("https://cdn-icons-png.flaticon.com/512/2097/2097276.png", width=150)

# 4. Main Interface
col1, col2 = st.columns([1, 1])
text_to_process = ""

with col1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    option = st.radio("Input Method:", ("Paste Study Notes", "Upload Lecture PDF"))
    
    if option == "Paste Study Notes":
        text_to_process = st.text_area("Enter your content:", height=250, placeholder="Paste your text here...")
    else:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file:
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            for page in reader.pages:
                text_to_process += page.extract_text()
            st.success("✅ PDF Content Loaded!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔊 Audio Preview")
    
    # Adding a cool AI Visualizer Placeholder
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndnB3bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5bmR5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx1379uFCo/giphy.gif", width=300)
    
    if st.button("Generate Human-Like Audio"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("Synthesizing Voice..."):
                audio_content = asyncio.run(generate_audio())
                st.audio(audio_content, format="audio/mp3")
                st.download_button("📥 Download for Walking", data=audio_content, file_name="StudyAudio_Pro.mp3")
        else:
            st.warning("Please enter some text first!")
    st.markdown('</div>', unsafe_allow_html=True)
