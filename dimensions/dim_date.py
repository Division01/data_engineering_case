import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np


class DimensionDate(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for dates.
        Returns a DataFrame with date.id and year stored in date.name.
        """
        # Create the dimension
        dim_date = self.df[["date.name"]].drop_duplicates().reset_index(drop=True)
        dim_date["date.id"] = dim_date.index + 1

        # Rename the column to reflect that it represents years
        # dim_date.rename(columns={"date.name": "date.year"}, inplace=True)

        # Define expected data types
        expected_types = {
            "date.id": "int64",  # Expecting integer for ID
            "date.name": "int64",  # Expecting integer for year
        }

        # Check data types
        check_data_types(dim_date, expected_types)

        self.dim = dim_date

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
        # Load dim_date
        for index, row in self.dim.iterrows():
            cursor.execute(
                """
                INSERT INTO dim_date (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
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

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Date dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
