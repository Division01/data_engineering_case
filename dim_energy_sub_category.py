import pandas as pd

def make_dim_energy_subcategory(df:pd.DataFrame):
    """
    energySubCategory.id
    energySubCategory.name
    """
    # Dimension - Energy Category & SubCategory
    dim_energy_subcategory = df[['energySubCategory.name']].drop_duplicates().reset_index(drop=True)
    dim_energy_subcategory['energySubCategory.id'] = dim_energy_subcategory.index + 1
    return dim_energy_subcategory