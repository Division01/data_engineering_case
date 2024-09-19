import pandas as pd
from dim_date import make_dim_date
from dim_energy_category import make_dim_energy_category
from dim_energy_sub_category import make_dim_energy_subcategory
from dim_flow_direction import make_dim_flow_direction
from dim_metric import make_dim_metric
from custom_library import read_excel_file, clean_dataframe
from fact_energy_metrics import make_fact_energy_metrics

file_path = "Case - Energy consumption and production.xlsx"

def make_dims(df:pd.DataFrame)-> dict:
    dimensions = {}
    dimensions["dim_energy_category"] = make_dim_energy_category(df)
    dimensions["dim_energy_subcategory"] = make_dim_energy_subcategory(df)
    dimensions["dim_date"]  = make_dim_date(df)
    dimensions["dim_flow_direction"]  = make_dim_flow_direction(df)
    dimensions["dim_metric"]  = make_dim_metric(df)

    # Preview dimension tables
    print("Dimension - Energy Category:\n", dimensions["dim_energy_category"] )
    print("Dimension - Energy Sub Category:\n", dimensions["dim_energy_subcategory"] )
    print("Dimension - Date:\n", dimensions["dim_date"] )
    print("Dimension - Flow Direction:\n", dimensions["dim_flow_direction"] )
    print("Dimension - Metric:\n", dimensions["dim_metric"] )

    return dimensions







#TODO patch the MWh and mwh

if __name__ == '__main__':
    df = read_excel_file(file_path=file_path)
    df = clean_dataframe(df)
    dimensions = make_dims(df)
    fact_energy_metrics = make_fact_energy_metrics(df, dimensions)