from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("stress_model.pkl")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"stress_level": int(prediction)}
