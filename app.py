import streamlit as st
import pandas as pd
import joblib
import time

# Page configuration
st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load model
@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# --- Custom Neon CSS ---
st.markdown("""
<style>
    /* Animated gradient background */
    .main {
        background: linear-gradient(270deg, #0F172A, #1E3A8A, #2563EB, #0F172A);
        background-size: 600% 600%;
        animation: gradientShift 10s ease infinite;
        color: #E0F2FE;
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Header styling */
    .header {
        text-align: center;
        padding: 1.4rem;
        border-radius: 15px;
        color: #E0F2FE;
        text-shadow: 0 0 10px #38BDF8, 0 0 25px #2563EB, 0 0 50px #60A5FA;
    }

    .glow {
        color: #93C5FD;
        text-align: center;
        font-weight: 700;
        font-size: 20px;
        text-shadow: 0 0 8px #38BDF8, 0 0 15px #2563EB, 0 0 25px #60A5FA;
        animation: flicker 3s infinite;
    }

    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            opacity: 1;
        }
        20%, 24%, 55% {
            opacity: 0.3;
        }
    }

    .stButton>button {
        background: linear-gradient(90deg, #2563EB, #38BDF8);
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 0 15px #2563EB;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        box-shadow: 0 0 25px #38BDF8;
        transform: scale(1.05);
    }

    .section-title {
        color: #A5B4FC;
        font-weight: 700;
        font-size: 19px;
        margin-top: 10px;
        text-shadow: 0 0 8px #818CF8;
    }

    .prediction-box {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
    }

    .metric-card {
        background: rgba(30, 58, 138, 0.4);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
        color: #E0F2FE;
        animation: pulse 3s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 10px #38BDF8; }
        50% { box-shadow: 0 0 25px #2563EB; }
        100% { box-shadow: 0 0 10px #38BDF8; }
    }

    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 13px;
        margin-top: 40px;
        text-shadow: 0 0 6px #2563EB;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<div class='header'><h2>🚗 EV Range Prediction Dashboard</h2></div>", unsafe_allow_html=True)
st.markdown("<div class='glow'>⚡ Neon Intelligence for a Smarter Drive ⚡</div>", unsafe_allow_html=True)
st.write("")

# --- Input Section ---
st.markdown("<div class='section-title'>🔧 Input Parameters</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    SoC = st.number_input("State of Charge (SoC) (%)", min_value=0.0, max_value=100.0, value=80.0)
    Speed = st.number_input("Speed (Km/h)", min_value=0.0, max_value=200.0, value=60.0)
    Temperature = st.number_input("Temperature (°C)", min_value=-20.0, max_value=60.0, value=25.0)
    Terrain = st.selectbox("Terrain Type", options=["Flat", "Hilly"])
with col2:
    Braking = st.number_input("Braking (m/s²)", min_value=0.0, max_value=10.0, value=0.5)
    Acceleration = st.number_input("Acceleration (m/s²)", min_value=0.0, max_value=10.0, value=1.0)
    Weather = st.selectbox("Weather Condition", options=["Normal", "Hot", "Cold", "Rainy"])
    Prev_SoC = st.number_input("Previous SoC (%)", min_value=0.0, max_value=100.0, value=85.0)

# Predict Button
st.markdown("---")
predict_btn = st.button("🔮 Predict Range")

if predict_btn:
    input_data = pd.DataFrame([{
        'SoC': SoC,
        'Speed (Km/h)': Speed,
        'Temperature': Temperature,
        'Terrain': Terrain,
        'Braking (m/s²)': Braking,
        'Acceleration (m/s²)': Acceleration,
        'Weather': Weather,
        'Prev_SoC': Prev_SoC
    }])

    with st.spinner("⚙️ Activating Neon Predictive Engine..."):
        time.sleep(1.2)
        predicted_SoC = model.predict(input_data)[0]

        def dynamic_energy_consumption_rate(speed_kmh, terrain, weather):
            rate = 0.15
            if speed_kmh <= 50:
                rate = 0.12
            elif speed_kmh > 80:
                rate = 0.18
            if terrain == 'Hilly':
                rate *= 1.2
            if weather == 'Hot':
                rate *= 1.1
            return rate

        battery_capacity_kwh = 40
        rate = dynamic_energy_consumption_rate(Speed, Terrain, Weather)
        remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
        predicted_range_km = remaining_energy_kwh / rate

    # Results
    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"<div class='metric-card'><h4>🔋 Predicted SoC</h4><h2>{predicted_SoC:.2f}%</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown(f"<div class='metric-card'><h4>🚘 Estimated Range</h4><h2>{predicted_range_km:.1f} km</h2></div>", unsafe_allow_html=True)

        st.progress(predicted_SoC / 100)
        st.markdown(
            f"**🔋 Remaining Battery:** {remaining_energy_kwh:.2f} kWh  \n"
            f"**⚙️ Energy Consumption:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Neon analysis complete! Your EV range has been illuminated. ⚡")

# --- Footer ---
st.markdown("---")
st.markdown("<div class='footer'>💡 Built with Streamlit + Machine Learning | Neon Edition ⚡</div>", unsafe_allow_html=True)
