"""
A/B Test Analysis
Determines whether the new checkout design significantly improved conversion.
Null hypothesis (H0):        the two designs convert at the same rate
Alternative hypothesis (H1): the new design converts at a different rate
Significance level (alpha):  0.05
"""

import numpy as np
import pandas as pd
from scipy import stats

ALPHA = 0.05

df = pd.read_csv("data/ab_test_data.csv")

# 1. Conversion rates per group
summary = df.groupby("group")["converted"].agg(["count", "sum", "mean"])
summary.columns = ["users", "conversions", "conversion_rate"]
print("=" * 60)
print("CONVERSION SUMMARY")
print("=" * 60)
print(summary.round(4))
print()

control = df[df["group"] == "control"]["converted"]
treatment = df[df["group"] == "treatment"]["converted"]

n_c, n_t = len(control), len(treatment)
conv_c, conv_t = control.sum(), treatment.sum()
rate_c, rate_t = control.mean(), treatment.mean()

# 2. Two-proportion z-test
p_pool = (conv_c + conv_t) / (n_c + n_t)
se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
z = (rate_t - rate_c) / se
p_value_z = 2 * (1 - stats.norm.cdf(abs(z)))

print("=" * 60)
print("TWO-PROPORTION Z-TEST")
print("=" * 60)
print(f"Control conversion:   {rate_c:.4f}  ({conv_c}/{n_c})")
print(f"Treatment conversion: {rate_t:.4f}  ({conv_t}/{n_t})")
print(f"Z-statistic: {z:.4f}")
print(f"P-value:     {p_value_z:.5f}")
print()

# 3. Chi-square test (cross-check)
contingency = pd.crosstab(df["group"], df["converted"])
chi2, p_value_chi, dof, expected = stats.chi2_contingency(contingency)
print("=" * 60)
print("CHI-SQUARE TEST (cross-check)")
print("=" * 60)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value:              {p_value_chi:.5f}")
print()

# 4. Lift and confidence interval
abs_diff = rate_t - rate_c
rel_lift = abs_diff / rate_c * 100
se_diff = np.sqrt(rate_c * (1 - rate_c) / n_c + rate_t * (1 - rate_t) / n_t)
ci_low = abs_diff - 1.96 * se_diff
ci_high = abs_diff + 1.96 * se_diff

print("=" * 60)
print("EFFECT SIZE")
print("=" * 60)
print(f"Absolute difference: {abs_diff:.4f}  ({abs_diff*100:.2f} percentage points)")
print(f"Relative lift:       {rel_lift:.1f}%")
print(f"95% CI for difference: [{ci_low:.4f}, {ci_high:.4f}]")
print()

# 5. Conclusion
print("=" * 60)
print("CONCLUSION")
print("=" * 60)
significant = p_value_z < ALPHA
if significant:
    print(f"P-value ({p_value_z:.5f}) < alpha ({ALPHA}) -> REJECT the null hypothesis.")
    print(f"The new checkout design produced a statistically significant")
    print(f"increase in conversion: a {rel_lift:.1f}% relative lift ({rate_c*100:.1f}% -> {rate_t*100:.1f}%).")
    print(f"Recommendation: roll out the new design.")
else:
    print(f"P-value ({p_value_z:.5f}) >= alpha ({ALPHA}) -> FAIL to reject the null.")
    print(f"No statistically significant difference detected.")