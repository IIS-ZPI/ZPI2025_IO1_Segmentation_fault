import unittest

from streamlit.testing.v1 import AppTest


class TestBasePriceAnalysisAcceptance(unittest.TestCase):

    def test_page_renders_with_valid_data(self):
        def app():
            import pandas
            from unittest.mock import patch
            from src.ui.base_price_analysis import render as render_base

            mock_df = pandas.DataFrame({
                "date": pandas.to_datetime([
                    "2025-01-02", "2025-01-03", "2025-01-06", "2025-01-07"
                ]),
                "rate": [4.0, 4.1, 4.2, 4.1],
            })
            with patch(
                "src.ui.base_price_analysis.get_exchange_rates",
                return_value=mock_df,
            ):
                render_base()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.selectbox), 2)
        self.assertEqual(at.selectbox[0].label, "Analysis Type")
        self.assertEqual(at.selectbox[1].label, "Currency")

        self.assertEqual(len(at.date_input), 1)
        self.assertEqual(at.date_input[0].label, "Start Date")

        self.assertEqual(len(at.dataframe), 2)

        md_texts = [m.value for m in at.markdown]
        self.assertTrue(
            any("**Statistical Indicators**" in t for t in md_texts),
            msg="Statistical Indicators heading not found in markdown",
        )
        self.assertTrue(
            any("**Price Changes**" in t for t in md_texts),
            msg="Price Changes heading not found in markdown",
        )

        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.warning), 0)

    def test_error_state_shows_error_message(self):
        def app():
            from unittest.mock import patch
            from src.ui.base_price_analysis import render as render_base

            with patch(
                "src.ui.base_price_analysis.get_exchange_rates",
                side_effect=ValueError("Mock API error"),
            ):
                render_base()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.error), 1)
        self.assertIn(
            "Failed to retrieve exchange rates", at.error[0].value
        )
        self.assertIn("Mock API error", at.error[0].value)
        self.assertEqual(len(at.warning), 0)
        self.assertEqual(len(at.dataframe), 0)

    def test_empty_data_shows_warning(self):
        def app():
            import pandas
            from unittest.mock import patch
            from src.ui.base_price_analysis import render as render_base

            empty_df = pandas.DataFrame({
                "date": pandas.to_datetime([]),
                "rate": [],
            })
            with patch(
                "src.ui.base_price_analysis.get_exchange_rates",
                return_value=empty_df,
            ):
                render_base()

        at = AppTest.from_function(app)
        at.run()

        self.assertEqual(len(at.warning), 1)
        self.assertIn(
            "No data returned for the selected range.",
            at.warning[0].value,
        )
        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.dataframe), 0)


if __name__ == "__main__":
    unittest.main()
