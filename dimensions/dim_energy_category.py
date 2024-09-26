import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np
from config import ENERGY_CATEGORY_FILE_PATH


class DimensionEnergyCategory(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for energy categories from EnergyCategory.xlsx.
        Checks that the number of unique categories in the Excel file matches the input DataFrame.

        """
        # Load the initial dimension from EnergyCategory.xlsx
        dim_energy_category = pd.read_excel(ENERGY_CATEGORY_FILE_PATH)

        # Rename columns to match expected format
        dim_energy_category.rename(
            columns={
                "name": "energyCategory.name",
                "description": "energyCategory.description",
            },
            inplace=True,
        )

        # Assign IDs (since they are not present in your file)
        dim_energy_category["energyCategory.id"] = range(
            1, len(dim_energy_category) + 1
        )

        # Verify that the number of categories in the Excel file matches the input DataFrame
        unique_categories_input = self.df["energyCategory.name"].nunique()
        unique_categories_excel = dim_energy_category["energyCategory.name"].nunique()

        if unique_categories_input != unique_categories_excel:
            print(
                f"Warning: Mismatch in category counts! "
                f"Input DataFrame: {unique_categories_input}, "
                f"Excel File: {unique_categories_excel}"
            )
        else:
            print("Category count matches between the input DataFrame and Excel file.")

        # Define expected data types and validate data types
        expected_types = {
            "energyCategory.id": "int64",  # Expecting integer for ID
            "energyCategory.name": "object",  # Expecting string for category name
            "energyCategory.description": "object",  # Expecting string for description
        }

        check_data_types(dim_energy_category, expected_types)

        # Store the dimension
        self.dim = dim_energy_category

    def load(self) -> None:
        """
        Load the transformed data into the database stored in db_config.
        Makes a correction of type between SQL and Pandas int type.
        """
        conn = psycopg2.connect(
            dbname=self.db_config["dbname"],
            user=self.db_config["user"],
            password=self.db_config["password"],
            host=self.db_config["host"],
            port=self.db_config["port"],
        )
        cursor = conn.cursor()
        cursor.execute("SET search_path TO public;")

        for index, row in self.dim.iterrows():
            cursor.execute(
                """
                INSERT INTO dim_energy_category (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (
                    (
                        int(row["energyCategory.id"])
                        if isinstance(row["energyCategory.id"], np.integer)
                        else row["energyCategory.id"]
                    ),
                    row["energyCategory.name"],
                    row["energyCategory.description"],
                ),
            )

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Energy Category dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
