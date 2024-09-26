import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np


class DimensionEnergyCategory(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for energy categories.
        Checks if the data type is the one expected.
        Returns a DataFrame with energyCategory.id and energyCategory.name.
        """
        # Create the dimension
        dim_energy_category = (
            self.df[["energyCategory.name"]].drop_duplicates().reset_index(drop=True)
        )
        dim_energy_category["energyCategory.id"] = dim_energy_category.index + 1

        # Define expected data types
        expected_types = {
            "energyCategory.id": "int64",  # Expecting integer for ID
            "energyCategory.name": "object",  # Expecting string for category name
        }

        # Check data types
        check_data_types(dim_energy_category, expected_types)

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

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Energy Category dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
