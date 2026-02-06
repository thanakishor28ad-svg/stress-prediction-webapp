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
    try:
        df = pd.DataFrame([[
            data["WorkHours"],
            data["SleepHours"],
            data["HeartRate"],
            data["ScreenTime"],
            data["ExerciseHours"]
        ]])

        prediction = model.predict(df)[0]
        return {"stress_level": int(prediction)}

    except Exception as e:
        return {"error": str(e)}


