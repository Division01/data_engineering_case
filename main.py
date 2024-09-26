import pandas as pd
import psycopg2
import numpy as np
from dimensions.dim_date import make_dim_date
from dimensions.dim_energy_category import make_dim_energy_category
from dimensions.dim_energy_sub_category import make_dim_energy_subcategory
from dimensions.dim_flow_direction import make_dim_flow_direction
from dimensions.dim_metric import make_dim_metric
from custom_library import clean_data
from facts.fact_energy_metrics import make_fact_energy_metrics, load_fact
from config import EXCEL_MAIN_DATA_FILE_PATH

# file_path = "Case - Energy consumption and production modif.xlsx"
file_path = EXCEL_MAIN_DATA_FILE_PATH


def make_dims(df: pd.DataFrame) -> dict:
    dimensions = {}
    dimensions["dim_energy_category"] = make_dim_energy_category(df)
    dimensions["dim_energy_subcategory"] = make_dim_energy_subcategory(df)
    dimensions["dim_date"] = make_dim_date(df)
    dimensions["dim_flow_direction"] = make_dim_flow_direction(df)
    dimensions["dim_metric"] = make_dim_metric(df)

    # Preview dimension tables
    print("Dimension - Energy Category:\n", dimensions["dim_energy_category"])
    print("Dimension - Energy Sub Category:\n", dimensions["dim_energy_subcategory"])
    print("Dimension - Date:\n", dimensions["dim_date"])
    print("Dimension - Flow Direction:\n", dimensions["dim_flow_direction"])
    print("Dimension - Metric:\n", dimensions["dim_metric"])

    return dimensions


def load_dimensions(dimensions: dict) -> None:
    """
    Loads dimension tables into the PostgreSQL database.
    """
    conn = psycopg2.connect(
        dbname="energy_db",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()
    cursor.execute("SET search_path TO public;")

    # Load dim_energy_category
    for index, row in dimensions["dim_energy_category"].iterrows():
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

    # Load dim_energy_subcategory
    for index, row in dimensions["dim_energy_subcategory"].iterrows():
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

    # Load dim_date
    for index, row in dimensions["dim_date"].iterrows():
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

    # Load dim_flow_direction
    for index, row in dimensions["dim_flow_direction"].iterrows():
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

    # Load dim_metric
    for index, row in dimensions["dim_metric"].iterrows():
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

    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":

    ## EXTRACT
    df = pd.read_excel(file_path, header=1)

    ## TRANSFORM
    df = clean_data(df)

    # Create dimensions and load them into the database
    dimensions = make_dims(df)
    load_dimensions(dimensions)

    # Create fact table and load into the database
    fact_energy_metrics = make_fact_energy_metrics(df, dimensions)

    ## LOAD
    load_fact(fact_energy_metrics)
