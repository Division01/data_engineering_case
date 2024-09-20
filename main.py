import pandas as pd
import psycopg2
import numpy as np
from dim_date import make_dim_date
from dim_energy_category import make_dim_energy_category
from dim_energy_sub_category import make_dim_energy_subcategory
from dim_flow_direction import make_dim_flow_direction
from dim_metric import make_dim_metric
from custom_library import resolve_case_typos, check_for_duplicates
from fact_energy_metrics import make_fact_energy_metrics

# file_path = "Case - Energy consumption and production modif.xlsx"
file_path = "Case - Energy consumption and production.xlsx"


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


def load_fact(df_fact: pd.DataFrame) -> None:
    """
    Loads fact_energy_metrics table into PostgreSQL database.
    """
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="energy_db",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()
    cursor.execute("SET search_path TO public;")

    # Example of converting NumPy types to native Python types
    for index, row in df_fact.iterrows():
        category_id = (
            float(row["energyCategory.id"])
            if isinstance(row["energyCategory.id"], np.float64)
            else row["energyCategory.id"]
        )
        subcategory_id = (
            float(row["energySubCategory.id"])
            if isinstance(row["energySubCategory.id"], np.float64)
            else row["energySubCategory.id"]
        )
        date_id = (
            int(row["date.id"])
            if isinstance(row["date.id"], np.float64)
            else row["date.id"]
        )
        flow_direction_id = (
            int(row["flowDirection.id"])
            if isinstance(row["flowDirection.id"], np.float64)
            else row["flowDirection.id"]
        )
        metric_id = (
            int(row["metric.id"])
            if isinstance(row["metric.id"], np.float64)
            else row["metric.id"]
        )
        metric_value = (
            float(row["metric.value"])
            if isinstance(row["metric.value"], np.float64)
            else row["metric.value"]
        )

        cursor.execute(
            """
            INSERT INTO fact_energy_metrics (
                energyCategory_id,
                energySubCategory_id,
                date_id,
                flowDirection_id,
                metric_id,
                metric_value
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                category_id,
                subcategory_id,
                date_id,
                flow_direction_id,
                metric_id,
                metric_value,
            ),
        )

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":

    # Read Excel file
    df = pd.read_excel(file_path, header=1)
    df = df.drop(columns=["Helptext"])

    # Resolve case issues and check for duplicates
    for col in df.columns:
        df[col] = resolve_case_typos(df[col])

    df = check_for_duplicates(df)

    # Create dimensions and load them into the database
    dimensions = make_dims(df)
    load_dimensions(dimensions)

    # Create fact table and load into the database
    fact_energy_metrics = make_fact_energy_metrics(df, dimensions)
    load_fact(fact_energy_metrics)
