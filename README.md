# ⚡ EV Range Predictor 🚗

A **Streamlit web application** that predicts the estimated **electric vehicle (EV) driving range** based on various environmental and driving parameters such as speed, temperature, terrain, and weather.  

This tool provides quick insights into how different driving conditions affect your EV’s efficiency and battery performance.

---

## 🚀 Features

- **Real-time EV Range Prediction** using a trained ML model (`ev_range_predictor_reduced.pkl`)
- **Interactive Input Panel** to adjust:
  - Speed (Km/h)  
  - Temperature (°C)  
  - Terrain Type (Flat / Hilly)  
  - Weather Condition (Normal / Hot / Cold / Rainy)  
  - Braking & Acceleration rates  
  - State of Charge (SoC) and Previous SoC  
- **Professional UI Design** with responsive layout and modern CSS styling
- **Quick Stats & Smart Driving Tips** to enhance EV efficiency
- **Performance Metrics** including:
  - Predicted State of Charge  
  - Estimated Driving Range (km)  
  - Remaining Battery Energy (kWh)  
  - Energy Consumption Rate (kWh/km)

---

## 🧩 Requirements

Before running the app, ensure the following dependencies are installed:

```bash
pip install streamlit pandas joblib
📦 Project Structure
bash
Copy code
EV-Range-Predictor/
│
├── ev_range_predictor_reduced.pkl     # Trained machine learning model
├── app.py                             # Main Streamlit application
└── README.md                          # Documentation file
▶️ How to Run the App
Clone this repository or download the project folder.

Place your trained model file (ev_range_predictor_reduced.pkl) in the same directory as app.py.

In the terminal, run:

bash
Copy code
streamlit run app.py
The app will open automatically in your browser at:

arduino
Copy code
http://localhost:8501
⚙️ How It Works
The app loads a pre-trained regression model using joblib.

User inputs are collected through Streamlit’s interactive widgets.

Inputs are processed into a DataFrame for prediction.

The model predicts remaining State of Charge (SoC).

The app calculates estimated range based on energy consumption formulas and efficiency factors.

📊 Example Calculation
If your EV has:

SoC: 80%

Speed: 60 km/h

Terrain: Flat

Temperature: 25°C

Then the model estimates your range using the formula:

ini
Copy code
remaining_energy_kWh = (predicted_SoC / 100) * battery_capacity_kWh
predicted_range_km = remaining_energy_kWh / energy_rate
Where energy_rate varies with terrain, speed, and weather.

🧠 Tips for Best Results
Use realistic SoC and driving parameters.

Avoid extreme inputs (e.g., 200 km/h + very hilly terrain) unless testing boundaries.

For deployment, ensure the .pkl file path is accessible to your Streamlit environment.

💡 Example Smart Tips Displayed in the App
Keep tire pressure optimal to maximize efficiency.

Avoid harsh acceleration for longer range.

Preheat or precool your EV while charging.

Use regenerative braking effectively in traffic.

🛠️ Customization
You can easily modify:

UI Design: Edit the embedded CSS section in app.py.

Model Logic: Replace the .pkl file with a retrained model.

Battery Specs: Adjust battery_capacity_kwh inside the script.
