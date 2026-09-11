from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "player_acquisition_forecast.csv"

df = pd.read_csv(INPUT_FILE)

df["first_seen"] = pd.to_datetime(df["first_seen"])

weekly_players = (
    df.set_index("first_seen")
    .resample("W")
    .size()
    .rename("new_players")
)

weekly_players = weekly_players.asfreq("W", fill_value=0)

model = ExponentialSmoothing(
    weekly_players,
    trend="add",
    seasonal=None
).fit()

forecast = model.forecast(8)

forecast_df = forecast.reset_index()
forecast_df.columns = ["week", "forecast_new_players"]

result = pd.concat(
    [
        weekly_players.reset_index().rename(
            columns={"first_seen": "week"}
        ),
        forecast_df
    ],
    ignore_index=True
)

result.to_csv(OUTPUT_FILE, index=False)

print("PLAYER ACQUISITION FORECAST")
print("=" * 60)

print("\nHistorical weekly players:")
print(weekly_players.tail(10).to_string())

print("\nNext 8 weeks forecast:")
print(forecast_df.to_string(index=False))

print(f"\nSaved: {OUTPUT_FILE}")

plt.figure(figsize=(12, 5))

plt.plot(
    weekly_players.index,
    weekly_players.values,
    label="Historical"
)

plt.plot(
    forecast.index,
    forecast.values,
    label="Forecast"
)

plt.xlabel("Week")
plt.ylabel("New Players")
plt.title("Weekly Player Acquisition Forecast")
plt.legend()
plt.tight_layout()

plt.show()