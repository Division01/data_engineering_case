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

## Future Work
- Implement the database schema in PostgreSQL.
- Develop scripts to load the transformed data into the database.
- Create BI dashboards to visualize energy consumption data with different breakdowns and drill-through functionality.

## Requirements
- Python 3.x
- Pandas
- PostgreSQL (or another database of choice)
- Additional libraries for data visualization (e.g., Matplotlib, Seaborn)

## How to Run
1. Set up the database schema as outlined in the project structure.
2. Run the ETL scripts to extract, transform, and load data.
3. Use your preferred BI tool to connect to the database and visualize the data.

## License
This project is licensed under the MIT License.
