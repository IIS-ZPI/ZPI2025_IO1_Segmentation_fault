from unittest.mock import Mock

import pytest
import requests

from src.utils.retrieve_data import retrieve_exchange_rates


def test_retrieve_exchange_rates_api_error(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 404

    def mock_get(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError, match="NBP API Error"):
        retrieve_exchange_rates("EUR", "2024-01-01", "2024-01-03")
