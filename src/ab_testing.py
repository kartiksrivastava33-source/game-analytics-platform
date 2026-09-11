from pathlib import Path

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "players_clean.csv"

df = pd.read_csv(INPUT_FILE)

np.random.seed(42)

df["experiment_group"] = np.random.choice(
    ["Control", "Treatment"],
    size=len(df)
)

control = df[df["experiment_group"] == "Control"]
treatment = df[df["experiment_group"] == "Treatment"]

control_rate = control["purchase_flag"].mean()
treatment_rate = treatment["purchase_flag"].mean()

table = pd.crosstab(
    df["experiment_group"],
    df["purchase_flag"]
)

chi2, p_value, dof, expected = chi2_contingency(table)

lift = (
    (treatment_rate - control_rate)
    / control_rate
) * 100

print("A/B TESTING")
print("=" * 50)

print(f"Control conversion rate   : {control_rate:.2%}")
print(f"Treatment conversion rate : {treatment_rate:.2%}")
print(f"Relative lift             : {lift:.2f}%")
print(f"p-value                   : {p_value:.4f}")

if p_value < 0.05:
    print("Result: Statistically significant difference")
else:
    print("Result: No statistically significant difference")