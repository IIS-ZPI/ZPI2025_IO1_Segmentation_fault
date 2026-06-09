import pandas


def session_analysis(exchange_rates: pandas.DataFrame) -> dict[str, int]:
    RISING_SESSION = "Rising session"
    FALLING_SESSION = "Falling session"
    STEADY_SESSION = "Steady session"

    if exchange_rates is None or exchange_rates.empty:
        raise ValueError("Input data cannot be empty")

    sessions: dict[str, int] = {
        RISING_SESSION: 0,
        FALLING_SESSION: 0,
        STEADY_SESSION: 0
    }

    if len(exchange_rates) < 2:
        return sessions

    diffs = exchange_rates['rate'].diff().dropna()

    sessions[RISING_SESSION] = int((diffs > 0).sum())
    sessions[FALLING_SESSION] = int((diffs < 0).sum())
    sessions[STEADY_SESSION] = int((diffs == 0).sum())

    return sessions
