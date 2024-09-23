import pandas as pd
from custom_library import check_data_types, clean_data, load_db_credentials
import psycopg2
import numpy as np


def make_dim_metric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for metrics.
    Returns a DataFrame with metric.id, metric.name, and metric.unit.
    """
    # Create the dimension
    dim_metric = (
        df[["metric.name", "metric.unit"]].drop_duplicates().reset_index(drop=True)
    )
    dim_metric["metric.id"] = dim_metric.index + 1

    # Define expected data types
    expected_types = {
        "metric.id": "int64",  # Expecting integer for ID
        "metric.name": "object",  # Expecting string for metric name
        "metric.unit": "object",  # Expecting string for metric unit
    }

    # Check data types
    check_data_types(dim_metric, expected_types)

    return dim_metric


def extract(file_path: str) -> pd.DataFrame:
    """
    For now only excel source.
    Returns the dataframe content of the excel.
    """
    return pd.read_excel(file_path, header=1)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean input data and makes the metric dimension.

    Args:
        df (pd.DataFrame): Input data from dataframe.

    Returns:
        dim_date_df (pd.DataFrame): Metric dimension
    """
    df = clean_data(df)
    dim_energy_subcategory_df = make_dim_metric(df)
    return dim_energy_subcategory_df


def load(dim_metric: pd.DataFrame):

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

    for index, row in dim_metric.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_metric (metric_id, metric_name, metric_unit)
            VALUES (%s, %s, %s)
            ON CONFLICT (metric_id) DO NOTHING;
            """,
            (
                (
                    int(row["metric.id"])
                    if isinstance(row["metric.id"], np.integer)
                    else row["metric.id"]
                ),
                row["metric.name"],
                row["metric.unit"],
            ),
        )


def main(path: str):
    dataframe = extract(filepath=path)
    cleaned_data = transform(dataframe)
    load(dim_metric=cleaned_data)


if __name__ == "__main__":
    main(path="Case - Energy consumption and production.xlsx")
