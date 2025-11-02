import streamlit as st
import pandas as pd
import joblib
import random
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

# --- Custom CSS for Neon Style ---
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
        .info-box, .tips-box {
            background: rgba(30, 41, 59, 0.7);
        }
    }
    @media (prefers-color-scheme: light) {
        .main {
            background: radial-gradient(circle at 20% 30%, #f1f5ff, #c7d2fe);
            color: var(--text-dark);
        }
        .info-box, .tips-box {
            background: rgba(255, 255, 255, 0.8);
        }
    }

    .header {
        text-align: center;
        padding: 1rem;
        font-size: 30px;
        font-weight: 800;
        text-shadow: 0 0 20px var(--neon-blue), 0 0 40px var(--neon-glow);
        margin-bottom: 10px;
    }

    .neon-box {
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(59,130,246,0.25);
        transition: all 0.3s ease;
    }

    .info-box, .tips-box {
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(59,130,246,0.25);
        text-align: left;
        animation: fadeIn 1s ease-in;
    }

    .section-title {
        color: var(--neon-blue);
        font-weight: 700;
        font-size: 18px;
        text-shadow: 0 0 8px var(--neon-glow);
        margin-bottom: 10px;
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
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 0 25px rgba(96, 165, 250, 0.3);
        backdrop-filter: blur(10px);
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

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
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
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'>🚗 EV Range Prediction Dashboard</div>", unsafe_allow_html=True)

# --- Layout: 3 Columns (Left Info | Center Form | Right Tips) ---
col_left, col_center, col_right = st.columns([1.2, 2.2, 1.2])

# ---------- LEFT COLUMN: EV STATS ----------
with col_left:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔋 EV Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - ⚡ **Avg Battery:** 40–75 kWh  
    - 🛣️ **Avg Range:** 300–500 km  
    - 🚀 **Top Speed:** 160–220 km/h  
    - 🌡️ **Optimal Temp:** 20–25°C  
    - 🔧 **Charging Time:** 30–60 mins  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- CENTER COLUMN: MAIN APP ----------
with col_center:
    st.markdown("<div class='section-title'>🔧 Input Parameters</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        SoC = st.number_input("State of Charge (SoC) (%)", 0.0, 100.0, 80.0)
        Speed = st.number_input("Speed (Km/h)", 0.0, 200.0, 60.0)
        Temperature = st.number_input("Temperature (°C)", -20.0, 60.0, 25.0)
        Terrain = st.selectbox("Terrain Type", ["Flat", "Hilly"])
    with c2:
        Braking = st.number_input("Braking (m/s²)", 0.0, 10.0, 0.5)
        Acceleration = st.number_input("Acceleration (m/s²)", 0.0, 10.0, 1.0)
        Weather = st.selectbox("Weather Condition", ["Normal", "Hot", "Cold", "Rainy"])
        Prev_SoC = st.number_input("Previous SoC (%)", 0.0, 100.0, 85.0)

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

        with st.spinner("⚙️ Calculating range..."):
            time.sleep(1)
            predicted_SoC = model.predict(input_data)[0]

            def energy_rate(speed, terrain, weather):
                rate = 0.15
                if speed <= 50:
                    rate = 0.12
                elif speed > 80:
                    rate = 0.18
                if terrain == 'Hilly':
                    rate *= 1.2
                if weather == 'Hot':
                    rate *= 1.1
                return rate

            battery_capacity_kwh = 40
            rate = energy_rate(Speed, Terrain, Weather)
            remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
            predicted_range_km = remaining_energy_kwh / rate

        st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
        cA, cB = st.columns(2)
        cA.metric("Predicted SoC (%)", f"{predicted_SoC:.2f}")
        cB.metric("Estimated Range (km)", f"{predicted_range_km:.1f}")

        st.markdown("<div class='charging-container'><div class='charging-bar'></div></div>", unsafe_allow_html=True)
        st.markdown(
            f"🔋 **Remaining Energy:** {remaining_energy_kwh:.2f} kWh  \n"
            f"⚙️ **Consumption Rate:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.success("✅ Prediction complete!")

# ---------- RIGHT COLUMN: TIPS ----------
with col_right:
    st.markdown("<div class='tips-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>💡 Efficiency Tips</div>", unsafe_allow_html=True)
    tips = [
        "Keep your tires properly inflated for maximum range.",
        "Avoid rapid acceleration to conserve battery.",
        "Use regenerative braking when possible.",
        "Precondition the battery before long trips.",
        "Drive smoothly at moderate speeds.",
        "Avoid heavy accessories usage in cold weather."
    ]
    st.write(f"👉 {random.choice(tips)}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='footer'>💡 Neon Ambient Edition | Streamlit + ML ⚡</div>", unsafe_allow_html=True)
