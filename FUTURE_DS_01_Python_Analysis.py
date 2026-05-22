"""
Future Interns – Data Science & Analytics
Task 1: Business Sales Performance Analytics
GitHub Repo: FUTURE_DS_01

This script:
  1. Generates a realistic sales dataset
  2. Cleans & preprocesses the data
  3. Computes KPIs: revenue trends, top products, category performance, regional sales
  4. Outputs charts as PNG files
  5. Saves cleaned dataset as CSV for dashboard use
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings, os

warnings.filterwarnings("ignore")
np.random.seed(42)

# ─── 1. GENERATE DATASET ──────────────────────────────────────────────────────

months    = pd.date_range("2024-01-01", periods=12, freq="MS")
regions   = ["North", "South", "East", "West"]
categories = {
    "Electronics":   ["Laptop", "Smartphone", "Tablet", "Headphones", "Smart Watch"],
    "Apparel":       ["Jacket", "Sneakers", "T-Shirt", "Jeans", "Cap"],
    "Home & Living": ["Sofa", "Lamp", "Curtains", "Cookware Set", "Wall Art"],
    "Sports":        ["Yoga Mat", "Dumbbells", "Cycling Gloves", "Running Shoes", "Water Bottle"],
}

rows = []
for month in months:
    for region in regions:
        for cat, products in categories.items():
            for product in products:
                units = np.random.randint(10, 300)
                base_price = {
                    "Electronics": np.random.uniform(150, 1200),
                    "Apparel": np.random.uniform(20, 150),
                    "Home & Living": np.random.uniform(30, 600),
                    "Sports": np.random.uniform(10, 200),
                }[cat]
                price     = round(base_price, 2)
                discount  = round(np.random.uniform(0, 0.3), 2)
                revenue   = round(units * price * (1 - discount), 2)
                rows.append({
                    "Month": month,
                    "Region": region,
                    "Category": cat,
                    "Product": product,
                    "Units_Sold": units,
                    "Unit_Price": price,
                    "Discount": discount,
                    "Revenue": revenue,
                })

df = pd.DataFrame(rows)

# ─── 2. DATA CLEANING ─────────────────────────────────────────────────────────
df.dropna(inplace=True)
df["Month_Label"] = df["Month"].dt.strftime("%b %Y")
df["Quarter"] = df["Month"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
df["Profit_Margin"] = ((df["Unit_Price"] * (1 - df["Discount"]) - df["Unit_Price"] * 0.4) /
                        (df["Unit_Price"] * (1 - df["Discount"]))).round(4)

print("✅ Dataset shape:", df.shape)
print(df.head(3))

# ─── 3. KPI SUMMARY ───────────────────────────────────────────────────────────
total_revenue  = df["Revenue"].sum()
total_units    = df["Units_Sold"].sum()
avg_order_val  = total_revenue / len(df)
top_product    = df.groupby("Product")["Revenue"].sum().idxmax()
top_region     = df.groupby("Region")["Revenue"].sum().idxmax()
top_category   = df.groupby("Category")["Revenue"].sum().idxmax()

print(f"\n📊 KPI SUMMARY")
print(f"  Total Revenue   : ₹{total_revenue:,.0f}")
print(f"  Total Units Sold: {total_units:,}")
print(f"  Avg Order Value : ₹{avg_order_val:,.2f}")
print(f"  Top Product     : {top_product}")
print(f"  Top Region      : {top_region}")
print(f"  Top Category    : {top_category}")

# ─── 4. CHARTS ────────────────────────────────────────────────────────────────
os.makedirs("/home/claude/charts", exist_ok=True)

PALETTE = ["#0F4C81", "#E63946", "#2DC653", "#FFB703", "#8338EC", "#FB5607"]
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                      "axes.spines.right": False})

# Chart 1 – Monthly Revenue Trend
monthly = df.groupby("Month")["Revenue"].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(monthly["Month"], monthly["Revenue"], alpha=0.15, color=PALETTE[0])
ax.plot(monthly["Month"], monthly["Revenue"], marker="o", color=PALETTE[0], lw=2.5, ms=7)
for x, y in zip(monthly["Month"], monthly["Revenue"]):
    ax.annotate(f'₹{y/1e6:.2f}M', (x, y), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=8, color="#444")
ax.set_title("Monthly Revenue Trend (2024)", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Revenue (₹)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1e6:.1f}M'))
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig("/home/claude/charts/01_monthly_revenue.png", dpi=150)
plt.close()

# Chart 2 – Top 10 Products by Revenue
top10 = df.groupby("Product")["Revenue"].sum().nlargest(10).sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top10.index, top10.values, color=PALETTE[0], edgecolor="white", height=0.6)
for bar, val in zip(bars, top10.values):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f'₹{val/1e6:.2f}M', va='center', fontsize=9, color="#333")
ax.set_title("Top 10 Products by Revenue", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Revenue (₹)", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1e6:.1f}M'))
plt.tight_layout()
plt.savefig("/home/claude/charts/02_top_products.png", dpi=150)
plt.close()

# Chart 3 – Category Revenue Share (Pie)
cat_rev = df.groupby("Category")["Revenue"].sum()
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    cat_rev, labels=cat_rev.index, autopct="%1.1f%%",
    colors=PALETTE[:len(cat_rev)], startangle=140,
    wedgeprops=dict(edgecolor="white", linewidth=2), pctdistance=0.75)
for at in autotexts: at.set_fontsize(11); at.set_fontweight("bold")
ax.set_title("Revenue by Category", fontsize=15, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("/home/claude/charts/03_category_pie.png", dpi=150)
plt.close()

# Chart 4 – Regional Revenue Comparison
reg_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(reg_rev.index, reg_rev.values, color=PALETTE[:4], edgecolor="white", width=0.5)
for bar, val in zip(bars, reg_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 20000,
            f'₹{val/1e6:.2f}M', ha='center', fontsize=10, fontweight="bold")
ax.set_title("Revenue by Region", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Revenue (₹)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1e6:.1f}M'))
plt.tight_layout()
plt.savefig("/home/claude/charts/04_regional_revenue.png", dpi=150)
plt.close()

# Chart 5 – Category × Region Heatmap
pivot = df.pivot_table(values="Revenue", index="Category", columns="Region", aggfunc="sum")
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(pivot/1e6, annot=True, fmt=".1f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Revenue (₹M)"})
ax.set_title("Category × Region Revenue Heatmap (₹M)", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("/home/claude/charts/05_heatmap.png", dpi=150)
plt.close()

# Chart 6 – Quarterly Revenue by Category
qtr = df.groupby(["Quarter", "Category"])["Revenue"].sum().reset_index()
qtr_pivot = qtr.pivot(index="Quarter", columns="Category", values="Revenue")
fig, ax = plt.subplots(figsize=(10, 6))
qtr_pivot.plot(kind="bar", ax=ax, color=PALETTE[:4], edgecolor="white", width=0.7)
ax.set_title("Quarterly Revenue by Category", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Revenue (₹)", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1e6:.1f}M'))
ax.tick_params(axis='x', rotation=0)
ax.legend(title="Category", bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig("/home/claude/charts/06_quarterly_category.png", dpi=150)
plt.close()

# ─── 5. SAVE CLEAN DATA ───────────────────────────────────────────────────────
df.to_csv("/home/claude/sales_data_clean.csv", index=False)
print("\n✅ All charts saved to /home/claude/charts/")
print("✅ Clean dataset saved to /home/claude/sales_data_clean.csv")

# ─── 6. INSIGHTS SUMMARY ──────────────────────────────────────────────────────
print("\n─── ACTIONABLE INSIGHTS ───")
monthly_growth = ((monthly["Revenue"].iloc[-1] - monthly["Revenue"].iloc[0]) /
                   monthly["Revenue"].iloc[0] * 100)
print(f"  Revenue growth Jan→Dec: {monthly_growth:+.1f}%")
print(f"  Highest revenue month : {monthly.loc[monthly['Revenue'].idxmax(), 'Month'].strftime('%B %Y')}")
low_region = df.groupby("Region")["Revenue"].sum().idxmin()
print(f"  Underperforming region: {low_region} — needs targeted campaigns")
high_disc = df[df["Discount"] > 0.25]["Revenue"].sum() / total_revenue * 100
print(f"  Revenue from >25% discounts: {high_disc:.1f}% — review discount strategy")
