# app.py
import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load('stress_model.pkl')

st.title("Stress Level Prediction")
st.write("Enter your daily metrics to predict stress level.")

# -----------------------------
# User Inputs
# -----------------------------
work_hours = st.number_input("Work Hours per Day", min_value=0, max_value=24, value=8)
sleep_hours = st.number_input("Sleep Hours per Day", min_value=0, max_value=24, value=7)
heart_rate = st.number_input("Average Heart Rate", min_value=40, max_value=200, value=75)
screen_time = st.number_input("Screen Time (hours/day)", min_value=0, max_value=24, value=5)
exercise_hours = st.number_input("Exercise Hours per Day", min_value=0, max_value=10, value=1)

# -----------------------------
# Calculate Stress Index
# -----------------------------
stress_index = (
    0.4 * work_hours * 10 +
    0.3 * (heart_rate - 60) +
    0.2 * screen_time * 10 -
    0.1 * sleep_hours * 10
)

# Rescale based on training data max (48)
stress_index = (stress_index / 48) * 100

# Clip between 0 and 100
stress_index = max(0, min(100, stress_index))

# -----------------------------
# Prepare DataFrame for prediction
# -----------------------------
input_data = pd.DataFrame({
    'WorkHours': [work_hours],
    'SleepHours': [sleep_hours],
    'HeartRate': [heart_rate],
    'ScreenTime': [screen_time],
    'ExerciseHours': [exercise_hours],
    'StressIndex': [stress_index]
})

# -----------------------------
# Predict Stress Level
# -----------------------------
prediction = model.predict(input_data)[0]

stress_map = {0: "Low Stress 😌", 1: "Medium Stress 😐", 2: "High Stress 😰"}
st.subheader("Predicted Stress Level:")
st.write(stress_map[prediction])

# -----------------------------
# Optional: Show Stress Index
# -----------------------------
st.write(f"Calculated Stress Index: {round(stress_index, 2)}")
