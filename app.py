import streamlit as st
import pandas as pd
import joblib
import time
import random
import openai

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

# --- CSS Styling ---
st.markdown("""
<style>
    .main { background-color: #FFFFFF; color: #111827; font-family: 'Inter', sans-serif; }
    .hero { text-align: center; background: linear-gradient(90deg, #E0F2FE, #F8FAFC); padding: 35px 15px; border-radius: 12px; margin-bottom: 40px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .hero-title { font-size: 42px; font-weight: 800; color: #0F172A; letter-spacing: 0.5px; margin-bottom: 10px; }
    .hero-subtitle { font-size: 16px; color: #475569; font-weight: 400; max-width: 650px; margin: 0 auto; }
    .section-title { font-size: 18px; font-weight: 600; color: #1E293B; margin-top: 10px; margin-bottom: 10px; }
    .stButton>button { background-color: #2563EB; color: #FFFFFF; border-radius: 6px; font-weight: 600; border: none; padding: 0.6rem 1.4rem; transition: background 0.2s ease, transform 0.15s ease; }
    .stButton>button:hover { background-color: #1E40AF; transform: scale(1.02); }
    .footer { text-align: center; font-size: 12px; margin-top: 50px; color: #6B7280; }
    .chat-container { border: 1px solid #E5E7EB; border-radius: 10px; padding: 15px; background-color: #F9FAFB; margin-top: 25px; }
    .user-msg { background-color: #2563EB; color: white; padding: 8px 12px; border-radius: 10px; margin-bottom: 5px; max-width: 80%; margin-left: auto; }
    .bot-msg { background-color: #E5E7EB; color: #111827; padding: 8px 12px; border-radius: 10px; margin-bottom: 5px; max-width: 80%; }
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
col1, col2, col3 = st.columns([1.2, 2.3, 1.2])

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

# CENTER PANEL – Prediction Form
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

# RIGHT PANEL – Quick Stats
with col3:
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%  
    - **Charging Infrastructure:** 82% coverage  
    - **Top Efficient Models:** Model 3, Kona, Leaf  
    - **Avg User Range:** 412 km  
    """)

# --- Chatbot Section ---
st.markdown("<div class='section-title'>🤖 EV Chat Assistant</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#475569;'>Ask any question about electric vehicles or driving efficiency.</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat Display ---
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"<div class='user-msg'>{chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{chat['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

user_input = st.text_input("Type your question:", placeholder="e.g., How can I extend my EV battery life?")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    try:
        # --- Load API key from Streamlit secrets ---
        openai.api_key = st.secrets["openai"]["api_key"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert EV assistant helping users with electric vehicle insights."},
                *st.session_state.chat_history
            ]
        )

        bot_reply = response["choices"][0]["message"]["content"]

    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.rerun()

# --- Footer --- 
st.markdown("<div class='footer'>© 2025 EV Predictor | Powered by Streamlit</div>", unsafe_allow_html=True)

