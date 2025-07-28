# Financial Charting AI

A Python package for loading and analyzing financial data from various sources, starting with the Federal Reserve Economic Data (FRED) API.

## Features

- **FRED Data Loader**: Complete interface to the FRED API
- **Protocol-based Design**: Consistent interface across different data sources
- **Easy to Use**: Simple API for common financial data operations
- **Type Hints**: Full type support for better development experience

## Installation

1. Install the required dependencies using `uv`:
```bash
uv sync
```

2. Get a FRED API key:
   - Visit [FRED API Documentation](https://fred.stlouisfed.org/docs/api/api_key.html)
   - Sign up for a free API key
   - Set the environment variable: `export FRED_API_KEY="your_api_key_here"`

## Quick Start

```python
from financial_charting_ai import FREDLoader

# Initialize the loader
fred = FREDLoader("your_api_key_here")

# Get GDP data
gdp_data = fred.get_series('GDP', start_date='2020-01-01')
print(gdp_data.head())

# Get multiple series
series_data = fred.get_multiple_series(['UNRATE', 'CPIAUCSL'])
```

## Usage Examples

### 1. Get a Single Time Series

```python
# Get GDP data for the last 5 years
gdp_data = fred.get_series('GDP', start_date='2019-01-01')
print(f"Retrieved {len(gdp_data)} observations")
```

### 2. Get Series Description

```python
# Get metadata about a series
description = fred.get_series_description('GDP')
print(f"Title: {description['title']}")
print(f"Frequency: {description['frequency']}")
print(f"Units: {description['units']}")
```

### 3. Get Multiple Time Series

```python
# Get unemployment rate, CPI, and federal funds rate
series_ids = ['UNRATE', 'CPIAUCSL', 'FEDFUNDS']
data = fred.get_multiple_series(series_ids, start_date='2023-01-01')

for series_id, df in data.items():
    print(f"{series_id}: {len(df)} observations")
```

### 4. Search for Available Series

```python
# Search for inflation-related series
inflation_series = fred.get_available_series(search_text='inflation', limit=10)
print(inflation_series[['id', 'title']].head())
```

### 5. Get Popular Series

```python
# Get a list of commonly used series
popular = fred.get_popular_series()
for series in popular:
    print(f"{series['id']}: {series['title']}")
```

## Running the Demo

Run the main demonstration script:

```bash
cd financial_charting_ai
python main_fred.py
```

This will show examples of all the main functionality.

## API Reference

### FREDLoader Class

#### `__init__(api_key: str)`
Initialize the FRED loader with your API key.

#### `get_series(series_id: str, start_date: str = None, end_date: str = None, frequency: str = None, aggregation_method: str = None) -> pd.DataFrame`
Get time series data for a specific series ID.

**Parameters:**
- `series_id`: The FRED series ID (e.g., 'GDP', 'UNRATE')
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format
- `frequency`: Data frequency ('d', 'w', 'm', 'q', 'sa', 'a')
- `aggregation_method`: Aggregation method ('avg', 'sum', 'eop')

**Returns:** DataFrame with 'date' and 'value' columns

#### `get_series_description(series_id: str) -> Dict`
Get detailed metadata for a series.

#### `get_multiple_series(series_ids: List[str], start_date: str = None, end_date: str = None, frequency: str = None) -> Dict[str, pd.DataFrame]`
Get multiple time series at once.

#### `get_available_series(search_text: str = None, category_id: int = None, limit: int = 1000) -> pd.DataFrame`
Search for available series.

#### `get_popular_series() -> List[Dict]`
Get a list of commonly used FRED series.

## DataLoader Protocol

The `DataLoader` protocol defines a consistent interface for data loaders. Any class implementing this protocol must provide:

- `get_series()`: Get individual time series
- `get_series_description()`: Get series metadata
- `get_multiple_series()`: Get multiple time series
- `get_available_series()`: Search available series

## Popular FRED Series

Some commonly used series IDs:

- `GDP`: Gross Domestic Product
- `UNRATE`: Unemployment Rate
- `CPIAUCSL`: Consumer Price Index
- `FEDFUNDS`: Federal Funds Rate
- `DGS10`: 10-Year Treasury Rate
- `DGS2`: 2-Year Treasury Rate
- `PAYEMS`: Total Nonfarm Payrolls
- `INDPRO`: Industrial Production
- `M2SL`: M2 Money Stock
- `PCE`: Personal Consumption Expenditures

## Error Handling

The FRED loader includes comprehensive error handling:

- Network errors are caught and reported
- Invalid series IDs are handled gracefully
- Missing data is handled appropriately
- API rate limits are respected

## Contributing

To extend this package:

1. Create a new data loader class that implements the `DataLoader` protocol
2. Add appropriate error handling and documentation
3. Include example usage in the main script
4. Update the package `__init__.py` to expose the new class

## License

This project is open source and available under the MIT License. 