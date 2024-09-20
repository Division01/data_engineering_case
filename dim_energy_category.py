import pandas as pd
from custom_library import check_data_types


def make_dim_energy_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for energy categories.
    Returns a DataFrame with energyCategory.id and energyCategory.name.
    """
    # Create the dimension
    dim_energy_category = (
        df[["energyCategory.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_energy_category["energyCategory.id"] = dim_energy_category.index + 1

    # Define expected data types
    expected_types = {
        "energyCategory.id": "int64",  # Expecting integer for ID
        "energyCategory.name": "object",  # Expecting string for category name
    }

    # Check data types
    check_data_types(dim_energy_category, expected_types)

    return dim_energy_category
