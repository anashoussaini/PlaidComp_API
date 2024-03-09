import pandas as pd


INTERNAL_TO_EXTERNAL_COLUMN_MAPPING = {
    'ID': None,
    'Address': None,
    'Asking Price': None,
    'Bathrooms': None,
    'Bedrooms': None,
    'DOM': None,
    'Living Area': None,
    'Garage': None,
    'Lot Area': None,
    'Municipality': None,
    'Rooms': None,
    'Sold Price': None,
    'Status': None
}


HARDCODED_MAPPING = {
    'ID': 'Centris No.',
    'Address': 'Address',
    'Asking Price': 'Asked/Sold Price',
    'Bathrooms': 'Bathrooms (number)',
    'Bedrooms': 'Bedrooms (number)',
    'DOM': 'DOM',
    'Living Area': 'Living Area (Imperial)',
    'Garage': 'Garage (number)',
    'Lot Area': 'Lot Area (Imperial)',
    'Municipality': 'Mun./Bor.',
    'Rooms': 'Rms',
    'Sold Price': 'Sold / Rented Price',
    'Status': 'ST',
}
import pandas as pd

class PCFormatter:
    """
    A class to format and clean property-centric data frames for analysis.
    """

    def __init__(self, mappings: dict):
        """
        Initialize the PCFormatter with a mapping dictionary.

        Parameters:
        - mappings (dict): A dictionary mapping internal column names to external indices.
        """
        self.mappings = mappings

    def map_columns_to_index(self, df: pd.DataFrame) -> dict:
        """
        Map internal column names to their corresponding index in the DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame whose columns need to be mapped.

        Returns:
        - dict: A dictionary with the internal column names and their index in the DataFrame.
        """
        column_index_mapping = {}
        for internal_name, external_name in self.mappings.items():
            column_index_mapping[internal_name] = df.columns.get_loc(external_name) if external_name in df.columns else None
        return column_index_mapping

    def create_pc_format_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a DataFrame with columns reordered and renamed according to a valid mapping.

        Parameters:
        - df (pd.DataFrame): The original DataFrame to format.

        Returns:
        - pd.DataFrame: The reformatted DataFrame.
        """
        valid_mapping = {k: v for k, v in self.mappings.items() if v is not None}
        new_df = pd.DataFrame()
        for internal_name, external_index in valid_mapping.items():
            new_df[internal_name] = df.iloc[:, external_index]
        return new_df

    def clean_numeric_columns(self, df: pd.DataFrame, columns_to_clean: list) -> pd.DataFrame:
        """
        Clean specified numeric columns in the DataFrame, removing non-numeric characters.

        Parameters:
        - df (pd.DataFrame): The DataFrame to clean.
        - columns_to_clean (list): A list of columns to apply numeric cleaning.

        Returns:
        - pd.DataFrame: The cleaned DataFrame.
        """
        columns_to_clean = ['Bathrooms', 'Bedrooms', 'DOM', 'Living Area', 'Garage', 'Lot Area', 'Rooms', 'Sold Price']

        clean_to_num = lambda x: pd.to_numeric(''.join(c for c in str(x) if c.isdigit() or c == '.'), errors='coerce')
        for column in columns_to_clean:
            if column in df.columns:
                df[column] = df[column].astype(str).apply(clean_to_num)
        return df

