from pathlib import Path
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "players_anomalies.csv"

df = pd.read_csv(INPUT_FILE)

features = [
    "sessions_per_week",
    "play_time_hours_per_week",
    "avg_session_duration_minutes",
    "total_events",
    "total_revenue_usd",
    "player_level",
    "achievements_unlocked"
]

X = df[features].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

df["anomaly_prediction"] = model.fit_predict(X_scaled)
df["anomaly_score"] = model.decision_function(X_scaled)

df["is_anomaly"] = (
    df["anomaly_prediction"] == -1
).astype(int)

anomalies = df[df["is_anomaly"] == 1].copy()

print("ANOMALY DETECTION")
print("=" * 60)

print(f"Total players     : {len(df):,}")
print(f"Anomalies detected: {len(anomalies):,}")
print(f"Anomaly rate      : {100 * len(anomalies) / len(df):.2f}%")

print("\nTop anomalous players")
print("=" * 60)

print(
    anomalies[
        [
            "player_id",
            "sessions_per_week",
            "play_time_hours_per_week",
            "total_events",
            "total_revenue_usd",
            "player_level",
            "anomaly_score"
        ]
    ]
    .sort_values("anomaly_score")
    .head(10)
    .to_string(index=False)
)

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")