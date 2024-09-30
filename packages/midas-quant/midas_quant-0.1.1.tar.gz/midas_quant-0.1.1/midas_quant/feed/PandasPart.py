from .IFeedPart import IFeedPart
from typing import Union, List
import pandas as pd

class PandasPart(IFeedPart):
    """
    A class that provides an interface to a Pandas DataFrame with additional functionality 
    for backward or forward indexing, comparison of values, and checking for cross events 
    between columns of the DataFrame. It allows integer and slice-based indexing in both 
    backward and forward directions and includes several helper methods for value comparison 
    and cross detection between columns.
    
    Attributes:
        _df (pd.DataFrame): The Pandas DataFrame that this class wraps around.
        _size (int): The size (number of rows) of the DataFrame.
        _backword (bool): A boolean flag that determines whether the class should index backward 
                           (True) or forward (False) through the DataFrame.
    """

    def __init__(self, df: pd.DataFrame, backword: bool = True) -> None:
        """
        Initializes the PandasPart class with a DataFrame and an optional direction flag.
        
        Args:
            df (pd.DataFrame): The Pandas DataFrame to be used.
            backword (bool): A boolean flag to determine if indexing should be backward (True) 
                             or forward (False). Defaults to True.
        """
        self._df: pd.DataFrame = df
        self._size: int = len(df)
        self._backword: bool = backword

    def _repr_html_(self) -> str:
        """
        Returns the HTML representation of the DataFrame, used for displaying in Jupyter Notebooks.
        
        Returns:
            str: A string containing the HTML representation of the DataFrame.
        """
        return self._df.to_html()

    def __repr__(self) -> str:
        """
        Returns the string representation of the DataFrame for displaying in the console.
        
        Returns:
            str: A string containing the DataFrame's standard string representation.
        """
        return repr(self._df)

    def __getitem__(self, index: Union[int, slice]) -> Union[pd.Series, 'PandasPart']:
        """
        Allows for both integer and slice indexing on the DataFrame, with support for backward indexing.
        
        Args:
            index (Union[int, slice]): Can be an integer (for single-row access) or a slice object 
                                       (for range access).

        Returns:
            Union[pd.Series, PandasPart]: 
                - pd.Series: If the index is an integer, returns a single row as a Series.
                - PandasPart: If the index is a slice, returns a new PandasPart instance 
                              containing the sliced DataFrame.
                
        Raises:
            TypeError: If the index is neither an int nor a slice.
            AssertionError: If the integer index is out of bounds.
        """
        if isinstance(index, int):
            # Handle integer indexing
            assert index < self._size, f"index must be smaller than {self._size}"
            position: int = -(index + 1) if self._backword else index
            return self._df.iloc[position]
        
        elif isinstance(index, slice):
            # Handle slice-based indexing
            start, stop, step = index.indices(self._size)
            indices: range = range(start, stop, step)
            
            if self._backword:
                # Reverse the indices for backward indexing
                positions: List[int] = [self._size - idx - 1 for idx in indices]
                if step > 0:
                    positions = positions[::-1]  # Reverse again if step is positive
            else:
                positions = list(indices)
            
            # Create a new PandasPart instance with the sliced DataFrame
            sliced_df: pd.DataFrame = self._df.iloc[positions].reset_index(drop=True)
            return PandasPart(sliced_df, self._backword)
        else:
            raise TypeError(f"Invalid argument type: {type(index)}")

    def upCompare(self, index: int, target: str, compare: str) -> bool:
        """
        Compares whether the target column value is greater than the compare column value at a specific index.
        
        Args:
            index (int): The index to compare values.
            target (str): The target column to compare.
            compare (str): The column to compare against the target.

        Returns:
            bool: True if the target column's value is greater than the compare column's value, else False.
        """
        return self[index][target] > self[index][compare]

    def downCompare(self, index: int, target: str, compare: str) -> bool:
        """
        Compares whether the target column value is less than the compare column value at a specific index.
        
        Args:
            index (int): The index to compare values.
            target (str): The target column to compare.
            compare (str): The column to compare against the target.

        Returns:
            bool: True if the target column's value is less than the compare column's value, else False.
        """
        return self[index][target] < self[index][compare]

    def upValue(self, index: int, target: str, value: float) -> bool:
        """
        Checks if the target column value is greater than a specified value at a specific index.
        
        Args:
            index (int): The index to check.
            target (str): The target column to check.
            value (float): The value to compare against.

        Returns:
            bool: True if the target column's value is greater than the specified value, else False.
        """
        return self[index][target] > value

    def downValue(self, index: int, target: str, value: float) -> bool:
        """
        Checks if the target column value is less than a specified value at a specific index.
        
        Args:
            index (int): The index to check.
            target (str): The target column to check.
            value (float): The value to compare against.

        Returns:
            bool: True if the target column's value is less than the specified value, else False.
        """
        return self[index][target] < value

    def betweenValue(self, index: int, target: str, value: float, percent: float = 1.0) -> bool:
        """
        Checks if the target column value is within a percentage range of a specified value at a specific index.
        
        Args:
            index (int): The index to check.
            target (str): The target column to check.
            value (float): The value to compare against.
            percent (float, optional): The percentage range around the value (default is 1.0%).

        Returns:
            bool: True if the target column's value is within the range of (value - percent%) 
                  and (value + percent%), else False.
        """
        percent_value: float = value * (percent / 100)
        up_value: float = value + percent_value
        dn_value: float = value - percent_value
        
        target_value: float = self[index][target]
        return dn_value < target_value < up_value

    def cross(self, index: int, target: str, compare: str, updn: str = "up") -> bool:
        """
        Detects if a 'cross' event occurs between the target and compare columns at a specific index.
        A 'cross' event is when the target column value crosses above (or below) the compare column value.

        Args:
            index (int): The index to check.
            target (str): The target column to compare.
            compare (str): The compare column to check against.
            updn (str, optional): A string indicating the direction of the cross event:
                                   "up" for crossing from below to above,
                                   "down" for crossing from above to below.
                                   Defaults to "up".

        Returns:
            bool: True if the 'cross' event occurs at the specified index, else False.
                
        Raises:
            AssertionError: If the index is out of bounds based on the direction (backward or forward).
            ValueError: If the `updn` parameter is neither "up" nor "down".
        """
        if self._backword:
            assert index < self._size - 1, (
                f"index must be smaller than {self._size - 1} because the direction is backward."
            )
        else:
            assert index > 0, (
                f"index must be greater than 0 because the direction is forward."
            )
        
        pre_position: int = index + 1 if self._backword else index - 1

        if updn == "up":
            # Detect upward cross: when target crosses above compare
            return (
                self[pre_position][target] <= self[pre_position][compare] and
                self[index][target] > self[index][compare]
            )
        elif updn == "down":
            # Detect downward cross: when target crosses below compare
            return (
                self[pre_position][target] >= self[pre_position][compare] and
                self[index][target] < self[index][compare]
            )
        else:
            raise ValueError("Parameter 'updn' must be either 'up' or 'down'.")
