"""
Gradio UI for Stock Analysis Multi-Agent System
"""

import os
import logging
import gradio as gr
from utils.auth import AuthManager

logger = logging.getLogger(__name__)

def build_ui():
    """
    Build and return the Gradio UI interface
    
    Returns:
        Gradio Interface object
    """
    # Set theme and styles
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
    ).set(
        button_primary_background_fill="*primary_500",
        button_primary_background_fill_hover="*primary_600",
        button_primary_text_color="white",
    )
    
    # Create the Gradio interface
    with gr.Blocks(theme=theme, title="Stock Analysis Multi-Agent System") as interface:
        gr.Markdown("# 📈 Stock Analysis Multi-Agent System")
        gr.Markdown("Enter a stock ticker symbol to get AI-powered analysis and recommendations")
        
        with gr.Row():
            with gr.Column(scale=3):
                ticker_input = gr.Textbox(
                    label="Stock Ticker Symbol",
                    placeholder="e.g. AAPL, MSFT, GOOGL",
                    info="Enter the stock symbol you want to analyze"
                )
                
                with gr.Row():
                    analyze_btn = gr.Button("Analyze Stock", variant="primary")
                    clear_btn = gr.Button("Clear Results")
                
                with gr.Accordion("Advanced Options", open=False):
                    email_input = gr.Textbox(
                        label="Email Address (Optional)",
                        placeholder="Enter email to receive the report",
                        info="Leave blank if you don't want an email report"
                    )
                    
                    custom_query = gr.Textbox(
                        label="Custom Analysis Question (Optional)",
                        placeholder="e.g. How does this stock compare to industry peers?",
                        info="Ask a specific question about this stock"
                    )
            
            with gr.Column(scale=7):
                with gr.Tabs():
                    with gr.TabItem("Analysis Results"):
                        result_container = gr.Markdown("Enter a ticker symbol and click 'Analyze Stock' to see results.")
                    
                    with gr.TabItem("Price Chart"):
                        chart_output = gr.Plot(label="Stock Price History")
                    
                    with gr.TabItem("Technical Indicators"):
                        indicators_output = gr.Dataframe()
                        
                    with gr.TabItem("AI Recommendation"):
                        recommendation_output = gr.Markdown("AI recommendation will appear here.")
        
        # Add footer
        gr.Markdown("Powered by AutoGen Multi-Agent System | Created by Your Name")
        
        # Define event handlers
        def analyze_stock(ticker, custom_query, email):
            """
            Handle analyze button click
            
            Args:
                ticker: Stock ticker symbol
                custom_query: Optional custom analysis question
                email: Optional email address for report delivery
                
            Returns:
                Analysis results to update UI components
            """
            if not ticker or len(ticker.strip()) == 0:
                return "Please enter a valid ticker symbol", None, None, "No ticker provided"
            
            ticker = ticker.strip().upper()
            
            # Placeholder for actual analysis logic
            # This would be replaced with calls to the agent system
            
            # Mock data for demonstration
            result_md = f"""
            ## Analysis Results for {ticker}
            
            **Company:** Apple Inc.
            **Sector:** Technology
            **Current Price:** $175.34 (as of 2025-03-01)
            
            ### Summary
            
            The stock is showing strong momentum with positive technical indicators.
            Recent performance indicates potential for continued growth based on:
            - Consistent uptrend over 50-day moving average
            - Low volatility compared to market
            - Positive earnings surprises in recent quarters
            
            ### Key Metrics
            
            | Metric | Value | Interpretation |
            | ------ | ----- | -------------- |
            | 50-Day MA | $170.23 | Above (Bullish) |
            | 200-Day MA | $165.78 | Above (Bullish) |
            | RSI (14) | 58.3 | Neutral |
            | 6-Month Return | +12.5% | Strong |
            | 30-Day Volatility | 1.3% | Low |
            """
            
            # Mock chart data
            import numpy as np
            import matplotlib.pyplot as plt
            
            dates = np.array([f"2025-{i:02d}-01" for i in range(1, 13)])
            prices = 150 + np.cumsum(np.random.normal(0, 3, 12))
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(dates, prices, marker='o')
            ax.set_title(f"{ticker} Price History")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price ($)")
            ax.grid(True)
            
            # Mock technical indicators
            import pandas as pd
            indicators = pd.DataFrame({
                "Indicator": ["50-Day MA", "200-Day MA", "RSI (14)", "MACD", "Bollinger Bands", "Volume Trend"],
                "Value": ["170.23", "165.78", "58.3", "Positive", "Middle Band", "Increasing"],
                "Signal": ["Bullish", "Bullish", "Neutral", "Bullish", "Neutral", "Bullish"]
            })
            
            # Mock recommendation
            recommendation = f"""
            ## AI Recommendation for {ticker}
            
            ### Overall Rating: 🟢 BUY
            
            **Confidence Level:** High (85%)
            
            **Reasoning:**
            - Strong technical position above both 50-day and 200-day moving averages
            - Reasonable valuation with P/E ratio below industry average
            - Solid fundamentals with consistent revenue growth
            - Positive analyst revisions for upcoming quarters
            
            **Risk Assessment:** Moderate
            - Main risks include industry competition and potential regulatory changes
            - Market volatility may affect short-term performance
            
            **Suggested Position Sizing:** Consider allocating 3-5% of portfolio
            """
            
            if email:
                # Mock email sending (would be implemented via Azure Logic Apps)
                recommendation += f"\n\n*Analysis report has been sent to {email}*"
            
            return result_md, fig, indicators, recommendation
        
        def clear_outputs():
            """Clear all output fields"""
            return (
                "Enter a ticker symbol and click 'Analyze Stock' to see results.",
                None,
                None,
                "AI recommendation will appear here."
            )
        
        # Connect event handlers
        analyze_btn.click(
            analyze_stock,
            inputs=[ticker_input, custom_query, email_input],
            outputs=[result_container, chart_output, indicators_output, recommendation_output]
        )
        
        clear_btn.click(
            clear_outputs,
            inputs=[],
            outputs=[result_container, chart_output, indicators_output, recommendation_output]
        )
        
    return interface

def launch_ui(port=7860):
    """
    Launch the Gradio UI
    
    Args:
        port: Port to run the UI on
    """
    auth_manager = AuthManager()
    interface = build_ui()
    
    auth_args = {}
    auth_middleware = auth_manager.get_auth_middleware()
    if auth_middleware:
        auth_args["auth"] = auth_middleware
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        **auth_args
    )

if __name__ ==