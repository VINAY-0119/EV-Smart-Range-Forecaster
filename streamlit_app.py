import streamlit as st
import pandas as pd
import requests
import joblib
import os
from model_utils import load_model

st.set_page_config(page_title='EV Range Predictor', layout='centered')
st.title('Electric Vehicle Range Predictor')
st.write('Enter vehicle specs and get a range estimate. You can use the built-in model or call a running API.')

# Try to load local model
model_path = os.environ.get('EV_MODEL_PATH', 'ev_range_model.joblib')
model_data = None
try:
    model_data = load_model(model_path)
except Exception as e:
    st.warning(f'Local model not found at {model_path}. You can still call a running API.')

use_api = st.checkbox('Call prediction API instead of local model', value=False)
api_url = st.text_input('API URL (if using API)', value='http://localhost:8000/predict')

if model_data is not None:
    features = model_data['features']
else:
    # fallback: minimal typical features
    features = ['Battery','Efficiency','Fast_charge','Top_speed','acceleration..0.100.','Price.DE.']

st.sidebar.header('Input vehicle specs')
user_input = {}
for f in features:
    # crude type inference for inputs
    if 'charge' in f.lower() or 'fast' in f.lower():
        user_input[f] = st.sidebar.selectbox(f, options=['Yes','No'], index=0)
    elif any(k in f.lower() for k in ['name','model','make']):
        user_input[f] = st.sidebar.text_input(f, value='')
    else:
        user_input[f] = st.sidebar.number_input(f, value=0.0, format='%.3f')

if st.sidebar.button('Predict range'):
    if use_api:
        try:
            resp = requests.post(api_url, json=user_input, timeout=10)
            resp.raise_for_status()
            result = resp.json()
            st.success(f"Predicted Range: {result['prediction']:.2f} km (API)")
        except Exception as e:
            st.error('API call failed: ' + str(e))
    else:
        if model_data is None:
            st.error('No local model available. Train or provide model_path environment variable.')
        else:
            try:
                pred = model_data['pipeline'].predict(pd.DataFrame([user_input]))[0]
                st.success(f"Predicted Range: {pred:.2f} km (Local model)")
            except Exception as e:
                st.error('Prediction failed: ' + str(e))

st.markdown('---')
st.markdown('**Model info**')
if model_data:
    st.write('Target:', model_data['target'])
    st.write('Features used:', model_data['features'])
else:
    st.write('No local model loaded.')
