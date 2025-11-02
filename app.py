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

# Load model with caching
@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 100%);
        font-family: "Inter", sans-serif;
    }
    .header {
        background: linear-gradient(90deg, #1E3A8A, #2563EB);
        color: white;
        padding: 1.2rem;
        text-align: center;
        border-radius: 15px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563EB, #1E40AF);
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #1E3A8A;
        transform: scale(1.02);
    }
    .section-title {
        color: #1E3A8A;
        font-weight: 700;
        font-size: 19px;
        margin-bottom: 10px;
    }
    .prediction-box {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    .footer {
        text-align: center;
        font-size: 13px;
        color: #6B7280;
        margin-top: 40px;
    }
    .glow {
        text-shadow: 0 0 10px #60A5FA, 0 0 20px #60A5FA, 0 0 30px #2563EB;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% {opacity: 0.9;}
        50% {opacity: 1;}
        100% {opacity: 0.9;}
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'><h2>🚗 EV Range Prediction Dashboard</h2><p>Estimate your electric vehicle’s range with intelligent ML predictions.</p></div>", unsafe_allow_html=True)
st.write("")

# Animated line
st.markdown("<h4 class='glow' style='text-align:center;'>⚡ Drive Smart. Predict Smarter. ⚡</h4>", unsafe_allow_html=True)
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

# Predict button
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

    with st.spinner("🔍 Calculating your vehicle range..."):
        time.sleep(1.5)
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

    # Results display
    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"<div class='metric-card'><h4>🔋 Predicted SoC</h4><h2 style='color:#2563EB;'>{predicted_SoC:.2f}%</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown(f"<div class='metric-card'><h4>🚘 Estimated Range</h4><h2 style='color:#16A34A;'>{predicted_range_km:.1f} km</h2></div>", unsafe_allow_html=True)

        st.progress(predicted_SoC / 100)
        st.markdown(
            f"**🔋 Remaining Battery:** {remaining_energy_kwh:.2f} kWh  \n"
            f"**⚙️ Energy Consumption:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Prediction complete! Your estimated EV range is ready.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div class='footer'>Made with ⚡ Streamlit & ML | Designed for clean energy enthusiasts 🌍</div>",
    unsafe_allow_html=True
)
