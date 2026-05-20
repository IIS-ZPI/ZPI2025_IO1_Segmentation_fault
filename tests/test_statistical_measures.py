import unittest

import pandas as pd

from src.utils.statistical_measures import calculate_statistical_measures


class TestCalculateStatisticalMeasures(unittest.TestCase):
    def test_valid_dataset(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"rate": [4.0, 4.1, 4.2, 4.1, 4.3, 4.1]})
        result: dict[str, float | None] = calculate_statistical_measures(df)

        self.assertIn("median", result)
        self.assertIn("mode", result)
        self.assertIn("standard_deviation", result)
        self.assertIn("coefficient_of_variation", result)
        self.assertIsNotNone(result["median"])
        self.assertIsNotNone(result["mode"])

        assert result["median"] is not None
        assert result["mode"] is not None

        self.assertAlmostEqual(result["median"], 4.1)
        self.assertAlmostEqual(result["mode"], 4.1)

    def test_missing_rate_column(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"value": [1, 2, 3]})

        with self.assertRaises(ValueError):
            calculate_statistical_measures(df)

    def test_empty_dataset(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"rate": []})

        with self.assertRaises(ValueError):
            calculate_statistical_measures(df)

    def test_multiple_modes_returns_first(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"rate": [1, 2, 2, 3, 3]})
        result: dict[str, float | None] = calculate_statistical_measures(df)

        self.assertIn(result["mode"], [2, 3])

    def test_coefficient_of_variation_zero_mean(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"rate": [0, 0, 0]})
        result: dict[str, float | None] = calculate_statistical_measures(df)

        self.assertIsNone(result["coefficient_of_variation"])

    def test_simple_array_input(self) -> None:
        data: list[float] = [4.0, 4.1, 4.2, 4.1, 4.3, 4.1]
        result: dict[str, float | None] = calculate_statistical_measures(data)

        self.assertIn("median", result)
        self.assertIn("mode", result)
        self.assertIn("standard_deviation", result)
        self.assertIn("coefficient_of_variation", result)
        self.assertIsNotNone(result["median"])
        self.assertIsNotNone(result["mode"])

        assert result["median"] is not None
        assert result["mode"] is not None

        self.assertAlmostEqual(result["median"], 4.1)
        self.assertAlmostEqual(result["mode"], 4.1)


if __name__ == "__main__":
    unittest.main()
