import streamlit as st
import pandas as pd
import joblib
import time
import random
import requests # New import for making API calls
# Removed: from openai import OpenAI
# Removed: from google.ai import generativelanguage as glm

# --- API CONFIGURATION FOR CHATBOT (The API Key will be injected by the environment) ---
API_KEY = ""
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# --- PATCH sklearn _RemainderColsList ISSUE ---
import sklearn.compose._column_transformer as ctf
if not hasattr(ctf, '_RemainderColsList'):
    class _RemainderColsList(list):
        pass
    ctf._RemainderColsList = _RemainderColsList

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded" # Changed to expanded to show chatbot immediately
)

# --- LOAD ML MODEL ---
@st.cache_resource
def load_model():
    try:
        # Assuming the model file path is correct in the execution environment
        model = joblib.load("ev_range_predictor_reduced.pkl")
        return model
    except FileNotFoundError:
        st.error("❌ Model file not found. Please upload 'ev_range_predictor_reduced.pkl' in the app folder.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {type(e).__name__} - {e}")
        return None

model = load_model()

# --- HELPER FUNCTION FOR ENERGY RATE ---
def energy_rate(speed, terrain, weather, braking, acceleration):
    """Calculates an estimated energy consumption rate (kWh/km) based on driving conditions."""
    rate = 0.15
    if speed <= 50: rate = 0.12
    elif speed > 80: rate = 0.18

    # Adjustments for environmental factors
    if terrain == "Hilly": rate *= 1.2

    # Temperature effects
    if weather == "Hot": rate *= 1.1
    if weather == "Cold": rate *= 1.15

    # Driving style effects
    rate *= 1 + 0.05 * braking + 0.07 * acceleration
    return rate

# --- GEMINI API CALL FUNCTION ---
def generate_response(prompt, chat_history):
    """Calls the Gemini API to get a response and grounding sources."""
    
    # 1. Construct the content array for the payload
    contents = []
    # Gemini API uses 'user' and 'model' roles
    role_map = {'user': 'user', 'assistant': 'model'} 
    for role, text in chat_history:
        if role == 'user':
             contents.append({"role": 'user', "parts": [{"text": text}]})
        elif role == 'assistant':
             contents.append({"role": 'model', "parts": [{"text": text}]})
    
    # Add the latest user prompt
    contents.append({"role": 'user', "parts": [{"text": prompt}]})

    # 2. Define the payload
    payload = {
        "contents": contents,
        # System instruction to define the chatbot's persona
        "systemInstruction": {
            "parts": [{"text": "You are an expert AI assistant specializing in Electric Vehicles (EVs), battery technology, and range prediction. Your responses should be informative, helpful, and concise. You MUST enable Google Search grounding for real-time information. Limit your answers to EV and automotive topics, and keep your tone encouraging."}]
        },
        # Enable Google Search grounding
        "tools": [{"google_search": {}}] 
    }

    # 3. Call the API
    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status() 
        result = response.json()

        # Check for errors in the response structure
        if not (result and 'candidates' in result and len(result['candidates']) > 0 and 
                'content' in result['candidates'][0] and 
                'parts' in result['candidates'][0]['content'] and 
                len(result['candidates'][0]['content']['parts']) > 0):
            return "Sorry, I received an empty or malformed response from the AI model."

        # 4. Extract generated text
        text = result['candidates'][0]['content']['parts'][0]['text']

        # 5. Extract grounding sources if available
        sources = []
        grounding_metadata = result['candidates'][0].get('groundingMetadata')
        if grounding_metadata and grounding_metadata.get('groundingAttributions'):
            for attr in grounding_metadata['groundingAttributions']:
                # Ensure the web attribute exists before accessing uri and title
                if attr.get('web'):
                    sources.append({
                        'uri': attr['web'].get('uri'),
                        'title': attr['web'].get('title')
                    })
        
        # Format sources into a Markdown list
        source_text = ""
        if sources:
            source_text = "\n\n---\n**Sources:**\n"
            # Limit to the first 3 or 4 unique sources for brevity in the chat
            unique_sources = {s['uri']: s for s in sources if s['uri']}.values()
            for i, source in enumerate(list(unique_sources)[:4]):
                source_text += f"- [{source['title']}]({source['uri']})\n"

        return text + source_text

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the Gemini API. Please check network connection or API setup. ({e})")
        return "I encountered an error trying to connect to the service."
    except Exception as e:
        st.error(f"An unexpected error occurred during response processing: {e}")
        return "I ran into a problem while generating the response."


# --- PAGE STYLING ---
st.markdown("""
<style>
    .main { background-color: #FFFFFF; color: #111827; font-family: 'Inter', sans-serif; }
    .hero { text-align: center; background: linear-gradient(90deg, #E0F2FE, #F8FAFC);
            padding: 35px 15px; border-radius: 12px; margin-bottom: 40px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
    .hero-title { font-size: 42px; font-weight: 800; color: #0F172A; margin-bottom: 10px; }
    .hero-subtitle { font-size: 16px; color: #475569; max-width: 650px; margin: 0 auto; }
    .section-title { font-size: 18px; font-weight: 600; color: #1E293B;
                    margin-top: 10px; margin-bottom: 10px; }
    .stButton>button { background-color: #2563EB; color: #FFFFFF; border-radius: 6px;
                        font-weight: 600; border: none; padding: 0.6rem 1.4rem;
                        transition: background 0.2s ease, transform 0.15s ease; }
    .stButton>button:hover { background-color: #1E40AF; transform: scale(1.02); }
    .footer { text-align: center; font-size: 12px; margin-top: 50px; color: #6B7280; }
    /* Chatbot specific styling */
    .st-emotion-cache-1c5c4f3 { padding-top: 2rem !important; }
    .st-emotion-cache-1c5c4f3 .st-emotion-cache-1v4ccg7 { padding-left: 1rem; padding-right: 1rem; }
    
    /* Styling for the chat message box */
    .stChatMessage { 
        border: 1px solid #E5E7EB; 
        border-radius: 8px; 
        padding: 10px;
        margin-bottom: 10px;
        background-color: #F9FAFB;
    }
</style>
""", unsafe_allow_html=True)

# --- CHATBOT SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='section-title'>💬 EV Chat Assistant</div>", unsafe_allow_html=True)
    st.caption("Ask questions about EV range, battery care, or driving efficiency.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ("assistant", "Hello! I'm your EV expert. Ask me anything about electric vehicles, range prediction, or efficiency tips!")
        ]

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for role, text in st.session_state.messages:
            with st.chat_message(role):
                st.markdown(text)

    # Chat input
    if prompt := st.chat_input("Ask a question..."):
        # 1. Add user message to history
        st.session_state.messages.append(("user", prompt))
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # 2. Get AI response
        with st.spinner("Thinking..."):
            # Prepare history for API call (list of tuples: (role, text))
            api_history = [(role, text) for role, text in st.session_state.messages if role != 'user' or text != prompt]
            
            ai_response = generate_response(prompt, api_history)
        
        # 3. Add assistant response to history and display
        st.session_state.messages.append(("assistant", ai_response))
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(ai_response)

    # Clear chat button
    if st.button("Clear Chat", help="Start a new conversation."):
        st.session_state["messages"] = [
            ("assistant", "Chat history cleared. How can I help you with your EV questions now?")
        ]
        st.rerun()


# --- HERO SECTION ---
st.markdown("""
<div class="hero">
    <div class="hero-title">⚡ EV Vehicle Range Predictor 🚗</div>
    <div class="hero-subtitle">
        Estimate your electric vehicle's driving range instantly.
        Adjust speed, terrain, and weather to see how they affect performance and battery life.
    </div>
</div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col1, col2, col3 = st.columns([1.2, 2.3, 1.2])

with col1:
    st.markdown("<div class='section-title'>⚙️ EV Insights</div>", unsafe_allow_html=True)
    st.markdown("""
    - Typical Battery Capacity: **40–75 kWh**
    - Average Driving Range: **300–500 km**
    - Charging Time (DC Fast): **30–60 minutes**
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

with col2:
    st.markdown("<div class='section-title'>🧩 Input Parameters</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        SoC = st.number_input("State of Charge (%)", 0.0, 100.0, 80.0, step=1.0, format="%.1f")
        Speed = st.number_input("Speed (Km/h)", 0.0, 200.0, 60.0, step=1.0, format="%.1f")
        Temperature = st.number_input("Temperature (°C)", -20.0, 60.0, 25.0, step=0.1, format="%.1f")
        Terrain = st.selectbox("Terrain Type", ["Flat", "Hilly"])
    with c2:
        Braking = st.number_input("Braking (m/s²)", 0.0, 10.0, 0.5, step=0.1, format="%.2f")
        Acceleration = st.number_input("Acceleration (m/s²)", 0.0, 10.0, 1.0, step=0.1, format="%.2f")
        Weather = st.selectbox("Weather Condition", ["Normal", "Hot", "Cold", "Rainy"])
        Prev_SoC = st.number_input("Previous SoC (%)", 0.0, 100.0, 85.0, step=1.0, format="%.1f")

    predict_btn = st.button("🚀 Predict Range")

    if predict_btn:
        if model is None:
            st.error("Model not loaded. Cannot predict.")
        else:
            # Prepare input data for the loaded ML model
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
                time.sleep(1) # Simulate calculation time
                try:
                    # 1. Predict the next SoC using the ML model
                    predicted_SoC = model.predict(input_data)[0]

                    # 2. Calculate the estimated range based on the predicted SoC and consumption rate
                    rate = energy_rate(Speed, Terrain, Weather, Braking, Acceleration)
                    # Use a fixed, typical battery capacity for estimation (e.g., 40 kWh)
                    battery_capacity_kwh = 40
                    # Energy remaining based on the predicted SoC
                    remaining_energy_kwh = (predicted_SoC / 100) * battery_capacity_kwh
                    # Estimated range (km) = remaining energy / consumption rate
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
                except Exception as e:
                    st.error(f"Error during prediction: {type(e).__name__} - {e}")

with col3:
    st.markdown("<div class='section-title'>📈 Quick Stats</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Energy Efficiency:** 91%
    - **Charging Infrastructure:** 82% coverage
    - **Top Efficient Models:** Tesla Model 3, Hyundai Kona, Nissan Leaf
    - **Avg User Range:** 412 km
    """)

# --- FOOTER ---
st.markdown("<div class='footer'>© 2025 EV Predictor | Powered by Streamlit and Gemini API</div>", unsafe_allow_html=True)
