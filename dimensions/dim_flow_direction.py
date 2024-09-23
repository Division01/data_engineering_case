import pandas as pd
from custom_library import check_data_types, clean_data, load_db_credentials
import psycopg2
import numpy as np


def make_dim_flow_direction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for flow directions.
    Returns a DataFrame with flowDirection.id and flowDirection.name.
    """
    # Create the dimension
    dim_flow_direction = (
        df[["flowDirection.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_flow_direction["flowDirection.id"] = dim_flow_direction.index + 1

    # Define expected data types
    expected_types = {
        "flowDirection.id": "int64",  # Expecting integer for ID
        "flowDirection.name": "object",  # Expecting string for name
    }

    # Check data types
    check_data_types(dim_flow_direction, expected_types)

    return dim_flow_direction


def extract(file_path: str) -> pd.DataFrame:
    """
    For now only excel source.
    Returns the dataframe content of the excel.
    """
    return pd.read_excel(file_path, header=1)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean input data and makes the flow direction dimension.

    Args:
        df (pd.DataFrame): Input data from dataframe.

    Returns:
        dim_date_df (pd.DataFrame): Flow direction dimension
    """
    df = clean_data(df)
    dim_energy_subcategory_df = make_dim_flow_direction(df)
    return dim_energy_subcategory_df


def load(dim_flow_direction: pd.DataFrame):
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

    for index, row in dim_flow_direction.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_flow_direction (flowDirection_id, flowDirection_name)
            VALUES (%s, %s)
            ON CONFLICT (flowDirection_id) DO NOTHING;
            """,
            (
                (
                    int(row["flowDirection.id"])
                    if isinstance(row["flowDirection.id"], np.integer)
                    else row["flowDirection.id"]
                ),
                row["flowDirection.name"],
            ),
        )


def main(path: str):
    dataframe = extract(filepath=path)
    cleaned_data = transform(dataframe)
    load(dim_flow_direction=cleaned_data)


if __name__ == "__main__":
    main(path="Case - Energy consumption and production.xlsx")
