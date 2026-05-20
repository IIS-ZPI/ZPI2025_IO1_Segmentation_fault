import unittest
import pandas

from src.utils.session_analysis import session_analysis

class TestSessionAnalysis(unittest.TestCase):
    RISING_SESSION_KEY: str = "Rising session"
    STEADY_SESSION_KEY: str = "Steady session"
    FALLING_SESSION_KEY: str = "Falling session"

    def testNullParameter(self) -> None:
        with self.assertRaises(ValueError):
            _ = session_analysis(None)

    def testEmptyExchangeRates(self) -> None:
        with self.assertRaises(ValueError):
            _ = session_analysis(pandas.DataFrame([]))

    def testOnlySteadySessions(self) -> None:
        onlySteadySessions = [
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.0},
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.0},
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.0},
        ]

        data = pandas.DataFrame(onlySteadySessions)
        sessions = session_analysis(data)
        self.assertEqual(sessions[self.RISING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.FALLING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.STEADY_SESSION_KEY], 5)

    def testOnlyFallingSessions(self) -> None:
        onlyFallingSessions = [
            {"date": "2024-01-02", "rate": 5.0},
            {"date": "2024-01-03", "rate": 4.8},
            {"date": "2024-01-04", "rate": 4.6},
            {"date": "2024-01-05", "rate": 4.4},
            {"date": "2024-01-06", "rate": 4.2},
            {"date": "2024-01-07", "rate": 4.0},
        ]

        data = pandas.DataFrame(onlyFallingSessions)
        sessions = session_analysis(data)
        self.assertEqual(sessions[self.RISING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.FALLING_SESSION_KEY], 5)
        self.assertEqual(sessions[self.STEADY_SESSION_KEY], 0)

    def testOnlyRisingSessions(self) -> None:
        onlyRisingSessions = [
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
            {"date": "2024-01-04", "rate": 4.4},
            {"date": "2024-01-05", "rate": 4.6},
            {"date": "2024-01-06", "rate": 4.8},
            {"date": "2024-01-07", "rate": 5.0},
        ]

        data = pandas.DataFrame(onlyRisingSessions)
        sessions = session_analysis(data)
        self.assertEqual(sessions[self.RISING_SESSION_KEY], 5)
        self.assertEqual(sessions[self.FALLING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.STEADY_SESSION_KEY], 0)

    def testOnlyOneDataPoint(self) -> None:
        oneDataPoint = [
            {"date": "2024-01-02", "rate": 4.0},
        ]

        data = pandas.DataFrame(oneDataPoint)
        sessions = session_analysis(data)
        self.assertEqual(sessions[self.RISING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.FALLING_SESSION_KEY], 0)
        self.assertEqual(sessions[self.STEADY_SESSION_KEY], 0)

    def testMixedSessions(self) -> None:
        mixedSessions = [
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
            {"date": "2024-01-04", "rate": 4.3},
            {"date": "2024-01-05", "rate": 4.1},
            {"date": "2024-01-06", "rate": 4.0},
        ]

        data = pandas.DataFrame(mixedSessions)
        sessions = session_analysis(data)
        self.assertEqual(sessions[self.RISING_SESSION_KEY], 2)
        self.assertEqual(sessions[self.FALLING_SESSION_KEY], 2)
        self.assertEqual(sessions[self.STEADY_SESSION_KEY], 0)

    def testOutputFormat(self) -> None:
        sessionsData = [
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
        ]

        data = pandas.DataFrame(sessionsData)
        sessions = session_analysis(data)
        self.assertIsInstance(sessions, dict)
        self.assertIn(self.RISING_SESSION_KEY, sessions)
        self.assertIn(self.FALLING_SESSION_KEY, sessions)
        self.assertIn(self.STEADY_SESSION_KEY, sessions)
        self.assertEqual(len(sessions), 3)


