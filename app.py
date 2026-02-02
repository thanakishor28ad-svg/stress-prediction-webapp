# app.py
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load('stress_model.pkl')

st.title("🌟 Stress Level Prediction Dashboard")
st.write("Enter your daily metrics to predict stress level and visualize your stress index.")

# -----------------------------
# User Inputs
# -----------------------------
work_hours = st.number_input("🕒 Work Hours per Day", min_value=0, max_value=24, value=8)
sleep_hours = st.number_input("🛌 Sleep Hours per Day", min_value=0, max_value=24, value=7)
heart_rate = st.number_input("❤️ Average Heart Rate", min_value=40, max_value=200, value=75)
screen_time = st.number_input("💻 Screen Time (hours/day)", min_value=0, max_value=24, value=5)
exercise_hours = st.number_input("🏃 Exercise Hours per Day", min_value=0, max_value=10, value=1)

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
stress_index = max(0, min(100, stress_index))  # Clip to 0-100

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

# -----------------------------
# Map stress level to text, color, advice
# -----------------------------
stress_map = {
    0: ("Low Stress 😌", "green", "You're doing great! Keep maintaining your healthy habits."),
    1: ("Medium Stress 😐", "orange", "Moderate stress detected. Consider short breaks and relaxation."),
    2: ("High Stress 😰", "red", "High stress detected! Take immediate steps to relax and reduce workload.")
}

stress_text, color, advice = stress_map[prediction]

# -----------------------------
# Display Stress Level
# -----------------------------
st.markdown(f"<h2 style='color:{color};'>{stress_text}</h2>", unsafe_allow_html=True)
st.info(advice)

# -----------------------------
# Display Stress Index
# -----------------------------
st.write(f"Calculated Stress Index: {round(stress_index, 2)}")

# -----------------------------
# Display Stress Gauge (Bar Chart)
# -----------------------------
fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = stress_index,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Stress Index (%)"},
    gauge = {
        'axis': {'range': [0, 100]},
        'bar': {'color': color},
        'steps': [
            {'range': [0, 35], 'color': "lightgreen"},
            {'range': [35, 65], 'color': "lightyellow"},
            {'range': [65, 100], 'color': "lightcoral"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': stress_index}
    }
))
st.plotly_chart(fig)
