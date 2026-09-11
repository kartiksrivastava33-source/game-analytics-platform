from pathlib import Path
import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"

df = pd.read_csv(INPUT_FILE)

print("STATISTICAL ANALYSIS")
print("=" * 60)

high = df[df["engagement_level"] == "High"]["total_revenue_usd"]
low = df[df["engagement_level"] == "Low"]["total_revenue_usd"]

t_stat, p_value = ttest_ind(high, low, equal_var=False)

print("\n1. Revenue: High vs Low Engagement")
print("-" * 60)
print(f"High engagement mean revenue: ${high.mean():.2f}")
print(f"Low engagement mean revenue : ${low.mean():.2f}")
print(f"t-statistic                  : {t_stat:.4f}")
print(f"p-value                      : {p_value:.6f}")

if p_value < 0.05:
    print("Result: Statistically significant difference")
else:
    print("Result: No statistically significant difference")


contingency = pd.crosstab(
    df["game_genre"],
    df["purchase_flag"]
)

chi2, p_value, dof, expected = chi2_contingency(contingency)

print("\n2. Genre vs Purchase Behavior")
print("-" * 60)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value            : {p_value:.6f}")
print(f"Degrees of freedom : {dof}")

if p_value < 0.05:
    print("Result: Genre and purchase behavior are statistically associated")
else:
    print("Result: No statistically significant association")


correlation_features = [
    "sessions_per_week",
    "play_time_hours_per_week",
    "avg_session_duration_minutes",
    "player_level",
    "achievements_unlocked",
    "total_events",
    "total_revenue_usd"
]

correlation = df[correlation_features].corr()

print("\n3. Correlation with Revenue")
print("-" * 60)

print(
    correlation["total_revenue_usd"]
    .sort_values(ascending=False)
    .to_string()
)