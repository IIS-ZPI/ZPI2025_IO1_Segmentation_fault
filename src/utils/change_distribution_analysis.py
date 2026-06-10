import pandas
from collections import Counter


def change_distribution_analysis( data1: pandas.DataFrame, data2: pandas.DataFrame) -> list:
    if data1 is None or data2 is None:
        raise ValueError('data1 or data2 is None')

    if data1.empty or data2.empty:
        raise ValueError('data1 or data2 is empty')

    def get_distribution(df):

        changes = df['rate'].diff().dropna()
        changes = changes.round(2)
        return dict(Counter(changes))

    return [get_distribution(data1), get_distribution(data2)]


