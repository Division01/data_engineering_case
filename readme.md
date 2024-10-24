# Energy Consumption Data Pipeline

## Overview
This project involves creating a data pipeline to extract, transform, and load (ETL) energy consumption data into a structured database. The primary goal is to enable data visualization through a BI dashboard, allowing for various breakdowns of energy consumption metrics.

## Project Structure

### ETL Process
1. **Extract**: Data is extracted from Excel files containing energy consumption metrics.
2. **Transform**: The data is cleaned, validated, and transformed into a star schema consisting of fact and dimension tables.
3. **Load**: The transformed data will be loaded into a database (e.g., PostgreSQL) for further analysis and visualization.

## Star Schema Structure

### Fact Table
**`fact_energy_metrics`**
- `energyCategory.id` (FK)
- `energySubCategory.id` (FK, nullable)
- `date.id` (FK)
- `flowDirection.id` (FK)
- `metric.id` (FK)
- `metric_value` (float)

### Dimension Tables
1. **`dim_energy_category`**
   - `energyCategory.id` (int)
   - `energyCategory.name` (string)

2. **`dim_energy_subcategory`**
   - `energySubCategory.id` (int)
   - `energySubCategory.name` (string, nullable)

3. **`dim_date`**
   - `date.id` (int)
   - `data.name` (int)

4. **`dim_flow_direction`**
   - `flowDirection.id` (int)
   - `flowDirection.name` (string)

5. **`dim_metric`**
   - `metric.id` (int)
   - `metric.name` (string)
   - `metric.unit` (string)

## Data Validation
Data validation checks are performed to ensure:
- No duplicates in the data.
- Correct data types for each column.
- Valid relationships between energy categories and subcategories.


## Requirements
- Python 3.x
- Pandas
- PostgreSQL (or another database of choice)

## How to Run
1. Set up a database or a database container. I used for the project : 
```bash
docker run --name test_postgres_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=test_db -p 5432:5432 -d postgres
```
2. Set up the database schema as outlined in the project structure. You can also run the generate_db.py if you already have a postrgresql database.
3. Replace database_credentials_example.json with your data, drop the _example to make it readable by the script.
4. Run main.py to run the ETL scripts to extract, transform, and load all data at once. An version with separate scripts to work on all dimensions on its own to parallelize the process is beging developped.
5. Use your preferred BI tool to connect to the database and visualize the data.

## Restore the database 
To restore the database from the .sql file, run the database/database_backup.sql file in a PostgreSQL instance.
This wouldn't make sense as the whole point of the excercise was to create a Database with the data from the excel, but whatever floats your boat.

## Future Work
- A better data validation function to catch typos.
- Add the structure from excel for EnergyCategory, SubCategory and FlowDirection.
