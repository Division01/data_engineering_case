import pandas as pd
from dimensions.dim_class import Dimension
from custom_library import check_data_types
import psycopg2
import numpy as np


class DimensionMetric(Dimension):
    def make_dim(self) -> None:
        """
        Creates a dimension for metrics.
        Returns a DataFrame with metric.id, metric.name, and metric.unit.
        """
        # Create the dimension
        dim_metric = (
            self.df[["metric.name", "metric.unit"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )
        dim_metric["metric.id"] = dim_metric.index + 1

        # Define expected data types
        expected_types = {
            "metric.id": "int64",  # Expecting integer for ID
            "metric.name": "object",  # Expecting string for metric name
            "metric.unit": "object",  # Expecting string for metric unit
        }

        # Check data types
        check_data_types(dim_metric, expected_types)
        self.dim = dim_metric

    def load(self):
        """
        Load the transformed data into the database stored in db_config.
        Makes a correction of type between SQL and Pandas int type.
        """
        print(self.dim)
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

        # Commit the changes to the database
        conn.commit()

        print("Load finished for Metric dimension.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
