import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('stress_model.pkl')

st.set_page_config(page_title="Stress Level Predictor", layout="centered")

st.title("🧠 Smart Stress Prediction System")
st.subheader("AI-based Mental Health Monitoring")

st.markdown("---")

# User Inputs
work_hours = st.slider("Work Hours per Day", 1, 14, 8)
sleep_hours = st.slider("Sleep Hours per Day", 1, 10, 6)
heart_rate = st.slider("Average Heart Rate", 60, 130, 80)
screen_time = st.slider("Screen Time (hours)", 1, 12, 5)
exercise_hours = st.slider("Exercise Time (hours)", 0.0, 2.0, 0.5)

# Stress Index Calculation
stress_index = (
    0.3 * work_hours * 10 +
    0.25 * (heart_rate - 60) +
    0.2 * screen_time * 10 -
    0.25 * sleep_hours * 10
)

stress_index = max(0, min(100, stress_index))

st.markdown(f"### 📊 Stress Index: `{int(stress_index)}`")

# Prediction Button
if st.button("🔍 Predict Stress Level"):
    input_data = pd.DataFrame([[work_hours, sleep_hours, heart_rate,
                                screen_time, exercise_hours, stress_index]],
                              columns=['WorkHours','SleepHours','HeartRate',
                                       'ScreenTime','ExerciseHours','StressIndex'])

    prediction = model.predict(input_data)[0]

    if prediction == 0:
        st.success("✅ Stress Level: LOW")
    elif prediction == 1:
        st.warning("⚠️ Stress Level: MEDIUM")
    else:
        st.error("🚨 Stress Level: HIGH")

    # Reasons
    st.markdown("### 📌 Possible Reasons")
    reasons = []
    if work_hours > 8:
        reasons.append("High work hours")
    if sleep_hours < 6:
        reasons.append("Low sleep duration")
    if heart_rate > 90:
        reasons.append("Elevated heart rate")
    if screen_time > 6:
        reasons.append("Excessive screen time")

    for r in reasons:
        st.write("•", r)

    # Recommendations
    st.markdown("### 💡 Recommendations")
    if sleep_hours < 6:
        st.write("• Increase sleep duration")
    if screen_time > 6:
        st.write("• Reduce screen exposure")
    if exercise_hours < 0.5:
        st.write("• Increase physical activity")
