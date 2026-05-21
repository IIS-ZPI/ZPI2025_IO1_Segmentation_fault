from datetime import date, timedelta

import pandas as pd
import streamlit as st

from src.utils.exchange_rates import get_exchange_rates
from src.utils.statistical_measures import calculate_statistical_measures


def render():
    st.title("Base Price Analysis")

    currency = st.selectbox(
        "Currency",
        ["USD", "EUR", "GBP", "CHF", "JPY"],
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date.today() - timedelta(days=7),
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=date.today(),
        )

    if st.button("Fetch Data"):
        try:
            if start_date > end_date:
                st.error("Start date cannot be after end date.")
                return

            with st.spinner("Fetching exchange rates..."):
                data = get_exchange_rates(
                    currency,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                )

            if data.empty:
                st.warning("No data returned for the selected range.")
                return

            data["date"] = pd.to_datetime(data["date"]).dt.date

            st.subheader("Exchange Rate")
            st.line_chart(data.set_index("date")["rate"])

            st.subheader("Statistical Measures")
            stats = calculate_statistical_measures(data)

            stats_df = pd.DataFrame(
                list(stats.items()),
                columns=["Metric", "Value"],
            )

            st.dataframe(stats_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Failed to retrieve exchange rates: {e}")
