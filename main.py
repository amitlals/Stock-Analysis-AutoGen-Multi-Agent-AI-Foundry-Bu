#!/usr/bin/env python3
"""
Stock Analysis Multi-Agent System - Main Entry Point
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application"""
    logger.info("Starting Stock Analysis Multi-Agent System")
    
    # Import here to ensure environment variables are loaded first
    from ui.app import launch_ui
    
    # Launch the Gradio UI
    ui_port = int(os.getenv("UI_PORT", 7860))
    launch_ui(port=ui_port)

if __name__ == "__main__":
    main()