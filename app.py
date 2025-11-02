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

# --- Professional Dark Theme CSS ---
st.markdown("""
<style>
    /* Global Styling */
    .main {
        background: linear-gradient(180deg, #0B1221, #111827);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    .header {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        color: #3B82F6;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
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
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
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

    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #64748B;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<div class='header'>EV Range Prediction Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Accurate range estimation powered by machine learning</div>", unsafe_allow_html=True)

# --- Layout ---
col1, col2, col3 = st.columns([1.3, 2.2, 1.3])

# LEFT PANEL – EV Insights
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Typical Battery Capacity: **40–75 kWh**  
    - Average Driving Range: **300–500 km**  
    - Charging Time: **30–60 minutes**  
    - Optimal Operating Temp: **20–25°C**  
    - Efficiency improves with **moderate speeds**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 Smart Driving Tip</div>", unsafe_allow_html=True)
    tips = [
        "Keep tire pressure optimal to maximize efficiency.",
        "Avoid harsh acceleration for longer range.",
        "Preheat or precool your EV while charging.",
        "Use regenerative braking effectively in traffic.",
        "Plan routes that avoid steep inclines."
    ]
    st.markdown(f"✅ {random.choice(tips)}")
    st.markdown("</div>", unsafe_allow_html=True)

# CENTER PANEL – Main Prediction Form
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
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with colB:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        **Remaining Battery Energy:** {remaining_energy_kwh:.2f} kWh  
        **Energy Consumption Rate:** {rate:.3f} kWh/km
        """)
        st.success("✅ Prediction complete! Check metrics above.")

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT PANEL – Analytics Placeholder
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%  
    - **Charging Infrastructure:** 82% coverage  
    - **Top Efficient Models:** Model 3, Kona, Leaf  
    - **Avg User Range:** 412 km  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("<div class='footer'>© 2025 AutoRange Technologies | Precision EV Range Intelligence</div>", unsafe_allow_html=True)

