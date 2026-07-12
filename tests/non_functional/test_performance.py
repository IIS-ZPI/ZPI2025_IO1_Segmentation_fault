import time
import unittest
from unittest.mock import Mock, patch

from src.utils.exchange_rates import get_exchange_rates


class TestPerformance(unittest.TestCase):
    @patch("src.utils.exchange_rates.requests.get")
    def test_results_generated_within_two_seconds(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": [
                {"effectiveDate": "2024-01-02", "mid": 4.0},
                {"effectiveDate": "2024-01-03", "mid": 4.1},
                {"effectiveDate": "2024-01-04", "mid": 4.2},
            ]
        }
        mock_get.return_value = mock_response

        start = time.time()
        get_exchange_rates("USD", "2024-01-02", "2024-01-04")
        elapsed = time.time() - start

        self.assertLess(elapsed, 2.0)

    @patch("src.utils.exchange_rates.requests.get")
    def test_no_redundant_api_calls_on_identical_requests(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": [
                {"effectiveDate": "2024-01-02", "mid": 4.0},
                {"effectiveDate": "2024-01-03", "mid": 4.1},
            ]
        }
        mock_get.return_value = mock_response

        get_exchange_rates("USD", "2024-01-02", "2024-01-03")
        get_exchange_rates("USD", "2024-01-02", "2024-01-03")

        self.assertEqual(
            mock_get.call_count, 1,
            msg="Redundant API call detected: identical request was sent twice",
        )


if __name__ == "__main__":
    unittest.main()
