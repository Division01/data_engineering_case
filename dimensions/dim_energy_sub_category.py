import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np
from config import ENERGY_SUBCATEGORY_FILE_PATH


class DimensionEnergySubCategory(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for energy subcategories from EnergySubCategory.xlsx.
        Dimension of type : []
        """
        # Load the initial dimension from EnergySubCategory.xlsx
        dim_energy_subcategory = pd.read_excel(ENERGY_SUBCATEGORY_FILE_PATH)

        # Rename columns to match expected format
        dim_energy_subcategory.rename(
            columns={
                "name": "energySubCategory.name",
                "description": "energySubCategory.description",
                "Associated energyCategory": "energySubCategory.associatedEnergyCategory",
            },
            inplace=True,
        )

        # Create the "Unknown" subcategory row as a DataFrame
        unknown_subcategory = pd.DataFrame(
            {
                "energySubCategory.name": ["Unknown"],
                "energySubCategory.description": [
                    "Total energy category consumption for the year"
                ],
                "energySubCategory.associatedEnergyCategory": [
                    "Fossil"
                ],  # Adjust this as needed
            }
        )

        # Assuming dim_energy_subcategory is already defined
        dim_energy_subcategory = pd.concat(
            [dim_energy_subcategory, unknown_subcategory], ignore_index=True
        )

        # Assign IDs (since they are not present in the Excel file)
        dim_energy_subcategory["energySubCategory.id"] = range(
            1, len(dim_energy_subcategory) + 1
        )

        # Define expected data types and validate
        expected_types = {
            "energySubCategory.id": "int64",  # Expecting integer for subcategory ID
            "energySubCategory.name": "object",  # Expecting string for subcategory name
            "energySubCategory.description": "object",  # Expecting string for description
            "energySubCategory.associatedEnergyCategory": "object",  # List of associated categories
        }

        check_data_types(dim_energy_subcategory, expected_types)

        # Store the dimension (with no formal link, just a check)
        self.dim = dim_energy_subcategory

    def load(self):
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
                INSERT INTO dim_energy_subcategory (id, name, description, associatedEnergyCategory)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (
                    (
                        int(row["energySubCategory.id"])
                        if isinstance(row["energySubCategory.id"], np.integer)
                        else row["energySubCategory.id"]
                    ),
                    row["energySubCategory.name"],
                    row["energySubCategory.description"],
                    row["energySubCategory.associatedEnergyCategory"],
                ),
            )

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Energy SubCategory dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
