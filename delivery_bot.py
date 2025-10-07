import streamlit as st
import pandas as pd
import joblib

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Delivery Time Prediction", page_icon="🚚", layout="wide")

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("🚚 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Delivery Prediction", "Projects", "About", "Contact"])

# ---------------------- LOAD MODEL ----------------------
try:
    model = joblib.load('delivery_model.pkl')
    model_columns = joblib.load('model_columns.pkl')
except Exception as e:
    st.error("⚠️ Could not load model files. Please make sure 'delivery_model.pkl' and 'model_columns.pkl' exist.")
    st.stop()

# ---------------------- HOME PAGE ----------------------
if page == "Home":
    st.title("Welcome to Smart Delivery AI 🚀")
    st.markdown("""
    ### Your intelligent assistant for predicting delivery times!
    Use the sidebar to navigate:
    - 🧠 **Delivery Prediction:** Get instant AI-based delivery time estimates.  
    - 💼 **Projects:** See more of our AI solutions.  
    - 👨‍💻 **About:** Learn who we are.  
    - 📬 **Contact:** Reach out for collaborations.
    """)

# ---------------------- DELIVERY PREDICTION PAGE ----------------------
elif page == "Delivery Prediction":
    st.title("🚚 Delivery Time Prediction AI")
    st.write("Enter order details below to predict delivery time:")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Enter Order Details")
        distance = st.number_input("📏 Distance (km)", min_value=0.0, value=5.0)
        prep_time = st.number_input("⏱ Preparation Time (min)", min_value=0, value=10)
        courier_exp = st.number_input("👨‍✈️ Courier Experience (yrs)", min_value=0, value=2)

        st.write("### Select Weather")
        weather_options = ['Sunny', 'Rainy', 'Foggy', 'Snowy', 'Windy']
        weather = st.selectbox("☀️ Weather", weather_options)

    with col2:
        st.write("### Select Traffic Level")
        traffic_options = ['Low', 'Medium', 'High']
        traffic = st.selectbox("🚦 Traffic Level", traffic_options)

        st.write("### Select Time of Day")
        time_options = ['Morning', 'Afternoon', 'Evening', 'Night']
        time_of_day = st.selectbox("🕒 Time of Day", time_options)

        st.write("### Select Vehicle Type")
        vehicle_options = ['Bike', 'Car', 'Van', 'Scooter']
        vehicle = st.selectbox("🚗 Vehicle Type", vehicle_options)

    st.markdown("---")

    with st.expander("See Input Summary"):
        st.write("### Summary of Inputs")
        st.warning(f"Distance: {distance} km")
        st.warning(f"Preparation Time: {prep_time} min")
        st.warning(f"Weather: {weather}")
        st.warning(f"Traffic Level: {traffic}")
        st.warning(f"Time of Day: {time_of_day}")
        st.warning(f"Vehicle Type: {vehicle}")

    # Prepare input
    user_input = {
        'Distance_km': distance,
        'Preparation_Time_min': prep_time,
        'Courier_Experience_yrs': courier_exp,
        f'Weather_{weather}': 1,
        f'Traffic_Level_{traffic}': 1,
        f'Time_of_Day_{time_of_day}': 1,
        f'Vehicle_Type_{vehicle}': 1
    }

    # Function to prepare input
    def prepare_input(user_input, model_columns):
        df = pd.DataFrame([user_input])
        for col in model_columns:
            if col not in df.columns:
                df[col] = 0
        return df[model_columns]

    # Prediction button
    if st.button("Predict Delivery Time"):
        sample_df = prepare_input(user_input, model_columns)
        pred = model.predict(sample_df)[0]
        st.success(f"🕒 Predicted Delivery Time: **{round(pred, 2)} minutes**")

# ---------------------- PROJECTS PAGE ----------------------
elif page == "Projects":
    st.title("💼 Our AI Projects")
    st.markdown("""
    - 📦 **Delivery Time Prediction:** Estimate delivery durations with real-time AI.
    - 🏪 **Inventory Optimizer:** Helps shops restock efficiently.
    - 🚗 **Route Optimizer:** Plans fastest delivery routes.
    - 📊 **Demand Forecasting:** Predicts customer order patterns.
    """)

# ---------------------- ABOUT PAGE ----------------------
elif page == "About":
    st.title("👨‍💻 About the Developer")
    st.markdown("""
    Hi! I'm **Nizar**, a passionate developer who loves building intelligent, data-driven web apps.  
    I focus on blending **AI + Streamlit** to create useful tools for everyday use.
    """)

# ---------------------- CONTACT PAGE ----------------------
elif page == "Contact":
    st.title("📬 Contact")
    st.markdown("Let's collaborate or talk about new projects!")
    st.info("Email: yourname@example.com")
    st.info("GitHub: [github.com/yourprofile](https://github.com/yourprofile)")
    st.info("LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)")
