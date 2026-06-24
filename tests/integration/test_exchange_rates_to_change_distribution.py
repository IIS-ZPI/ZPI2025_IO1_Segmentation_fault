import unittest
from unittest.mock import patch

from src.utils.exchange_rates import get_exchange_rates
from src.utils.change_distribution_analysis import change_distribution_analysis
from ._integration_helpers import mock_nbp_response, rates_from_values


class TestExchangeRatesToChangeDistribution(unittest.TestCase):

    @patch("src.utils.exchange_rates.requests.get")
    def test_rounding_to_two_decimals(self, mock_get):
        mock_get.side_effect = [
            mock_nbp_response(rates_from_values([4.001, 4.202, 4.103])),
            mock_nbp_response(rates_from_values([3.0, 3.2, 3.1])),
        ]
        df1 = get_exchange_rates("EUR", "2025-01-02", "2025-01-04")
        df2 = get_exchange_rates("USD", "2025-01-02", "2025-01-04")
        result = change_distribution_analysis(df1, df2)
        for key in result[0]:
            self.assertEqual(key, round(key, 2))


if __name__ == "__main__":
    unittest.main()
