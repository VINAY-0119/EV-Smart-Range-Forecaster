import streamlit as st
import pandas as pd
import joblib
import time
import random

# --- App Config ---
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

# --- Clean Professional Theme ---
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0B1221, #111827);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    .header {
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        color: #3B82F6;
        margin-bottom: 8px;
    }
    .subheader {
        text-align: center;
        color: #94A3B8;
        margin-bottom: 35px;
        font-size: 15px;
    }
    .card {
        background: #1E293B;
        border-radius: 15px;
        padding: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #60A5FA;
        margin-bottom: 12px;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.4rem;
        transition: background 0.2s ease, transform 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: scale(1.02);
    }
    .metric-box {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 10px 15px;
        margin-top: 5px;
    }
    .tip-text {
        color: #E2E8F0;
        font-size: 14px;
        margin-bottom: 8px;
        line-height: 1.5;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #64748B;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>EV Range Prediction Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Accurate range estimation powered by AI</div>", unsafe_allow_html=True)

# --- Layout ---
col1, col2, col3 = st.columns([1.3, 2.2, 1.3])

# LEFT COLUMN – EV Info
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Battery Capacity: **40–75 kWh**  
    - Average Range: **300–500 km**  
    - Fast Charge: **30–60 min**  
    - Best Efficiency: **60–90 km/h**  
    - Ideal Temp: **20–25°C**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# CENTER COLUMN – Prediction Section
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
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

        with st.spinner("Analyzing data..."):
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

        st.markdown("<div class='section-title'>📊 Results</div>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with colB:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        **Remaining Energy:** {remaining_energy_kwh:.2f} kWh  
        **Energy Consumption Rate:** {rate:.3f} kWh/km
        """)
        st.success("✅ Prediction complete.")
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN – Clean Tips
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 Smart Driving Tips</div>", unsafe_allow_html=True)

    tips_general = [
        "Keep tire pressure optimal to reduce rolling resistance.",
        "Use Eco or Comfort driving modes whenever possible.",
        "Avoid sudden acceleration and braking for better efficiency.",
        "Limit air conditioning or heater use during long trips."
    ]
    tips_hot = [
        "Pre-cool the cabin while charging to save battery.",
        "Avoid direct sunlight when parking to protect cells."
    ]
    tips_cold = [
        "Preheat your EV while plugged in to reduce drain.",
        "Keep battery above 20% in cold conditions."
    ]
    tips_hilly = [
        "Use regenerative braking downhill to regain energy.",
        "Maintain a steady speed uphill for best range."
    ]
    tips_rainy = [
        "Drive smoothly; wet roads increase rolling resistance.",
        "Turn off defoggers when not needed."
    ]

    selected_tips = tips_general.copy()
    if Weather == "Hot":
        selected_tips += tips_hot
    elif Weather == "Cold":
        selected_tips += tips_cold
    elif Weather == "Rainy":
        selected_tips += tips_rainy
    if Terrain == "Hilly":
        selected_tips += tips_hilly

    random.shuffle(selected_tips)
    for t in selected_tips[:4]:
        st.markdown(f"<p class='tip-text'>• {t}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div class='footer'>© 2025 AutoRange Technologies | Intelligent EV Analytics</div>", unsafe_allow_html=True)
