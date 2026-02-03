import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Smart Stress Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ======================================================
# CUSTOM CSS (Glassmorphism + UI polish)
# ======================================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.card {
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
}
.subtitle {
    text-align:center;
    font-size:18px;
    opacity:0.85;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD MODEL
# ======================================================
model = joblib.load("stress_model.pkl")

# ======================================================
# HERO SECTION
# ======================================================
st.markdown("""
<div class="card">
<div class="title">🧠 Smart Stress Analyzer</div>
<div class="subtitle">
AI-powered stress prediction with explainable insights & health guidance
</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR INPUTS (GUI)
# ======================================================
st.sidebar.title("⚙️ Daily Inputs")

work_hours = st.sidebar.slider("🕒 Work Hours", 0, 24, 8)
sleep_hours = st.sidebar.slider("🛌 Sleep Hours", 0, 24, 7)
heart_rate = st.sidebar.slider("❤️ Heart Rate", 40, 200, 75)
screen_time = st.sidebar.slider("💻 Screen Time", 0, 24, 5)
exercise_hours = st.sidebar.slider("🏃 Exercise Hours", 0, 10, 1)

theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    body { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ======================================================
# STRESS INDEX CALCULATION
# ======================================================
stress_index = (
    0.4 * work_hours * 10 +
    0.3 * (heart_rate - 60) +
    0.2 * screen_time * 10 -
    0.1 * sleep_hours * 10
)

stress_index = (stress_index / 48) * 100
stress_index = max(0, min(100, stress_index))

# ======================================================
# MODEL PREDICTION
# ======================================================
input_df = pd.DataFrame({
    "WorkHours": [work_hours],
    "SleepHours": [sleep_hours],
    "HeartRate": [heart_rate],
    "ScreenTime": [screen_time],
    "ExerciseHours": [exercise_hours],
    "StressIndex": [stress_index]
})

prediction = model.predict(input_df)[0]

stress_map = {
    0: ("Low Stress 😌", "green"),
    1: ("Medium Stress 😐", "orange"),
    2: ("High Stress 😰", "red")
}

stress_text, color = stress_map[prediction]

# ======================================================
# MAIN DASHBOARD
# ======================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
    <h2 style="color:{color};">{stress_text}</h2>
    <h4>Stress Index: {stress_index:.2f}%</h4>
    </div>
    """, unsafe_allow_html=True)

    # Explainable AI
    st.markdown("<div class='card'><h3>🔍 Why are you stressed?</h3>", unsafe_allow_html=True)

    factors = {
        "Work Hours": work_hours * 10,
        "Heart Rate": heart_rate - 60,
        "Screen Time": screen_time * 10,
        "Low Sleep": (8 - sleep_hours) * 10,
        "Low Exercise": (2 - exercise_hours) * 10
    }

    main_reason = max(factors, key=factors.get)
    st.warning(f"Primary contributor: **{main_reason}**")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'><h3>📊 Stress Gauge</h3>", unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_index,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 35], "color": "lightgreen"},
                {"range": [35, 65], "color": "lightyellow"},
                {"range": [65, 100], "color": "lightcoral"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# PERSONALIZED ACTION PLAN
# ======================================================
st.markdown("<div class='card'><h3>🧠 Personalized Action Plan</h3>", unsafe_allow_html=True)

if sleep_hours < 6:
    st.write("🛌 Increase sleep to 7–8 hours.")
if work_hours > 9:
    st.write("🕒 Reduce work hours and take breaks.")
if screen_time > 6:
    st.write("💻 Reduce screen usage before sleep.")
if exercise_hours < 1:
    st.write("🏃 Add light exercise or walking daily.")

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# BURNOUT RISK
# ======================================================
burnout_risk = (
    (work_hours * 0.4) +
    ((8 - sleep_hours) * 0.4) +
    (screen_time * 0.2)
) * 10

burnout_risk = max(0, min(100, burnout_risk))

st.markdown("<div class='card'><h3>🔥 Burnout Risk</h3>", unsafe_allow_html=True)
st.progress(int(burnout_risk))
st.write(f"Estimated Burnout Risk: **{int(burnout_risk)}%**")
st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# STRESS HISTORY
# ======================================================
st.markdown("<div class='card'><h3>📈 Stress Trend</h3>", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append(stress_index)
st.line_chart(st.session_state.history)

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# FUN FEEDBACK
# ======================================================
if prediction == 0:
    st.balloons()
elif prediction == 2:
    st.error("⚠️ High stress detected! Please slow down.")

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
Built with ❤️ using Machine Learning & Streamlit
</p>
""", unsafe_allow_html=True)
