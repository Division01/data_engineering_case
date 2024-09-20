import pandas as pd
from custom_library import check_data_types


def make_dim_flow_direction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for flow directions.
    Returns a DataFrame with flowDirection.id and flowDirection.name.
    """
    # Create the dimension
    dim_flow_direction = (
        df[["flowDirection.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_flow_direction["flowDirection.id"] = dim_flow_direction.index + 1

    # Define expected data types
    expected_types = {
        "flowDirection.id": "int64",  # Expecting integer for ID
        "flowDirection.name": "object",  # Expecting string for name
    }

    # Check data types
    check_data_types(dim_flow_direction, expected_types)

    return dim_flow_direction
