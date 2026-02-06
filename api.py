from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("stress_model.pkl")

class StressInput(BaseModel):
    work_hours: int
    sleep_hours: int
    heart_rate: int

@app.get("/")
def home():
    return {"message": "Stress Prediction API is running"}

@app.post("/predict")
def predict(data: StressInput):
    df = pd.DataFrame([{
        "work_hours": data.work_hours,
        "sleep_hours": data.sleep_hours,
        "heart_rate": data.heart_rate
    }])

    prediction = model.predict(df)[0]
    return {"stress_level": int(prediction)}

