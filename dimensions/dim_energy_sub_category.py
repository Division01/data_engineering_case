import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np


class DimensionEnergySubCategory(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for energy subcategories.
        Returns a DataFrame with energySubCategory.id and energySubCategory.name.
        """
        # Create the dimension
        dim_energy_subcategory = (
            self.df[["energySubCategory.name"]].drop_duplicates().reset_index(drop=True)
        )
        dim_energy_subcategory["energySubCategory.id"] = (
            dim_energy_subcategory.index + 1
        )
        # Define expected data types
        expected_types = {
            "energySubCategory.id": "int64",  # Expecting integer for ID
            "energySubCategory.name": "object",  # Expecting string for subcategory name
        }
        # Check data types
        check_data_types(dim_energy_subcategory, expected_types)
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

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Energy SubCategory dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
