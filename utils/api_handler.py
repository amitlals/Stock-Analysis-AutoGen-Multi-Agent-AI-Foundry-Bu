"""
API handler for stock data retrieval with automatic failover
"""

import os
import time
import logging
import json
from typing import Dict, Any, Optional
import requests
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

class StockDataProvider:
    """
    Handles stock data retrieval with automatic failover between Alpha Vantage and Yahoo Finance
    """
    
    def __init__(self, alpha_vantage_key: str, cache_duration: int = 3600, cache_dir: str = "./data/cache"):
        """
        Initialize the API handler.
        
        Args:
            alpha_vantage_key: API key for Alpha Vantage
            cache_duration: How long to cache data in seconds (default: 1 hour)
            cache_dir: Directory to store cached data
        """
        self.alpha_vantage_key = alpha_vantage_key
        self.cache_duration = int(os.getenv("CACHE_DURATION", cache_duration))
        self.cache_dir = os.getenv("CACHE_DIRECTORY", cache_dir)
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get stock data for a given ticker with caching and automatic failover.
        
        Args:
            ticker: Stock ticker symbol (e.g., AAPL)
            
        Returns:
            Dictionary with stock data or None if retrieval failed
        """
        # Check cache first
        cache_file = os.path.join(self.cache_dir, f"{ticker.lower()}_data.json")
        
        # If cache exists and is fresh, return cached data
        if os.path.exists(cache_file):
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age < self.cache_duration:
                logger.info(f"Using cached data for {ticker}")
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"Error reading cache file: {str(e)}")
        
        # Try Alpha Vantage first
        data = self._get_alpha_vantage_data(ticker)
        
        # Failover to Yahoo Finance if Alpha Vantage fails
        if not data:
            logger.info(f"Falling back to Yahoo Finance for {ticker}")
            data = self._get_yahoo_finance_data(ticker)
        
        # Cache the data if retrieval was successful
        if data:
            try:
                with open(cache_file, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                logger.warning(f"Error writing cache file: {str(e)}")
        
        return data
    
    def _get_alpha_vantage_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get stock data from Alpha Vantage API.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock data or None if retrieval failed
        """
        if not self.alpha_vantage_key:
            logger.warning("No Alpha Vantage API key provided")
            return None
            
        try:
            # Get daily time series
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": ticker,
                "outputsize": "full",
                "apikey": self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.warning(f"Alpha Vantage API returned status code {response.status_code}")
                return None
                
            data = response.json()
            
            # Check for error messages
            if "Error Message" in data or "Information" in data or "Note" in data:
                logger.warning(f"Alpha Vantage API returned error: {data.get('Error Message', data.get('Information', data.get('Note')))}")
                return None
                
            # Process the data
            time_series = data.get("Time Series (Daily)", {})
            if not time_series:
                return None
                
            # Convert to our standard format
            processed_data = {
                "ticker": ticker,
                "source": "alphavantage",
                "last_updated": data.get("Meta Data", {}).get("3. Last Refreshed", ""),
                "prices": self._process_alpha_vantage_time_series(time_series)
            }
            
            # Get company overview
            overview_params = {
                "function": "OVERVIEW",
                "symbol": ticker,
                "apikey": self.alpha_vantage_key
            }
            
            overview_response = requests.get(url, params=overview_params)
            if overview_response.status_code == 200:
                overview_data = overview_response.json()
                if "Symbol" in overview_data:
                    processed_data["company_info"] = overview_data
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error retrieving data from Alpha Vantage: {str(e)}")
            return None
    
    def _get_yahoo_finance_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get stock data from Yahoo Finance as fallback.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock data or None if retrieval failed
        """
        try:
            # Get stock data from Yahoo Finance
            stock = yf.Ticker(ticker)
            history = stock.history(period="2y")
            
            if history.empty:
                logger.warning(f"No data returned from Yahoo Finance for {ticker}")
                return None
            
            # Get company info
            company_info = {
                "Symbol": ticker,
                "Name": stock.info.get("shortName", ""),
                "Description": stock.info.get("longBusinessSummary", ""),
                "Exchange": stock.info.get("exchange", ""),
                "Industry": stock.info.get("industry", ""),
                "Sector": stock.info.get("sector", ""),
                "MarketCapitalization": stock.info.get("marketCap", ""),
                "PERatio": stock.info.get("trailingPE", ""),
                "DividendYield": stock.info.get("dividendYield", ""),
            }
            
            # Process historical data
            prices = []
            for date, row in history.iterrows():
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"]
                })
            
            return {
                "ticker": ticker,
                "source": "yahoo",
                "last_updated": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "prices": prices,
                "company_info": company_info
            }
            
        except Exception as e:
            logger.error(f"Error retrieving data from Yahoo Finance: {str(e)}")
            return None
    
    def _process_alpha_vantage_time_series(self, time_series):
        """
        Process Alpha Vantage time series data into standard format.
        
        Args:
            time_series: Time series data from Alpha Vantage
            
        Returns:
            List of dictionaries with standardized price data
        """
        prices = []
        for date, values in time_series.items():
            prices.append({
                "date": date,
                "open": float(values.get("1. open", 0)),
                "high": float(values.get("2. high", 0)),
                "low": float(values.get("3. low", 0)),
                "close": float(values.get("4. close", 0)),
                "volume": int(values.get("5. volume", 0))
            })
        
        # Sort by date, most recent first
        prices.sort(key=lambda x: x["date"], reverse=True)
        return prices