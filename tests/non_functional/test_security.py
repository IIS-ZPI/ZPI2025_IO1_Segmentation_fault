import unittest
from unittest.mock import Mock, patch

from src.utils.exchange_rates import get_exchange_rates


class TestSecurity(unittest.TestCase):
    @patch("src.utils.exchange_rates.requests.get")
    def test_api_communication_uses_https(self, mock_get):
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

        called_url = mock_get.call_args[0][0]
        self.assertTrue(
            called_url.startswith("https://"),
            msg=f"API URL does not use HTTPS: {called_url}",
        )
        self.assertNotIn("http://", called_url.replace("https://", ""))


if __name__ == "__main__":
    unittest.main()
