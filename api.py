from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("stress_model.pkl")

@app.get("/")
def home():
    return {"message": "Stress Prediction API is running"}

@app.post("/predict")
def predict(data: dict):

    # Recalculate StressIndex (same logic used during training)
    stress_index = (
        0.4 * data["WorkHours"] * 10 +
        0.3 * (data["HeartRate"] - 60) +
        0.2 * data["ScreenTime"] * 10 -
        0.1 * data["SleepHours"] * 10
    )

    stress_index = max(0, min(100, stress_index))

    df = pd.DataFrame([{
        "WorkHours": data["WorkHours"],
        "SleepHours": data["SleepHours"],
        "HeartRate": data["HeartRate"],
        "ScreenTime": data["ScreenTime"],
        "ExerciseHours": data["ExerciseHours"],
        "StressIndex": stress_index   # ✅ 6th feature added
    }])

    prediction = int(model.predict(df)[0])

labels = {
    0: "Low Stress 😌",
    1: "Medium Stress 😐",
    2: "High Stress 😰"
}

return {
    "stress_level": prediction,
    "label": labels[prediction]
}





