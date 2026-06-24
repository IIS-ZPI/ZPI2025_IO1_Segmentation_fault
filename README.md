# Forex Advisory

A Streamlit web application for analyzing historical foreign-exchange rates. It fetches
official rates from the [National Bank of Poland (NBP) API](https://api.nbp.pl/) and
presents statistical insights, price trends, and cross-rate change distributions for
**160+ world currencies**. The interface is available in **English and Polish**.

## Features

The app has a shared header — logo, a language switch, and buttons to move between the two
analysis pages — followed by the selected page.

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

Analysis periods: **1 week, 2 weeks, 1 month, 1 quarter, half a year, or 1 year**.

### Forex Pair Analysis
Compare two currencies by computing their cross-rate (`currency_1 / currency_2`).

- **Cross-rate change distribution** — a histogram (with companion table) of the
  day-to-day changes in the cross-rate, with automatically chosen bins.
- **PLN as a pair side** — the Polish Złoty can be selected as either currency
  (e.g. `USD / PLN`). Since PLN is the NBP's reference currency it has a constant
  rate of `1.0`, so the cross-rate reduces to the other currency's rate in PLN.

Analysis periods: **Monthly (30 days)** or **Quarterly (90 days)**.

### Internationalization
The UI ships with **English** and **Polish** translations, switchable from the language
selector in the header. English is the default. Translations live in
[`src/ui/i18n.py`](src/ui/i18n.py).

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — web UI
- **[pandas](https://pandas.pydata.org/)** / **[NumPy](https://numpy.org/)** — data processing
- **[Altair](https://altair-viz.github.io/)** — charts
- **[Requests](https://requests.readthedocs.io/)** — HTTP client for the NBP API
- **[NBP Web API](https://api.nbp.pl/)** — exchange-rate data source
- **[pytest](https://docs.pytest.org/)** — tests · **flake8** — linting · **PyInstaller** — packaging

## Project Structure

```
.
├── app.py                  # Entry point — bootstraps Streamlit on init.py (used by the packaged executable)
├── init.py                 # Page config, header (logo + language switch + nav), and page routing
├── app.spec                # PyInstaller build spec
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme (colors, font)
├── assets/
│   └── ForexAdvisory.svg   # App logo
├── diagrams/               # UML diagrams (activity, components, sequence)
├── src/
│   ├── ui/
│   │   ├── base_price_analysis.py    # Base Price Analysis page
│   │   ├── forex_pair_analysis.py    # Forex Pair Analysis page
│   │   └── i18n.py                   # English/Polish translations + translate() helper
│   └── utils/
│       ├── exchange_rates.py             # Fetches rates from the NBP API (Table A, falls back to Table B)
│       ├── statistical_measures.py       # Median, mode, std. dev., coeff. of variation
│       ├── session_analysis.py           # Counts rising / steady / falling sessions
│       └── change_distribution_analysis.py  # Frequency distribution of day-to-day changes
└── tests/
    ├── test_*.py           # Unit tests for the utils modules
    ├── integration/        # End-to-end pipeline tests (NBP fetch → analysis)
    └── acceptance/         # Streamlit page-rendering tests (AppTest)
```

## Getting Started

### Prerequisites

- Python 3.11, 3.12, or 3.13
- An internet connection (the app calls the live NBP API)

### Installation

```bash
pip install -r requirements.txt
```

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

Tests live in the `tests/` directory and use [pytest](https://docs.pytest.org/):

```bash
pytest tests/
```

They are organized into three layers:

- **Unit tests** (`tests/test_*.py`) — cover the individual `utils` modules.
- **Integration tests** (`tests/integration/`) — exercise the full pipeline from an NBP
  response through each analysis step.
- **Acceptance tests** (`tests/acceptance/`) — render the Streamlit pages with mocked data
  using Streamlit's `AppTest`.

## Data Source & Limitations

- Exchange rates come from the NBP average rates, quoted against **PLN**. Each request
  tries **Table A** first and falls back to **Table B** for currencies not listed there.
- **PLN** is the NBP's reference currency, so there is no `PLN/PLN` endpoint. It is handled
  as a constant rate of `1.0` for every day in the period, which lets it be used as one
  side of a forex pair.
- The earliest available date is **2 January 2002**; the end date cannot be in the future.
- The NBP API publishes rates only on banking days, so non-trading days are absent from
  the data.

## Diagrams

UML diagrams describing the system live in [`diagrams/`](diagrams/): an activity diagram,
a components diagram, and a sequence diagram.

## Continuous Integration / Delivery

- **CI** (`.github/workflows/ci.yml`) — on pull requests to `main`, `develop`, and
  `release`, runs flake8 linting and the pytest suite across Python 3.11–3.13.
- **CD** (`.github/workflows/cd.yml`) — on push to `release`, builds standalone
  **Linux and Windows** executables with PyInstaller, auto-increments the `v2.0.x`
  version tag, and publishes a GitHub Release with both binaries.
