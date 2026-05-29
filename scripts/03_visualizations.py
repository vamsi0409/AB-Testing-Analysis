"""
A/B Test Visualizations
Creates presentation-ready charts for the checkout redesign A/B test.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.style.use("seaborn-v0_8-whitegrid")

df = pd.read_csv("data/ab_test_data.csv")

control = df[df["group"] == "control"]["converted"]
treatment = df[df["group"] == "treatment"]["converted"]
rate_c, rate_t = control.mean(), treatment.mean()
n_c, n_t = len(control), len(treatment)

C_CONTROL = "#6c757d"
C_TREAT = "#c8a96e"

# Chart 1: Conversion rate bar chart with error bars
fig, ax = plt.subplots(figsize=(8, 6))
se_c = np.sqrt(rate_c * (1 - rate_c) / n_c)
se_t = np.sqrt(rate_t * (1 - rate_t) / n_t)
bars = ax.bar(
    ["Control\n(old design)", "Treatment\n(new design)"],
    [rate_c * 100, rate_t * 100],
    yerr=[se_c * 196, se_t * 196],
    capsize=10,
    color=[C_CONTROL, C_TREAT],
    edgecolor="black",
    linewidth=0.8,
)
for bar, rate in zip(bars, [rate_c, rate_t]):
    ax.text(bar.get_x() + bar.get_width() / 2, rate * 100 + 0.4,
            f"{rate*100:.2f}%", ha="center", fontsize=13, fontweight="bold")
ax.set_ylabel("Conversion Rate (%)", fontsize=12)
ax.set_title("Checkout Conversion Rate by Group\n(error bars = 95% confidence interval)",
             fontsize=13, fontweight="bold")
ax.set_ylim(0, max(rate_c, rate_t) * 100 + 3)
plt.tight_layout()
plt.savefig("visualizations/01_conversion_rates.png", dpi=140)
plt.close()

# Chart 2: Conversion by device
fig, ax = plt.subplots(figsize=(9, 6))
device_rates = df.groupby(["device", "group"])["converted"].mean().unstack() * 100
device_rates = device_rates[["control", "treatment"]]
device_rates.plot(kind="bar", ax=ax, color=[C_CONTROL, C_TREAT],
                  edgecolor="black", linewidth=0.6)
ax.set_xlabel("Device", fontsize=12)
ax.set_ylabel("Conversion Rate (%)", fontsize=12)
ax.set_title("Conversion Rate by Device and Group", fontsize=13, fontweight="bold")
ax.set_xticklabels(device_rates.index, rotation=0)
ax.legend(["Control", "Treatment"])
plt.tight_layout()
plt.savefig("visualizations/03_by_device.png", dpi=140)
plt.close()

# Chart 3: Significance visualization
fig, ax = plt.subplots(figsize=(9, 6))
p_pool = (control.sum() + treatment.sum()) / (n_c + n_t)
se_diff = np.sqrt(p_pool * (1 - p_pool) * (1 / n_c + 1 / n_t))
x = np.linspace(-4 * se_diff, 4 * se_diff, 500)
y = stats.norm.pdf(x, 0, se_diff)
ax.plot(x * 100, y, color="#333", lw=2, label="Distribution under H0 (no difference)")
ax.fill_between(x * 100, y, where=(np.abs(x) >= abs(rate_t - rate_c)),
                color=C_TREAT, alpha=0.5, label="Rejection region (p-value area)")
observed = (rate_t - rate_c) * 100
ax.axvline(observed, color="red", lw=2, linestyle="--",
           label=f"Observed difference = {observed:.2f} pts")
ax.set_xlabel("Difference in Conversion Rate (percentage points)", fontsize=12)
ax.set_ylabel("Probability Density", fontsize=12)
ax.set_title("Why the Result Is Significant", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig("visualizations/04_significance.png", dpi=140)
plt.close()

print("Created 3 visualizations in the visualizations folder")