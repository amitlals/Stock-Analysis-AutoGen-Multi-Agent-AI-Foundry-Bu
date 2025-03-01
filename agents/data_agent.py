"""
Stock Data Agent - Handles retrieving stock data from APIs
"""

import os
import logging
from typing import Dict, Any, Optional
import autogen
from utils.api_handler import StockDataProvider

logger = logging.getLogger(__name__)

class StockDataAgent:
    """
    Agent responsible for retrieving stock data from APIs
    with automatic failover between Alpha Vantage and Yahoo Finance.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the stock data agent.
        
        Args:
            config: Dictionary containing agent configuration
        """
        self.config = config
        self.data_provider = StockDataProvider(
            alpha_vantage_key=os.getenv("ALPHAVANTAGE_API_KEY", "")
        )
        
        # Create AutoGen agent
        self.agent = autogen.AssistantAgent(
            name="data_agent",
            system_message="""You are a stock data retrieval agent.
            You retrieve historical price data, trading volume, and other fundamental
            data for stocks. You know how to handle missing data and API failures.
            """,
            llm_config=self.config.get("llm_config")
        )
    
    async def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve stock data for a given ticker symbol.
        
        Args:
            ticker: Stock symbol (e.g., AAPL, MSFT)
            
        Returns:
            Dictionary containing stock data or None if retrieval failed
        """
        logger.info(f"Fetching stock data for {ticker}")
        
        try:
            # Attempt to get data from APIs with automatic failover
            data = self.data_provider.get_stock_data(ticker)
            
            if not data:
                logger.error(f"Failed to retrieve data for {ticker}")
                return None
                
            return data
            
        except Exception as e:
            logger.error(f"Error retrieving stock data: {str(e)}")
            return None