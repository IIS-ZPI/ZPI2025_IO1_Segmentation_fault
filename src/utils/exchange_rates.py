from datetime import date, datetime, timedelta

import pandas
import requests
import streamlit

FIRST_VALID_DATE = datetime(2002, 1, 2)


@streamlit.cache_data(ttl=timedelta(hours=1))
def get_exchange_rates(
    currency: str, start_date: str, end_date: str
) -> pandas.DataFrame:
    """
    This function fetches historical exchange rates for a given currency in a given period from the official NBP API.

    Parameters:
        currency (str): Currency in ISO4217 code format.
        start_date (str): Start date in string format 'YYYY-MM-DD'
        end_date (str): End date in string format 'YYYY-MM-DD'

    Returns:
        pandas.DataFrame: DataFrame with dates and the exchange rate for each one.
    """

    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

    if start_datetime < FIRST_VALID_DATE:
        raise ValueError("The start date cannot be before the 2nd of January 2002!")

    if end_datetime.date() > date.today():
        raise ValueError("The end date cannot be in the future!")

    if start_datetime > end_datetime:
        raise ValueError("The end date cannot be before the start date!")

    endpoint = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency.lower()}/{start_date}/{end_date}/?format=json"

    response = requests.get(endpoint)

    if response.status_code != 200:
        raise ValueError(f"Cannot retrieve the exhange rates: {response.text}")

    data = response.json()

    exchange_rates = data.get("rates", [])

    if not exchange_rates:
        raise ValueError("No data returned with the given parameters.")

    exchange_rates = pandas.DataFrame(exchange_rates)

    exchange_rates = exchange_rates.loc[:, ["effectiveDate", "mid"]]

    exchange_rates.columns = ["date", "rate"]

    exchange_rates["date"] = pandas.to_datetime(exchange_rates["date"])

    return exchange_rates
