from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

MODEL_FILE = ROOT / "models" / "purchase_model.pkl"
DATA_FILE = ROOT / "data" / "processed" / "players_clean.csv"

model = joblib.load(MODEL_FILE)
df = pd.read_csv(DATA_FILE)

features = [
    "age",
    "gender",
    "location",
    "game_genre",
    "game_difficulty",
    "sessions_per_week",
    "avg_session_duration_minutes",
    "player_level",
    "achievements_unlocked",
    "total_events",
    "days_since_last_seen",
    "account_age_days"
]

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["model"]

feature_names = preprocessor.get_feature_names_out()

importance = pd.Series(
    classifier.feature_importances_,
    index=feature_names
).sort_values(ascending=False).head(10)

print("TOP FEATURES")
print("=" * 50)
print(importance)

importance.sort_values().plot(kind="barh")

plt.title("Top Features for Purchase Prediction")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()