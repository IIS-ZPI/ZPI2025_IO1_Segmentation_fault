import unittest

from streamlit.testing.v1 import AppTest


class TestForexPairAnalysisAcceptance(unittest.TestCase):

    def test_page_renders_with_valid_data(self):
        def app():
            import pandas
            from unittest.mock import patch
            from src.ui.forex_pair_analysis import render as render_forex

            df1 = pandas.DataFrame({
                "date": pandas.to_datetime([
                    "2025-01-02", "2025-01-03", "2025-01-06", "2025-01-07"
                ]),
                "rate": [4.0, 4.1, 4.2, 4.1],
            })
            df2 = pandas.DataFrame({
                "date": pandas.to_datetime([
                    "2025-01-02", "2025-01-03", "2025-01-06", "2025-01-07"
                ]),
                "rate": [3.0, 3.1, 3.2, 3.1],
            })
            with patch(
                "src.ui.forex_pair_analysis.get_exchange_rates",
                side_effect=[df1, df2],
            ):
                render_forex()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.selectbox), 3)
        self.assertEqual(at.selectbox[0].label, "Analysis Type")
        self.assertEqual(at.selectbox[1].label, "First Currency")
        self.assertEqual(at.selectbox[2].label, "Second Currency")
        self.assertEqual(len(at.date_input), 1)

        self.assertEqual(len(at.dataframe), 1)

        md_texts = [m.value for m in at.markdown]
        self.assertTrue(
            any("Cross-Rate Change Distribution" in t for t in md_texts),
            msg="Cross-Rate title not found in markdown",
        )

        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.warning), 0)

    def test_no_overlapping_dates_shows_warning(self):
        def app():
            import pandas
            from unittest.mock import patch
            from src.ui.forex_pair_analysis import render as render_forex

            df1 = pandas.DataFrame({
                "date": pandas.to_datetime(["2025-01-02", "2025-01-03"]),
                "rate": [4.0, 4.1],
            })
            df2 = pandas.DataFrame({
                "date": pandas.to_datetime(["2025-02-01", "2025-02-02"]),
                "rate": [3.0, 3.1],
            })
            with patch(
                "src.ui.forex_pair_analysis.get_exchange_rates",
                side_effect=[df1, df2],
            ):
                render_forex()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.warning), 1)
        self.assertIn(
            "No overlapping dates between the two currencies.",
            at.warning[0].value,
        )
        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.dataframe), 0)

    def test_not_enough_data_points_shows_warning(self):
        def app():
            import pandas
            from unittest.mock import patch
            from src.ui.forex_pair_analysis import render as render_forex

            df = pandas.DataFrame({
                "date": pandas.to_datetime(["2025-01-02"]),
                "rate": [4.0],
            })
            with patch(
                "src.ui.forex_pair_analysis.get_exchange_rates",
                side_effect=[df, df],
            ):
                render_forex()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.warning), 1)
        self.assertIn(
            "Not enough data points to compute changes.",
            at.warning[0].value,
        )
        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.dataframe), 0)

    def test_error_state_shows_error_message(self):
        def app():
            from unittest.mock import patch
            from src.ui.forex_pair_analysis import render as render_forex

            with patch(
                "src.ui.forex_pair_analysis.get_exchange_rates",
                side_effect=ValueError("Forex API error"),
            ):
                render_forex()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.error), 1)
        self.assertIn(
            "Failed to retrieve exchange rates", at.error[0].value
        )
        self.assertEqual(len(at.warning), 0)
        self.assertEqual(len(at.dataframe), 0)


if __name__ == "__main__":
    unittest.main()
