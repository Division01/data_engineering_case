import pandas as pd
from custom_library import check_data_types, clean_data, load_db_credentials
import psycopg2
import numpy as np


def make_dim_energy_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for energy subcategories.
    Returns a DataFrame with energySubCategory.id and energySubCategory.name.
    """
    # Create the dimension
    dim_energy_subcategory = (
        df[["energySubCategory.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_energy_subcategory["energySubCategory.id"] = dim_energy_subcategory.index + 1

    # Define expected data types
    expected_types = {
        "energySubCategory.id": "int64",  # Expecting integer for ID
        "energySubCategory.name": "object",  # Expecting string for subcategory name
    }

    # Check data types
    check_data_types(dim_energy_subcategory, expected_types)

    return dim_energy_subcategory


def extract(file_path: str) -> pd.DataFrame:
    """
    For now only excel source.
    Returns the dataframe content of the excel.
    """
    return pd.read_excel(file_path, header=1)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean input data and makes the energy subcategory dimension.

    Args:
        df (pd.DataFrame): Input data from dataframe.

    Returns:
        dim_date_df (pd.DataFrame): Energy SubCategory dimension
    """
    df = clean_data(df)
    dim_energy_subcategory_df = make_dim_energy_subcategory(df)
    return dim_energy_subcategory_df


def load(dim_energy_subcategory: pd.DataFrame):
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

    for index, row in dim_energy_subcategory.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_energy_subcategory (energySubCategory_id, energySubCategory_name)
            VALUES (%s, %s)
            ON CONFLICT (energySubCategory_id) DO NOTHING;
            """,
            (
                (
                    int(row["energySubCategory.id"])
                    if isinstance(row["energySubCategory.id"], np.integer)
                    else row["energySubCategory.id"]
                ),
                row["energySubCategory.name"],
            ),
        )


def main(path: str):
    dataframe = extract(filepath=path)
    cleaned_data = transform(dataframe)
    load(dim_energy_subcategory=cleaned_data)


if __name__ == "__main__":
    main(path="Case - Energy consumption and production.xlsx")
