import streamlit as st
import pandas as pd
import joblib
import time

# --- Page Config ---
st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Load Model ---
@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# --- Universal Neon CSS (Light + Dark Adaptive) ---
st.markdown("""
<style>
    :root {
        --neon-blue: #38BDF8;
        --neon-glow: #2563EB;
        --text-light: #E0F2FE;
        --text-dark: #0F172A;
    }

    /* Dark & Light mode backgrounds */
    @media (prefers-color-scheme: dark) {
        .main {
            background: linear-gradient(135deg, #000000 0%, #0a0f2d 40%, #0a1b3e 100%);
            color: var(--text-light);
        }
        .prediction-box {
            background: rgba(17, 24, 39, 0.7);
        }
        .metric-card {
            background: rgba(30, 58, 138, 0.4);
            color: var(--text-light);
        }
    }
    @media (prefers-color-scheme: light) {
        .main {
            background: linear-gradient(135deg, #f1f5ff 0%, #e0e7ff 60%, #c7d2fe 100%);
            color: var(--text-dark);
        }
        .prediction-box {
            background: rgba(255, 255, 255, 0.85);
        }
        .metric-card {
            background: rgba(219, 234, 254, 0.7);
            color: var(--text-dark);
        }
    }

    .header {
        text-align: center;
        padding: 1.2rem;
        font-weight: 700;
        font-size: 28px;
        text-shadow: 0 0 15px var(--neon-blue), 0 0 30px var(--neon-glow);
    }

    .glow {
        text-align: center;
        font-size: 18px;
        color: var(--neon-blue);
        animation: flicker 3s infinite;
    }

    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; }
        20%, 24%, 55% { opacity: 0.4; }
    }

    .section-title {
        color: var(--neon-blue);
        font-weight: 700;
        font-size: 18px;
        margin-top: 20px;
        text-shadow: 0 0 8px var(--neon-glow);
    }

    .stButton>button {
        background: linear-gradient(90deg, var(--neon-glow), var(--neon-blue));
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 0 20px var(--neon-blue);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 35px var(--neon-blue);
        transform: scale(1.05);
    }

    .prediction-box {
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 0 25px rgba(96, 165, 250, 0.25);
        transition: all 0.5s ease;
    }

    .metric-card {
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.25);
        animation: pulse 3s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 10px var(--neon-blue); }
        50% { box-shadow: 0 0 25px var(--neon-glow); }
        100% { box-shadow: 0 0 10px var(--neon-blue); }
    }

    /* Charging bar animation */
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
        box-shadow: 0 0 25px #38BDF8;
        animation: chargeAnimation 3s forwards;
    }

    @keyframes chargeAnimation {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    .footer {
        text-align: center;
        font-size: 13px;
        margin-top: 40px;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>🚗 EV Range Prediction Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='glow'>⚡ Neon Intelligence for Every Mode ⚡</div>", unsafe_allow_html=True)
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

st.markdown("---")
predict_btn = st.button("🔮 Predict Range")

# --- Prediction Logic ---
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

    with st.spinner("⚙️ Calculating neon-powered range..."):
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

    # --- Results ---
    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"<div class='metric-card'><h4>🔋 Predicted SoC</h4><h2>{predicted_SoC:.2f}%</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown(f"<div class='metric-card'><h4>🚘 Estimated Range</h4><h2>{predicted_range_km:.1f} km</h2></div>", unsafe_allow_html=True)

        # Neon Charging Animation
        st.markdown("<div class='section-title'>⚡ Charging Simulation</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="charging-container">
            <div class="charging-bar"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<br>🔋 <b>Remaining Battery:</b> {remaining_energy_kwh:.2f} kWh<br>"
            f"⚙️ <b>Energy Consumption:</b> {rate:.3f} kWh/km>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.success("✅ Neon analysis complete! Your EV range has been calculated. ⚡")

# --- Footer ---
st.markdown("---")
st.markdown("<div class='footer'>💡 Built with Streamlit + ML | Adaptive Neon Edition ⚡</div>", unsafe_allow_html=True)
