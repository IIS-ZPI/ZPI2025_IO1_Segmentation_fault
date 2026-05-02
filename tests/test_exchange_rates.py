import unittest
from unittest.mock import Mock, patch

import pandas as pd

from src.utils.exchange_rates import get_exchange_rates


class TestGetExchangeRates(unittest.TestCase):
    @patch("src.utils.exchange_rates.requests.get")
    def test_successful_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": [
                {"effectiveDate": "2024-01-02", "mid": 4.0},
                {"effectiveDate": "2024-01-03", "mid": 4.1},
                {"effectiveDate": "2024-01-02", "mid": 4.2},
                {"effectiveDate": "2024-01-03", "mid": 4.3},
                {"effectiveDate": "2024-01-02", "mid": 4.4},
                {"effectiveDate": "2024-01-03", "mid": 4.5},
            ]
        }
        mock_get.return_value = mock_response

        dataframe = get_exchange_rates("USD", "2024-01-02", "2024-01-03")

        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertEqual(list(dataframe.columns), ["date", "rate"])
        self.assertEqual(len(dataframe), len(mock_response.json.return_value["rates"]))
        self.assertAlmostEqual(dataframe.iloc[0]["rate"], 4.0)

    @patch("src.utils.exchange_rates.requests.get")
    def test_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_exchange_rates("USD", "2024-01-02", "2024-01-03")

    @patch("src.utils.exchange_rates.requests.get")
    def test_empty_rates(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": []}
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_exchange_rates("USD", "2024-01-02", "2024-01-03")

    def test_start_date_before_allowed(self):
        with self.assertRaises(ValueError):
            get_exchange_rates("USD", "2000-01-01", "2024-01-01")

    def test_end_date_in_future(self):
        future_date = "2999-01-01"
        with self.assertRaises(ValueError):
            get_exchange_rates("USD", "2024-01-01", future_date)

    def test_start_after_end(self):
        with self.assertRaises(ValueError):
            get_exchange_rates("USD", "2024-02-01", "2024-01-01")


if __name__ == "__main__":
    unittest.main()
