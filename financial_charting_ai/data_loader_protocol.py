from typing import Protocol, List, Dict, Union
from datetime import date, datetime
import pandas as pd


class DataLoader(Protocol):
    """
    Protocol defining the interface for data loaders.
    
    This protocol ensures that all data loader classes implement
    the same basic interface for consistency across different data sources.
    """
    
    def get_series(self, series_id: str, 
                   start_date: int | date | datetime | None = None,
                   end_date: int | date | datetime | None = None,
                   frequency: str | None = None,
                   **kwargs) -> pd.DataFrame:
        """
        Get time series data for a specific series ID.
        
        Args:
            series_id (str): The series identifier
            start_date (int | date | datetime, optional): Start date as int (YYYYMMDD), date, or datetime
            end_date (int | date | datetime, optional): End date as int (YYYYMMDD), date, or datetime
            frequency (str, optional): Frequency of data
            **kwargs: Additional parameters specific to the data source
            
        Returns:
            pd.DataFrame: DataFrame with time series data
        """
        ...
    
    def get_series_description(self, series_id: str) -> Dict:
        """
        Get detailed description and metadata for a specific series.
        
        Args:
            series_id (str): The series identifier
            
        Returns:
            Dict: Dictionary containing series metadata
        """
        ...
    
    def get_multiple_series(self, series_ids: List[str],
                           start_date: int | date | datetime | None = None,
                           end_date: int | date | datetime | None = None,
                           frequency: str | None = None,
                           **kwargs) -> Dict[str, pd.DataFrame]:
        """
        Get multiple time series data at once.
        
        Args:
            series_ids (List[str]): List of series identifiers
            start_date (int | date | datetime, optional): Start date as int (YYYYMMDD), date, or datetime
            end_date (int | date | datetime, optional): End date as int (YYYYMMDD), date, or datetime
            frequency (str, optional): Frequency of data
            **kwargs: Additional parameters specific to the data source
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping series IDs to their DataFrames
        """
        ...
    
    def get_available_series(self, search_text: str | None = None,
                           category_id: int | None = None,
                           limit: int = 1000,
                           **kwargs) -> pd.DataFrame:
        """
        Get a list of available series that match search criteria.
        
        Args:
            search_text (str, optional): Text to search for in series titles
            category_id (int, optional): Category ID to filter by
            limit (int): Maximum number of results to return
            **kwargs: Additional parameters specific to the data source
            
        Returns:
            pd.DataFrame: DataFrame with series information
        """
        ... 