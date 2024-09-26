import pandas as pd
from dimensions.dim_date import DimensionDate
from dimensions.dim_energy_category import DimensionEnergyCategory
from dimensions.dim_energy_sub_category import DimensionEnergySubCategory
from dimensions.dim_flow_direction import DimensionFlowDirection
from dimensions.dim_metric import DimensionMetric
from custom_library import load_db_credentials
from facts.fact_energy_metrics import make_fact_energy_metrics, load_fact
from config import EXCEL_MAIN_DATA_FILE_PATH


if __name__ == "__main__":

    db_config = load_db_credentials("database_credentials.json")

    ## EXTRACT
    df = pd.read_excel(EXCEL_MAIN_DATA_FILE_PATH, header=1)

    # DimensionEnergyCategory
    dim_energy_category = DimensionEnergyCategory(raw_df=df, db_config=db_config)
    dim_energy_category.transform()
    dim_energy_category.load()
    print(dim_energy_category.dim)

    # DimensionDate
    dim_date = DimensionDate(raw_df=df, db_config=db_config)
    dim_date.transform()
    dim_date.load()

    # DimensionEnergySubCategory
    dim_energy_subcategory = DimensionEnergySubCategory(raw_df=df, db_config=db_config)
    dim_energy_subcategory.transform()
    dim_energy_subcategory.load()

    # DimensionFlowDirection
    dim_flow_direction = DimensionFlowDirection(raw_df=df, db_config=db_config)
    dim_flow_direction.transform()
    dim_flow_direction.load()

    # DimensionMetric
    dim_metric = DimensionMetric(raw_df=df, db_config=db_config)
    dim_metric.transform()
    dim_metric.load()

    dimensions = {
        "dim_energy_category": dim_energy_category.dim,
        "dim_date": dim_date.dim,
        "dim_energy_subcategory": dim_energy_subcategory.dim,
        "dim_flow_direction": dim_flow_direction.dim,
        "dim_metric": dim_metric.dim,
    }

    # Create fact table and load into the database
    # We use dim_metric.df instead of df to get the cleaned one.
    fact_energy_metrics = make_fact_energy_metrics(
        df=dim_metric.df, dimensions=dimensions
    )

    ## LOAD
    load_fact(fact_energy_metrics)
