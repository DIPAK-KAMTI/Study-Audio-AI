import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Config
st.set_page_config(page_title="PraxisPages Pro", page_icon="🎓", layout="wide")

# 2. Smooth Mouse Trail Effect (Custom JavaScript & CSS)
st.markdown("""
    <style>
        /* Modern Background */
        .main { background-color: #0e1117; color: white; }
        .stButton>button { border-radius: 25px; background: linear-gradient(45deg, #4A90E2, #9013FE); color: white; border: none; transition: 0.3s; }
        .stButton>button:hover { transform: scale(1.05); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        
        /* Particle Dots Style */
        .particle {
            position: fixed;
            top: 0; left: 0;
            width: 6px; height: 6px;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease-out;
        }
    </style>

    <script>
    const DOTS = 30; // Number of white dots
    const dots = [];
    const mouse = { x: 0, y: 0 };

    for (let i = 0; i < DOTS; i++) {
        const d = document.createElement('div');
        d.className = 'particle';
        document.body.appendChild(d);
        dots.push({ el: d, x: 0, y: 0 });
    }

    document.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    function animate() {
        let x = mouse.x;
        let y = mouse.y;

        dots.forEach((dot, index) => {
            const nextDot = dots[index + 1] || dots[0];
            dot.x = x;
            dot.y = y;
            dot.el.style.transform = `translate(${x}px, ${y}px)`;
            
            // This creates the "delay" / trail effect
            x += (nextDot.x - dot.x) * 0.3;
            y += (nextDot.y - dot.y) * 0.3;
        });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """, unsafe_allow_html=True)

st.title("🎓 PraxisPages: AI Study Narrator")
st.info("Experience professional human-like voices for your study notes.")

# --- Rest of your logic (Keep exactly as before) ---
with st.sidebar:
    st.header("⚙️ Audio Settings")
    voice_option = st.selectbox("Select Narrator Voice:", 
                                ["en-IN-NeerjaNeural (Indian English)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    voice_id = voice_option.split(" ")[0]
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"

col1, col2 = st.columns([1, 1])
text_to_process = ""

with col1:
    option = st.radio("Input Method:", ("Paste Study Notes", "Upload Lecture PDF"))
    if option == "Paste Study Notes":
        text_to_process = st.text_area("Enter your content:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file:
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            for page in reader.pages:
                text_to_process += page.extract_text()
            st.success("✅ PDF Loaded!")

with col2:
    st.subheader("🔊 Audio Preview")
    if st.button("Generate Human-Like Audio"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("Synthesizing..."):
                audio_content = asyncio.run(generate_audio())
                st.audio(audio_content, format="audio/mp3")
                st.download_button("📥 Download MP3", data=audio_content, file_name="StudyAudio.mp3")
