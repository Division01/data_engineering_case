import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np


class DimensionFlowDirection(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for flow directions.
        Returns a DataFrame with flowDirection.id and flowDirection.name.
        """
        # Create the dimension
        dim_flow_direction = (
            self.df[["flowDirection.name"]].drop_duplicates().reset_index(drop=True)
        )
        dim_flow_direction["flowDirection.id"] = dim_flow_direction.index + 1

        # Define expected data types
        expected_types = {
            "flowDirection.id": "int64",  # Expecting integer for ID
            "flowDirection.name": "object",  # Expecting string for name
        }

        # Check data types
        check_data_types(dim_flow_direction, expected_types)

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

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Flow Direction dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
