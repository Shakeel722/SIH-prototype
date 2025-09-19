"""
Streamlit prototype for:
Smart Crop Advisory System (Punjab) - demo/proof-of-concept with Real-time Chatbot
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import random
import datetime
import json
import time

# --------------------
# Page settings
# --------------------
st.set_page_config(page_title="Smart Crop Advisory (Punjab) - Prototype", layout="wide")

# --------------------
# Chatbot Functions
# --------------------

def initialize_chat():
    """Initialize chat session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Smart Crop Advisory assistant. I can help you with soil advice, weather alerts, pest identification, and market prices. How can I help you today?", "timestamp": datetime.datetime.now()}
        ]

def process_chat_message(user_input):
    """Process user message and generate response"""
    user_input_lower = user_input.lower()
    
    # Intent detection based on keywords
    if any(word in user_input_lower for word in ["soil", "fertilizer", "ph", "मिट्टी", "ਮਿੱਟੀ"]):
        return handle_soil_query(user_input)
    elif any(word in user_input_lower for word in ["weather", "rain", "temperature", "मौसम", "ਮੌਸਮ"]):
        return handle_weather_query(user_input)
    elif any(word in user_input_lower for word in ["pest", "disease", "insect", "कीट", "ਕੀੜੇ"]):
        return handle_pest_query(user_input)
    elif any(word in user_input_lower for word in ["price", "market", "mandi", "कीमत", "ਕੀਮਤ"]):
        return handle_market_query(user_input)
    elif any(word in user_input_lower for word in ["crop", "wheat", "paddy", "rice", "फसल", "ਫਸਲ"]):
        return handle_crop_query(user_input)
    else:
        return handle_general_query(user_input)

def handle_soil_query(query):
    """Handle soil-related queries"""
    responses = [
        "For soil testing, I recommend checking your soil pH first. Most crops in Punjab prefer pH 6.0-7.5. Would you like specific fertilizer recommendations for your crop?",
        "Soil health is crucial! Consider organic matter content, NPK levels, and micronutrients. What crop are you planning to grow?",
        "Punjab soils often need balanced fertilization. Upload your soil test report or tell me your crop type for specific advice."
    ]
    return random.choice(responses)

def handle_weather_query(query):
    """Handle weather-related queries"""
    # Simulate real-time weather data
    weather_conditions = [
        "Current weather looks favorable for farming. No immediate alerts for your area.",
        "Heavy rainfall expected in next 24-48 hours. Consider postponing irrigation and ensure proper drainage.",
        "High temperatures predicted this week. Increase irrigation frequency and consider mulching.",
        "Favorable weather conditions for the next 5 days. Good time for field operations."
    ]
    return random.choice(weather_conditions)

def handle_pest_query(query):
    """Handle pest and disease queries"""
    responses = [
        "Common pests in Punjab include aphids, brown plant hopper, and stem borer. Can you describe the symptoms or upload an image?",
        "For pest identification, I'd need to see the affected plant parts. Upload an image and I'll help identify the issue.",
        "Preventive measures include proper crop rotation, biological pest control, and timely application of recommended pesticides."
    ]
    return random.choice(responses)

def handle_market_query(query):
    """Handle market price queries"""
    crops = ["wheat", "paddy", "maize", "mustard"]
    crop = random.choice(crops)
    price = random.randint(1500, 2500)
    return f"Current {crop} prices in Punjab mandis average around ₹{price} per quintal. Prices vary by quality and location. Would you like specific mandi information?"

def handle_crop_query(query):
    """Handle crop-specific queries"""
    responses = [
        "Wheat is Punjab's major rabi crop. Best sowing time is November-December. Need specific cultivation advice?",
        "Rice (paddy) is the main kharif crop. Requires careful water management. What specific information do you need?",
        "For crop selection, consider soil type, water availability, and market demand. What's your current situation?"
    ]
    return random.choice(responses)

def handle_general_query(query):
    """Handle general queries"""
    responses = [
        "I can help you with soil testing, weather alerts, pest identification, market prices, and crop advisory. What would you like to know?",
        "I'm here to assist with all your farming needs. You can ask about fertilizers, weather, pests, market prices, or crop management.",
        "Feel free to ask me about soil health, weather conditions, pest control, or market information. How can I help?"
    ]
    return random.choice(responses)

# --------------------
# Original Helper functions (mock logic for demo)
# --------------------

def mock_soil_advice(soil_ph, crop):
    """
    Return soil and fertilizer recommendations based on soil pH and crop.
    - Uses simple rule-based conditions (not real expert system).
    - For demo only, replace with real soil test data + recommendation engine.
    """
    rec = []
    ph = soil_ph

    # Basic soil pH guidance
    if ph < 5.5:
        rec.append("Add lime (calcium carbonate) to raise pH.")
    elif ph > 7.8:
        rec.append("Consider sulfur to lower pH slowly.")
    else:
        rec.append("pH looks suitable for most crops.")

    # Crop-specific fertilizer guidance
    if crop.lower() in ["wheat", "गेहूँ", "ਗੰਙੂ"]:
        rec.append("Apply N:P:K -> 100:50:30 kg/ha as baseline (adjust per soil test).")
    elif crop.lower() in ["paddy", "rice", "ਧਾਨ"]:
        rec.append("Apply N:P:K -> 120:60:40 kg/ha baseline; split nitrogen into 3 doses.")
    else:
        rec.append("Apply balanced NPK; consult soil test for exact doses.")
    return rec

def mock_weather_alerts(location):
    """
    Return a mock weather alert for a given location.
    - Randomly picks from a small set of pre-defined alerts.
    - In final version, replace with real weather API.
    """
    events = [
        ("Heavy rainfall expected in next 24 hours. Delay irrigation.", "rain"),
        ("Heatwave warning: protect seedlings and increase mulching.", "heat"),
        ("No critical weather alerts for next 5 days.", "ok"),
        ("Cold night expected; take frost protection measures.", "cold"),
    ]
    # Probability weights → more chance of "OK" message
    weights = [0.15, 0.15, 0.5, 0.2]
    chosen = random.choices(events, weights)[0]
    return chosen

def mock_pest_detector(image_bytes):
    """
    Mock pest/disease detector using image input.
    - Randomly returns one detection with confidence and advice.
    - Replace with ML model trained on crop disease dataset.
    """
    pests = [
        ("Brown spot (fungal)", 0.86, "Use recommended fungicide; remove infected leaves."),
        ("Leaf blast (rice)", 0.79, "Isolate field area; apply blast-specific fungicide."),
        ("Aphids infestation", 0.72, "Use neem oil spray or introduce ladybird beetles."),
        ("No major pest detected", 0.92, "Looks healthy; monitor for 7 days."),
    ]
    return random.choice(pests)

def get_sample_market_prices():
    """
    Return a mock dataframe with mandi market prices for major crops.
    - Currently hardcoded sample values.
    - Replace with real mandi price API for production.
    """
    data = {
        "Commodity": ["Wheat (Per Quintal)", "Paddy (Per Quintal)", "Maize (Per Quintal)", "Mustard (Per Quintal)"],
        "Top Mandi (example)": [2150, 1900, 1700, 4600],
        "Nearby Avg (example)": [2100, 1850, 1680, 4500],
        "Date": [str(datetime.date.today())]*4
    }
    return pd.DataFrame(data)

# --------------------
# Initialize chat
# --------------------
initialize_chat()

# --------------------
# UI Layout
# --------------------

st.title("🌾 Smart Crop Advisory — Prototype (Punjab) with AI Chatbot")

# Add tabs for better organization
tab1, tab2 = st.tabs(["🤖 AI Assistant Chat", "📊 Detailed Analysis Tools"])

with tab1:
    st.header("🌾 AI Crop Advisory Chatbot")
    st.markdown("Ask me anything about farming, soil, weather, pests, or market prices!")
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(f"⏰ {message['timestamp'].strftime('%H:%M:%S')}")
    
    # Chat input
    if prompt := st.chat_input("Type your farming question here... (e.g., 'What fertilizer for wheat?', 'Weather forecast?', 'Pest in my crop')"):
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt, 
            "timestamp": datetime.datetime.now()
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            st.caption(f"⏰ {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)  # Simulate processing time
                response = process_chat_message(prompt)
                st.write(response)
                timestamp = datetime.datetime.now()
                st.caption(f"⏰ {timestamp.strftime('%H:%M:%S')}")
        
        # Add assistant message to session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response, 
            "timestamp": timestamp
        })
    
    # Quick action buttons
    st.markdown("### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌱 Soil Advice"):
            quick_response = "I can help with soil testing and fertilizer recommendations. What's your soil pH and which crop are you growing?"
            st.session_state.messages.append({
                "role": "assistant",
                "content": quick_response,
                "timestamp": datetime.datetime.now()
            })
            st.rerun()
    
    with col2:
        if st.button("🌤️ Weather Alert"):
            quick_response = handle_weather_query("weather")
            st.session_state.messages.append({
                "role": "assistant",
                "content": quick_response,
                "timestamp": datetime.datetime.now()
            })
            st.rerun()
    
    with col3:
        if st.button("🐛 Pest Help"):
            quick_response = "Upload an image of the affected plant or describe the symptoms. I'll help identify pests and suggest treatment."
            st.session_state.messages.append({
                "role": "assistant",
                "content": quick_response,
                "timestamp": datetime.datetime.now()
            })
            st.rerun()
    
    with col4:
        if st.button("💰 Market Prices"):
            quick_response = handle_market_query("price")
            st.session_state.messages.append({
                "role": "assistant",
                "content": quick_response,
                "timestamp": datetime.datetime.now()
            })
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Smart Crop Advisory assistant. How can I help you today?", "timestamp": datetime.datetime.now()}
        ]
        st.rerun()

with tab2:
    # Language toggle for demo
    lang = st.sidebar.selectbox("Select language for demo labels", ["English", "Punjabi (sample)"])
    
    # Small helper function to switch text based on language choice
    def t(en, pa):
        return pa if lang.startswith("Punjabi") else en
    
    # Collapsible project summary section
    with st.expander("Project summary (click to open)", expanded=False):
        st.markdown("""
    **Problem:** Small & marginal farmers in Punjab face soil degradation, overuse of chemicals, water stress and limited access to localized, real-time advisory in Punjabi/Hindi.  
    
    **Solution (prototype):** Multilingual AI-backed mobile/chatbot to provide soil & fertilizer guidance, weather alerts, pest detection from images, market price insight, and voice-friendly interactions (mocked here).  
    This demo shows the *concept and flow* for a college-level prototype presentation.
    """)
    
    # --------------------
    # Two-column main layout
    # --------------------
    left, right = st.columns([2,1])
    
    # ---- LEFT side: Main demo flow ----
    with left:
        st.header(t("Demo: Farmer Interaction Flow", "ਡੈਮੋ: ਕਿਸਾਨ ਇੰਟਰੈਕਸ਼ਨ ਫਲੋ"))
    
        # Soil advisory
        st.subheader(t("1) Soil & Fertilizer Recommendation", "1) ਮਿੱਟੀ ਅਤੇ ਖ਼ਾਦ ਸਲਾਹ"))
        col1, col2 = st.columns(2)
    
        # Column 1: user inputs for soil pH and crop
        with col1:
            soil_ph = st.number_input(t("Enter soil pH (example: 6.5)", "ਮਿੱਟੀ ਦਾ pH ਦਰਜ ਕਰੋ (ਉਦਾਹਰਨ: 6.5)"),
                                      min_value=3.0, max_value=9.0, value=6.5, step=0.1)
            crop = st.text_input(t("Preferred crop (e.g., Wheat / Paddy)", "ਫਸਲ (ਉਦਾਹਰਨ: ਗੰਙੂ / ਧਾਨ)"), value="Wheat")
            if st.button(t("Get Soil Advice", "ਮਿੱਟੀ ਸਲਾਹ ਲਓ")):
                rec = mock_soil_advice(soil_ph, crop)
                st.success(t("Recommendations:", "ਸੁਝਾਵ:"))
                for r in rec:
                    st.write("- " + r)
    
        # Column 2: optional soil test image upload
        with col2:
            st.subheader(t("Soil test / sample screenshot", "ਮਿੱਟੀ ਟੈਸਟ / ਨਮੂਨਾ"))
            st.info(t("Upload soil test image or paste values in left panel (this is a prototype).",
                      "ਮਿੱਟੀ ਟੈਸਟ ਦੀ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ ਜਾਂ ਇੱਥੇ ਮੁੱਲ ਦੱਵੋ (ਪ੍ਰੋਟੋਟਾਇਪ)।"))
            uploaded = st.file_uploader(t("Upload soil test image (optional)", "ਮਿੱਟੀ ਟੈਸਟ ਅਪਲੋਡ ਕਰੋ (ਵਿਕਲਪਿਕ)"), 
                                        type=["png","jpg","jpeg"])
            if uploaded:
                st.image(uploaded, caption=t("Uploaded soil report", "ਅਪਲੋਡ ਕੀਤੀ ਮਿੱਟੀ ਰਿਪੋਰਟ"), use_column_width=True)
    
        # Weather alerts
        st.markdown("---")
        st.subheader(t("2) Weather Alerts (mock)", "2) ਮੌਸਮ ਸੂਚਨਾ (ਮੌਕ)"))
        loc = st.text_input(t("Enter location / village (example: Ludhiana)", 
                              "ਸਟੇਸ਼ਨ/ਪਿੰਡ ਦਰਜ ਕਰੋ (ਉਦਾਹਰਨ: ਲੁਧਿਆਣਾ)"), value="Ludhiana")
        if st.button(t("Check Weather Alerts", "ਮੌਸਮ ਚੈੱਕ ਕਰੋ")):
            evt, tag = mock_weather_alerts(loc)
            if tag == "ok":
                st.success(evt)
            else:
                st.warning(evt)
    
        # Pest detection
        st.markdown("---")
        st.subheader(t("3) Pest/Disease Detection (image)", "3) ਕੀੜੇ/ਰੋਗ ਪਛਾਣ (ਤਸਵੀਰ)"))
        pest_file = st.file_uploader(t("Upload crop leaf / affected part image", 
                                       "ਕਿਰਪਾ ਕਰ ਕੇ ਪੱਤੇ/ਪ੍ਰਭਾਵਿਤ ਹਿੱਸੇ ਦੀ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ"), 
                                     type=["png","jpg","jpeg"])
        if pest_file:
            image_bytes = pest_file.read()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            st.image(image, caption=t("Uploaded image", "ਅਪਲੋਡ ਕੀਤੀ ਤਸਵੀਰ"), use_column_width=True)
            if st.button(t("Analyze Image", "ਤਸਵੀਰ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ")):
                label, conf, advice = mock_pest_detector(image_bytes)
                st.write(f"**{t('Detection','ਪਛਾਣ')}:** {label}")
                st.write(f"**{t('Confidence','ਭਰੋਸਾ')}:** {conf*100:.1f}%")
                st.write(f"**{t('Advice','ਸਲਾਹ')}:** {advice}")
    
        # Market price tracker
        st.markdown("---")
        st.subheader(t("4) Market Price Tracker (sample)", "4) ਮਾਰਕੀਟ ਕੀਮਤ ਟ੍ਰੈਕਰ (ਨਮੂਨਾ)"))
        df_prices = get_sample_market_prices()
        st.dataframe(df_prices, use_container_width=True)
        st.caption(t("Note: These are mock prices to demonstrate the feature in prototype.", 
                     "ਨੋਟ: ਇਹ ਮੌਕ ਕੀਮਤਾਂ ਹਨ"))
    
    # ---- RIGHT side: Feature summary and feedback ----
    with right:
        st.header(t("Quick Features & Flow", "ਤਰਤੀਬ ਅਤੇ ਫੀਚਰ"))
        st.markdown(f"""
    - {t('🤖 Real-time AI Chatbot for instant help', '🤖 ਰੀਅਲ-ਟਾਈਮ AI ਚੈਟਬਾਟ')}
    - {t('Multilingual UI (Punjabi/Hindi/English).', 'ਬਹੁਭਾਸ਼ੀ UI (ਪੰਜਾਬੀ/ਹਿੰਦੀ/ਇੰਗਲਿਸ਼)')}
    - {t('Soil-based fertilizer suggestions (rule-based demo).', 'ਮਿੱਟੀ ਅਧਾਰਿਤ ਖ਼ਾਦ ਸੁਝਾਅ (ਨਿਯਮ-ਆਧਾਰਿਤ ਡੈਮੋ)')}
    - {t('Weather alerts (mock).', 'ਮੌਸਮ ਸੂਚਨਾਵਾਂ (ਮੌਕ)')}
    - {t('Pest detection from image (mock classifier).', 'ਤਸਵੀਰ ਤੋਂ ਕੀੜਾ ਪਛਾਣ (ਮੌਕ)')}
    - {t('Market price table (sample data).', 'ਮਾਰਕੀਟ ਕੀਮਤ ਟੇਬਲ (ਨਮੂਨਾ)')}
    - {t('Feedback collection for continuous improvement.', 'ਬਹਿਤਰੀ ਲਈ ਫੀਡਬੈਕ ਇਕੱਠਾ')}
    """)
    
        # Chatbot features
        st.markdown("---")
        st.header("🤖 Chatbot Features")
        st.write("""
        - **Smart Intent Detection**: Understands farming queries
        - **Multilingual Support**: English, Hindi, Punjabi keywords
        - **Quick Actions**: Instant access to common requests  
        - **Real-time Responses**: Immediate assistance
        - **Context Awareness**: Remembers conversation history
        - **Image Integration**: Can guide through pest detection
        """)
    
        # Prototype notes
        st.markdown("---")
        st.header(t("Prototype Notes", "ਪ੍ਰੋਟੋਟਾਇਪ ਨੋਟ"))
        st.write(t(
            "This demo now includes a real-time chatbot interface that farmers can use for instant help. The chatbot uses intent detection to provide relevant responses. In production, integrate with real APIs and ML models.",
            "ਇਸ ਡੈਮੋ ਵਿੱਚ ਹੁਣ ਰੀਅਲ-ਟਾਈਮ ਚੈਟਬਾਟ ਸ਼ਾਮਲ ਹੈ ਜੋ ਕਿਸਾਨ ਤਤਕਾਲ ਮਦਦ ਲਈ ਵਰਤ ਸਕਦੇ ਹਨ।"
        ))
    
        # Feedback form
        st.markdown("---")
        st.subheader(t("Feedback (will save locally)", "ਫੀਡਬੈਕ (ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਸੰਭਾਲਾ ਜਾਵੇਗਾ)"))
        name = st.text_input(t("Your name", "ਤੁਹਾਡਾ ਨਾਮ"))
        comments = st.text_area(t("Comments / suggestions", "ਟਿੱਪਣੀਆਂ / ਸੁਝਾਅ"))
        if st.button(t("Submit Feedback", "ਫੀਡਬੈਕ ਭੇਜੋ")):
            # Save feedback into a local CSV file
            fb = {"time": str(datetime.datetime.now()), "name": name, "comments": comments}
            try:
                import csv, os
                file_exists = os.path.exists("feedback.csv")
                with open("feedback.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["time","name","comments"])
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(fb)
                st.success(t("Thanks! Feedback saved locally as feedback.csv", "ਸ਼ੁਕਰੀਆ! ਫੀਡਬੈਕ feedback.csv ਵਿੱਚ ਸੰਭਾਲ ਲਈ।"))
            except Exception as e:
                st.error("Error saving feedback: " + str(e))

# Footer note
st.markdown("---")
st.caption("Enhanced prototype with real-time chatbot for college SIH selection demo — mock data only. Replace mocks with real services in full project.")