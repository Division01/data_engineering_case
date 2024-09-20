import pandas as pd
from custom_library import check_data_types


def make_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for dates.
    Returns a DataFrame with date.id and year stored in date.name.
    """
    # Create the dimension
    dim_date = df[["date.name"]].drop_duplicates().reset_index(drop=True)
    dim_date["date.id"] = dim_date.index + 1

    # Rename the column to reflect that it represents years
    # dim_date.rename(columns={"date.name": "date.year"}, inplace=True)

    # Define expected data types
    expected_types = {
        "date.id": "int64",  # Expecting integer for ID
        "date.name": "int64",  # Expecting integer for year
    }

    # Check data types
    check_data_types(dim_date, expected_types)

    return dim_date
