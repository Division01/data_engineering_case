import pandas as pd
from datetime import datetime
import os
from fuzzywuzzy import process


def resolve_case_typos(column: pd.DataFrame) -> pd.DataFrame:
    """
    Corrects any case typo on strings. Returns the column if not string.
    eg. If you send in
    a = [mwh, Mwh, MWh, MWh, GWh, Gwh]
    it will return
    b = [MWh, MWh, MWh, MWh, GWh, GWh ]

    Args:
        column (pd.DataFrame): A column from a dataframe

    Returns:
        column (pd.DataFrame): The same column without case issues.
    """
    # Check if the column is of object type (string)
    if column.dtype == "object":
        # Create a lowercase version for grouping
        lowercase_col = column.str.lower()

        # Get the most frequent value for each lowercase group while retaining original casing
        majority_values = column.groupby(lowercase_col).agg(lambda x: x.mode()[0])

        # Map the original values to the majority values, without filling NaNs
        return lowercase_col.map(majority_values)
    else:
        print("Not a string type column.")
        return column


# Function to group similar values and choose the most frequent one
def resolve_typos(column):
    """
    NOT WORKING.
    Was intended to see the similarity between values to get rid of typo.
    It doesn't work yet, need to be refactored.

    Args:
        column (_type_): _description_

    Returns:
        _type_: _description_
    """
    unique_values = column.unique()
    print("unique : %s", unique_values)
    # Dictionary to store the correct (majority) values
    resolved_values = {}

    for value in unique_values:
        # Find close matches (within 90% similarity)
        similar_values = process.extractBests(value, unique_values, score_cutoff=90)
        print("similar : %s", similar_values)
        # [('MWh', 100), ('Mwh', 100)]

        # Get the majority value from the similar ones
        similar_values = [x[0] for x in similar_values]
        majority_value = column[column.isin(similar_values)].mode()[
            0
        ]  # Find the most frequent one
        print("majority_value : %s", majority_value)
        # MWh

        # Map all similar values to the majority value
        for similar in similar_values:
            resolved_values[similar] = majority_value

    return column.replace(resolved_values)


def check_for_duplicates(df: pd.DataFrame):
    """
    Checks that there are no duplicates in the dataframe.
    If there is, logs them in a txt and send back the dataframe without duplicates.

    Args:
        df (pd.DataFrame): dataframe with duplicates

    Returns:
        df (pd.DataFrame): dataframe without duplicates (but keeps one of the duplicates)
    """
    # Check for duplicates
    duplicates = df[df.duplicated(keep=False)]  # Keep all duplicates for logging

    # Prepare the directory for logs
    log_directory = "duplicates_logs"
    os.makedirs(log_directory, exist_ok=True)  # Create directory if it doesn't exist

    # Get today's date in the format YYYYMMDD
    today_date = datetime.now().strftime("%Y%m%d")

    # Log duplicates to a text file
    if not duplicates.empty:
        log_file_path = os.path.join(log_directory, f"{today_date}.txt")
        duplicates.to_csv(
            log_file_path, index=True
        )  # Write DataFrame to file with index
    else:
        print("No duplicates found.")

    # Remove duplicates, keeping one copy
    cleaned_df = df.drop_duplicates()

    return cleaned_df


def check_data_types(df: pd.DataFrame, expected_types: dict):
    """
    Checks if the DataFrame columns match the expected data types.
    Raises a ValueError if any data type does not match.
    """
    for column, expected_type in expected_types.items():
        if df[column].dtype != expected_type:
            raise ValueError(
                f"Column '{column}' has type {df[column].dtype}, expected {expected_type}."
            )
    print("All data types match the expected values.")


if __name__ == "__main__":
    # Sample DataFrame
    data = {
        "Energy Category": ["Fossil", "Renewable", "Fossil", "Fossil"],
        "Energy Subcategory": ["Crude Oil", "Solar", "Coal", "Coal"],
    }
    df = pd.DataFrame(data)
    print(check_for_duplicates(df))
