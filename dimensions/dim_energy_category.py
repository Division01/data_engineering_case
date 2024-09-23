import pandas as pd
from custom_library import check_data_types, clean_data, load_db_credentials
import psycopg2
import numpy as np


def make_dim_energy_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for energy categories.
    Returns a DataFrame with energyCategory.id and energyCategory.name.
    """
    # Create the dimension
    dim_energy_category = (
        df[["energyCategory.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_energy_category["energyCategory.id"] = dim_energy_category.index + 1

    # Define expected data types
    expected_types = {
        "energyCategory.id": "int64",  # Expecting integer for ID
        "energyCategory.name": "object",  # Expecting string for category name
    }

    # Check data types
    check_data_types(dim_energy_category, expected_types)

    return dim_energy_category


def extract(file_path: str) -> pd.DataFrame:
    """
    For now only excel source.
    Returns the dataframe content of the excel.
    """
    return pd.read_excel(file_path, header=1)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean input data and makes the energy category dimension.

    Args:
        df (pd.DataFrame): Input data from dataframe.

    Returns:
        dim_date_df (pd.DataFrame): EnergyCategory dimension
    """
    df = clean_data(df)
    dim_energy_category_df = make_dim_energy_category(df)
    return dim_energy_category_df


def load(dim_energy_category: pd.DataFrame):
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

    for index, row in dim_energy_category.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_energy_category (energyCategory_id, energyCategory_name)
            VALUES (%s, %s)
            ON CONFLICT (energyCategory_id) DO NOTHING;
            """,
            (
                (
                    int(row["energyCategory.id"])
                    if isinstance(row["energyCategory.id"], np.integer)
                    else row["energyCategory.id"]
                ),
                row["energyCategory.name"],
            ),
        )


def main(path: str):
    dataframe = extract(filepath=path)
    cleaned_data = transform(dataframe)
    load(dim_energy_category=cleaned_data)


if __name__ == "__main__":
    main(path="Case - Energy consumption and production.xlsx")
