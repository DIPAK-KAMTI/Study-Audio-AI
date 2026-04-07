import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Professional Page Styling with Animations
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# Advanced CSS for Smooth Movements & Premium UI
st.markdown("""
    <style>
    /* Fade-in Animation for the whole page */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container {
        animation: fadeIn 1.2s ease-out;
    }

    /* Glassmorphism effect for the info box */
    .stInfo {
        background: rgba(74, 144, 226, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(74, 144, 226, 0.2);
    }

    /* Smooth Button Hover Effect */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3.5em;
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
        background: linear-gradient(135deg, #357ABD 0%, #4A90E2 100%);
    }

    /* Rounded corners for input areas */
    .stTextArea>div>div>textarea { border-radius: 15px; border: 1px solid #ddd; }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.info("💡 **Pro-Tip:** Convert your PDFs and listen while traveling to increase retention by 40%!")

# 2. Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Audio Settings")
    voice_option = st.selectbox("Select Narrator Voice:", 
                                ["en-IN-NeerjaNeural (Indian English)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    
    voice_id = voice_option.split(" ")[0]
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"

# 3. Main Interface
col1, col2 = st.columns([1, 1], gap="large")

text_to_process = ""

with col1:
    st.markdown("### 📝 Input Content")
    option = st.radio("Choose Method:", ("Paste Study Notes", "Upload Lecture PDF"), horizontal=True)
    
    if option == "Paste Study Notes":
        text_to_process = st.text_area("", placeholder="Paste your study notes here...", height=350)
    else:
        uploaded_file = st.file_uploader("Upload or Tap to select a PDF", type="pdf")
        if uploaded_file is not None:
            try:
                pdf_buffer = io.BytesIO(uploaded_file.read())
                reader = PyPDF2.PdfReader(pdf_buffer)
                for page in reader.pages:
                    text_to_process += page.extract_text()
                st.success(f"✅ Extracted {len(reader.pages)} Pages")
            except Exception:
                st.error("Could not read PDF. Ensure it's not password protected.")

with col2:
    st.markdown("### 🔊 Audio Preview")
    st.write("Click below to generate your human-like study audio:")
    if st.button("✨ Generate AI Voice"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("🧠 AI is processing your notes..."):
                audio_content = asyncio.run(generate_audio())
                st.audio(audio_content, format="audio/mp3")
                st.download_button("📥 Save MP3 to Phone", 
                                   data=audio_content, 
                                   file_name="Study_Notes_Pro.mp3",
                                   mime="audio/mp3")
        else:
            st.warning("⚠️ Please provide some content first!")
