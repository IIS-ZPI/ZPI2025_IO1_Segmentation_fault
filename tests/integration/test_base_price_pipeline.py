import unittest
from unittest.mock import patch

from src.utils.exchange_rates import get_exchange_rates
from src.utils.session_analysis import session_analysis
from src.utils.statistical_measures import calculate_statistical_measures
from ._integration_helpers import mock_nbp_response, rates_from_values


class TestBasePricePipeline(unittest.TestCase):

    @patch("src.utils.exchange_rates.requests.get")
    def test_price_change_stats_and_sessions(self, mock_get):
        mock_get.return_value = mock_nbp_response(
            rates_from_values([4.0, 4.1, 4.2, 4.1, 4.3, 4.2])
        )
        df = get_exchange_rates("EUR", "2025-01-02", "2025-01-07")

        stats = calculate_statistical_measures(df)
        self.assertAlmostEqual(stats["median"], 4.15)
        self.assertAlmostEqual(stats["mode"], 4.1)

        sessions = session_analysis(df)
        self.assertEqual(sessions["Rising session"], 3)
        self.assertEqual(sessions["Falling session"], 2)
        self.assertEqual(sessions["Steady session"], 0)

    @patch("src.utils.exchange_rates.requests.get")
    def test_single_data_point_edge_case(self, mock_get):
        mock_get.return_value = mock_nbp_response(
            rates_from_values([4.0])
        )
        df = get_exchange_rates("EUR", "2025-01-02", "2025-01-02")

        stats = calculate_statistical_measures(df)
        self.assertAlmostEqual(stats["median"], 4.0)

        sessions = session_analysis(df)
        self.assertEqual(sessions["Rising session"], 0)
        self.assertEqual(sessions["Falling session"], 0)
        self.assertEqual(sessions["Steady session"], 0)

if __name__ == "__main__":
    unittest.main()
