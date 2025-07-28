import requests
import pandas as pd
from typing import List, Dict, Union
from datetime import datetime, timedelta, date
import json


class FREDLoader:
    """
    A class to load economic data from the Federal Reserve Economic Data (FRED) API.
    
    This class provides methods to:
    - Get individual time series data
    - Get series descriptions
    - Get multiple time series at once
    - Get a list of available series
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the FRED loader with an API key.
        
        Args:
            api_key (str): Your FRED API key from https://fred.stlouisfed.org/docs/api/api_key.html
        """
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred"
    
    def _convert_date_to_string(self, date_input: int | date | datetime | None) -> str | None:
        """
        Convert date input to FRED API string format (YYYY-MM-DD).
        
        Args:
            date_input: Date as int (YYYYMMDD), date, datetime, or None
            
        Returns:
            Date string in YYYY-MM-DD format or None
        """
        if date_input is None:
            return None
        
        if isinstance(date_input, int):
            # Convert YYYYMMDD to YYYY-MM-DD
            date_str = str(date_input)
            if len(date_str) == 8:
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            else:
                raise ValueError(f"Invalid date format. Expected YYYYMMDD, got {date_input}")
        
        elif isinstance(date_input, (date, datetime)):
            return date_input.strftime("%Y-%m-%d")
        
        else:
            raise TypeError(f"Unsupported date type: {type(date_input)}")
        
    def get_series(self, series_id: str, 
                   start_date: int | date | datetime | None = None,
                   end_date: int | date | datetime | None = None,
                   frequency: str | None = None,
                   aggregation_method: str | None = None) -> pd.DataFrame:
        """
        Get time series data for a specific series ID.
        
        Args:
            series_id (str): The FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL')
            start_date (int | date | datetime, optional): Start date as int (YYYYMMDD), date, or datetime
            end_date (int | date | datetime, optional): End date as int (YYYYMMDD), date, or datetime
            frequency (str, optional): Frequency of data ('d', 'w', 'm', 'q', 'sa', 'a')
            aggregation_method (str, optional): Aggregation method ('avg', 'sum', 'eop')
            
        Returns:
            pd.DataFrame: DataFrame with 'date' and 'value' columns
        """
        endpoint = f"{self.base_url}/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        # Convert dates to string format
        start_date_str = self._convert_date_to_string(start_date)
        end_date_str = self._convert_date_to_string(end_date)
        
        if start_date_str:
            params['observation_start'] = start_date_str
        if end_date_str:
            params['observation_end'] = end_date_str
        if frequency:
            params['frequency'] = frequency
        if aggregation_method:
            params['aggregation_method'] = aggregation_method
            
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'observations' not in data:
                raise ValueError(f"No observations found for series {series_id}")
                
            observations = data['observations']
            df = pd.DataFrame(observations)
            
            # Convert date and value columns
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            # Remove rows with missing values
            df = df.dropna()
            
            return df[['date', 'value']].reset_index(drop=True)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data for series {series_id}: {str(e)}")
        except (KeyError, ValueError) as e:
            raise Exception(f"Error processing data for series {series_id}: {str(e)}")
    
    def get_series_description(self, series_id: str) -> Dict:
        """
        Get detailed description and metadata for a specific series.
        
        Args:
            series_id (str): The FRED series ID
            
        Returns:
            Dict: Dictionary containing series metadata
        """
        endpoint = f"{self.base_url}/series"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'seriess' not in data or not data['seriess']:
                raise ValueError(f"No series found with ID {series_id}")
                
            return data['seriess'][0]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching description for series {series_id}: {str(e)}")
        except (KeyError, ValueError) as e:
            raise Exception(f"Error processing description for series {series_id}: {str(e)}")
    
    def get_multiple_series(self, series_ids: List[str],
                           start_date: int | date | datetime | None = None,
                           end_date: int | date | datetime | None = None,
                           frequency: str | None = None) -> Dict[str, pd.DataFrame]:
        """
        Get multiple time series data at once.
        
        Args:
            series_ids (List[str]): List of FRED series IDs
            start_date (int | date | datetime, optional): Start date as int (YYYYMMDD), date, or datetime
            end_date (int | date | datetime, optional): End date as int (YYYYMMDD), date, or datetime
            frequency (str, optional): Frequency of data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping series IDs to their DataFrames
        """
        result = {}
        
        for series_id in series_ids:
            try:
                df = self.get_series(series_id, start_date, end_date, frequency)
                result[series_id] = df
            except Exception as e:
                print(f"Warning: Could not fetch series {series_id}: {str(e)}")
                continue
                
        return result
    
    def get_available_series(self, search_text: str | None = None,
                           category_id: int | None = None,
                           limit: int = 1000) -> pd.DataFrame:
        """
        Get a list of available series that match search criteria.
        
        Args:
            search_text (str, optional): Text to search for in series titles
            category_id (int, optional): Category ID to filter by
            limit (int): Maximum number of results to return
            
        Returns:
            pd.DataFrame: DataFrame with series information
        """
        endpoint = f"{self.base_url}/series/search"
        params = {
            'api_key': self.api_key,
            'file_type': 'json',
            'limit': limit
        }
        
        if search_text:
            params['search_text'] = search_text
        if category_id:
            params['category_id'] = category_id
            
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'seriess' not in data:
                return pd.DataFrame()
                
            series_list = data['seriess']
            df = pd.DataFrame(series_list)
            
            # Convert date columns
            date_columns = ['realtime_start', 'realtime_end', 'observation_start', 'observation_end']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])
                    
            return df
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching available series: {str(e)}")
        except (KeyError, ValueError) as e:
            raise Exception(f"Error processing available series: {str(e)}")
    
    def get_popular_series(self) -> List[Dict]:
        """
        Get a list of commonly used FRED series.
        
        Returns:
            List[Dict]: List of popular series with their IDs and descriptions
        """
        popular_series = [
            {'id': 'GDP', 'title': 'Gross Domestic Product', 'frequency': 'Quarterly'},
            {'id': 'UNRATE', 'title': 'Unemployment Rate', 'frequency': 'Monthly'},
            {'id': 'CPIAUCSL', 'title': 'Consumer Price Index for All Urban Consumers', 'frequency': 'Monthly'},
            {'id': 'FEDFUNDS', 'title': 'Federal Funds Effective Rate', 'frequency': 'Monthly'},
            {'id': 'DGS10', 'title': '10-Year Treasury Constant Maturity Rate', 'frequency': 'Daily'},
            {'id': 'DGS2', 'title': '2-Year Treasury Constant Maturity Rate', 'frequency': 'Daily'},
            {'id': 'PAYEMS', 'title': 'Total Nonfarm Payrolls', 'frequency': 'Monthly'},
            {'id': 'INDPRO', 'title': 'Industrial Production: Total Index', 'frequency': 'Monthly'},
            {'id': 'M2SL', 'title': 'M2 Money Stock', 'frequency': 'Monthly'},
            {'id': 'PCE', 'title': 'Personal Consumption Expenditures', 'frequency': 'Monthly'}
        ]
        return popular_series 