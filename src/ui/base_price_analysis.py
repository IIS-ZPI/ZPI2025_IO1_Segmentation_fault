from datetime import date, timedelta

import streamlit

from src.utils.retrieve_data import retrieve_exchange_rates


def render():
    streamlit.title("Base Price Analysis")

    currency = streamlit.selectbox("Currency", ["USD", "EUR", "GBP", "CHF", "JPY"])

    start_date = streamlit.date_input(
        "Start Date", value=(date.today() - timedelta(days=1))
    )
    end_date = streamlit.date_input("End Date")

    if streamlit.button("Fetch Data"):
        try:
            data = retrieve_exchange_rates(
                currency, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
            )

            streamlit.subheader("Exchange Rate")
            streamlit.line_chart(data)

            streamlit.subheader("Raw Data")
            streamlit.dataframe(data)
        except Exception as error:
            streamlit.error(f"Failed to retrieve exchange rates: {error}")
