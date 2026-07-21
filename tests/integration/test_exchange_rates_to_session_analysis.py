import unittest
from unittest.mock import patch

from src.utils.exchange_rates import get_exchange_rates
from src.utils.session_analysis import session_analysis
from ._integration_helpers import mock_nbp_response, rates_from_values


class TestExchangeRatesToSessionAnalysis(unittest.TestCase):

    @patch("src.utils.exchange_rates.requests.get")
    def test_two_points_one_rising_diff(self, mock_get):
        mock_get.return_value = mock_nbp_response(
            rates_from_values([4.0, 4.2])
        )
        df = get_exchange_rates("EUR", "2025-01-02", "2025-01-03")
        sessions = session_analysis(df)
        self.assertEqual(sessions["Rising session"], 1)
        self.assertEqual(sessions["Falling session"], 0)
        self.assertEqual(sessions["Steady session"], 0)


if __name__ == "__main__":
    unittest.main()
