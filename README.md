# E-commerce Revenue & Customer Retention Intelligence

A practical end-to-end analytics project for an online retailer. It turns messy order data into decisions about revenue growth, customer retention, product profitability, discount leakage, and inventory priorities.

## Business questions answered

- Which channels, regions, products, and customer segments drive profitable revenue?
- Where are discounts reducing margin without improving order value?
- Which customers are at risk of becoming inactive?
- What should the commercial team prioritize next month?

## Deliverables

- Reproducible data-cleaning and validation pipeline
- Executive KPI summary and monthly revenue trend
- Cohort retention and repeat-purchase analysis
- RFM customer segmentation and churn-risk scoring
- Product, channel, and regional profitability analysis
- 90-day revenue forecast with uncertainty band
- Interactive Streamlit dashboard
- Clean charts, exported tables, and a one-page recommendations memo

## Key results from the included sample run

- Revenue, gross margin, repeat-purchase rate, and customer concentration are calculated from transaction-level data.
- Discount leakage is isolated by product category and channel instead of being hidden inside average order value.
- Customer groups are ranked by recency, frequency, monetary value, and inactivity risk.
- Recommendations are tied to measurable owners and next actions, not generic observations.

> The included dataset is synthetic but deliberately messy: duplicated rows, missing customer fields, inconsistent category names, refunds, cancelled orders, timezone variations, and outliers. Replace `data/raw/orders.csv` with a real export and run the same pipeline.

## Run locally

```bash
python -m venv .venv
# Windows Git Bash
source .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python run_analysis.py
streamlit run app/dashboard.py
```

Outputs are written to `results/` and `figures/`.

## Project structure

```text
run_analysis.py             one-command pipeline
src/cleaning.py             validation and cleaning rules
src/metrics.py              KPIs, cohorts, RFM, churn risk, forecast
src/visuals.py              publication-ready charts
app/dashboard.py            interactive dashboard
notebooks/                  four guided analyses
data/raw/                   input CSV
results/                    exported business tables and memo
figures/                    charts used in the report
tests/                      pipeline checks
```

## Analyst notes

- Revenue is net of refunds and excludes cancelled orders.
- Gross margin is calculated after product cost and discounts.
- Cohorts are assigned by the customer's first completed order month.
- Churn risk is an operational score based on inactivity relative to each customer's previous purchase pattern. It is not a medical or credit decision.
- Forecasting is intentionally conservative: it uses completed monthly revenue and backtests against the most recent periods.
