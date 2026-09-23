from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


ROOT = Path(__file__).resolve().parents[1]
MODEL_FILE = ROOT / "models" / "purchase_model.pkl"

model = joblib.load(MODEL_FILE)

app = FastAPI(
    title="Game Analytics Prediction API",
    version="1.0"
)


class PlayerInput(BaseModel):
    age: int
    gender: str
    location: str
    game_genre: str
    game_difficulty: str
    sessions_per_week: float
    avg_session_duration_minutes: float
    player_level: int
    achievements_unlocked: int
    total_events: int
    days_since_last_seen: int
    account_age_days: int


@app.get("/")
def root():
    return {
        "message": "Game Analytics Prediction API is running"
    }


@app.post("/predict")
def predict(player: PlayerInput):

    data = pd.DataFrame([player.model_dump()])

    probability = model.predict_proba(data)[0][1]
    prediction = int(probability >= 0.5)

    return {
        "purchase_prediction": prediction,
        "purchase_probability": round(float(probability), 4)
    }