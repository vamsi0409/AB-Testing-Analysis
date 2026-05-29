"""
A/B Test Data Generation
Simulates a realistic e-commerce A/B test for a checkout page redesign.
Control group   = sees the old checkout page
Treatment group = sees the new checkout page
We measure: did the user complete a purchase (converted = 1) or not (0)?
"""

import numpy as np
import pandas as pd

np.random.seed(42)

n_per_group = 5000
control_rate = 0.118
treatment_rate = 0.137

control = pd.DataFrame({
    "user_id": np.arange(1, n_per_group + 1),
    "group": "control",
    "converted": np.random.binomial(1, control_rate, n_per_group),
})

treatment = pd.DataFrame({
    "user_id": np.arange(n_per_group + 1, 2 * n_per_group + 1),
    "group": "treatment",
    "converted": np.random.binomial(1, treatment_rate, n_per_group),
})

df = pd.concat([control, treatment], ignore_index=True)

df["device"] = np.random.choice(
    ["desktop", "mobile", "tablet"],
    size=len(df),
    p=[0.45, 0.45, 0.10],
)

base_duration = np.random.gamma(shape=2.0, scale=60, size=len(df))
df["session_seconds"] = (base_duration + df["converted"] * 45).round(1)

df = df.sample(frac=1, random_state=7).reset_index(drop=True)

out_path = "data/ab_test_data.csv"
df.to_csv(out_path, index=False)

print(f"Generated {len(df)} rows")
print(df["group"].value_counts())
print(df.head())
print(f"\nSaved to {out_path}")