from pathlib import Path
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "players_segmented.csv"

df = pd.read_csv(INPUT_FILE)

features = [
    "sessions_per_week",
    "play_time_hours_per_week",
    "avg_session_duration_minutes",
    "player_level",
    "achievements_unlocked",
    "total_revenue_usd",
    "days_since_last_seen"
]

X = df[features].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["segment"] = kmeans.fit_predict(X_scaled)

segment_summary = (
    df.groupby("segment")[features]
    .mean()
    .round(2)
)

print("\nSegment Summary")
print("=" * 60)
print(segment_summary)

segment_counts = (
    df["segment"]
    .value_counts()
    .sort_index()
)

print("\nPlayers per Segment")
print("=" * 60)
print(segment_counts)

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")