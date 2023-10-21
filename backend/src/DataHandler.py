import pandas as pd
from sqlalchemy import create_engine

class DataHandler:

    def __init__(self, data_source=None, query=None) -> None:
        """
        Initialize the DataHandler object with data from a CSV, Excel, JSON file, or a Pandas DataFrame.

        Args:
            data_source (str or pd.DataFrame, optional): If provided, can be a file path to a CSV, Excel, or JSON file
                or a Pandas DataFrame. If data_source is a database connection URL, provide query parameter.
                Default is None.
            query (str, optional): SQL query to fetch data from the database. Required if data_source is a database connection URL.
                Default is None.

        Raises:
            ValueError: If the provided data_source is not a valid file path, a Pandas DataFrame, or None.
                        If data_source is a database connection URL without a query.

        Example usage:
            # Initialize with a CSV file
            data_handler = DataHandler('path/to/your/data.csv')

            # Initialize with an Excel file
            data_handler = DataHandler('path/to/your/data.xlsx')

            # Initialize with a JSON file
            data_handler = DataHandler('path/to/your/data.json')

            # Initialize with an SQL database
            data_handler = DataHandler('sqlite:///example.db', query='SELECT * FROM your_table')
        """
        if data_source is None:
            self.data = pd.DataFrame()
        else:
            try:
                if isinstance(data_source, str):
                    try:
                        if data_source.endswith('.csv'):
                            self.data = pd.read_csv(data_source)
                        elif data_source.endswith('.xlsx'):
                            self.data = pd.read_excel(data_source, engine='openpyxl')
                        elif data_source.endswith('.xls'):
                            self.data = pd.read_excel(data_source)
                        elif data_source.endswith('.json'):
                            self.data = pd.read_json(data_source)
                        elif query is not None:
                            try:
                                engine = create_engine(data_source)
                                self.data = pd.read_sql(query, engine)
                            except Exception as e:
                                raise Exception(f"Error: Unable to fetch data from the database. {str(e)}")
                        else:
                            raise ValueError("Error: Unsupported file format, incorrect path, or invalid database connection.")
                    except FileNotFoundError:
                        raise ValueError(f"Error: File '{data_source}' not found.")
                elif isinstance(data_source, pd.DataFrame):
                    self.data = data_source
                else:
                    raise ValueError("Error: Invalid data source. Provide a file path to a CSV, Excel, or JSON file or a Pandas DataFrame.")
            except Exception as e:
                print(f"Error initializing data: {e}")
                print("Creating empty DataFrame instead.")
                self.data = pd.DataFrame()

    def remove_duplicates(self):
        """
        Remove duplicate rows from the DataFrame.

        Returns:
            None: Modifies the DataFrame in-place by removing duplicate rows.

        Example:
            data_handler.remove_duplicates()
        """
        self.data.drop_duplicates(inplace=True)

    def remove_null_values(self):
        """
        Remove rows containing null (NaN) values from the DataFrame.

        Returns:
            None: Modifies the DataFrame in-place by removing rows with null values.

        Example:
            data_handler.remove_null_values()
        """
        self.data.dropna(inplace=True)

    def remove_outliers(self, column_name, lower=0.25, upper=0.75, factor=1.5):
        """
        Remove outliers from a specific column based on the specified quantile range and outlier factor.

        Args:
            column_name (str): Name of the column to remove outliers from.
            lower (float, optional): Lower quantile value (inclusive) for defining the outlier range. Default is 0.25 (Q1).
            upper (float, optional): Upper quantile value (inclusive) for defining the outlier range. Default is 0.75 (Q3).
            factor (float, optional): Multiplier to determine the outlier boundaries. Default is 1.5 times the interquartile range (IQR).

        Returns:
            None: Modifies the DataFrame in-place by removing outliers.

        Examples:
            # Remove outliers from the 'column_name' using the default lower and upper quantiles (Q1 and Q3)
            data_handler.remove_outliers('column_name')

            # Remove outliers from the 'column_name' using custom lower and upper quantiles
            data_handler.remove_outliers('column_name', lower=0.1, upper=0.9)

            # Remove outliers from the 'column_name' using custom quantiles and a higher outlier factor
            data_handler.remove_outliers('column_name', lower=0.2, upper=0.8, factor=2.0)
        """
        
        Q1 = self.data[column_name].quantile(lower)
        Q3 = self.data[column_name].quantile(upper)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR

        if lower_bound is not None:
            self.data = self.data[self.data[column_name] > lower_bound]
        if upper_bound is not None:
            self.data = self.data[self.data[column_name] < upper_bound]

    def convert_to_numeric(self, column_name=None):
        """
        Convert a specific column or the entire DataFrame to numeric data type.

        Args:
            column_name (str, optional): Name of the column to be converted to numeric type.
                If None, converts the entire DataFrame to numeric type. Default is None.

        Returns:
            None: Modifies the DataFrame in-place by converting the specified column or the entire DataFrame to numeric type.

        Example:
            # Convert a specific column to numeric type
            data_handler.convert_to_numeric('column_name')

            # Convert the entire DataFrame to numeric type
            data_handler.convert_to_numeric()
        """
        if column_name is not None:
            try:
                self.data[column_name] = pd.to_numeric(self.data[column_name])
            except ValueError:
                print(f"Error: Could not convert '{column_name}' to numeric.")
        else:
            self.data = self.data.apply(pd.to_numeric, errors='coerce')

    def convert_to_string(self, column_name=None):
        """
        Convert a specific column or the entire DataFrame to string data type.

        Args:
            column_name (str, optional): Name of the column to be converted to string type.
                If None, converts the entire DataFrame to string type. Default is None.

        Returns:
            None: Modifies the DataFrame in-place by converting the specified column or the entire DataFrame to string type.

        Example:
            # Convert a specific column to string type
            data_handler.convert_to_string('column_name')

            # Convert the entire DataFrame to string type
            data_handler.convert_to_string()
        """
        if column_name is not None:
            self.data[column_name] = self.data[column_name].astype(str)
        else:
            self.data = self.data.applymap(str)

    def normalize_column(self, column_name):
        """
        Normalize values in a specific column to a range between 0 and 1.

        Args:
            column_name (str): Name of the column to be normalized.

        Returns:
            None: Modifies the DataFrame in-place by normalizing the specified column.

        Example:
            data_handler.normalize_column('column_name')
        """
        if column_name in self.data.columns:
            self.data[column_name] = (self.data[column_name] - self.data[column_name].min()) / \
                                      (self.data[column_name].max() - self.data[column_name].min())

    def normalize(self):
        """
        Normalize values in all columns to a range between 0 and 1.

        Returns:
            None: Modifies the DataFrame in-place by normalizing all columns.

        Example:
            data_handler.normalize()
        """
        for column in self.data.columns:
            self.normalize_column(column)

    def to_csv(self, output_path):
        """
        Write the DataFrame to a CSV file.

        Args:
            output_path (str): File path where the CSV file will be saved.

        Returns:
            None: Writes the DataFrame to the specified CSV file.

        Example:
            data_handler.to_csv('output_file.csv')
        """
        self.data.to_csv(output_path, index=False)

    def nullify(self, values_to_replace=("\\N", "", "null", "N/A"), column_name=None):
        """
        Replace specified values with None (null) in the specified column or in the entire DataFrame if column_name is not provided.

        Args:
            values_to_replace (any, list, tuple, set, optional): Single value or iterable of values to be replaced with None.
                Default values_to_replace are ("\\N", "", "null", "N/A").
            column_name (str, optional): Name of the column in which values will be replaced. If not provided, replaces values
                in the entire DataFrame.

        Returns:
            None: Modifies the DataFrame in-place by replacing specified values with None.

        Examples:
            # Replace default null values ("\\N", "", "null", "N/A") with None in the entire DataFrame
            data_handler.nullify()

            # Replace occurrences of 0 and 'N/A' with None in the column 'example_column'
            data_handler.nullify(values_to_replace=[0, 'N/A'], column_name='example_column')
        """
        if column_name:
            self.data[column_name] = self.data[column_name].replace(to_replace=values_to_replace, value=None)
        else:
            self.data = self.data.replace(to_replace=values_to_replace, value=None)


