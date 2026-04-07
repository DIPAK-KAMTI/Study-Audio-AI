import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Setup
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# 2. Advanced CSS for a Clean, High-End AI Look
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #0f0c29, #24243e);
            color: white;
        }
        /* Custom Card for Main Input */
        .content-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        h1, h2, h3, p, label { color: #ffffff !important; }
        .stButton>button {
            border-radius: 50px;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: #000;
            font-weight: bold;
            border: none;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.markdown("---")

# 3. Sidebar
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
    st.write("📖 **Student Info**")
    st.write("Name: Dipak")
    st.write("Subject: Basic AI Tools (6BWUVAC01)")

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
            st.success("✅ PDF Analysis Complete")

with col2:
    st.markdown("### 🔊 Audio Synthesis")
    
    # NEW: Professional Message instead of the broken GIF
    st.info("💡 **AI Tip:** Choose the 'Neerja' voice for the best Indian English accent during walking.")
    
    # Animated Visualization (Using a reliable public Lottie/GIF)
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2I1YzVkODExNjc5YjQ4NDgyY2RhNmY4Yjg4Yzg4Yjg4Yjg4Yjg4YiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/3o7TKMGpxx1379uFCo/giphy.gif", width=250)
    
    if st.button("🚀 Generate AI Voice"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("AI Narrator is speaking..."):
                audio_content = asyncio.run(generate_audio())
                st.audio(audio_content, format="audio/mp3")
                st.download_button("📥 Save to Phone (MP3)", data=audio_content, file_name="PraxisPages_Audio.mp3")
        else:
            st.warning("⚠️ Please provide text or a PDF first.")
