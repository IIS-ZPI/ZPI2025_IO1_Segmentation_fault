import unittest
import pandas

from src.utils.change_distribution_analysis import change_distribution_analysis


class TestChangeDistributionAnalysis(unittest.TestCase):

    def testNullParameter(self) -> None:
        with self.assertRaises(ValueError):
            change_distribution_analysis(None, None)

    def testEmptyExchangeRates(self) -> None:
        with self.assertRaises(ValueError):
            change_distribution_analysis(
                pandas.DataFrame([]), pandas.DataFrame([])
            )

    def testOnlySteadySessions(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.0},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 5.0},
            {"date": "2024-01-03", "rate": 5.0},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertEqual(result[0], {0.0: 1})
        self.assertEqual(result[1], {0.0: 1})

    def testOnlyFallingSessions(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 5.0},
            {"date": "2024-01-03", "rate": 4.8},
            {"date": "2024-01-04", "rate": 4.6},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 3.8},
            {"date": "2024-01-04", "rate": 3.6},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertEqual(result[0], {-0.2: 2})
        self.assertEqual(result[1], {-0.2: 2})

    def testOnlyRisingSessions(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
            {"date": "2024-01-04", "rate": 4.4},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 1.0},
            {"date": "2024-01-03", "rate": 1.2},
            {"date": "2024-01-04", "rate": 1.4},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertEqual(result[0], {0.2: 2})
        self.assertEqual(result[1], {0.2: 2})

    def testOnlyOneDataPoint(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 5.0},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertEqual(result[0], {})
        self.assertEqual(result[1], {})

    def testMixedSessions(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
            {"date": "2024-01-04", "rate": 4.3},
            {"date": "2024-01-05", "rate": 4.1},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 5.0},
            {"date": "2024-01-03", "rate": 4.8},
            {"date": "2024-01-04", "rate": 4.6},
            {"date": "2024-01-05", "rate": 4.4},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertEqual(result[0], {0.2: 1, 0.1: 1, -0.2: 1})
        self.assertEqual(result[1], {-0.2: 3})

    def testOutputFormat(self) -> None:
        data1 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 4.0},
            {"date": "2024-01-03", "rate": 4.2},
        ])
        data2 = pandas.DataFrame([
            {"date": "2024-01-02", "rate": 5.0},
            {"date": "2024-01-03", "rate": 4.8},
        ])

        result = change_distribution_analysis(data1, data2)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertIsInstance(result[1], dict)
