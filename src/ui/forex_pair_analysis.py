from datetime import date, timedelta

import altair
import numpy
import pandas
import streamlit

from src.utils.exchange_rates import get_exchange_rates

PERIODS = {
    "Monthly": 30,
    "Quarterly": 90,
}

CURRENCIES = {
    "USD": "U.S. Dollar",
    "AUD": "Australian Dollar",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EUR": "Euro",
    "GBP": "British Pound",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli Shekel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "JPY": "Japanese Yen",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PHP": "Philippine Peso",
    "PLN": "Polish Zloty",
    "RON": "Romanian Leu",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "UAH": "Ukrainian Hryvnia",
    "ZAR": "South African Rand",
}


def render():
    streamlit.markdown(
        """
        <style>
        [data-testid="stVerticalBlock"] {
            border-color: #e2e2e2 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    column_type, column_date, column_currency1, column_currency2 = streamlit.columns(4)

    with column_type:
        period_label = streamlit.selectbox("Analysis Type", list(PERIODS.keys()))

    with column_date:
        maximum_start_date = date.today() - timedelta(days=PERIODS[period_label])
        start_date = streamlit.date_input(
            "Start Date",
            value=min(
                date.today() - timedelta(days=PERIODS[period_label]), maximum_start_date
            ),
            max_value=maximum_start_date,
        )

    with column_currency1:
        currency_1 = streamlit.selectbox(
            "First Currency",
            list(CURRENCIES.keys()),
            format_func=lambda code: f"{CURRENCIES[code]} ({code})",
        )

    with column_currency2:
        currency_2 = streamlit.selectbox(
            "Second Currency",
            list(CURRENCIES.keys()),
            index=1,
            format_func=lambda code: f"{CURRENCIES[code]} ({code})",
        )

    end_date = start_date + timedelta(days=PERIODS[period_label])
    if end_date > date.today():
        end_date = date.today()

    try:
        with streamlit.spinner("Fetching exchange rates..."):
            rates_1 = get_exchange_rates(
                currency_1,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
            rates_2 = get_exchange_rates(
                currency_2,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
    except Exception as e:
        streamlit.error(f"Failed to retrieve exchange rates: {e}")
        return

    if rates_1.empty or rates_2.empty:
        streamlit.warning("No data returned for the selected range.")
        return

    rates_1["date"] = pandas.to_datetime(rates_1["date"]).dt.date
    rates_2["date"] = pandas.to_datetime(rates_2["date"]).dt.date

    merged = rates_1.merge(rates_2, on="date", suffixes=("_1", "_2"))

    if merged.empty:
        streamlit.warning("No overlapping dates between the two currencies.")
        return

    merged["cross_rate"] = merged["rate_1"] / merged["rate_2"]

    changes = merged["cross_rate"].diff().dropna()

    if changes.empty:
        streamlit.warning("Not enough data points to compute changes.")
        return

    counts, bin_edges = numpy.histogram(changes, bins="auto")

    bin_ranges = [
        f"[{bin_edges[i]:.6f}, {bin_edges[i + 1]:.6f})"
        for i in range(len(bin_edges) - 1)
    ]

    hist_data = pandas.DataFrame(
        {
            "bin_range": bin_ranges,
            "count": counts,
        }
    )

    currency_1_label = f"{CURRENCIES[currency_1]} ({currency_1})"
    currency_2_label = f"{CURRENCIES[currency_2]} ({currency_2})"

    pair_title = f"{currency_1_label} / {currency_2_label}"

    streamlit.markdown(f"**Cross-Rate Change Distribution — {pair_title}**")

    column_hist, column_table = streamlit.columns(2)

    with column_hist:
        hist_chart = (
            altair.Chart(hist_data)
            .mark_bar(color="#000299")
            .encode(
                x=altair.X("count:Q", axis=altair.Axis(title="Frequency")),
                y=altair.Y(
                    "bin_range:N",
                    title="Change",
                    sort=None,
                    axis=altair.Axis(labelLimit=200),
                ),
            )
            .properties(height=400)
        )
        streamlit.altair_chart(hist_chart, width="stretch")

    with column_table:
        table_data = hist_data[["bin_range", "count"]].copy()
        table_data.columns = ["Bin Range", "Count"]
        streamlit.dataframe(table_data, width="stretch", hide_index=True)
