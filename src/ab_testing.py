from pathlib import Path

import pandas as pd
from scipy.stats import ttest_ind


ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "ab_test_results.csv"


df = pd.read_csv(INPUT_FILE)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df["group"] = ["A"] * (len(df) // 2) + ["B"] * (len(df) - len(df) // 2)

control = df[df["group"] == "A"]["total_revenue_usd"]
treatment = df[df["group"] == "B"]["total_revenue_usd"]

control_mean = control.mean()
treatment_mean = treatment.mean()

difference = treatment_mean - control_mean

statistic, p_value = ttest_ind(
    control,
    treatment,
    equal_var=False
)

result = pd.DataFrame(
    [{
        "control_mean_revenue": control_mean,
        "treatment_mean_revenue": treatment_mean,
        "difference": difference,
        "p_value": p_value
    }]
)

result.to_csv(OUTPUT_FILE, index=False)

print("A/B TEST RESULTS")
print("=" * 50)
print(f"Control mean revenue:   {control_mean:.2f}")
print(f"Treatment mean revenue: {treatment_mean:.2f}")
print(f"Difference:             {difference:.2f}")
print(f"P-value:                {p_value:.4f}")

if p_value < 0.05:
    print("Result: statistically significant")
else:
    print("Result: not statistically significant")

print(f"\nSaved: {OUTPUT_FILE}")