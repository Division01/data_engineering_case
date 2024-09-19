import pandas as pd

def make_dim_energy_category(df:pd.DataFrame):
    """
    energyCategory.id
    energyCategory.name
    """
    # Dimension - Energy Category & SubCategory
    dim_energy_category = df[['energyCategory.name']].drop_duplicates().reset_index(drop=True)
    dim_energy_category['energyCategory.id'] = dim_energy_category.index + 1
    return dim_energy_category