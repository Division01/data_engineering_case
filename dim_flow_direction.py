import pandas as pd


def make_dim_flow_direction(df:pd.DataFrame):
    """
    flowDirection.id
    flowDirection_name
    """
    # Dimension - Flow Direction
    dim_flow_direction = df[['flowDirection.name']].drop_duplicates().reset_index(drop=True)
    dim_flow_direction['flowDirection.id'] = dim_flow_direction.index + 1
    return dim_flow_direction