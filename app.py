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
            background: linear-gradient(-45deg, #0f0c29, #1a1a2e);
            color: white;
        }
        h1, h2, h3, p, label, .stMarkdown { color: #ffffff !important; }
        
        .stButton>button {
            border-radius: 50px;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: #000 !important;
            font-weight: bold;
            border: none;
            transition: 0.3s;
            padding: 0.5rem 2rem;
        }
        .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 15px #4facfe; }
        
        [data-testid="stSidebar"] {
            background-color: rgba(15, 12, 41, 0.9);
        }

        /* Glassmorphism for images */
        .img-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.markdown("---")

# 3. Sidebar: Settings
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
    st.markdown("### 🚶 Walk and Learn")
    
    # FIXED: High-reliability GIF for Sidebar
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHIwdWswYXBqbmx4bm5ndHVsZ3VnZnZ4bmh4eGZ5bmx4eGZ5bmx4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eKNCR7qhO797y/giphy.gif", 
             caption="Keep moving, keep learning.")

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
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text_to_process += content
                st.success("✅ PDF Content Loaded")
            except Exception:
                st.error("Error reading PDF.")

with col2:
    st.markdown("### 🔊 Audio Synthesis")
    
    # FIXED: Reliable Visualizer GIF for Main Section
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp6ZzR6ZzR6ZzR6ZzR6ZzR6ZzR6ZzR6ZzR6ZzR6ZzR6ZzRmJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/UXit9hA88h4Nog9Rsh/giphy.gif", 
             use_container_width=True)
    
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
                try:
                    audio_content = asyncio.run(generate_audio())
                    st.audio(audio_content, format="audio/mp3")
                    st.download_button("📥 Save MP3 to Phone", 
                                       data=audio_content, 
                                       file_name="PraxisPages_Audio.mp3",
                                       mime="audio/mp3")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please provide text first.")

st.markdown("---")
st.caption("PraxisPages | Developed by Dipak | Brainware University")
