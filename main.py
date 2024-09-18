import pandas as pd


file_path = "Case - Energy consumption and production.xlsx"


def read_excel_file(path:str) -> pd.DataFrame:
    # Read the Excel file
    excel_data = pd.read_excel(file_path, header=1)

    # Display the first few rows to inspect the contents
    print(excel_data.head())
    return excel_data

def make_dims(df:pd.DataFrame)-> dict:
    dimensions = {}
    dimensions["dim_energy_category"] = make_dim_energy_category(df)
    dimensions["dim_date"]  = make_dim_date(df)
    dimensions["dim_flow_direction"]  = make_dim_flow_direction(df)
    dimensions["dim_metric"]  = make_dim_metric(df)

    # Preview dimension tables
    print("Dimension - Energy Category:\n", dimensions["dim_energy_category"] )
    print("Dimension - Date:\n", dimensions["dim_date"] )
    print("Dimension - Flow Direction:\n", dimensions["dim_flow_direction"] )
    print("Dimension - Metric:\n", dimensions["dim_metric"] )

    return dimensions

def make_dim_energy_category(df:pd.DataFrame):
    """
    energyCategory.id
    energyCategory.name
    energySubCategory.name
    """
    # Dimension - Energy Category & SubCategory
    dim_energy_category = df[['energyCategory.name', 'energySubCategory.name']].drop_duplicates().reset_index(drop=True)
    dim_energy_category['energyCategory.id'] = dim_energy_category.index + 1
    dim_energy_category['energySubCategory.id'] = dim_energy_category.index + 1
    return dim_energy_category

def make_dim_date(df:pd.DataFrame):
    """
    data.id
    year
    """
    # Dimension - Date (extracting year from date column)
    dim_date = df[['date.name']].drop_duplicates().reset_index(drop=True)
    dim_date['date.id'] = dim_date.index + 1
    dim_date['year'] = pd.to_datetime(dim_date['date.name']).dt.year  # Extract year
    return dim_date


def make_dim_flow_direction(df:pd.DataFrame):
    """
    flowDirection.id
    flowDirection_name
    """
    # Dimension - Flow Direction
    dim_flow_direction = df[['flowDirection.name']].drop_duplicates().reset_index(drop=True)
    dim_flow_direction['flowDirection.id'] = dim_flow_direction.index + 1
    return dim_flow_direction

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
    dim_date = dimensions["dim_date"]
    dim_flow_direction = dimensions["dim_flow_direction"]
    dim_metric = dimensions["dim_metric"]

    # Create the fact table by merging all dimension tables with the raw data
    fact_energy_metrics = df.merge(dim_energy_category, left_on=['energyCategory.id', 'energySubCategory.id'], right_on=['energyCategory.id', 'energySubCategory.id'])\
                            .merge(dim_date, left_on='date.id', right_on='date.id')\
                            .merge(dim_flow_direction, left_on='flowDirection.id', right_on='flowDirection.id')\
                            .merge(dim_metric, on=['metric.id', 'metric.unit'], how='left')

    # Create the final fact table with only IDs and metric_value
    fact_energy_metrics = fact_energy_metrics[['energyCategory.id', 'energySubCategory.id', 'date.id', 'flowDirection.id', 'metric.id', 'metric.value']]

    # Preview the fact table
    print("Fact Table:\n", fact_energy_metrics)



if __name__ == '__main__':
    df = read_excel_file(file_path)
    dimensions = make_dims(df)
    fact_energy_metrics = make_fact_energy_metrics(df, dimensions)