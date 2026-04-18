import pandas
import requests


def retrieve_exchange_rates(currency: str, start_date, end_date) -> pandas.DataFrame:
    """
    Fetches exchange rates data from the official NBP API and returns it as a DataFrame.
    """

    uri = (
        f"https://api.nbp.pl/api/exchangerates/rates/A/"
        f"{currency}/{start_date}/{end_date}/?format=json"
    )

    response = requests.get(uri)

    if response.status_code != 200:
        raise ValueError(f"NBP API Error: {response.status_code}")

    data = response.json()

    exchange_rates = [x["mid"] for x in data["rates"]]

    return pandas.DataFrame(exchange_rates, columns=["rate"])
