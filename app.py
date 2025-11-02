import streamlit as st
import pandas as pd
import joblib
import time

st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# --- Neon Dual Mode with Animated Side Glow ---
st.markdown("""
<style>
    :root {
        --neon-blue: #38BDF8;
        --neon-glow: #2563EB;
        --text-light: #E0F2FE;
        --text-dark: #0F172A;
    }

    @media (prefers-color-scheme: dark) {
        .main {
            background: radial-gradient(circle at 20% 30%, #0f172a, #000);
            color: var(--text-light);
        }
        .side-glow::before, .side-glow::after {
            background: radial-gradient(circle, rgba(37,99,235,0.3), transparent 70%);
        }
    }

    @media (prefers-color-scheme: light) {
        .main {
            background: radial-gradient(circle at 20% 30%, #f1f5ff, #c7d2fe);
            color: var(--text-dark);
        }
        .side-glow::before, .side-glow::after {
            background: radial-gradient(circle, rgba(59,130,246,0.25), transparent 70%);
        }
    }

    /* --- Side ambient glows --- */
    .side-glow {
        position: relative;
        overflow: hidden;
    }

    .side-glow::before,
    .side-glow::after {
        content: "";
        position: fixed;
        top: 0;
        width: 300px;
        height: 100vh;
        z-index: 0;
        animation: glowMove 10s infinite alternate ease-in-out;
    }
    .side-glow::before { left: -150px; }
    .side-glow::after { right: -150px; }

    @keyframes glowMove {
        0% { transform: translateY(0); opacity: 0.4; }
        50% { transform: translateY(20px); opacity: 0.8; }
        100% { transform: translateY(-20px); opacity: 0.4; }
    }

    .header {
        text-align: center;
        padding: 1rem;
        font-size: 30px;
        font-weight: 800;
        text-shadow: 0 0 20px var(--neon-blue), 0 0 40px var(--neon-glow);
        z-index: 1;
        position: relative;
    }

    .section-title {
        color: var(--neon-blue);
        font-weight: 700;
        font-size: 18px;
        margin-top: 20px;
        text-shadow: 0 0 10px var(--neon-glow);
    }

    .stButton>button {
        background: linear-gradient(90deg, var(--neon-glow), var(--neon-blue));
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 0 25px var(--neon-blue);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px var(--neon-glow);
    }

    .prediction-box {
        background: rgba(17, 24, 39, 0.6);
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 0 25px rgba(96, 165, 250, 0.3);
        backdrop-filter: blur(10px);
        z-index: 1;
        position: relative;
    }

    @media (prefers-color-scheme: light) {
        .prediction-box {
            background: rgba(255, 255, 255, 0.85);
        }
    }

    .metric-card {
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(59,130,246,0.25);
        margin: 10px;
    }

    .charging-container {
        width: 100%;
        background-color: rgba(255,255,255,0.15);
        border-radius: 15px;
        overflow: hidden;
        margin-top: 15px;
        height: 25px;
        box-shadow: 0 0 20px rgba(59,130,246,0.3);
    }
    .charging-bar {
        height: 100%;
        background: linear-gradient(90deg, #0EA5E9, #38BDF8, #60A5FA);
        width: 0%;
        border-radius: 15px;
        animation: chargeAnim 3s forwards;
    }

    @keyframes chargeAnim {
        from { width: 0%; }
        to { width: 100%; }
    }

    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 40px;
        opacity: 0.8;
    }
</style>
<div class="side-glow"></div>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>🚗 EV Range Prediction Dashboard</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#38BDF8;'>⚡ Adaptive Neon Mode + Ambient Side Glow</p>", unsafe_allow_html=True)

# --- Input Fields ---
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

    with st.spinner("⚙️ Analyzing energy data..."):
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

    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        colA.markdown(f"<div class='metric-card'><h4>🔋 Predicted SoC</h4><h2>{predicted_SoC:.2f}%</h2></div>", unsafe_allow_html=True)
        colB.markdown(f"<div class='metric-card'><h4>🚘 Estimated Range</h4><h2>{predicted_range_km:.1f} km</h2></div>", unsafe_allow_html=True)

        st.markdown("<div class='charging-container'><div class='charging-bar'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<br>🔋 <b>Remaining Energy:</b> {remaining_energy_kwh:.2f} kWh<br>⚙️ <b>Energy Rate:</b> {rate:.3f} kWh/km>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Range prediction complete!")

st.markdown("---")
st.markdown("<div class='footer'>💡 Neon Ambient Edition | Streamlit + ML ⚡</div>", unsafe_allow_html=True)
