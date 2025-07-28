#!/usr/bin/env python3
"""
Main script demonstrating the usage of the FRED data loader.

This script shows how to:
1. Initialize the FRED loader
2. Get individual time series data
3. Get series descriptions
4. Get multiple time series
5. Search for available series

Prerequisites:
- Install dependencies: uv sync
- Get FRED API key from: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fred_loader import FREDLoader
from data_loader_protocol import DataLoader


def main():
    """
    Main function demonstrating FRED data loader usage.
    """
    
    # Get API key from environment variable or prompt user
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        print("FRED API key not found in environment variables.")
        print("Please set FRED_API_KEY environment variable or enter your API key:")
        api_key = input("Enter your FRED API key: ").strip()
        
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    # Initialize the FRED loader
    print("Initializing FRED data loader...")
    fred_loader = FREDLoader(api_key)
    
    # Verify that FREDLoader implements the DataLoader protocol
    if isinstance(fred_loader, DataLoader):
        print("✓ FREDLoader correctly implements the DataLoader protocol")
    else:
        print("✗ FREDLoader does not implement the DataLoader protocol")
    
    try:
        # Example 1: Get a single time series (GDP) - using different date formats
        print("\n" + "="*50)
        print("EXAMPLE 1: Getting GDP time series data with different date formats")
        print("="*50)
        
        # Using integer format (YYYYMMDD)
        gdp_data = fred_loader.get_series('GDP', start_date=20200101)
        print(f"Retrieved {len(gdp_data)} observations for GDP (using int date)")
        
        # Using datetime object
        from datetime import datetime
        gdp_data_dt = fred_loader.get_series('GDP', start_date=datetime(2020, 1, 1))
        print(f"Retrieved {len(gdp_data_dt)} observations for GDP (using datetime)")
        
        # Using date object
        from datetime import date
        gdp_data_date = fred_loader.get_series('GDP', start_date=date(2020, 1, 1))
        print(f"Retrieved {len(gdp_data_date)} observations for GDP (using date)")
        
        print("Latest GDP values:")
        print(gdp_data.tail())
        
        # Example 2: Get series description
        print("\n" + "="*50)
        print("EXAMPLE 2: Getting series description")
        print("="*50)
        
        gdp_description = fred_loader.get_series_description('GDP')
        print(f"Series ID: {gdp_description.get('id')}")
        print(f"Title: {gdp_description.get('title')}")
        print(f"Frequency: {gdp_description.get('frequency')}")
        print(f"Units: {gdp_description.get('units')}")
        print(f"Seasonal Adjustment: {gdp_description.get('seasonal_adjustment')}")
        
        # Example 3: Get multiple time series
        print("\n" + "="*50)
        print("EXAMPLE 3: Getting multiple time series")
        print("="*50)
        
        series_ids = ['UNRATE', 'CPIAUCSL', 'FEDFUNDS']
        multiple_data = fred_loader.get_multiple_series(
            series_ids, 
            start_date=20230101
        )
        
        for series_id, data in multiple_data.items():
            print(f"{series_id}: {len(data)} observations")
            print(f"  Latest value: {data['value'].iloc[-1]:.2f} on {data['date'].iloc[-1].strftime('%Y-%m-%d')}")
        
        # Example 4: Search for available series
        print("\n" + "="*50)
        print("EXAMPLE 4: Searching for available series")
        print("="*50)
        
        # Search for inflation-related series
        inflation_series = fred_loader.get_available_series(
            search_text='inflation',
            limit=5
        )
        
        if not inflation_series.empty:
            print("Found inflation-related series:")
            for _, row in inflation_series.iterrows():
                print(f"  {row['id']}: {row['title']}")
        else:
            print("No inflation-related series found")
        
        # Example 5: Get popular series list
        print("\n" + "="*50)
        print("EXAMPLE 5: Popular FRED series")
        print("="*50)
        
        popular_series = fred_loader.get_popular_series()
        print("Popular FRED series:")
        for series in popular_series:
            print(f"  {series['id']}: {series['title']} ({series['frequency']})")
        
        # Example 6: Advanced usage - Treasury yields comparison
        print("\n" + "="*50)
        print("EXAMPLE 6: Treasury yields comparison")
        print("="*50)
        
        treasury_series = ['DGS2', 'DGS10']
        treasury_data = fred_loader.get_multiple_series(
            treasury_series,
            start_date=20230101
        )
        
        if 'DGS2' in treasury_data and 'DGS10' in treasury_data:
            # Calculate yield spread
            dgs2 = treasury_data['DGS2'].set_index('date')['value']
            dgs10 = treasury_data['DGS10'].set_index('date')['value']
            
            # Align the series and calculate spread
            aligned_data = pd.concat([dgs2, dgs10], axis=1).dropna()
            aligned_data.columns = ['2Y', '10Y']
            aligned_data['Spread'] = aligned_data['10Y'] - aligned_data['2Y']
            
            print("Treasury yield spread (10Y - 2Y):")
            print(f"Current spread: {aligned_data['Spread'].iloc[-1]:.2f}%")
            print(f"Average spread: {aligned_data['Spread'].mean():.2f}%")
            print(f"Min spread: {aligned_data['Spread'].min():.2f}%")
            print(f"Max spread: {aligned_data['Spread'].max():.2f}%")
        
        print("\n" + "="*50)
        print("All examples completed successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main() 