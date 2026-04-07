import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Professional Page Styling
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# Custom CSS for a "Premium" Look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4A90E2; color: white; }
    .stTextArea>div>div>textarea { border-radius: 15px; }
    .css-10trblm { color: #4A90E2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.info("Convert your PDFs and Notes into High-Quality Human Voices for on-the-go learning.")

# 2. Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Audio Settings")
    # Human Voice Selection (Microsoft Neural Voices)
    voice_option = st.selectbox("Select Narrator Voice:", 
                                ["en-IN-NeerjaNeural (Indian English)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    
    voice_id = voice_option.split(" ")[0]
    
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    # Convert slider value to edge-tts format (e.g., "+20%")
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"

# 3. Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    option = st.radio("Input Method:", ("Paste Study Notes", "Upload Lecture PDF"))
    text_to_process = ""

    if option == "Paste Study Notes":
        text_to_process = st.text_area("Enter your content:", placeholder="Paste your text here...", height=300)
    else:
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text_to_process += page.extract_text()
            st.success("PDF Loaded Successfully!")

with col2:
    st.subheader("🔊 Audio Preview")
    if st.button("Generate Human-Like Audio"):
        if text_to_process:
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            audio_content = asyncio.run(generate_audio())
            
            st.audio(audio_content, format="audio/mp3")
            st.download_button("📥 Download MP3 for WhatsApp", data=audio_content, file_name="StudyNotes_Pro.mp3")
        else:
            st.warning("Please enter text or upload a PDF first.")

# Updated File Uploader for Mobile Compatibility
uploaded_file = st.file_uploader("Tap to select a Study PDF", type="pdf", key="mobile_pdf_picker")

if uploaded_file is not None:
    try:
        # We use a memory buffer for mobile stability
        pdf_buffer = io.BytesIO(uploaded_file.read())
        reader = PyPDF2.PdfReader(pdf_buffer)
        for page in reader.pages:
            text_to_process += page.extract_text()
        st.success(f"✅ Loaded {len(reader.pages)} pages from your phone!")
    except Exception as e:
        st.error("Error reading PDF. Try a different file.")
