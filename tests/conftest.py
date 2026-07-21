import pytest

from src.utils.exchange_rates import get_exchange_rates


@pytest.fixture(autouse=True)
def _clear_exchange_rate_cache():
    get_exchange_rates.clear()
