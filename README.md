# Forex Advisory

A Streamlit web application for analyzing historical foreign-exchange rates. It fetches
official rates from the [National Bank of Poland (NBP) API](https://api.nbp.pl/) and
presents statistical insights, price trends, and cross-rate change distributions for 30+
world currencies.

## Features

The app is organized into two analysis pages:

### Base Price Analysis
Analyze a single currency against the Polish Złoty (PLN).

- **Price chart** — line chart of the exchange rate over the selected period, with a
  reference line marking the current price.
- **Current price card** — latest rate plus the absolute and percentage change from the
  previous session, color-coded for gains and losses.
- **Statistical indicators** — median, mode, standard deviation, and coefficient of
  variation.
- **Price changes (sessions)** — a count of rising, steady, and falling sessions, shown
  as both a table and a bar chart.

### Forex Pair Analysis
Compare two currencies by computing their cross-rate (`currency_1 / currency_2`).

- **Cross-rate change distribution** — a histogram (with companion table) of the
  day-to-day changes in the cross-rate, with automatically chosen bins.

Both pages let you choose an **analysis period** (e.g. 1 week up to 1 year), a **start
date**, and the **currency / currency pair** to analyze.

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — web UI
- **[pandas](https://pandas.pydata.org/)** / **[NumPy](https://numpy.org/)** — data processing
- **[Altair](https://altair-viz.github.io/)** — charts
- **[NBP Web API](https://api.nbp.pl/)** — exchange-rate data source

## Project Structure

```
.
├── app.py                  # Entry point — launches Streamlit on init.py
├── init.py                 # Page config, logo, and navigation between analysis pages
├── requirements.txt        # Python dependencies
├── assets/
│   └── ForexAdvisory.svg   # App logo
├── src/
│   ├── ui/
│   │   ├── base_price_analysis.py    # Base Price Analysis page
│   │   └── forex_pair_analysis.py    # Forex Pair Analysis page
│   └── utils/
│       ├── exchange_rates.py             # Fetches rates from the NBP API
│       ├── statistical_measures.py       # Median, mode, std. dev., coeff. of variation
│       ├── session_analysis.py           # Counts rising / steady / falling sessions
│       └── change_distribution_analysis.py
└── tests/                  # pytest unit tests for the utils modules
```

## Getting Started

### Prerequisites

- Python 3.11, 3.12, or 3.13
- An internet connection (the app calls the live NBP API)

### Running the app

Either run through the entry point:

```bash
python app.py
```

or start Streamlit directly:

```bash
streamlit run init.py
```

The app opens in your browser (default: <http://localhost:8501>).

## Running Tests

Unit tests live in the `tests/` directory and use [pytest](https://docs.pytest.org/):

```bash
pytest tests/
```

## Data Source & Limitations

- Exchange rates come from the NBP "Table A" average rates, quoted against **PLN**.
- The earliest available date is **2 January 2002**; the end date cannot be in the future.
- The NBP API publishes rates only on banking days, so non-trading days are absent from
  the data.

## Continuous Integration / Delivery

- **CI** (`.github/workflows/ci.yml`) — on pull requests to `main`, `develop`, and
  `release`, runs flake8 linting and the pytest suite across Python 3.11–3.13.
- **CD** (`.github/workflows/cd.yml`) — on push to `release`, builds a standalone
  executable with PyInstaller, auto-increments the version tag, and publishes a GitHub
  Release.
