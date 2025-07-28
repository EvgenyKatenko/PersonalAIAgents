"""
Financial Charting AI Package

This package provides tools for loading and analyzing financial data from various sources.
"""

from .fred_loader import FREDLoader
from .data_loader_protocol import DataLoader

__version__ = "0.1.0"
__author__ = "Financial Charting AI"

__all__ = [
    "FREDLoader",
    "DataLoader"
] 