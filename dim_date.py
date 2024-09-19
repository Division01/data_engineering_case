import pandas as pd


def make_dim_date(df:pd.DataFrame):
    """
    data.id
    year
    """
    # Dimension - Date (extracting year from date column)
    dim_date = df[['date.name']].drop_duplicates().reset_index(drop=True)
    dim_date['date.id'] = dim_date.index + 1
    return dim_date