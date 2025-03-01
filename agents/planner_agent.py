"""
Planner Agent - Coordinates the analysis workflow between specialized agents
"""

import autogen
from typing import Dict, List, Optional, Any

class PlannerAgent:
    """
    Planner Agent that orchestrates the workflow between multiple agents
    for stock analysis tasks.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the planner agent with configuration.
        
        Args:
            config: Dictionary containing agent configuration
        """
        self.config = config
        
        # Create AutoGen agent for planning
        self.agent = autogen.AssistantAgent(
            name="planner",
            system_message="""You are a planning agent that coordinates stock analysis.
            You break down user requests into tasks that can be handled by specialized agents:
            - data_agent: Retrieves stock price and fundamental data
            - analyst_agent: Performs technical analysis on stock data
            - recommender_agent: Provides investment recommendations
            
            Create a plan for each user request, assign tasks to agents, and synthesize the final response.
            """,
            llm_config=self.config.get("llm_config")
        )
    
    async def create_analysis_plan(self, ticker: str, user_query: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a plan for analyzing a stock.
        
        Args:
            ticker: Stock ticker symbol
            user_query: Optional specific query from the user
            
        Returns:
            Dictionary containing the analysis plan
        """
        # Implementation will coordinate with other agents
        pass