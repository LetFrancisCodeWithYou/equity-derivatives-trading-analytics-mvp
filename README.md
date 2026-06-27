# Equity Derivatives Trading Analytics MVP

A small front-office style equity options analytics MVP built for quant developer / trading analytics applications.

## What it does

- Prices European call and put options using Black-Scholes
- Calculates Greeks: delta, gamma, vega, theta
- Runs simple scenario analysis across spot and volatility shocks
- Displays a basic Streamlit dashboard for pricing and risk analytics
- Uses Python, pandas, NumPy, SciPy, Matplotlib and Streamlit

## Why this project is relevant

This project demonstrates desk-style analytics for equity derivatives:

- Pricing analytics
- Risk analytics
- Greeks and exposures
- Scenario testing
- Dashboard-style tooling for traders/quants
- Python-based quantitative application development

## Quick start

```bash
git clone <your-repo-url>
cd equity-derivatives-trading-analytics-mvp
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows PowerShell

pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
.
├── app.py
├── black_scholes.py
├── requirements.txt
└── README.md
```

## Example outputs

The dashboard returns:

- Option price
- Delta
- Gamma
- Vega
- Theta
- Scenario table
- Price sensitivity chart
## Dashboard Screenshot

![Dashboard screenshot](screenshots/dashboard.png)

## Notes

This is intentionally a small MVP, not a production trading system. It is designed to show practical front-office analytics skills quickly and clearly.
