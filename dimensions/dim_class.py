import pandas as pd
from custom_library import clean_data


class Dimension:
    """
    A class used to represent a Dimension in a star schema ETL process.

    This class handles the extraction, transformation, and loading (ETL)
    of dimension data into a PostgreSQL database.

    Attributes:
    -----------
    source_path : str
        Path to the source Excel file for extraction.
    raw_df : pd.DataFrame
        DataFrame that stores the extracted and transformed data.
    df : pd.DataFrame
        DataFrame that stores the raw_df data after it has been cleaned.
    dim : pd.DataFrame
        DataFrame that stores the dimension after the transform process.
    db_config : dict
        Database configuration details (dbname, user, password, etc.).
    """

    def __init__(
        self,
        source_path: str = None,
        db_config: dict = None,
        raw_df: pd.DataFrame = None,
    ):
        """
        Initialize with the source file path and database configuration.

        source_path: Path to the Excel or data source.
        db_config: A dictionary with database connection info (host, dbname, user, password, port).
        """
        self.source_path = source_path
        self.db_config = db_config
        self.raw_df = raw_df
        self.df = None
        self.dim = None
        if source_path is None and raw_df is None:
            raise BaseException
        elif source_path:
            self.extract()

    def extract(self):
        """
        Extract data from the source file.
        """
        try:
            print("Extracting data from:", self.source_path)
            self.raw_df = pd.read_excel(self.source_path)
            print("Data extracted successfully.")
        except Exception as e:
            print(f"Error during extraction: {e}")

    def transform(self):
        """
        Perform any necessary data transformation. Override this method in subclasses.
        """
        self.df = clean_data(df=self.raw_df)
        self.make_dim()

    def load(self):
        """
        Load the transformed data into the database stored in db_config.
        Makes a correction of type between SQL and Pandas int type.
        """
        raise NotImplementedError(
            "Transform method needs to be implemented in a subclass."
        )

    def make_dim(self):
        """
        Creates the dimension in a dataframe from the cleaned_dataframe.
        """
        raise NotImplementedError(
            "Make_dim method needs to be implemented in a subclass."
        )
