import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Stress Prediction Dashboard", layout="wide")

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("stress_model.pkl")

st.title("🧠 Smart Stress Prediction Dashboard")
st.write("AI-powered stress analysis with explainability and health insights")

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

# =============================
# INPUTS
# =============================
with col1:
    st.header("📥 Daily Inputs")

    work_hours = st.number_input("🕒 Work Hours", 0, 24, 8)
    sleep_hours = st.number_input("🛌 Sleep Hours", 0, 24, 7)
    heart_rate = st.number_input("❤️ Heart Rate", 40, 200, 75)
    screen_time = st.number_input("💻 Screen Time", 0, 24, 5)
    exercise_hours = st.number_input("🏃 Exercise Hours", 0, 10, 1)

# =============================
# STRESS INDEX
# =============================
stress_index = (
    0.4 * work_hours * 10 +
    0.3 * (heart_rate - 60) +
    0.2 * screen_time * 10 -
    0.1 * sleep_hours * 10
)

stress_index = (stress_index / 48) * 100
stress_index = max(0, min(100, stress_index))

# =============================
# PREDICTION
# =============================
input_data = pd.DataFrame({
    "WorkHours": [work_hours],
    "SleepHours": [sleep_hours],
    "HeartRate": [heart_rate],
    "ScreenTime": [screen_time],
    "ExerciseHours": [exercise_hours],
    "StressIndex": [stress_index]
})

prediction = model.predict(input_data)[0]

stress_map = {
    0: ("Low Stress 😌", "green"),
    1: ("Medium Stress 😐", "orange"),
    2: ("High Stress 😰", "red")
}

stress_text, color = stress_map[prediction]

# =============================
# OUTPUT DASHBOARD
# =============================
with col2:
    st.header("📊 Stress Dashboard")

    st.markdown(f"<h2 style='color:{color};'>{stress_text}</h2>", unsafe_allow_html=True)
    st.write(f"Stress Index: **{stress_index:.2f}%**")

    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_index,
        title={"text": "Stress Index"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 35], "color": "lightgreen"},
                {"range": [35, 65], "color": "lightyellow"},
                {"range": [65, 100], "color": "lightcoral"},
            ],
        },
    ))
    st.plotly_chart(fig, use_container_width=True)

# =============================
# EXPLAINABLE AI (WHY STRESS?)
# =============================
st.subheader("🔍 Why is your stress high?")

factors = {
    "Work Hours": work_hours * 10,
    "Heart Rate": heart_rate - 60,
    "Screen Time": screen_time * 10,
    "Low Sleep": (8 - sleep_hours) * 10,
    "Low Exercise": (2 - exercise_hours) * 10
}

main_reason = max(factors, key=factors.get)
st.warning(f"Primary stress contributor: **{main_reason}**")

# =============================
# PERSONALIZED ACTION PLAN
# =============================
st.subheader("🧠 Personalized Action Plan")

if sleep_hours < 6:
    st.write("🛌 Increase sleep to at least 7–8 hours.")
if work_hours > 9:
    st.write("🕒 Reduce work hours or add short breaks.")
if screen_time > 6:
    st.write("💻 Reduce screen exposure, especially before sleep.")
if exercise_hours < 1:
    st.write("🏃 Try light exercise or walking daily.")

# =============================
# BURNOUT RISK PREDICTION
# =============================
st.subheader("🔥 Burnout Risk Score")

burnout_risk = (
    (work_hours * 0.4) +
    ((8 - sleep_hours) * 0.4) +
    (screen_time * 0.2)
) * 10

burnout_risk = max(0, min(100, burnout_risk))

st.progress(int(burnout_risk))
st.write(f"Estimated Burnout Risk: **{int(burnout_risk)}%**")

# =============================
# STRESS HISTORY TRACKING
# =============================
st.subheader("📈 Stress Trend Over Time")

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append(stress_index)
st.line_chart(st.session_state.history)
