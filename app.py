from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import os
from chatbot import Chatbot

app = Flask(__name__)
CORS(app)  # Allow frontend to access chatbot API

# Function to clean CSV Data
def clean_csv_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    for col in ['Crop price', 'Demand(Tons)']:
        if col in df.columns:
            df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    
    return df

# Load and preprocess Crop Price data
try:
    crop_price_data = clean_csv_data('data/data.csv')
    crop_price_data['Month'] = crop_price_data['Month'].apply(lambda x: pd.to_datetime(x, format='%B').month)
    
    X_crop_price = crop_price_data[['Month', 'Crop', 'Rainfall', 'Demand(Tons)', 'year']]
    y_crop_price = crop_price_data['Crop price']

    le = LabelEncoder()
    X_crop_price['Crop'] = le.fit_transform(X_crop_price['Crop'])

    crop_price_model = RandomForestRegressor(n_estimators=100, random_state=42)
    crop_price_model.fit(X_crop_price, y_crop_price)

except Exception as e:
    print(f"Error loading crop price data: {e}")

# Load and preprocess Crop Recommendation data
try:
    crop_recommendation_data = clean_csv_data('data/Crop_recommendation.csv')
    X_crop_rec = crop_recommendation_data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y_crop_rec = crop_recommendation_data['label']

    crop_rec_model = RandomForestClassifier(n_estimators=100, random_state=42)
    crop_rec_model.fit(X_crop_rec, y_crop_rec)

except Exception as e:
    print(f"Error loading crop recommendation data: {e}")

# Initialize Chatbot with the models and data
chatbot_instance = Chatbot(
    crop_price_model=crop_price_model,
    crop_rec_model=crop_rec_model,
    label_encoder=le,
    crop_price_data=crop_price_data,
    crop_recommendation_data=crop_recommendation_data
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hcrop', methods=['GET', 'POST'])
def hcrop():
    if request.method == 'POST':
        try:
            month = int(request.form['month'])
            crop = request.form['crop']
            rainfall = float(request.form['rainfall'])
            demand = float(request.form['demand'])
            year = int(request.form['year'])

            if crop not in le.classes_:
                return render_template('hcrop.html', error="Invalid crop name.")

            crop_encoded = le.transform([crop])[0]
            prediction = crop_price_model.predict([[month, crop_encoded, rainfall, demand, year]])[0]

            return render_template('hcrop.html', predicted_price=prediction)

        except Exception as e:
            return render_template('hcrop.html', error=str(e))

    return render_template('hcrop.html')

@app.route('/hweather', methods=['GET', 'POST'])
def hweather():
    if request.method == 'POST':
        try:
            features = [
                float(request.form['nitrogen']),
                float(request.form['phosphorus']),
                float(request.form['potassium']),
                float(request.form['temperature']),
                float(request.form['humidity']),
                float(request.form['ph']),
                float(request.form['rainfall'])
            ]

            prediction = crop_rec_model.predict([features])[0]

            return render_template('hweather.html', recommended_crop=prediction)

        except Exception as e:
            return render_template('hweather.html', error=str(e))

    return render_template('hweather.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Invalid request. Please send a message."})

        user_input = data["message"].strip()
        if not user_input:
            return jsonify({"response": "Please enter a message."})

        response_text = chatbot_instance.get_response(user_input)
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)