# ⚡EV-Smart-Range-Forecaster 🚗

A professional Streamlit web application that predicts the driving range of an electric vehicle (EV) under different driving and environmental conditions such as speed, temperature, terrain, and weather.  
It provides real-time insights into battery performance and helps users understand how driving behavior affects efficiency.

-----------------------------------------------------------------------------------

## 🧭 Overview

The EV-Smart-Range-Forecaster uses a trained machine learning model to estimate the remaining State of Charge (SoC) and expected range (km) of an electric vehicle.  
It allows users to input variables like speed, terrain, and weather to see how these affect range and battery life.

This tool is useful for:
- EV owners optimizing driving range
- Researchers testing vehicle efficiency
- Manufacturers simulating driving conditions

-----------------------------------------------------------------------------------

## 🚀 Features

- EV-Smart-Range-Forecaster using ML model (ev_range_predictor_reduced.pkl)
- Interactive Streamlit dashboard for easy input and live feedback
- Professional UI design with custom CSS and clean layout
- Dynamic insights on SoC, energy use, and driving range
- Smart energy formula that adapts to speed, terrain, and weather
- **AI Chatbot** integrated for instant help, advice, and EV-related queries

-----------------------------------------------------------------------------------

## ⚙️ Installation & Running the App

### Step 1: Clone the Repository
git clone https://github.com/yourusername/EV-Smart-Range-Forecaster.git
cd EV-Smart-Range-Forecaster

### Step 2: Install Dependencies
pip install streamlit pandas joblib openai

(Optional) You can also create a virtual environment:
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

### Step 3: Run the Application
streamlit run app.py

### Step 4: Open in Browser
http://localhost:8501

-----------------------------------------------------------------------------------

## 🧮 How the App Works

1. The app loads a trained machine learning regression model stored as ev_range_predictor_reduced.pkl.
2. You input driving and environmental variables such as:
   - Speed (Km/h)
   - Temperature (°C)
   - Terrain (Flat / Hilly)
   - Weather (Normal, Hot, Cold, Rainy)
   - Acceleration / Braking
   - SoC and Previous SoC (%)
3. The model predicts the remaining State of Charge (SoC).
4. The app calculates estimated range (km) using a custom energy rate formula.
5. The AI Chatbot provides on-demand explanations, tips, and answers to EV-related questions.

### 🔋 Energy Formula

remaining_energy_kWh = (predicted_SoC / 100) * battery_capacity_kWh  
predicted_range_km = remaining_energy_kWh / energy_rate  

Where:
- battery_capacity_kWh = 40 (default)
- energy_rate changes with:
  - Speed
  - Terrain type (higher for hilly)
  - Weather condition (higher for hot)

-----------------------------------------------------------------------------------

## 🧠 Example Usage

### Input Parameters
Parameter | Value
-----------|--------
SoC | 80%
Speed | 60 km/h
Temperature | 25°C
Terrain | Flat
Weather | Normal
Acceleration | 1.0 m/s²
Braking | 0.5 m/s²
Prev_SoC | 85%

### Model Output Example
Metric | Result
--------|--------
Predicted SoC | 72.4 %
Estimated Range | 193.1 km
Remaining Battery Energy | 28.96 kWh
Energy Consumption Rate | 0.15 kWh/km

### Interpretation:
- The model predicts your battery will have 72.4% charge left after your drive.
- You can drive approximately 193 km before the battery is depleted.
- Efficiency improves with lower speeds and flat terrain.

-----------------------------------------------------------------------------------

## 💡 Smart Driving Tips (Shown in App)

- Maintain optimal tire pressure for better efficiency
- Avoid harsh acceleration or braking
- Preheat or precool your EV while charging
- Use regenerative braking effectively
- Plan routes that avoid steep inclines

Each app session displays one random smart driving tip.

-----------------------------------------------------------------------------------

## 🤖 AI Chatbot Feature

The integrated AI chatbot helps you by:
- Answering questions about EV range, battery performance, and efficiency
- Providing personalized driving advice based on your inputs
- Explaining how different factors impact your EV’s range
- Offering troubleshooting tips for battery issues or driving habits

Simply type your query in the chatbot panel and get instant responses powered by AI.

-----------------------------------------------------------------------------------

## 🧾 Example Run (Step-by-Step)

### 1. Launch the App
streamlit run app.py

### 2. Open in Your Browser
You’ll see a clean dashboard with:
- Left panel → EV insights & driving tips
- Center panel → Input fields for model prediction
- Right panel → Quick stats & AI chatbot

### 3. Enter Example Values:
Input | Example
--------|----------
State of Charge (%) | 80
Speed (Km/h) | 60
Temperature (°C) | 25
Terrain Type | Flat
Braking (m/s²) | 0.5
Acceleration (m/s²) | 1.0
Weather Condition | Normal
Previous SoC (%) | 85

Click "🚀 Predict Range".

### 4. Output Example:
Predicted SoC: 72.4%  
Estimated Range: 193.1 km  
Remaining Energy: 28.96 kWh  
Energy Rate: 0.15 kWh/km  

Use the chatbot to ask any additional questions or for driving advice.

-----------------------------------------------------------------------------------

## 📁 Project Structure

EV-Smart-Range-Forecaster/  
│  
├── app.py                          # Main Streamlit application  
├── ev_range_predictor_reduced.pkl  # Trained ML model  
├── requirements.txt                # Dependencies  
└── README.md                       # Documentation  

-----------------------------------------------------------------------------------

## ⚙️ Customization

Component | Description
-----------|-------------
battery_capacity_kWh | Change to match your EV’s capacity  
CSS Section | Modify UI colors or layout  
energy_rate() function | Adjust consumption rate formula  
Model File | Replace with your own .pkl model  
AI Chatbot | Customize prompt, API keys, and behavior in app.py  

-----------------------------------------------------------------------------------

## ☁️ Deployment (Optional)

### 🌐 Deploy to Streamlit Cloud

1. Push your project to GitHub  
2. Visit https://share.streamlit.io  
3. Connect your repository  
4. Select entry file → app.py  
5. Click Deploy  

Your app will be live in minutes!

-----------------------------------------------------------------------------------

> “Drive smarter, not farther — predict, plan, and power your EV journey with confidence.”
