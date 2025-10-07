import streamlit as st
import pandas as pd
import joblib

# Page Configuration
st.set_page_config(page_title="Delivery Time Prediction", page_icon="🚚")


page = st.sidebar.radio("Go to", ["Home", "About", "Projects", "Contact"])
if page == "Home":
    st.title("Welcome!")
elif page == "About":
    st.markdown("### About Me")


# Load model and columns
model = joblib.load('delivery_model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Function to prepare user input
def prepare_input(user_input, model_columns):
    df = pd.DataFrame([user_input])
    # Add missing columns with 0
    for col in model_columns:
        if col not in df.columns:
            df[col] = 0
    # Reorder columns to match training
    df = df[model_columns]
    return df

# Streamlit App UI
st.title("Delivery Time Prediction AI")
st.write("Enter order details below to predict delivery time:")
st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    st.write("### Enter Order Details")
    # Inputs
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
    st.warning(f"Distance: {distance} (km)" )
    st.warning(f"Preparation Time: {prep_time} (min)" )
    st.warning(f"Wheater : {weather}")

    # Prepare input dictionary
user_input = {
    'Distance_km': distance,
    'Preparation_Time_min': prep_time,
    'Courier_Experience_yrs': courier_exp,
    f'Weather_{weather}': 1,
    f'Traffic_Level_{traffic}': 1,
    f'Time_of_Day_{time_of_day}': 1,
    f'Vehicle_Type_{vehicle}': 1
    }

# Prediction button
if st.button("Predict Delivery Time"):
    sample_df = prepare_input(user_input, model_columns)
    pred = model.predict(sample_df)[0]
    st.success(f"Predicted Delivery Time: {round(pred, 2)} minutes")
