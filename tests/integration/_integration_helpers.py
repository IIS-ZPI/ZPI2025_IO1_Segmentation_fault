from datetime import datetime, timedelta
from unittest.mock import Mock


def mock_nbp_response(rates, status_code=200, error_text=""):
    resp = Mock()
    resp.status_code = status_code
    if status_code == 200:
        resp.json.return_value = {"rates": rates}
    else:
        resp.text = error_text or "Error"
    return resp


def rates_from_values(values, start="2025-01-02"):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    return [
        {"effectiveDate": (start_dt + timedelta(days=i)).strftime("%Y-%m-%d"), "mid": v}
        for i, v in enumerate(values)
    ]
