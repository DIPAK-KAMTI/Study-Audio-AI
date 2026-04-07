import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Configuration
st.set_page_config(
    page_title="PraxisPages Pro", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Professional UI: CSS & Canvas Particle Engine
st.markdown("""
    <style>
    /* Midnight Premium Theme */
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #020617; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
    }

    /* Input Box Styling */
    .stTextArea>div>div>textarea, .stFileUploader, .stSelectbox>div {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Particle Canvas Overlay */
    #particle-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    </style>

    <canvas id="particle-canvas"></canvas>

    <script>
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let width, height;
    let mouse = { x: -500, y: -500 }; // Start off-screen
    const particles = [];
    const particleCount = 100;

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resize);
    resize();

    // Universal Mouse/Touch Tracker
    const updateMouse = (e) => {
        if (e.touches) {
            mouse.x = e.touches[0].clientX;
            mouse.y = e.touches[0].clientY;
        } else {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        }
    };
    window.addEventListener('mousemove', updateMouse);
    window.addEventListener('touchstart', updateMouse);
    window.addEventListener('touchmove', updateMouse);

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 1.5 + 0.5;
            // Easing/Delay factor: different for each dot
            this.ease = 0.04 + Math.random() * 0.12; 
        }

        update() {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            this.x += dx * this.ease;
            this.y += dy * this.ease;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.fill();
        }
    }

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """, unsafe_allow_html=True)

# 3. App Logic
st.title("🎓 PraxisPages Pro")
st.markdown("### AI-Powered Study Narrator")
st.write("Turn your PDFs into human-like audio for effortless learning.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Audio Engine")
    voice_option = st.selectbox("Narrator Voice:", 
                                ["en-IN-NeerjaNeural (Indian Female)", 
                                 "en-US-GuyNeural (Deep Male)", 
                                 "en-GB-SoniaNeural (Professional Female)"])
    
    voice_id = voice_option.split(" ")[0]
    speed_pct = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
    speed_str = f"{int((speed_pct - 1) * 100):+d}%"
    
    st.divider()
    st.info("Tip: Use Neerja for clear Indian English pronunciation.")

# Main Layout
col1, col2 = st.columns([1, 1], gap="large")
text_to_process = ""

with col1:
    st.subheader("📝 Source Material")
    option = st.radio("Input Method:", ("Paste Study Notes", "Upload Lecture PDF"))
    
    if option == "Paste Study Notes":
        text_to_process = st.text_area("Input:", placeholder="Paste your study material here...", height=350)
    else:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file is not None:
            try:
                pdf_buffer = io.BytesIO(uploaded_file.read())
                reader = PyPDF2.PdfReader(pdf_buffer)
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text_to_process += content
                st.success(f"✅ Successfully extracted {len(reader.pages)} pages.")
            except Exception:
                st.error("Could not read PDF. Ensure it's not password protected.")

with col2:
    st.subheader("🔊 Audio Dashboard")
    if st.button("🚀 Generate AI Narrator"):
        if text_to_process.strip():
            async def generate_audio():
                communicate = edge_tts.Communicate(text_to_process, voice_id, rate=speed_str)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            with st.spinner("Synthesizing High-Quality Voice..."):
                try:
                    audio_content = asyncio.run(generate_audio())
                    st.audio(audio_content, format="audio/mp3")
                    st.download_button("📥 Download Study MP3", 
                                       data=audio_content, 
                                       file_name="PraxisPages_Lecture.mp3",
                                       mime="audio/mp3")
                except Exception as e:
                    st.error(f"TTS Error: {e}")
        else:
            st.warning("Please provide some text or a PDF first.")

st.divider()
st.caption("PraxisPages | Final Year CSE Project")
