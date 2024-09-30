from .IFeeder import IFeeder
from .IFeedPart import IFeedPart
from typing import List, Tuple, Optional, Type, TypeVar, Generic, Union
import pandas as pd

# Define a generic type variable bound to IFeedPart
T = TypeVar('T', bound=IFeedPart)

class PandasFeeder(IFeeder, Generic[T]):
    """
    A feeder class that iterates over a list of Pandas DataFrames, providing windowed 
    segments of each DataFrame as specified by the window size. It supports both 
    backward and forward indexing and utilizes a specified part class (defaulting to 
    IFeedPart) to handle each windowed segment.

    This class implements the IFeeder interface, ensuring it adheres to the required 
    methods and behaviors defined by the interface.

    Attributes:
        _dfs (List[pd.DataFrame]): A list of Pandas DataFrames to be fed.
        _window (int): The size of the window (number of rows) for each segment.
        _backword (bool): Determines the direction of indexing. True for backward, False for forward.
        _part_class (Type[T]): The class used to create parts from DataFrame segments.

        _dfs_index (int): Current index in the list of DataFrames.
        _dfs_size (int): Total number of DataFrames.
        _df (pd.DataFrame): The current DataFrame being processed.
        _df_index (int): Current row index within the current DataFrame.
        _df_size (int): Total number of rows in the current DataFrame.

        _size_item (int): Total number of windowed segments across all DataFrames.
    """

    def __init__(
        self, 
        dfs: List[pd.DataFrame], 
        window: int = 5, 
        backword: bool = True, 
        part_class: Type[T] = IFeedPart
    ) -> None:
        """
        Initializes the PandasFeeder with a list of DataFrames, window size, indexing direction,
        and the part class used for creating segments.

        Args:
            dfs (List[pd.DataFrame]): The list of Pandas DataFrames to be fed.
            window (int, optional): The number of rows in each windowed segment. Defaults to 5.
            backword (bool, optional): If True, indexes backward; otherwise, indexes forward. Defaults to True.
            part_class (Type[T], optional): The class used to create parts from DataFrame segments.
                                             Must be a subclass of IFeedPart. Defaults to IFeedPart.
        """
        self._dfs: List[pd.DataFrame] = dfs
        self._window: int = window
        self._backword: bool = backword
        self._part_class: Type[T] = part_class
        
        self._dfs_index: int = 0
        self._dfs_size: int = len(dfs)
        self._df: pd.DataFrame = dfs[self._dfs_index] if self._dfs_size > 0 else pd.DataFrame()
        self._df_index: int = window
        self._df_size: int = len(self._df)
        
        # Calculate total number of windowed segments across all DataFrames
        self._size_item: int = 0
        for df in dfs:
            self._size_item += max(len(df) - window + 1, 0)

    def datas(self) -> List[pd.DataFrame]:
        """
        Retrieves the list of all DataFrames managed by the feeder.

        Returns:
            List[pd.DataFrame]: The list of DataFrames.
        """
        return self._dfs

    def __iter__(self) -> 'PandasFeeder[T]':
        """
        Resets the feeder to the initial state and returns the iterator object.

        Returns:
            PandasFeeder[T]: The iterator object itself.
        """
        self._dfs_index = 0
        self._dfs_size = len(self._dfs)
        self._df = self._dfs[self._dfs_index] if self._dfs_size > 0 else pd.DataFrame()
        self._df_index = self._window
        self._df_size = len(self._df)
        return self

    def __len__(self) -> int:
        """
        Retrieves the total number of windowed segments across all DataFrames.

        Returns:
            int: The total number of segments.
        """
        return self._size_item

    def __next__(self) -> Tuple[T, bool]:
        """
        Retrieves the next windowed segment and indicates if a DataFrame change has occurred.

        Returns:
            Tuple[T, bool]: 
                - T: An instance of the part_class containing the windowed DataFrame segment.
                - bool: True if the feeder has moved to a new DataFrame, False otherwise.

        Raises:
            StopIteration: If all DataFrames have been processed.
        """
        is_change: bool = False

        # Check if current index exceeds the size of the current DataFrame
        if self._df_index > self._df_size:
            # Attempt to move to the next DataFrame
            self._dfs_index += 1
            if self._dfs_index >= self._dfs_size:
                # No more DataFrames to process
                raise StopIteration
            # Update current DataFrame and reset indices
            self._df = self._dfs[self._dfs_index]
            self._df_index = self._window
            self._df_size = len(self._df)
            is_change = True

        # Ensure there are enough rows for the window
        if self._df_index - self._window < 0 or self._df_index > self._df_size:
            raise StopIteration

        # Slice the DataFrame to create a windowed segment
        df_part: pd.DataFrame = self._df.iloc[self._df_index - self._window : self._df_index].reset_index(drop=True)
        # Instantiate the part_class with the sliced DataFrame
        part: T = self._part_class(df_part, self._backword)
        # Increment the DataFrame index for the next iteration
        self._df_index += 1

        return part, is_change

    def reset(self) -> None:
        """
        Resets the feeder to its initial state, allowing iteration to start from the beginning.
        """
        self.__iter__()

    def next(self) -> Tuple[Optional[T], Optional[bool]]:
        """
        Retrieves the next windowed segment in a safe manner, returning (None, None) 
        if the iteration has completed.

        Returns:
            Tuple[Optional[T], Optional[bool]]: 
                - Optional[T]: An instance of the part_class containing the windowed DataFrame segment, or None if iteration is complete.
                - Optional[bool]: True if a DataFrame change has occurred, False if not, or None if iteration is complete.
        """
        try:
            return self.__next__()
        except StopIteration:
            return None, None
