import streamlit as st
import edge_tts
import asyncio
import PyPDF2
import io

# 1. Page Configuration
st.set_page_config(
    page_title="PraxisPages Pro", 
    page_icon="🎓", 
    layout="wide"
)

# 2. Force-Injected CSS & Particle Engine
# Note: z-index is set to 999999 to stay ABOVE all Streamlit elements
st.markdown("""
    <style>
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }
    
    /* The Canvas Container */
    #particle-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none; /* Crucial: allows clicking buttons 'through' the dots */
        z-index: 999999;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        transition: 0.3s;
    }
    </style>

    <canvas id="particle-canvas"></canvas>

    <script>
    const canvas = document.getElementById('particle-canvas');
    const ctx = canvas.getContext('2d');
    let width, height;
    let mouse = { x: -100, y: -100 };
    const particles = [];
    const particleCount = 100;

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }

    window.addEventListener('resize', resize);
    resize();

    // Track Mouse & Touch
    const updateMouse = (e) => {
        if (e.touches) {
            mouse.x = e.touches[0].clientX;
            mouse.y = e.touches[0].clientY;
        } else {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        }
    };
    
    // Attach to window to ensure it captures movement everywhere
    window.addEventListener('mousemove', updateMouse);
    window.addEventListener('touchmove', updateMouse);

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 3 + 1; // Bigger dots
            this.ease = 0.05 + Math.random() * 0.1; // Smooth delay
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
            ctx.fillStyle = 'rgba(255, 255, 255, 1)'; // Solid white
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

# 3. Main App Logic (Rest of your code)
st.title("🎓 PraxisPages: AI Study Narrator")
st.markdown("Move your mouse or touch the screen to see the particle movement.")

col1, col2 = st.columns(2)
text_to_process = ""

with col1:
    option = st.radio("Input:", ("Text", "PDF"))
    if option == "Text":
        text_to_process = st.text_area("Paste here:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text_to_process += page.extract_text()

with col2:
    voice = st.selectbox("Voice", ["en-IN-NeerjaNeural", "en-US-GuyNeural"])
    if st.button("Generate Audio"):
        if text_to_process:
            async def run_tts():
                communicate = edge_tts.Communicate(text_to_process, voice)
                data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        data += chunk["data"]
                return data
            
            with st.spinner("Processing..."):
                audio_bytes = asyncio.run(run_tts())
                st.audio(audio_bytes)
