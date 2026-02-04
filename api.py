from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="Stress Prediction API")

# Load ML model
model = joblib.load("stress_model.pkl")

# Root route (health check)
@app.get("/")
def home():
    return {"message": "Stress Prediction API is running"}

# Prediction route
@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"stress_level": int(prediction)}
