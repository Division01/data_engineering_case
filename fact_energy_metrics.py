import pandas as pd

def make_fact_energy_metrics(df:pd.DataFrame, dimensions:dict):
    """
    metric.id
    energyCategory.id
    energySubCategory.id
    date.id
    flowDirection.id
    metric_value
    """
    dim_energy_category = dimensions["dim_energy_category"]
    dim_energy_sub_category = dimensions["dim_energy_subcategory"]
    dim_date = dimensions["dim_date"]
    dim_flow_direction = dimensions["dim_flow_direction"]
    dim_metric = dimensions["dim_metric"]

    # # Create the fact table by merging all dimension tables with the raw data
    # fact_energy_metrics = df.merge(dim_energy_category, on=['energyCategory.id', 'energySubCategory.id'])\
    #                         .merge(dim_date, left_on='date.id', right_on='date.id')\
    #                         .merge(dim_flow_direction, on='flowDirection.id')\
    #                         .merge(dim_metric, on=['metric.id', 'metric.unit'], how='left')

    # # Create the final fact table with only IDs and metric_value
    # fact_energy_metrics = fact_energy_metrics[['energyCategory.id', 'energySubCategory.id', 'date.id', 'flowDirection.id', 'metric.id', 'metric.value']]

    # # Preview the fact table
    # print("Fact Table:\n", fact_energy_metrics)

    # Merge the DataFrame with dimension tables using the IDs instead of the names
    fact_energy_metrics = df.merge(dim_energy_category, on='energyCategory.name', how='left')\
                            .merge(dim_energy_sub_category, on='energySubCategory.name', how='left')\
                            .merge(dim_date, on='date.name', how='left')\
                            .merge(dim_flow_direction, on='flowDirection.name', how='left')\
                            .merge(dim_metric, on=['metric.name', 'metric.unit'], how='left')

    # Create the final fact table with only IDs and metric_value
    fact_energy_metrics = fact_energy_metrics[['energyCategory.id', 'energySubCategory.id', 'date.id', 'flowDirection.id', 'metric.id', 'metric.value']]

    # Preview the fact table
    print("Fact Table:\n", fact_energy_metrics)

