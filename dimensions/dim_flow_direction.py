import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np
from config import FLOW_DIRECTION_FILE_PATH


class DimensionFlowDirection(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for flow directions.
        Returns a DataFrame with flowDirection.id, flowDirection.name,
        and flowDirection.description.
        """
        # Load data from the Excel file (assuming it's in self.df)
        dim_flow_direction = pd.read_excel(FLOW_DIRECTION_FILE_PATH)

        # Rename columns to match the expected schema
        dim_flow_direction = dim_flow_direction.rename(
            columns={
                "name": "flowDirection.name",  # Rename Name column to flowDirection.name
                "description": "flowDirection.description",  # Rename Description to flowDirection.description
            }
        )

        # Create a unique ID for each flow direction
        dim_flow_direction["flowDirection.id"] = dim_flow_direction.index + 1

        # Define expected data types
        expected_types = {
            "flowDirection.id": "int64",  # Expecting integer for ID
            "flowDirection.name": "object",  # Expecting string for flow direction name
            "flowDirection.description": "object",  # Expecting string for flow direction description
        }

        # Check data types
        check_data_types(dim_flow_direction, expected_types)

        # Assign the final DataFrame to the dimension
        self.dim = dim_flow_direction

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
                INSERT INTO dim_flow_direction (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (
                    (
                        int(row["flowDirection.id"])
                        if isinstance(row["flowDirection.id"], np.integer)
                        else row["flowDirection.id"]
                    ),
                    row["flowDirection.name"],
                    row["flowDirection.description"],
                ),
            )

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Flow Direction dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
