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

    df = pd.DataFrame([{
        "WorkHours": data["WorkHours"],
        "SleepHours": data["SleepHours"],
        "HeartRate": data["HeartRate"],
        "ScreenTime": data["ScreenTime"],
        "ExerciseHours": data["ExerciseHours"]
    }])

    prediction = model.predict(df)[0]
    return {"stress_level": int(prediction)}
