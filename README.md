project:
  name: "EV Range Predictor"
  description: >
    An interactive Streamlit web app that predicts your EV’s remaining range 
    and battery efficiency using a trained machine learning regression model.

setup:
  steps:
    - step: "Clone the Repository"
      commands:
        - git clone https://github.com/yourusername/ev-range-predictor.git
        - cd ev-range-predictor

    - step: "Create Virtual Environment (optional but recommended)"
      commands:
        - python -m venv venv
        - source venv/bin/activate  # For Mac/Linux
        - venv\Scripts\activate     # For Windows

    - step: "Install Dependencies"
      options:
        - pip install -r requirements.txt
        - pip install streamlit pandas joblib

    - step: "Run the Application"
      command: streamlit run app.py

    - step: "Open in Browser"
      url: "http://localhost:8501"

how_it_works:
  model_file: "ev_range_predictor_reduced.pkl"
  description: >
    The app uses a trained regression model to predict the remaining State of Charge (SoC) 
    based on multiple driving and environmental parameters.
  inputs:
    - parameter: Speed
      unit: "Km/h"
      example: 60
    - parameter: Temperature
      unit: "°C"
      example: 25
    - parameter: Terrain
      options: ["Flat", "Hilly"]
      example: "Flat"
    - parameter: Weather
      options: ["Normal", "Hot", "Cold", "Rainy"]
      example: "Normal"
    - parameter: Acceleration
      unit: "m/s²"
      example: 1.0
    - parameter: Braking
      unit: "m/s²"
      example: 0.5
    - parameter: SoC
      unit: "%"
      example: 80
    - parameter: Previous_SoC
      unit: "%"
      example: 85

energy_formula:
  code: |
    remaining_energy_kWh = (predicted_SoC / 100) * battery_capacity_kWh
    predicted_range_km = remaining_energy_kWh / energy_rate
  constants:
    battery_capacity_kWh: 40
    energy_rate_dependence:
      - Speed: "Higher speed → higher rate"
      - Terrain: "Hilly → higher rate"
      - Weather: "Hot/Cold → higher rate"

example_prediction:
  input:
    SoC: "80%"
    Speed: "60 km/h"
    Temperature: "25°C"
    Terrain: "Flat"
    Weather: "Normal"
    Acceleration: "1.0 m/s²"
    Braking: "0.5 m/s²"
    Previous_SoC: "85%"
  output:
    Predicted_SoC: "72.4%"
    Estimated_Range: "193.1 km"
    Remaining_Battery_Energy: "28.96 kWh"
    Energy_Consumption_Rate: "0.15 kWh/km"
  interpretation: >
    The model predicts your battery will have approximately 72.4% charge left after your trip. 
    You can drive around 193 km before the battery is depleted. 
    Efficiency improves at lower speeds and on flat terrain.

smart_driving_tips:
  - Maintain proper tire pressure.
  - Avoid harsh acceleration or braking.
  - Preheat or precool your EV while charging.
  - Use regenerative braking effectively.
  - Plan routes that minimize elevation changes.
  display_note: "Each session displays one random smart driving tip."

example_run:
  steps:
    - step: "Launch the app"
      command: "streamlit run app.py"
    - step: "Open the dashboard in browser"
      layout:
        left_panel: "EV insights and driving tips"
        center_panel: "Input fields for model prediction"
        right_panel: "Quick stats and performance metrics"
    - step: "Enter sample input values"
      example:
        State_of_Charge: 80
        Speed: 60
        Temperature: 25
        Terrain_Type: "Flat"
        Braking: 0.5
        Acceleration: 1.0
        Weather_Condition: "Normal"
        Previous_SoC: 85
    - step: "Click the Predict Range button"
      emoji: "🚀"
    - step: "Example Output"
      output:
        Predicted_SoC: "72.4%"
        Estimated_Range: "193.1 km"
        Remaining_Energy: "28.96 kWh"
        Energy_Rate: "0.15 kWh/km"
      note: "Metrics appear in colored info boxes on the dashboard."

tech_stack:
  - Python
  - Streamlit
  - Pandas
  - Joblib
  - Scikit-learn

file_structure: |
  ev-range-predictor/
  ├── app.py
  ├── ev_range_predictor_reduced.pkl
  ├── requirements.txt
  ├── README.md
  └── assets/  # Optional folder for visuals or icons

author:
  name: "Your Name"
  linkedin: "https://www.linkedin.com/"
  portfolio: "https://yourwebsite.com"
