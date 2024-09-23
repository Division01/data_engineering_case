import pandas as pd
from custom_library import check_data_types, clean_data, load_db_credentials
import psycopg2
import numpy as np


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


def extract(file_path: str) -> pd.DataFrame:
    """
    For now only excel source.
    Returns the dataframe content of the excel.
    """
    return pd.read_excel(file_path, header=1)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean input data and makes the date dimension.

    Args:
        df (pd.DataFrame): Input data from dataframe.

    Returns:
        dim_date_df (pd.DataFrame): Date dimension
    """
    df = clean_data(df)
    dim_date_df = make_dim_date(df)
    return dim_date_df


def load(dim_date: pd.DataFrame):
    credentials = load_db_credentials("database_credentials.json")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=credentials["dbname"],
        user=credentials["user"],
        password=credentials["password"],
        host=credentials["host"],
        port=credentials["port"],
    )
    cursor = conn.cursor()
    cursor.execute("SET search_path TO public;")
    # Load dim_date
    for index, row in dim_date.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_date (date_id, date_name)
            VALUES (%s, %s)
            ON CONFLICT (date_id) DO NOTHING;
            """,
            (
                (
                    int(row["date.id"])
                    if isinstance(row["date.id"], np.integer)
                    else row["date.id"]
                ),
                (
                    int(row["date.name"])
                    if isinstance(row["date.name"], np.integer)
                    else row["date.name"]
                ),
            ),
        )


def main(path: str):
    dataframe = extract(filepath=path)
    cleaned_data = transform(dataframe)
    load(dim_date=cleaned_data)


if __name__ == "__main__":
    main(path="Case - Energy consumption and production.xlsx")
