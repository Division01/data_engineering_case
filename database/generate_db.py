import psycopg2
from custom_library import load_db_credentials

credentials = load_db_credentials("database_credentials.json")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=credentials["dbname"],
    user=credentials["user"],
    password=credentials["password"],
    host=credentials["host"],
    port=credentials["port"],
)
cursor = conn.cursor()

# Create Dimension Tables
cursor.execute(
    """
CREATE TABLE dim_energy_category (
    energyCategory_id SERIAL PRIMARY KEY,
    energyCategory_name VARCHAR(255) NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_energy_subcategory (
    energySubCategory_id SERIAL PRIMARY KEY,
    energySubCategory_name VARCHAR(255)
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    date_name INT NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_flow_direction (
    flowDirection_id SERIAL PRIMARY KEY,
    flowDirection_name VARCHAR(255) NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_metric (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_unit VARCHAR(50)
);
"""
)

# Create Fact Table
cursor.execute(
    """
CREATE TABLE fact_energy_metrics (
    energyCategory_id INT REFERENCES dim_energy_category(energyCategory_id),
    energySubCategory_id INT REFERENCES dim_energy_subcategory(energySubCategory_id),
    date_id INT REFERENCES dim_date(date_id),
    flowDirection_id INT REFERENCES dim_flow_direction(flowDirection_id),
    metric_id INT REFERENCES dim_metric(metric_id),
    metric_value FLOAT
);
"""
)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
