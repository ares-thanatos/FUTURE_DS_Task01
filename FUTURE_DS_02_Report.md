# Customer Retention & Churn Analysis
## Future Interns · Data Science & Analytics · FUTURE_DS_02

---

## 1. Executive Summary

This report analyses subscription customer data to identify churn patterns, key retention drivers, and customer lifetime trends. The dataset covers **1,200 customers** across 3 subscription plans acquired via 5 channels between January 2023 and June 2024.

**Churn Rate: 31.5% | Retention Rate: 68.5% | Avg CLV: ₹6,875 | MRR: ₹4,68,578**

---

## 2. Dataset Overview

| Field | Details |
|---|---|
| Total Customers | 1,200 |
| Period | Jan 2023 – Jun 2024 |
| Plans | Basic (₹299/mo), Standard (₹599/mo), Premium (₹999/mo) |
| Acquisition Channels | Organic, Paid Ads, Referral, Social Media, Email |
| Age Groups | 18-24, 25-34, 35-44, 45-54, 55+ |
| Features | Customer ID, Signup Date, Plan, Channel, Age Group, Monthly Fee, Tenure, CLV, Churn Status, Churn Reason |

---

## 3. Key Performance Indicators

| KPI | Value |
|---|---|
| Total Customers | 1,200 |
| Active Customers | 822 (68.5%) |
| Churned Customers | 378 (31.5%) |
| Monthly Recurring Revenue | ₹4,68,578 |
| Average CLV | ₹6,875 |
| Avg Tenure (Active) | 14.6 months |
| Avg Tenure (Churned) | 6.0 months |
| MRR at Risk | ₹2,19,177/mo |

---

## 4. Churn Analysis

### 4.1 Churn Rate by Subscription Plan

| Plan | Monthly Fee | Churn Rate | Avg CLV |
|---|---|---|---|
| Basic | ₹299 | ~34% | ₹3,200 |
| Standard | ₹599 | ~31% | ₹6,500 |
| Premium | ₹999 | ~27% | ₹12,800 |

Premium plan customers churn the least and deliver the highest CLV. Basic plan customers are the most price-sensitive and churn earliest.

### 4.2 Churn Reasons

| Reason | Customers | Share |
|---|---|---|
| Price too high | 122 | 32.3% |
| Better competitor | 83 | 22.0% |
| Lack of features | 68 | 18.0% |
| Poor support | 53 | 14.0% |
| No longer needed | 38 | 10.1% |
| Technical issues | 14 | 3.7% |

Price sensitivity is the single biggest churn driver (32.3%), followed by competitive pressure (22%).

### 4.3 Churn Rate by Acquisition Channel

| Channel | Churn Rate |
|---|---|
| Referral | 34.0% (highest) |
| Paid Ads | 33.2% |
| Social Media | 31.8% |
| Organic | 29.5% |
| Email | 28.7% (lowest) |

Organically and email-acquired customers churn less — they arrive with higher intent. Referral customers, despite lower acquisition cost, show the highest churn, suggesting mismatch between expectation and product.

---

## 5. Cohort Retention Analysis

| Cohort | Total | Churned | Retained | Retention % |
|---|---|---|---|---|
| Jan 2023 | 69 | 21 | 48 | 69.6% |
| Feb 2023 | 61 | 22 | 39 | 63.9% |
| Mar 2023 | 68 | 28 | 40 | 58.8% |
| Apr 2023 | 66 | 16 | 50 | 75.8% |
| May 2023 | 68 | 19 | 49 | 72.1% |
| Jun 2023 | 66 | 20 | 46 | 69.7% |

March 2023 cohort has the lowest retention (58.8%) — warrants investigation into what changed that month (pricing, onboarding, product changes).

---

## 6. Customer Lifetime Value Analysis

- Premium customers deliver **4× more CLV** than Basic customers
- Churned customers on average only stay **6 months** vs 14.6 months for active customers
- Every month of retention gained = ₹299–₹999 additional CLV per customer
- Improving avg tenure by 2 months across churned customers = **₹7,56,000 recovered CLV**

---

## 7. Actionable Recommendations

### 7.1 Address Price Sensitivity (Priority: High)
32.3% cite price as the reason to leave. Introduce:
- Flexible monthly/annual toggle with annual discount (20–30%)
- Pause option instead of cancel for at-risk users
- Downgrade path from Standard/Premium to Basic (retain the customer, not the plan)

### 7.2 Improve First 6 Months Onboarding (Priority: High)
Churned customers leave at an average of 6 months — the danger window. Launch:
- Automated onboarding email sequences (day 1, 7, 14, 30)
- In-app feature discovery tooltips for new users
- 30-day check-in calls for Standard/Premium customers

### 7.3 Upsell Basic Plan Customers (Priority: Medium)
Basic customers churn 34% vs Premium's 27%. A targeted upgrade campaign showing Premium value can:
- Reduce churn by moving customers to higher-commitment plans
- Increase MRR and CLV simultaneously

### 7.4 Fix Referral Channel Quality (Priority: Medium)
Referral has the highest churn (34%) despite low acquisition cost. Review:
- Referral incentive structure — are incentives attracting wrong customers?
- Set better expectations in referral messaging
- Add referral customer onboarding variant

### 7.5 Invest in Support Quality (Priority: Medium)
14% of churn cites poor support. A dedicated customer success team for Standard/Premium accounts can reduce this. Track CSAT and time-to-resolution as KPIs.

### 7.6 Reactivate Churned Customers (Priority: Low–Medium)
378 churned customers represent ₹2.19L in potential monthly revenue. A win-back campaign:
- Offer 2 months free on annual plan
- Target customers who left for "price" or "no longer needed"
- Best reactivation window: 30–90 days post-churn

---

## 8. Conclusion

The business retains 68.5% of customers but faces significant revenue risk — ₹2.19L MRR is at risk monthly if churn continues unchecked. The top priorities are fixing the first-6-month experience, addressing price sensitivity, and improving referral channel quality. With focused retention strategies, a **5–8 percentage point improvement in retention** is achievable within 2 quarters, recovering ₹60–90L in annual CLV.

---

*Report prepared by: Future Interns DS Intern*
*Tools: Python (pandas, numpy, matplotlib, seaborn)*
*GitHub: FUTURE_DS_02*
