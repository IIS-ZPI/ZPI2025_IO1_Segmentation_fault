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
    "AED": "UAE Dirham",
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "AMD": "Armenian Dram",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat",
    "BAM": "Bosnia and Herzegovina Convertible Mark",
    "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka",
    "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc",
    "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano",
    "BRL": "Brazilian Real",
    "BSD": "Bahamian Dollar",
    "BWP": "Botswana Pula",
    "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    "CAD": "Canadian Dollar",
    "CDF": "Congolese Franc",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "COP": "Colombian Peso",
    "CRC": "Costa Rican Colón",
    "CUP": "Cuban Peso",
    "CVE": "Cape Verdean Escudo",
    "CZK": "Czech Koruna",
    "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone",
    "DOP": "Dominican Peso",
    "DZD": "Algerian Dinar",
    "EGP": "Egyptian Pound",
    "ERN": "Eritrean Nakfa",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    "FJD": "Fijian Dollar",
    "GBP": "British Pound",
    "GEL": "Georgian Lari",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GMD": "Gambian Dalasi",
    "GNF": "Guinean Franc",
    "GTQ": "Guatemalan Quetzal",
    "GYD": "Guyanese Dollar",
    "HKD": "Hong Kong Dollar",
    "HNL": "Honduran Lempira",
    "HTG": "Haitian Gourde",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Shekel",
    "INR": "Indian Rupee",
    "IQD": "Iraqi Dinar",
    "IRR": "Iranian Rial",
    "ISK": "Icelandic Króna",
    "JMD": "Jamaican Dollar",
    "JOD": "Jordanian Dinar",
    "JPY": "Japanese Yen",
    "KES": "Kenyan Shilling",
    "KHR": "Cambodian Riel",
    "KGS": "Kyrgyzstani Som",
    "KMF": "Comorian Franc",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "KZT": "Kazakhstani Tenge",
    "LAK": "Lao Kip",
    "LBP": "Lebanese Pound",
    "LKR": "Sri Lankan Rupee",
    "LRD": "Liberian Dollar",
    "LSL": "Lesotho Loti",
    "LYD": "Libyan Dinar",
    "MAD": "Moroccan Dirham",
    "MDL": "Moldovan Leu",
    "MGA": "Malagasy Ariary",
    "MKD": "Macedonian Denar",
    "MMK": "Myanmar Kyat",
    "MNT": "Mongolian Tögrög",
    "MOP": "Macanese Pataca",
    "MRU": "Mauritanian Ouguiya",
    "MUR": "Mauritian Rupee",
    "MVR": "Maldivian Rufiyaa",
    "MWK": "Malawian Kwacha",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "MZN": "Mozambican Metical",
    "NAD": "Namibian Dollar",
    "NGN": "Nigerian Naira",
    "NIO": "Nicaraguan Córdoba",
    "NOK": "Norwegian Krone",
    "NPR": "Nepalese Rupee",
    "NZD": "New Zealand Dollar",
    "OMR": "Omani Rial",
    "PAB": "Panamanian Balboa",
    "PEN": "Peruvian Sol",
    "PGK": "Papua New Guinean Kina",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PYG": "Paraguayan Guaraní",
    "QAR": "Qatari Rial",
    "RON": "Romanian Leu",
    "RSD": "Serbian Dinar",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan Franc",
    "SAR": "Saudi Riyal",
    "SBD": "Solomon Islands Dollar",
    "SCR": "Seychellois Rupee",
    "SDG": "Sudanese Pound",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "SLE": "Sierra Leonean Leone",
    "SOS": "Somali Shilling",
    "SRD": "Surinamese Dollar",
    "SSP": "South Sudanese Pound",
    "STN": "São Tomé and Príncipe Dobra",
    "SVC": "Salvadoran Colón",
    "SYP": "Syrian Pound",
    "SZL": "Eswatini Lilangeni",
    "THB": "Thai Baht",
    "TJS": "Tajikistani Somoni",
    "TMT": "Turkmenistani Manat",
    "TND": "Tunisian Dinar",
    "TOP": "Tongan Paʻanga",
    "TRY": "Turkish Lira",
    "TTD": "Trinidad and Tobago Dollar",
    "TWD": "New Taiwan Dollar",
    "TZS": "Tanzanian Shilling",
    "UAH": "Ukrainian Hryvnia",
    "UGX": "Ugandan Shilling",
    "UYU": "Uruguayan Peso",
    "UZS": "Uzbekistani Som",
    "VES": "Venezuelan Bolívar",
    "VND": "Vietnamese Đồng",
    "VUV": "Vanuatu Vatu",
    "WST": "Samoan Tala",
    "XAF": "Central African CFA Franc",
    "XCD": "East Caribbean Dollar",
    "XCG": "Caribbean Guilder",
    "XOF": "West African CFA Franc",
    "XPF": "CFP Franc",
    "YER": "Yemeni Rial",
    "ZAR": "South African Rand",
    "ZMW": "Zambian Kwacha",
    "ZWG": "Zimbabwe Gold",
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
            min_value=date(2002, 1, 2),
            max_value=maximum_start_date,
        )

    with column_currency:
        currency = streamlit.selectbox(
            "Currency",
            list(CURRENCIES.keys()),
            format_func=lambda code: f"{CURRENCIES[code]} ({code})",
        )

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
            streamlit.dataframe(
                session_counts_df,
                width="stretch",
                hide_index=True,
            )

        with column_chart:
            session_counts_chart = (
                altair.Chart(session_counts_df)
                .mark_bar(color="#000299")
                .encode(
                    y=altair.Y(
                        "Type:N", axis=altair.Axis(title=None, grid=False), sort=None
                    ),
                    x=altair.X(
                        "Count:Q",
                        scale=altair.Scale(
                            domain=[
                                0,
                                max(rising_sessions, steady_sessions, falling_sessions),
                            ]
                        ),
                        axis=altair.Axis(
                            title=None,
                            tickMinStep=1,
                            format="d",
                            tickCount=max(
                                rising_sessions, steady_sessions, falling_sessions
                            ),
                            grid=False,
                        ),
                    ),
                )
                .properties(height=3 * 35 + 38)
            )
            with streamlit.container(border=True):
                streamlit.altair_chart(session_counts_chart, width="stretch")
