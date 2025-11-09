import streamlit as st
import pandas as pd
import joblib
import time
import random
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, FunctionDeclaration

# =========================================================
# --- PAGE CONFIGURATION ---
# =========================================================
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# --- LOAD ML MODEL ---
# =========================================================
@st.cache_resource
def load_model():
    return joblib.load("ev_range_predictor_reduced.pkl")

model = load_model()

# =========================================================
# --- CONFIGURE GEMINI CHATBOT ---
# =========================================================
@st.cache_resource
def load_genai_model():
    """Connects to Gemini API and sets up the EV chat model."""
    try:
        # --- Load API Key ---
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("❌ Gemini API key missing in Streamlit secrets.")
            return None

        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)

        # --- Connection Test ---
        try:
            test_model = genai.GenerativeModel("gemini-pro")
            _ = test_model.generate_content("ping")
            st.success("✅ Gemini API connected successfully.")
        except Exception as conn_err:
            st.error(f"Gemini API connection failed: {conn_err}")
            return None

        # --- Define Function Tool ---
        predict_range_tool = FunctionDeclaration(
            name="predict_ev_range",
            description="Predicts EV range and SoC given conditions like speed, temperature, terrain, etc.",
            parameters={
                "type": "OBJECT",
                "properties": {
                    "speed_kmh": {"type": "NUMBER", "description": "Vehicle speed in km/h"},
                    "temperature_c": {"type": "NUMBER", "description": "Ambient temperature in Celsius"},
                    "terrain": {"type": "STRING", "description": "Terrain type: Flat or Hilly"},
                    "weather": {"type": "STRING", "description": "Weather condition: Normal, Hot, Cold, Rainy"},
                    "soc": {"type": "NUMBER", "description": "Current battery state of charge (%)"},
                },
                "required": []
            }
        )

        # --- Initialize Gemini Model ---
        genai_model = genai.GenerativeModel(
            model_name="gemini-pro",  # ✅ Corrected model name
            tools=[predict_range_tool],
            generation_config=GenerationConfig(temperature=0.1)
        )
        return genai_model

    except Exception as e:
        st.error(f"Error loading Gemini API: {type(e).__name__} - {e}")
        return None


# --- Initialize Gemini Model ---
genai_model = load_genai_model()

# =========================================================
# --- CHAT SESSION SETUP ---
# =========================================================
@st.cache_resource
def start_chat_session(_genai_model):
    return _genai_model.start_chat(enable_automatic_function_calling=False)

if genai_model:
    chat = start_chat_session(genai_model)
else:
    chat = None

# =========================================================
# --- PAGE STYLING ---
# =========================================================
st.markdown("""
<style>
    .main { background-color: #FFFFFF; color: #111827; font-family: 'Inter', sans-serif; }
    .hero { text-align: center; background: linear-gradient(90deg, #E0F2FE, #F8FAFC);
            padding: 35px 15px; border-radius: 12px; margin-bottom: 40px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .hero-title { font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 10px; }
    .hero-subtitle { font-size: 16px; color: #475569; max-width: 650px; margin: 0 auto; }
    .section-title { font-size: 18px; font-weight: 600; color: #1E293B; margin-top: 10px; margin-bottom: 10px; }
    .stButton>button { background-color: #2563EB; color: #FFFFFF; border-radius: 6px; font-weight: 600;
                       border: none; padding: 0.6rem 1.4rem; transition: background 0.2s ease, transform 0.15s ease; }
    .stButton>button:hover { background-color: #1E40AF; transform: scale(1.02); }
    .footer { text-align: center; font-size: 12px; margin-top: 50px; color: #6B7280; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# --- HERO SECTION ---
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ EV Vehicle Range Predictor 🚗</div>
    <div class="hero-subtitle">
        Estimate your electric vehicle's driving range instantly.  
        Adjust speed, terrain, and weather to see how they affect performance and battery life.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# --- MAIN LAYOUT ---
# =========================================================
col1, col2, col3 = st.columns([1.2, 2.3, 1.2])

# ---------------- LEFT PANEL ----------------
with col1:
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Typical Battery Capacity: **40–75 kWh**  
    - Average Driving Range: **300–500 km**  
    - Charging Time: **30–60 minutes**  
    - Optimal Temperature: **20–25°C**  
    - Efficiency improves with **moderate speeds**
    """)
    st.markdown("<div class='section-title'>💡 Smart Driving Tip</div>", unsafe_allow_html=True)
    tips = [
        "Keep tire pressure optimal to maximize efficiency.",
        "Avoid harsh acceleration for longer range.",
        "Preheat or precool your EV while charging.",
        "Use regenerative braking effectively in traffic.",
        "Plan routes that avoid steep inclines."
    ]
    st.markdown(f"✅ {random.choice(tips)}")

# ---------------- CENTER PANEL ----------------
with col2:
    st.markdown("<div class='section-title'>🧩 Input Parameters</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        SoC = st.number_input("State of Charge (%)", 0.0, 100.0, 80.0)
        Speed = st.number_input("Speed (Km/h)", 0.0, 200.0, 60.0)
        Temperature = st.number_input("Temperature (°C)", -20.0, 60.0, 25.0)
        Terrain = st.selectbox("Terrain Type", ["Flat", "Hilly"])
    with c2:
        Braking = st.number_input("Braking (m/s²)", 0.0, 10.0, 0.5)
        Acceleration = st.number_input("Acceleration (m/s²)", 0.0, 10.0, 1.0)
        Weather = st.selectbox("Weather Condition", ["Normal", "Hot", "Cold", "Rainy"])
        Prev_SoC = st.number_input("Previous SoC (%)", 0.0, 100.0, 85.0)

    predict_btn = st.button("🚀 Predict Range")

    if predict_btn:
        input_data = pd.DataFrame([{
            "SoC": SoC,
            "Speed (Km/h)": Speed,
            "Temperature": Temperature,
            "Terrain": Terrain,
            "Braking (m/s²)": Braking,
            "Acceleration (m/s²)": Acceleration,
            "Weather": Weather,
            "Prev_SoC": Prev_SoC
        }])

        with st.spinner("Calculating optimal range..."):
            time.sleep(1)
            predicted_SoC = model.predict(input_data)[0]

            def energy_rate(speed, terrain, weather):
                rate = 0.15
                if speed <= 50: rate = 0.12
                elif speed > 80: rate = 0.18
                if terrain == "Hilly": rate *= 1.2
                if weather == "Hot": rate *= 1.1
                return rate

            rate = energy_rate(Speed, Terrain, Weather)
            battery_capacity_kwh = 40
            remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
            predicted_range_km = remaining_energy_kwh / rate

        st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
        with colB:
            st.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")

        st.markdown(f"""
        **Remaining Battery Energy:** {remaining_energy_kwh:.2f} kWh  
        **Energy Consumption Rate:** {rate:.3f} kWh/km
        """)
        st.success("✅ Prediction complete! Check metrics above.")

# ---------------- RIGHT PANEL ----------------
with col3:
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%  
    - **Charging Infrastructure:** 82% coverage  
    - **Top Efficient Models:** Model 3, Kona, Leaf  
    - **Avg User Range:** 412 km  
    """)

# =========================================================
# --- CHATBOT SECTION ---
# =========================================================
st.divider()
st.markdown("<div class='section-title'>🤖 EV Chat Assistant</div>", unsafe_allow_html=True)
st.info("Ask questions like 'What’s my range at 100 km/h in hot weather on hilly roads?'")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me about EVs, battery, or range predictions..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        if not genai_model:
            ai_text = "❌ The Gemini chatbot connection failed. Please check your API setup."
        else:
            try:
                response = chat.send_message(prompt)
                part = response.candidates[0].content.parts[0]

                if hasattr(part, "function_call") and part.function_call and part.function_call.name == "predict_ev_range":
                    args = part.function_call.args
                    speed = args.get("speed_kmh", 60)
                    temp = args.get("temperature_c", 25)
                    terrain = args.get("terrain", "Flat")
                    weather = args.get("weather", "Normal")
                    soc = args.get("soc", 80)

                    rate = 0.15
                    if speed <= 50: rate = 0.12
                    elif speed > 80: rate = 0.18
                    if terrain == "Hilly": rate *= 1.2
                    if weather == "Hot": rate *= 1.1

                    remaining_energy_kwh = (soc / 100) * 40
                    range_km = remaining_energy_kwh / rate
                    ai_text = f"At {speed} km/h in {weather.lower()} {terrain.lower()} conditions, your estimated range is **{range_km:.1f} km**."
                else:
                    ai_text = getattr(part, "text", None) or "I’m not sure, but let’s try adjusting your inputs."

            except Exception as e:
                ai_text = f"⚠️ Error while processing your question: {e}"

    with st.chat_message("assistant"):
        st.markdown(ai_text)
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_text})

# =========================================================
# --- FOOTER ---
# =========================================================
st.markdown("<div class='footer'>© 2025 EV Predictor | Powered by Streamlit + Gemini AI</div>", unsafe_allow_html=True)
