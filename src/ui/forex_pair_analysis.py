from datetime import date, timedelta

import altair
import numpy
import pandas
import streamlit

from src.ui.i18n import translate
from src.utils.exchange_rates import get_exchange_rates

PERIODS = {
    "Monthly": 30,
    "Quarterly": 90,
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

    column_type, column_date, column_currency1, column_currency2 = streamlit.columns(4)

    with column_type:
        period_label = streamlit.selectbox(
            translate("analysis_type"), list(PERIODS.keys()), format_func=translate
        )

    with column_date:
        maximum_start_date = date.today() - timedelta(days=PERIODS[period_label])
        start_date = streamlit.date_input(
            translate("start_date"),
            value=min(
                date.today() - timedelta(days=PERIODS[period_label]), maximum_start_date
            ),
            min_value=date(2002, 1, 2),
            max_value=maximum_start_date,
        )

    with column_currency1:
        currency_1 = streamlit.selectbox(
            translate("first_currency"),
            list(CURRENCIES.keys()),
            format_func=lambda code: f"{CURRENCIES[code]} ({code})",
        )

    with column_currency2:
        currency_2 = streamlit.selectbox(
            translate("second_currency"),
            list(CURRENCIES.keys()),
            index=1,
            format_func=lambda code: f"{CURRENCIES[code]} ({code})",
        )

    end_date = start_date + timedelta(days=PERIODS[period_label])
    if end_date > date.today():
        end_date = date.today()

    try:
        with streamlit.spinner(translate("fetching_exchange_rates")):
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
        streamlit.error(translate("failed_to_retrieve", error=e))
        return

    if rates_1.empty or rates_2.empty:
        streamlit.warning(translate("no_data_returned"))
        return

    rates_1["date"] = pandas.to_datetime(rates_1["date"]).dt.date
    rates_2["date"] = pandas.to_datetime(rates_2["date"]).dt.date

    merged = rates_1.merge(rates_2, on="date", suffixes=("_1", "_2"))

    if merged.empty:
        streamlit.warning(translate("no_overlapping_dates"))
        return

    merged["cross_rate"] = merged["rate_1"] / merged["rate_2"]

    changes = merged["cross_rate"].diff().dropna()

    if changes.empty:
        streamlit.warning(translate("not_enough_data"))
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

    streamlit.markdown(
        f"**{translate('cross_rate_distribution', pair=pair_title)}**"
    )

    column_hist, column_table = streamlit.columns(2)

    with column_hist:
        hist_chart = (
            altair.Chart(hist_data)
            .mark_bar(color="#000299")
            .encode(
                x=altair.X("count:Q", axis=altair.Axis(title=translate("frequency"))),
                y=altair.Y(
                    "bin_range:N",
                    title=translate("change"),
                    sort=None,
                    axis=altair.Axis(labelLimit=200),
                ),
            )
            .properties(height=400)
        )
        streamlit.altair_chart(hist_chart, width="stretch")

    with column_table:
        table_data = hist_data[["bin_range", "count"]].copy()
        table_data.columns = [translate("bin_range"), translate("count")]
        streamlit.dataframe(table_data, width="stretch", hide_index=True)
