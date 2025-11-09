import streamlit as st
import pandas as pd
import joblib
import time
import random

# --- App Configuration ---
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load("ev_range_predictor_reduced.pkl")

model = load_model()

# --- Modern Clean CSS ---
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
        color: #111827;
        font-family: 'Inter', sans-serif;
    }
    .hero {
        text-align: center;
        background: linear-gradient(90deg, #E0F2FE, #F8FAFC);
        padding: 35px 15px;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #475569;
        font-weight: 400;
        max-width: 650px;
        margin: 0 auto;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #2563EB;
        color: #FFFFFF;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.4rem;
        transition: background 0.2s ease, transform 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        transform: scale(1.02);
    }
    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #6B7280;
    }
    .chatbox {
        border: 1px solid #E5E7EB;
        background: #F9FAFB;
        border-radius: 12px;
        padding: 1rem;
        height: 500px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ EV Vehicle Range Predictor 🚗</div>
    <div class="hero-subtitle">
        Estimate your electric vehicle's driving range instantly.  
        Adjust speed, terrain, and weather to see how they affect performance and battery life.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Layout ---
col1, col2, col3 = st.columns([1.2, 2.3, 1.5])

# LEFT PANEL – EV Insights
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

# CENTER PANEL – Prediction
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

    st.markdown("<br>", unsafe_allow_html=True)
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
                if speed <= 50:
                    rate = 0.12
                elif speed > 80:
                    rate = 0.18
                if terrain == "Hilly":
                    rate *= 1.2
                if weather == "Hot":
                    rate *= 1.1
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

# RIGHT PANEL – Chatbot
with col3:
    st.markdown("<div class='section-title'>💬 EV Assistant Chatbot</div>", unsafe_allow_html=True)
    st.markdown("Ask me about EV range, battery tips, or driving efficiency!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Simple rule-based chatbot for demonstration (you can connect GPT API if needed)
        if "range" in user_input.lower():
            bot_reply = "The driving range depends on factors like speed, temperature, and terrain. Moderate speed (60–80 km/h) gives the best range."
        elif "battery" in user_input.lower():
            bot_reply = "Keep your battery between 20–80% for long-term health. Avoid frequent full charges."
        elif "charge" in user_input.lower():
            bot_reply = "Fast chargers can recharge most EVs in 30–45 minutes. Use them sparingly to extend battery life."
        elif "weather" in user_input.lower():
            bot_reply = "Cold and hot weather can reduce efficiency by 10–20%. Keep the cabin preconditioned while charging."
        else:
            bot_reply = "I can help with EV range, battery care, charging tips, and efficiency insights!"

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

        # Display assistant message instantly
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# --- Footer ---
st.markdown("<div class='footer'>© 2025 EV Predictor | Powered by Streamlit</div>", unsafe_allow_html=True)
