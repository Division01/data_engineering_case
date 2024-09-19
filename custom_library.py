import pandas as pd 

def read_excel_file(file_path:str) -> pd.DataFrame:
    # Read the Excel file
    excel_data = pd.read_excel(file_path, header=1)

    # Display the first few rows to inspect the contents
    print(excel_data.head())
    return excel_data

def clean_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.drop(columns=['Helptext'])  # Replace 'Helptext' with the correct column if necessary
    return df_cleaned