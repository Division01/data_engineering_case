import pandas as pd 

def make_dim_metric(df:pd.DataFrame):
    """
    metric.id
    metric_name
    metric_unit
    """
    # Dimension - Metric (currently fixed as "Energy" and unit "MWh", but scalable)
    dim_metric = df[['metric.name', 'metric.unit']].drop_duplicates().reset_index(drop=True)
    dim_metric['metric.id'] = dim_metric.index + 1 
    return dim_metric