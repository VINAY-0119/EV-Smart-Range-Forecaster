import streamlit as st
import pandas as pd
import joblib
import time

# --- Page Config ---
st.set_page_config(
    page_title="EV Range Prediction App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Model ---
@st.cache_resource
def load_model():
    return joblib.load('ev_range_predictor_reduced.pkl')

model = load_model()

# --- Custom Professional Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    .header {
        text-align: center;
        padding: 1rem 0;
        color: #1e3a8a;
    }
    .section-title {
        color: #334155;
        font-weight: 600;
        font-size: 18px;
        margin-top: 10px;
    }
    .prediction-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .metric-card {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: inset 0 0 8px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: scale(1.03);
    }
    .tips-box, .range-box {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
        font-size: 14px;
    }
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='header'><h2>🚗 EV Range Prediction Dashboard</h2><p>Accurate insights to plan your next drive efficiently.</p></div>", unsafe_allow_html=True)

# --- Input + Side Panels Layout ---
left_col, center_col, right_col = st.columns([1.2, 2.5, 1.2])

with left_col:
    st.markdown("### 💡 Efficiency Tips")
    st.markdown(
        """
        <div class='tips-box'>
        • Maintain moderate speeds (50–80 km/h) for optimal range.  
        • Avoid sudden acceleration or braking.  
        • Keep tire pressure optimal.  
        • Precondition your EV before driving in extreme weather.  
        • Use Eco mode and minimize AC/heater load.
        </div>
        """,
        unsafe_allow_html=True
    )

with center_col:
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
    predict_btn = st.button("🚀 Predict Range")

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

        with st.spinner("Calculating your EV range..."):
            time.sleep(1)
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
        st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"<div class='metric-card'><h4>🔋 Predicted SoC</h4><h2>{predicted_SoC:.2f}%</h2></div>", unsafe_allow_html=True)
        with colB:
            st.markdown(f"<div class='metric-card'><h4>🚘 Estimated Range</h4><h2>{predicted_range_km:.1f} km</h2></div>", unsafe_allow_html=True)

        st.progress(predicted_SoC / 100)
        st.markdown(
            f"**Remaining Battery:** {remaining_energy_kwh:.2f} kWh  \n"
            f"**Energy Consumption:** {rate:.3f} kWh/km"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.success("Prediction complete! Drive safely and efficiently.")

with right_col:
    st.markdown("### 📈 Predicted Range Insights")
    st.markdown(
        f"""
        <div class='range-box'>
        **Optimal Range:** ~{predicted_range_km * 0.9:.1f} km  
        **Aggressive Driving Range:** ~{predicted_range_km * 0.7:.1f} km  
        **Eco Mode Range:** ~{predicted_range_km * 1.1:.1f} km  
        <hr>
        <small>These estimates consider driving style, terrain, and weather conditions.</small>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Footer ---
st.markdown("---")
st.markdown("<div class='footer'>Built with Streamlit + Machine Learning | Smart EV Edition ⚡</div>", unsafe_allow_html=True)
