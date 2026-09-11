from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "gaming_player_engagement.csv"
DB = ROOT / "data" / "processed" / "game_analytics.db"

df = pd.read_csv(RAW)

df["first_seen"] = pd.to_datetime(df["first_seen"])
df["last_seen"] = pd.to_datetime(df["last_seen"])

snapshot = df["last_seen"].max()

df["days_since_last_seen"] = (
    snapshot - df["last_seen"]
).dt.days

df["account_age_days"] = (
    df["last_seen"] - df["first_seen"]
).dt.days.clip(lower=1)

df["purchase_flag"] = (
    df["in_game_purchases"] > 0
).astype(int)

df["revenue_per_session"] = (
    df["total_revenue_usd"] /
    df["total_sessions"].clip(lower=1)
)

df["events_per_session"] = (
    df["total_events"] /
    df["total_sessions"].clip(lower=1)
)

df["at_risk"] = (
    df["days_since_last_seen"] >= 14
).astype(int)

df = df.drop_duplicates(subset="player_id")

DB.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(
    ROOT / "data" / "processed" / "players_clean.csv",
    index=False
)

with sqlite3.connect(DB) as conn:
    df.to_sql(
        "players",
        conn,
        if_exists="replace",
        index=False
    )

print(f"Rows loaded: {len(df):,}")
print(f"Database created: {DB}")