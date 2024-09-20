import pandas as pd
from custom_library import check_data_types


def make_dim_metric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for metrics.
    Returns a DataFrame with metric.id, metric.name, and metric.unit.
    """
    # Create the dimension
    dim_metric = (
        df[["metric.name", "metric.unit"]].drop_duplicates().reset_index(drop=True)
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

    return dim_metric
