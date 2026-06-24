import unittest
from unittest.mock import patch

import pandas

from src.utils.exchange_rates import get_exchange_rates
from src.utils.statistical_measures import calculate_statistical_measures
from ._integration_helpers import mock_nbp_response, rates_from_values


class TestExchangeRatesToStatisticalMeasures(unittest.TestCase):

    @patch("src.utils.exchange_rates.requests.get")
    def test_identical_rates_zero_variation(self, mock_get):
        mock_get.return_value = mock_nbp_response(
            rates_from_values([4.0, 4.0, 4.0])
        )
        df = get_exchange_rates("USD", "2025-01-02", "2025-01-04")
        result = calculate_statistical_measures(df)
        self.assertAlmostEqual(result["median"], 4.0)
        self.assertAlmostEqual(result["mode"], 4.0)
        self.assertAlmostEqual(result["standard_deviation"], 0.0)
        self.assertAlmostEqual(result["coefficient_of_variation"], 0.0)

    @patch("src.utils.exchange_rates.requests.get")
    def test_single_rate(self, mock_get):
        mock_get.return_value = mock_nbp_response(
            rates_from_values([4.0])
        )
        df = get_exchange_rates("USD", "2025-01-02", "2025-01-02")
        result = calculate_statistical_measures(df)
        self.assertAlmostEqual(result["median"], 4.0)
        self.assertAlmostEqual(result["mode"], 4.0)
        self.assertTrue(result["standard_deviation"] is None or pandas.isna(result["standard_deviation"]))


if __name__ == "__main__":
    unittest.main()
