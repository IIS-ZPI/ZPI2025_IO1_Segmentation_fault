import pandas


def session_analysis(exchange_rates: pandas.DataFrame) -> dict[str, int]:
    RISING_SESSION = "Rising session"
    FALLING_SESSION = "Falling session"
    STEADY_SESSION = "Steady session"

    sessions: dict[str, int] = {}
    sessions[RISING_SESSION] = 0
    sessions[STEADY_SESSION] = 0
    sessions[FALLING_SESSION] = 0

    return sessions
