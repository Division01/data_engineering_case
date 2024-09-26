import pandas as pd
from custom_library import load_db_credentials
import psycopg2
import numpy as np


def make_fact_energy_metrics(df: pd.DataFrame, dimensions: dict):
    """
    Creates a fact table for energy metrics by merging data with dimension tables.

    The resulting DataFrame contains the following columns:
    - energyCategory.id: ID of the energy category
    - energySubCategory.id: ID of the energy subcategory
    - date.id: ID of the date
    - flowDirection.id: ID of the flow direction
    - metric.id: ID of the metric
    - metric.value: The value of the energy metric

    Parameters:
    - df: DataFrame containing the raw energy data.
    - dimensions: A dictionary of DataFrames for the various dimensions.

    Returns:
    - A DataFrame representing the fact table with IDs and metric values.
    """
    dim_energy_category = dimensions["dim_energy_category"]
    dim_energy_sub_category = dimensions["dim_energy_subcategory"]
    dim_date = dimensions["dim_date"]
    dim_flow_direction = dimensions["dim_flow_direction"]
    dim_metric = dimensions["dim_metric"]

    # Merge the DataFrame with dimension tables using the names
    fact_energy_metrics = (
        df.merge(dim_energy_category, on="energyCategory.name", how="left")
        .merge(dim_energy_sub_category, on="energySubCategory.name", how="left")
        .merge(dim_date, on="date.name", how="left")
        .merge(dim_flow_direction, on="flowDirection.name", how="left")
        .merge(dim_metric, on=["metric.name", "metric.unit"], how="left")
    )

    # Create the final fact table with only IDs and metric.value
    fact_energy_metrics = fact_energy_metrics[
        [
            "energyCategory.id",
            "energySubCategory.id",
            "date.id",
            "flowDirection.id",
            "metric.id",
            "metric.value",
        ]
    ]

    # Handle empty subcategory cases (NaN values)
    fact_energy_metrics.loc[
        fact_energy_metrics["energySubCategory.id"].isna(), "energySubCategory.id"
    ] = 1  # Assuming 1 is for NaN

    # Validate relationships
    validate_energy_relationships(
        fact_energy_metrics, dim_energy_category, dim_energy_sub_category
    )

    # Preview the fact table
    print("Fact Table:\n", fact_energy_metrics)
    return fact_energy_metrics


def validate_energy_relationships(
    fact_df: pd.DataFrame, dim_category: pd.DataFrame, dim_subcategory: pd.DataFrame
) -> None:
    """
    Checks the validity of energy category and subcategory relationships in the fact table.
    Raises a ValueError if any subcategory does not match a valid category.

    Parameters:
    - fact_df: DataFrame containing the fact energy metrics.
    - dim_category: DataFrame containing energy categories.
    - dim_subcategory: DataFrame containing energy subcategories.
    """
    # Create a mapping of subcategories to their associated categories
    # TODO : Read it from a file. Shouldn't be hardcoded.
    valid_relationships = {
        "coal and coal products": ["Fossil"],
        "crude oil and petroleum products": ["Fossil"],
        "natural gas": ["Fossil"],
        "other fossil": ["Fossil"],
        "purchased or acquired electricity, heat, steam, and cooling": [
            "Fossil",
            "Renewable",
        ],
        "fuel (incl. biomass)": ["Renewable"],
        "self-generated non-fuel energy": ["Renewable"],
        "wind": ["Renewable"],
        "solar": ["Renewable"],
    }

    # Check each row in the fact DataFrame
    for index, row in fact_df.iterrows():
        subcategory_id = row["energySubCategory.id"]
        category_id = row["energyCategory.id"]

        # Get subcategory name from the subcategory dimension
        subcategory_name = dim_subcategory.loc[
            dim_subcategory["energySubCategory.id"] == subcategory_id,
            "energySubCategory.name",
        ].values

        # TODO : Validate this check (and the one for category.)
        # If the dimension is created from the excel file it should always exist making this check irrelevant.
        if not subcategory_name.size:
            raise ValueError(
                f"Subcategory ID '{subcategory_id}' not found in subcategory dimension."
            )

        subcategory_name = subcategory_name[0]

        if pd.isna(subcategory_name):
            continue  # Skip NaN for the empty subcategories

        # Check if the subcategory has valid associated categories
        expected_categories = valid_relationships.get(
            subcategory_name.lower(), "Not found"
        )

        if expected_categories == "Not found":
            raise ValueError(
                f"Subcategory name '{subcategory_name}' not found in valid relationship."
            )

        # Get the actual category name from the category dimension
        actual_category = dim_category.loc[
            dim_category["energyCategory.id"] == category_id, "energyCategory.name"
        ].values

        # TODO : Like above, valide this check.
        if not actual_category.size:
            raise ValueError(
                f"Category ID '{category_id}' not found in category dimension."
            )

        actual_category = actual_category[0]

        # Check if the actual category is in the expected categories
        if actual_category not in expected_categories:
            raise ValueError(
                f"Subcategory '{subcategory_name}' with ID '{subcategory_id}' is associated with an invalid category '{actual_category}'. Expected categories: {expected_categories}."
            )

    print("All subcategory relationships are valid in the fact table.")


def load_fact(df_fact: pd.DataFrame) -> None:
    """
    Loads fact_energy_metrics table into PostgreSQL database.
    """
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
