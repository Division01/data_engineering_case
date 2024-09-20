import pandas as pd
from custom_library import check_data_types


def make_dim_energy_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dimension for energy subcategories.
    Returns a DataFrame with energySubCategory.id and energySubCategory.name.
    """
    # Create the dimension
    dim_energy_subcategory = (
        df[["energySubCategory.name"]].drop_duplicates().reset_index(drop=True)
    )
    dim_energy_subcategory["energySubCategory.id"] = dim_energy_subcategory.index + 1

    # Define expected data types
    expected_types = {
        "energySubCategory.id": "int64",  # Expecting integer for ID
        "energySubCategory.name": "object",  # Expecting string for subcategory name
    }

    # Check data types
    check_data_types(dim_energy_subcategory, expected_types)

    return dim_energy_subcategory
