import streamlit

LANGUAGES = {
    "English": "en",
    "Polski": "pl",
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS = {
    "en": {
        "base_price_analysis": "Base Price Analysis",
        "forex_pair_analysis": "Forex Pair Analysis",
        "language": "Language",
        "analysis_type": "Analysis Type",
        "start_date": "Start Date",
        "currency": "Currency",
        "first_currency": "First Currency",
        "second_currency": "Second Currency",
        "1 Week": "1 Week",
        "2 Weeks": "2 Weeks",
        "1 Month": "1 Month",
        "1 Quarter": "1 Quarter",
        "Half a Year": "Half a Year",
        "1 Year": "1 Year",
        "Monthly": "Monthly",
        "Quarterly": "Quarterly",
        "fetching_exchange_rates": "Fetching exchange rates...",
        "failed_to_retrieve": "Failed to retrieve exchange rates: {error}",
        "no_data_returned": "No data returned for the selected range.",
        "no_overlapping_dates": "No overlapping dates between the two currencies.",
        "not_enough_data": "Not enough data points to compute changes.",
        "price": "Price",
        "date": "Date",
        "rate_pln": "Rate (PLN)",
        "current_price": "Current Price",
        "statistical_indicators": "Statistical Indicators",
        "median": "Median",
        "mode": "Mode",
        "standard_deviation": "Standard Deviation",
        "coefficient_of_variation": "Coefficient of Variation",
        "indicator": "Indicator",
        "value": "Value",
        "price_changes": "Price Changes",
        "upwards": "Upwards",
        "no_change": "No Change",
        "downwards": "Downwards",
        "type": "Type",
        "count": "Count",
        "cross_rate_distribution": "Cross-Rate Change Distribution — {pair}",
        "frequency": "Frequency",
        "change": "Change",
        "bin_range": "Bin Range",
    },
    "pl": {
        "base_price_analysis": "Analiza ceny bazowej",
        "forex_pair_analysis": "Analiza pary walutowej",
        "language": "Język",
        "analysis_type": "Typ analizy",
        "start_date": "Data początkowa",
        "currency": "Waluta",
        "first_currency": "Pierwsza waluta",
        "second_currency": "Druga waluta",
        "1 Week": "1 tydzień",
        "2 Weeks": "2 tygodnie",
        "1 Month": "1 miesiąc",
        "1 Quarter": "1 kwartał",
        "Half a Year": "Pół roku",
        "1 Year": "1 rok",
        "Monthly": "Miesięcznie",
        "Quarterly": "Kwartalnie",
        "fetching_exchange_rates": "Pobieranie kursów walut...",
        "failed_to_retrieve": "Nie udało się pobrać kursów walut: {error}",
        "no_data_returned": "Brak danych dla wybranego zakresu.",
        "no_overlapping_dates": "Brak wspólnych dat dla obu walut.",
        "not_enough_data": "Za mało punktów danych, aby obliczyć zmiany.",
        "price": "Cena",
        "date": "Data",
        "rate_pln": "Kurs (PLN)",
        "current_price": "Aktualna cena",
        "statistical_indicators": "Wskaźniki statystyczne",
        "median": "Mediana",
        "mode": "Dominanta",
        "standard_deviation": "Odchylenie standardowe",
        "coefficient_of_variation": "Współczynnik zmienności",
        "indicator": "Wskaźnik",
        "value": "Wartość",
        "price_changes": "Zmiany ceny",
        "upwards": "Wzrost",
        "no_change": "Bez zmian",
        "downwards": "Spadek",
        "type": "Typ",
        "count": "Liczba",
        "cross_rate_distribution": "Rozkład zmian kursu krzyżowego — {pair}",
        "frequency": "Częstość",
        "change": "Zmiana",
        "bin_range": "Zakres przedziału",
    },
}


def get_language() -> str:
    return streamlit.session_state.get("language", DEFAULT_LANGUAGE)


def translate(key: str, **kwargs) -> str:
    catalog = TRANSLATIONS.get(get_language(), TRANSLATIONS[DEFAULT_LANGUAGE])
    text = catalog.get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
    return text.format(**kwargs) if kwargs else text
