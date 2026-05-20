import pandas


def change_distribution_analysis(
    data1: pandas.DataFrame, data2: pandas.DataFrame
) -> list[dict[float, int]]:

    data1_distribution: dict[float, int] = {}
    data2_distribution: dict[float, int] = {}

    return [data1_distribution, data2_distribution]
