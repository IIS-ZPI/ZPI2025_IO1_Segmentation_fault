from typing import Union

import pandas


def calculate_statistical_measures(
    dataset: Union[pandas.DataFrame, pandas.Series, list[float]],
) -> dict[str, float | None]:
    """
    This function calculates statistical measures from a given dataset and returns them in a structured dictionary format.

    Parameters:
        dataset: Dataset containing a set of values over a time interval.

    Returns:
        dict: A structured dictionary containing median, mode, standard deviation, and coefficients of variation.
    """

    if isinstance(dataset, pandas.DataFrame):
        if "rate" not in dataset.columns:
            raise ValueError("DataFrame must contain a 'rate' column!")
        values = dataset["rate"]
    elif isinstance(dataset, pandas.Series):
        values = dataset
    else:
        values = pandas.Series(dataset)

    if values.empty:
        raise ValueError("Dataset is empty!")

    median_value = values.median()

    mode_series = values.mode()
    mode_value = mode_series.iloc[0] if not mode_series.empty else None

    standard_deviation_value = values.std()

    mean_value = values.mean()
    coefficient_of_variation_value = (
        standard_deviation_value / mean_value if mean_value != 0 else None
    )

    return {
        "median": median_value,
        "mode": mode_value,
        "standard_deviation": standard_deviation_value,
        "coefficient_of_variation": coefficient_of_variation_value,
    }
