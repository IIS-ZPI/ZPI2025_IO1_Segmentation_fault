from datetime import date, timedelta

import altair
import pandas
import streamlit

from src.utils.exchange_rates import get_exchange_rates
from src.utils.session_analysis import session_analysis
from src.utils.statistical_measures import calculate_statistical_measures

PERIODS = {
    "1 Week": 7,
    "2 Weeks": 14,
    "1 Month": 30,
    "1 Quarter": 90,
    "Half a Year": 180,
    "1 Year": 365,
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
    "RON": "Romanian Leu",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "UAH": "Ukrainian Hryvnia",
    "XDR": "IMF SDR",
    "ZAR": "South African Rand",
}


def render():
    column_type, column_date, column_currency = streamlit.columns(3)

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

    with column_currency:
        currency = streamlit.selectbox("Currency", list(CURRENCIES.keys()))

    end_date = start_date + timedelta(days=PERIODS[period_label])
    if end_date > date.today():
        end_date = date.today()

    try:
        with streamlit.spinner("Fetching exchange rates..."):
            exchange_rates = get_exchange_rates(
                currency,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
    except Exception as e:
        streamlit.error(f"Failed to retrieve exchange rates: {e}")
        return

    if exchange_rates.empty:
        streamlit.warning("No data returned for the selected range.")
        return

    exchange_rates["date"] = pandas.to_datetime(exchange_rates["date"]).dt.date

    current_price = exchange_rates["rate"].iloc[-1]
    previous_price = (
        exchange_rates["rate"].iloc[-2] if len(exchange_rates) > 1 else current_price
    )
    price_change = current_price - previous_price
    price_change_pct = (
        (price_change / previous_price * 100) if previous_price != 0 else 0
    )
    price_change_color = "#d32f2f" if price_change < 0 else "#2e7d32"

    price_container = streamlit.container(border=True)

    with price_container:
        column_chart, column_price = streamlit.columns([3, 1])

        with column_chart:
            streamlit.markdown("**Price**")
            rate_min = exchange_rates["rate"].min()
            rate_max = exchange_rates["rate"].max()
            rate_padding = (rate_max - rate_min) * 0.1
            price_chart = (
                altair.Chart(exchange_rates)
                .mark_line(color="#000299")
                .encode(
                    x=altair.X("date:T", axis=altair.Axis(title=None)),
                    y=altair.Y(
                        "rate:Q",
                        scale=altair.Scale(
                            domain=[rate_min - rate_padding, rate_max + rate_padding]
                        ),
                        axis=altair.Axis(title=None),
                    ),
                )
            )
            current_price_rule = (
                altair.Chart(pandas.DataFrame({"price": [current_price]}))
                .mark_rule(color="#888", strokeDash=[10, 10], opacity=0.25)
                .encode(y=altair.Y("price:Q"))
            )
            streamlit.altair_chart(price_chart + current_price_rule, width="stretch")

        with column_price:
            streamlit.markdown(
                f"""
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: flex-end;
                    justify-content: center;
                    height: 100%;
                    padding-top: 32px;
                    padding-right: 32px;
                ">
                    <div style="
                        font-size: 1rem;
                        font-weight: 600;
                        color: #0a0a0a;
                    ">Current Price</div>
                    <div style="
                        margin-top: 24px;
                        font-size: 1.25rem;
                        color: #888;
                        text-align: right;
                    ">{CURRENCIES[currency]}</div>
                    <div style="
                        font-size: 48px;
                        font-weight: 700;
                        line-height: 1;
                        letter-spacing: -0.02em;
                    ">{current_price:.4f}</div>
                    <div style="
                        background: {price_change_color};
                        margin-top: 8px;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 13px;
                        font-weight: 600;
                        white-space: nowrap;
                    ">{price_change:+.4f} ({price_change_pct:+.2f}%)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    column_stats, column_sessions = streamlit.columns(2)

    with column_stats:
        streamlit.markdown("**Statistical Indicators**")
        statistical_measures = calculate_statistical_measures(exchange_rates)
        statistical_measures_df = pandas.DataFrame(
            [
                ("Median", statistical_measures.get("median")),
                ("Mode", statistical_measures.get("mode")),
                ("Standard Deviation", statistical_measures.get("standard_deviation")),
                (
                    "Coefficient of Variation",
                    statistical_measures.get("coefficient_of_variation"),
                ),
            ],
            columns=["Indicator", "Value"],
        )
        streamlit.dataframe(statistical_measures_df, width="stretch", hide_index=True)

    with column_sessions:
        streamlit.markdown("**Price Changes**")
        session_counts = session_analysis(exchange_rates)
        rising_sessions = session_counts.get("Rising session", 0)
        steady_sessions = session_counts.get("Steady session", 0)
        falling_sessions = session_counts.get("Falling session", 0)

        session_counts_df = pandas.DataFrame(
            [
                ("Upwards", rising_sessions),
                ("No Change", steady_sessions),
                ("Downwards", falling_sessions),
            ],
            columns=["Type", "Count"],
        )

        column_table, column_chart = streamlit.columns(2)

        with column_table:
            streamlit.dataframe(session_counts_df, width="stretch", hide_index=True)

        with column_chart:
            session_counts_chart = (
                altair.Chart(session_counts_df)
                .mark_bar(color="#000299")
                .encode(
                    y=altair.Y("Type:N", axis=altair.Axis(title=None), sort=None),
                    x=altair.X(
                        "Count:Q",
                        scale=altair.Scale(
                            domain=[
                                0,
                                max(rising_sessions, steady_sessions, falling_sessions)
                                + 1,
                            ]
                        ),
                        axis=altair.Axis(title=None),
                    ),
                )
                .properties(height=3 * 35 + 38)
            )
            with streamlit.container(border=True):
                streamlit.altair_chart(session_counts_chart, width="stretch")
