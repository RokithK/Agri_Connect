import google.generativeai as genai
import re

class Chatbot:
    def __init__(self, crop_price_model=None, crop_rec_model=None, label_encoder=None, crop_price_data=None, crop_recommendation_data=None):
        #Place your API key
        genai.configure(api_key=self.API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Store the models and data from app.py for integration
        self.crop_price_model = crop_price_model
        self.crop_rec_model = crop_rec_model
        self.label_encoder = label_encoder
        self.crop_price_data = crop_price_data
        self.crop_recommendation_data = crop_recommendation_data

        # System prompt to set the context for AgriBot
        self.system_prompt = """
        You are AgriBot, an AI-powered assistant for the Agri-Connect web application, designed to help farmers make smarter decisions. Your primary focus is on agriculture, including crop price prediction, crop recommendations, weather impacts, sustainable farming practices, and general farming advice. Agri-Connect has two main tools: HCrop (for crop price prediction) and HWeather (for crop recommendation based on soil and weather conditions). When answering questions:
        - Provide accurate, practical, and concise advice tailored to farmers.
        - If the question is about crop prices, explain factors affecting prices or guide the user to use the HCrop tool.
        - If the question is about crop recommendations, explain relevant factors (e.g., soil nutrients, weather) or guide the user to use the HWeather tool.
        - If the question is outside your expertise, suggest using Agri-Connect's tools or provide a general farming tip.
        - Use a friendly and supportive tone, as if you're a trusted advisor for farmers.
        """

    def get_response(self, user_input):
        try:
            # Check for specific types of questions
            user_input_lower = user_input.lower()

            # Crop Price Prediction Query
            if re.search(r"(price|cost|market|sell).*?(crop|wheat|rice|maize|soybean|corn)", user_input_lower):
                return self.handle_price_query(user_input)

            # Crop Recommendation Query
            elif re.search(r"(what|which).*?(crop|plant|grow).*?(soil|weather|temperature|rainfall|nitrogen)", user_input_lower):
                return self.handle_recommendation_query(user_input)

            # General Agri-Connect Query
            elif "agri-connect" in user_input_lower or "what do you do" in user_input_lower:
                return """
                I’m AgriBot, your assistant for Agri-Connect! Agri-Connect helps farmers like you with two powerful tools:  
                - **HCrop**: Predicts crop prices based on factors like rainfall, demand, and market trends.  
                - **HWeather**: Recommends the best crops to plant based on soil nutrients, temperature, humidity, and rainfall.  
                I’m here to answer your farming questions, guide you on using these tools, and provide tips for smarter farming. What’s on your mind?
                """

            # Default: Use the generative model with the system prompt
            else:
                prompt = f"{self.system_prompt}\nUser: {user_input}\nAgriBot:"
                response = self.model.generate_content(prompt)
                return response.text if response else "Sorry, I couldn’t process that. Can you try asking in a different way?"

        except Exception as e:
            return f"Sorry, I ran into an issue: {str(e)}. Please try asking again or use Agri-Connect’s tools for more precise answers!"

    def handle_price_query(self, user_input):
        # Extract crop name if possible
        crops = ["wheat", "rice", "maize", "soybean", "corn"]
        user_input_lower = user_input.lower()
        crop = next((c for c in crops if c in user_input_lower), None)

        if crop and self.crop_price_model and self.label_encoder:
            # Example: Use the model to predict a price (simplified for demo purposes)
            # In a real scenario, you'd need user inputs for month, rainfall, demand, etc.
            return f"To predict the price of {crop}, I’d need details like the month, rainfall, and demand. You can use the **HCrop** tool on Agri-Connect to input these details and get an accurate prediction! For now, I can tell you that crop prices are influenced by factors like weather, demand-supply dynamics, and market trends. Would you like to know more about these factors?"
        else:
            return """
            Crop prices depend on factors like rainfall, demand, market trends, and the time of year. For an accurate prediction, I recommend using the **HCrop** tool on Agri-Connect. You can input details like the crop type, month, rainfall, and demand to get a precise forecast. Would you like to learn more about how these factors affect prices?
            """

    def handle_recommendation_query(self, user_input):
        # Extract conditions if possible
        user_input_lower = user_input.lower()
        conditions = []
        if "nitrogen" in user_input_lower:
            conditions.append("high nitrogen levels")
        if "hot" in user_input_lower or "humid" in user_input_lower:
            conditions.append("hot and humid weather")
        if "rainfall" in user_input_lower:
            conditions.append("specific rainfall conditions")

        if conditions and self.crop_rec_model:
            # Example: Use the model to recommend a crop (simplified for demo purposes)
            return f"Based on your conditions ({', '.join(conditions)}), I can suggest some crops, but for the best recommendation, use the **HWeather** tool on Agri-Connect. It analyzes soil nutrients (like nitrogen, phosphorus, potassium), temperature, humidity, and rainfall to recommend the best crops. For now, crops like corn and tomatoes often do well in nitrogen-rich soils, while peppers and okra thrive in hot, humid conditions. Want to know more about soil preparation?"
        else:
            return """
            To recommend the best crops, I need details like soil nutrients (nitrogen, phosphorus, potassium), temperature, humidity, and rainfall. You can use the **HWeather** tool on Agri-Connect to input these details and get a tailored recommendation. Generally, crops like corn, tomatoes, and leafy greens do well in nitrogen-rich soils, while peppers and okra thrive in hot, humid climates. Would you like tips on preparing your soil?
            """
