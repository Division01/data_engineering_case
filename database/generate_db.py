import psycopg2
import json

with open("database_credentials.json", "r") as file:
    credentials = json.load(file)

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
    id SERIAL PRIMARY KEY,
    description TEXT,
    name VARCHAR(255) NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_energy_subcategory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    associatedEnergyCategory VARCHAR(255)
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_date (
    id SERIAL PRIMARY KEY,
    name INT NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_flow_direction (
    id SERIAL PRIMARY KEY,
    description TEXT,
    name VARCHAR(255) NOT NULL
);
"""
)

cursor.execute(
    """
CREATE TABLE dim_metric (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50)
);
"""
)

# Create Fact Table
cursor.execute(
    """
CREATE TABLE fact_energy_metrics (
    id SERIAL PRIMARY KEY,
    energyCategory_id INT REFERENCES dim_energy_category(id),
    energySubCategory_id INT REFERENCES dim_energy_subcategory(id),
    date_id INT REFERENCES dim_date(id),
    flowDirection_id INT REFERENCES dim_flow_direction(id),
    metric_id INT REFERENCES dim_metric(id),
    metric_value FLOAT
);
"""
)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
