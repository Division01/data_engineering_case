import pandas as pd
from datetime import datetime
import os
import json


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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataframe.
    First drops the helptext column.
    Then resolve case typos so that "Mwh" and MWh" is the same.
    Finaly check for duplicates before returning the dataframe.

    Args:
        df (pd.DataFrame): Input raw dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    df = df.drop(columns=["Helptext"])

    # Resolve case issues and check for duplicates
    for col in df.columns:
        df[col] = resolve_case_typos(df[col])

    df = check_for_duplicates(df)
    return df


def load_db_credentials(json_file_path):
    with open(json_file_path, "r") as file:
        credentials = json.load(file)
    return credentials


if __name__ == "__main__":
    # Sample DataFrame
    data = {
        "Energy Category": ["Fossil", "Renewable", "Fossil", "Fossil"],
        "Energy Subcategory": ["Crude Oil", "Solar", "Coal", "Coal"],
    }
    df = pd.DataFrame(data)
    print(check_for_duplicates(df))
