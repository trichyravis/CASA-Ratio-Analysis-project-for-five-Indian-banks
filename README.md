# Indian Bank CASA Ratio Analytics

A classroom-ready Streamlit dashboard comparing the period-end CASA ratios of SBI, HDFC Bank, ICICI Bank, Axis Bank and Kotak Mahindra Bank over FY2021–FY2025. The complete Mountain Path visual design is embedded directly in `app.py`; no separate stylesheet is required.

## Why the app does not call CASA “live market data”

CASA is an accounting ratio disclosed periodically by banks, not a continuously traded value. The most accurate current observation is therefore the latest officially published annual or quarterly figure. This project ships a five-year, source-tagged annual dataset and permits a validated CSV override when a new disclosure is published.

## Features

- Multi-bank and fiscal-year filters
- Five-year trend chart and latest-year ranking
- Heat map, descriptive statistics and trend slope
- Individual bank deep dive with interpretation prompts
- Basis labels (period-end/MEB versus average/QAB)
- Source URL and reporting date for every observation
- CSV download and user-uploaded data override
- Data-quality checks for bounds, duplicates and required fields

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload this project, preserving the `data` folder.
2. In Streamlit Community Cloud choose **Create app**.
3. Select the repository, branch and `app.py`.
4. Deploy. No API key or secret is required.

## Data methodology

The main series uses the ratio at 31 March for each fiscal year. Axis Bank labels the March-end measure MEB; its QAB figure must not be substituted into this series. HDFC Bank’s FY2024 number follows the HDFC Ltd merger and is not strictly comparable with earlier standalone HDFC Bank years. Each row contains `basis`, `source_id` and `notes`; `sources.csv` contains the audit trail.

Formula:

`CASA ratio = (Current account deposits + Savings account deposits) / Total deposits × 100`

For a new year, add one row per bank to `data/casa_ratios.csv`, add the official disclosure to `data/sources.csv`, and run:

```bash
python validate_data.py
```

Never mix average/QAB CASA with period-end/MEB CASA in a single trend without clearly separating the series.

## Suggested classroom discussion

- Why can a falling CASA ratio pressure cost of deposits and NIM?
- Can a high CASA ratio coexist with weak deposit growth?
- Why did HDFC Bank’s merger affect comparability?
- What is the difference between Axis Bank’s MEB and QAB ratios?
- Why should analysts study deposit concentration and stability alongside CASA?

## Disclaimer

Official bank disclosures are the source of record. Recheck the linked report before using the dataset for investment, regulatory or publication purposes. The dashboard is educational and is not investment advice.
