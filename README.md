# 🌾 Agri-Connect: Smart Farming Assistant

**Agri-Connect** is an AI-powered web application designed to support farmers with real-time predictions and recommendations. It features two intelligent modules — **HCrop** for crop price forecasting and **HWeather** for crop recommendation — along with an interactive **AI Chatbot** that provides agriculture-related guidance using a generative model (Gemini/GPT).

---

## 🚀 Features

- 💰 **HCrop** – Predicts crop prices using rainfall, demand, month, and year  
- 🌱 **HWeather** – Recommends the most suitable crop based on soil and weather parameters  
- 🤖 **AgriBot Chatbot** – Interactive AI assistant trained to answer agriculture-related queries  
- 📊 Real-time prediction using **RandomForestClassifier** and **RandomForestRegressor**  
- 🧠 Models trained with **LabelEncoder**, accuracy & R² scoring  
- 🔐 Input validation and error handling  
- 🌐 CORS-enabled API for frontend integration  

---

## 🧠 Machine Learning Models

### HCrop (Crop Price Prediction)
- **Model**: `RandomForestRegressor`
- **Features**: Month, Crop, Rainfall, Demand, Year
- **Target**: Crop Price  
- **Preprocessing**: Label Encoding (Crop), Cleaning with Pandas  
- **Metric**: R² Score

### HWeather (Crop Recommendation)
- **Model**: `RandomForestClassifier`
- **Features**: Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, Rainfall  
- **Target**: Recommended Crop  
- **Metric**: Accuracy Score

---

## 🧠 AI Chatbot (AgriBot)

AgriBot uses a **Generative AI model (Gemini/GPT)** to:
- Answer farming queries about crop prices, weather effects, and soil nutrients  
- Guide users to **HCrop** or **HWeather** tools when specific predictions are needed  
- Provide general farming advice and sustainable practices  
- Maintain a friendly and supportive tone  

---

## 🛠 How It Works

1. **User Input**: Data entered via forms (crop type, weather, soil values, etc.)
2. **Prediction**: Trained models generate price forecasts or crop recommendations
3. **Chatbot**: Users can interact with AgriBot for personalized farming help
4. **Response**: Results are displayed or sent back as chatbot responses (JSON)

---

## 📁 Project Structure

