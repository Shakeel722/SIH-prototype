"""
Streamlit prototype for:
Smart Crop Advisory System (Punjab) - demo/proof-of-concept
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import random
import datetime

# --------------------
# Page settings
# --------------------
st.set_page_config(page_title="Smart Crop Advisory (Punjab) - Prototype", layout="wide")

# --------------------
# Helper functions (mock logic for demo)
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
# UI Layout
# --------------------

st.title("🌾 Smart Crop Advisory — Prototype (Punjab)")

# Collapsible project summary section
with st.expander("Project summary (click to open)", expanded=True):
    st.markdown("""
**Problem:** Small & marginal farmers in Punjab face soil degradation, overuse of chemicals, water stress and limited access to localized, real-time advisory in Punjabi/Hindi.  

**Solution (prototype):** Multilingual AI-backed mobile/chatbot to provide soil & fertilizer guidance, weather alerts, pest detection from images, market price insight, and voice-friendly interactions (mocked here).  
This demo shows the *concept and flow* for a college-level prototype presentation.
""")

# Language toggle for demo
lang = st.sidebar.selectbox("Select language for demo labels", ["English", "Punjabi (sample)"])

# Small helper function to switch text based on language choice
def t(en, pa):
    return pa if lang.startswith("Punjabi") else en


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
- {t('Multilingual UI (Punjabi/Hindi/English).', 'ਬਹੁਭਾਸ਼ੀ UI (ਪੰਜਾਬੀ/ਹਿੰਦੀ/ਇੰਗਲਿਸ਼)')}
- {t('Soil-based fertilizer suggestions (rule-based demo).', 'ਮਿੱਟੀ ਅਧਾਰਿਤ ਖ਼ਾਦ ਸੁਝਾਅ (ਨਿਯਮ-ਆਧਾਰਿਤ ਡੈਮੋ)')}
- {t('Weather alerts (mock).', 'ਮੌਸਮ ਸੂਚਨਾਵਾਂ (ਮੌਕ)')}
- {t('Pest detection from image (mock classifier).', 'ਤਸਵੀਰ ਤੋਂ ਕੀੜਾ ਪਛਾਣ (ਮੌਕ)')}
- {t('Market price table (sample data).', 'ਮਾਰਕੀਟ ਕੀਮਤ ਟੇਬਲ (ਨਮੂਨਾ)')}
- {t('Feedback collection for continuous improvement.', 'ਬਹਿਤਰੀ ਲਈ ਫੀਡਬੈਕ ਇਕੱਠਾ')}
""")

    # Prototype notes
    st.markdown("---")
    st.header(t("Prototype Notes", "ਪ੍ਰੋਟੋਟਾਇਪ ਨੋਟ"))
    st.write(t(
        "This demo is intentionally simple: it shows the interaction flow you can present to judges. Replace mock logic with real APIs (weather, mandi prices), soil dataset and ML model for pest detection when building a full prototype.",
        "ਇਹ ਡੈਮੋ ਸਧਾਰਨ ਰੱਖੀ ਗਈ ਹੈ: ਇਹ ਉਹ ਇੰਟਰੈਕਸ਼ਨ ਦਿਖਾਉਂਦੀ ਹੈ ਜੋ ਤੁਸੀਂ ਜੱਜਜ਼ ਨੂੰ ਦਿਖਾ ਸਕਦੇ ਹੋ। ਪੂਰੇ ਪ੍ਰੋਟੋਟਾਇਪ ਵਿੱਚ ਮੌਕ ਲਾਜਿਕ ਨੂੰ ਅਸਲੀ APIs (ਮੌਸਮ, ਮੰਡੀ), ਮਿੱਟੀ ਡੇਟਾਸੈੱਟ ਅਤੇ ML ਮਾਡਲ ਨਾਲ ਬਦਲੋ।"
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
            st.success(t("Thanks! Feedback saved locally as feedback.csv", "ਸ਼ੁਕਰੀਆ! ਫੀਡਬੈਕ feedback.csv ਵਿੱਚ ਸੰਭਾਲ ਲਈ।"))
        except Exception as e:
            st.error("Error saving feedback: " + str(e))


# Footer note
st.markdown("---")
st.caption("Prototype created for college SIH selection demo — mock data only. Replace mocks with real services in full project.")