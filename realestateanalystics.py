import pandas as pd

class RealEstateAnalytics:
    """
    A class that encapsulates methods for performing analytics on real estate data.
    """
    
    def calculate_status_statistics(self, df: pd.DataFrame, status_column: str = 'Status') -> dict:
        """
        Calculate and return the count of different statuses within the DataFrame.

        Parameters:
        - df (pd.DataFrame): The DataFrame to process.
        - status_column (str): The name of the column containing status data.

        Returns:
        - dict: A dictionary with status counts.
        """
        status_counts = df[status_column].value_counts()
        return status_counts.to_dict()

    def graph_sqft_price(self, df: pd.DataFrame, sqft_column: str = 'Living Area', price_column: str = 'Sold Price') -> tuple:
        """
        Prepare data for a scatter plot showing price per square foot.

        Parameters:
        - df (pd.DataFrame): The DataFrame to process.
        - sqft_column (str): The name of the column containing square footage data.
        - price_column (str): The name of the column containing sold price data.

        Returns:
        - tuple: Two lists containing the x and y values for the graph.
        """
        valid_entries = df.dropna(subset=[sqft_column, price_column])
        x_values = valid_entries[sqft_column]
        y_values = valid_entries[price_column] / valid_entries[sqft_column]
        return x_values.tolist(), y_values.tolist()

    def graph_sold_price_dom(self, df: pd.DataFrame, price_column: str = 'Sold Price', dom_column: str = 'DOM') -> tuple:
        """
        Prepare data for a scatter plot showing sold price by days on market (DOM).

        Parameters:
        - df (pd.DataFrame): The DataFrame to process.
        - price_column (str): The name of the column containing sold price data.
        - dom_column (str): The name of the column containing days on market data.

        Returns:
        - tuple: Two lists containing the x and y values for the graph.
        """
        valid_entries = df.dropna(subset=[price_column, dom_column])
        x_values = valid_entries[dom_column]
        y_values = valid_entries[price_column]
        return x_values.tolist(), y_values.tolist()

    def calculate_average(self, df: pd.DataFrame, column_name: str) -> float:
        """
        Calculate the average of a given column.

        Parameters:
        - df (pd.DataFrame): The DataFrame to process.
        - column_name (str): The name of the column to calculate the average for.

        Returns:
        - float: The average value of the specified column.
        """
        return df[column_name].mean()

    def calculate_statistics(self, df: pd.DataFrame, uncleaned_df: pd.DataFrame) -> dict:
        """
        Calculate a set of statistics and graph data from the DataFrame.

        Parameters:
        - df (pd.DataFrame): The '\' DataFrame to process.
        - uncleaned_df (pd.DataFrame): The original DataFrame to calculate status counts.

        Returns:
        - dict: A dictionary containing various calculated statistics and graph data.
        """
        statistics = {
            'Average Bathrooms': self.calculate_average(df, 'Bathrooms'),
            'Average Bedrooms': self.calculate_average(df, 'Bedrooms'),
            'Average DOM': self.calculate_average(df, 'DOM'),
            'Average Living Area': self.calculate_average(df, 'Living Area'),
            'Average Garage': self.calculate_average(df, 'Garage'),
            'Average Lot Area': self.calculate_average(df, 'Lot Area'),
            'Average Rooms': self.calculate_average(df, 'Rooms'),
            'Average Sold Price': self.calculate_average(df, 'Sold Price'),
            'Status Counts': self.calculate_status_statistics(uncleaned_df)
        }
        
        # Graph Data
        statistics['Graph - Sqft/Price X'], statistics['Graph - Sqft/Price Y'] = self.graph_sqft_price(df)
        statistics['Graph - Sold Price/DOM X'], statistics['Graph - Sold Price/DOM Y'] = self.graph_sold_price_dom(df)

        return statistics



class GraphGenerator:
    def __init__(self):
        pass