"""
Future Interns – Data Science & Analytics
Task 2: Customer Retention & Churn Analysis
GitHub Repo: FUTURE_DS_02

This script:
  1. Generates a realistic subscription customer dataset
  2. Cleans & preprocesses the data
  3. Computes KPIs: churn rate, retention rate, CLV, cohort analysis
  4. Outputs charts as PNG files
  5. Saves cleaned dataset as CSV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings, os

warnings.filterwarnings("ignore")
np.random.seed(99)

# ─── 1. GENERATE DATASET ──────────────────────────────────────────────────────
n = 1200
plans       = ["Basic", "Standard", "Premium"]
channels    = ["Organic", "Paid Ads", "Referral", "Social Media", "Email"]
reasons     = ["Price too high", "Better competitor", "Lack of features",
               "Poor support", "No longer needed", "Technical issues"]

signup_dates = pd.date_range("2023-01-01", "2024-06-30", periods=n)

data = {
    "customer_id":   [f"C{str(i+1).zfill(4)}" for i in range(n)],
    "signup_date":   np.random.choice(signup_dates, n, replace=False),
    "plan":          np.random.choice(plans, n, p=[0.40, 0.35, 0.25]),
    "channel":       np.random.choice(channels, n, p=[0.30, 0.25, 0.20, 0.15, 0.10]),
    "age_group":     np.random.choice(["18-24","25-34","35-44","45-54","55+"], n, p=[0.15,0.35,0.25,0.15,0.10]),
    "monthly_fee":   np.where(np.random.choice(plans, n, p=[0.40,0.35,0.25]) == "Basic", 299,
                     np.where(np.random.choice(plans, n, p=[0.40,0.35,0.25]) == "Standard", 599, 999)),
    "churned":       np.random.choice([0,1], n, p=[0.68, 0.32]),
}

df = pd.DataFrame(data)
df["signup_date"] = pd.to_datetime(df["signup_date"])

# Assign monthly_fee properly by plan
fee_map = {"Basic": 299, "Standard": 599, "Premium": 999}
df["monthly_fee"] = df["plan"].map(fee_map)

# Tenure: active customers have longer tenure, churned shorter
df["tenure_months"] = np.where(
    df["churned"] == 0,
    np.random.randint(6, 24, n),
    np.random.randint(1, 12, n)
)

# Churn date for churned customers
df["churn_date"] = np.where(
    df["churned"] == 1,
    df["signup_date"] + pd.to_timedelta(df["tenure_months"] * 30, unit="D"),
    pd.NaT
)
df["churn_date"] = pd.to_datetime(df["churn_date"])

# Churn reason only for churned
df["churn_reason"] = np.where(
    df["churned"] == 1,
    np.random.choice(reasons, n, p=[0.30, 0.22, 0.18, 0.14, 0.10, 0.06]),
    None
)

# CLV = monthly_fee × tenure
df["clv"] = df["monthly_fee"] * df["tenure_months"]

# Cohort = month of signup
df["cohort"] = df["signup_date"].dt.to_period("M").astype(str)
df["signup_month"] = df["signup_date"].dt.strftime("%b %Y")

print("✅ Dataset shape:", df.shape)
print(df[["customer_id","plan","churned","tenure_months","clv","churn_reason"]].head(5))

# ─── 2. KPIs ──────────────────────────────────────────────────────────────────
total_customers   = len(df)
churned_customers = df["churned"].sum()
active_customers  = total_customers - churned_customers
churn_rate        = round(churned_customers / total_customers * 100, 1)
retention_rate    = round(100 - churn_rate, 1)
avg_clv           = round(df["clv"].mean())
avg_tenure_active = round(df[df["churned"]==0]["tenure_months"].mean(), 1)
avg_tenure_churned= round(df[df["churned"]==1]["tenure_months"].mean(), 1)
mrr               = round(df[df["churned"]==0]["monthly_fee"].sum())

print(f"\n📊 KPI SUMMARY")
print(f"  Total Customers   : {total_customers:,}")
print(f"  Active            : {active_customers:,}")
print(f"  Churned           : {churned_customers:,}")
print(f"  Churn Rate        : {churn_rate}%")
print(f"  Retention Rate    : {retention_rate}%")
print(f"  Avg CLV           : ₹{avg_clv:,}")
print(f"  Avg Tenure Active : {avg_tenure_active} months")
print(f"  Avg Tenure Churned: {avg_tenure_churned} months")
print(f"  MRR (Active only) : ₹{mrr:,}")

# ─── 3. CHARTS ────────────────────────────────────────────────────────────────
os.makedirs("/home/claude/charts2", exist_ok=True)
BLUE, RED, GREEN, AMBER = "#185FA5", "#A32D2D", "#0F6E56", "#854F0B"
PALETTE = [BLUE, RED, GREEN, AMBER, "#533AB7", "#993C1D"]
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False})

# Chart 1 – Churn vs Retention donut
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie([retention_rate, churn_rate], labels=["Retained","Churned"],
       colors=[GREEN, RED], autopct="%1.1f%%", startangle=90,
       wedgeprops=dict(edgecolor="white", linewidth=2.5), pctdistance=0.75)
ax.set_title("Churn vs Retention Rate", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout(); plt.savefig("/home/claude/charts2/01_churn_retention.png", dpi=150); plt.close()

# Chart 2 – Churn rate by plan
plan_churn = df.groupby("plan")["churned"].mean().mul(100).round(1).reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(plan_churn["plan"], plan_churn["churned"],
              color=[BLUE, GREEN, AMBER], edgecolor="white", width=0.5)
for bar, val in zip(bars, plan_churn["churned"]):
    ax.text(bar.get_x()+bar.get_width()/2, val+0.3, f"{val}%",
            ha="center", fontsize=11, fontweight="bold")
ax.set_title("Churn Rate by Subscription Plan", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Churn Rate (%)"); ax.set_ylim(0, plan_churn["churned"].max()+8)
plt.tight_layout(); plt.savefig("/home/claude/charts2/02_plan_churn.png", dpi=150); plt.close()

# Chart 3 – Churn reasons bar
reason_counts = df[df["churned"]==1]["churn_reason"].value_counts()
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(reason_counts.index, reason_counts.values,
               color=PALETTE[:len(reason_counts)], edgecolor="white", height=0.55)
for bar, val in zip(bars, reason_counts.values):
    ax.text(val+1, bar.get_y()+bar.get_height()/2, str(val), va="center", fontsize=10)
ax.set_title("Churn Reasons Distribution", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Number of Customers")
plt.tight_layout(); plt.savefig("/home/claude/charts2/03_churn_reasons.png", dpi=150); plt.close()

# Chart 4 – Avg CLV by plan
clv_plan = df.groupby("plan")["clv"].mean().round(0).reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(clv_plan["plan"], clv_plan["clv"],
              color=[BLUE, GREEN, AMBER], edgecolor="white", width=0.5)
for bar, val in zip(bars, clv_plan["clv"]):
    ax.text(bar.get_x()+bar.get_width()/2, val+100, f"₹{val:,.0f}",
            ha="center", fontsize=10, fontweight="bold")
ax.set_title("Average Customer Lifetime Value by Plan", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Avg CLV (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
plt.tight_layout(); plt.savefig("/home/claude/charts2/04_clv_plan.png", dpi=150); plt.close()

# Chart 5 – Tenure distribution by churn status
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df[df["churned"]==0]["tenure_months"], bins=12, alpha=0.7, color=GREEN, label="Active", edgecolor="white")
ax.hist(df[df["churned"]==1]["tenure_months"], bins=12, alpha=0.7, color=RED, label="Churned", edgecolor="white")
ax.set_title("Tenure Distribution: Active vs Churned", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Tenure (Months)"); ax.set_ylabel("Customers")
ax.legend()
plt.tight_layout(); plt.savefig("/home/claude/charts2/05_tenure_dist.png", dpi=150); plt.close()

# Chart 6 – Churn rate by acquisition channel
channel_churn = df.groupby("channel")["churned"].mean().mul(100).round(1).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(channel_churn.index, channel_churn.values,
               color=PALETTE[:len(channel_churn)], edgecolor="white", height=0.5)
for bar, val in zip(bars, channel_churn.values):
    ax.text(val+0.2, bar.get_y()+bar.get_height()/2, f"{val}%", va="center", fontsize=10)
ax.set_title("Churn Rate by Acquisition Channel", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Churn Rate (%)")
plt.tight_layout(); plt.savefig("/home/claude/charts2/06_channel_churn.png", dpi=150); plt.close()

# ─── 4. COHORT RETENTION TABLE ────────────────────────────────────────────────
cohort_summary = df.groupby("cohort").agg(
    total=("customer_id","count"),
    churned=("churned","sum")
).reset_index()
cohort_summary["retained"] = cohort_summary["total"] - cohort_summary["churned"]
cohort_summary["retention_pct"] = (cohort_summary["retained"]/cohort_summary["total"]*100).round(1)
print("\n─── COHORT RETENTION (first 6 cohorts) ───")
print(cohort_summary.head(6).to_string(index=False))

# ─── 5. SAVE DATA ─────────────────────────────────────────────────────────────
df.to_csv("/home/claude/churn_data_clean.csv", index=False)
cohort_summary.to_csv("/home/claude/cohort_summary.csv", index=False)
print("\n✅ Charts saved to /home/claude/charts2/")
print("✅ Data saved: churn_data_clean.csv, cohort_summary.csv")

# ─── 6. ACTIONABLE INSIGHTS ───────────────────────────────────────────────────
top_reason = reason_counts.idxmax()
worst_channel = channel_churn.idxmax()
best_plan_clv = clv_plan.loc[clv_plan["clv"].idxmax(), "plan"]
print(f"\n─── INSIGHTS ───")
print(f"  Top churn reason  : {top_reason} ({reason_counts.max()} customers)")
print(f"  Highest churn channel: {worst_channel} ({channel_churn.max()}%)")
print(f"  Best CLV plan     : {best_plan_clv}")
print(f"  MRR at risk if churn continues: ₹{round(churned_customers * df['monthly_fee'].mean()):,}/mo")
