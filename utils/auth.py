"""
Authentication module for the stock analysis application
"""

import os
import logging
from typing import Dict, Tuple, List, Optional
import gradio as gr

logger = logging.getLogger(__name__)

class AuthManager:
    """
    Manages authentication for the application
    """
    
    def __init__(self):
        """Initialize the authentication manager"""
        self.auth_enabled = os.getenv("AUTH_ENABLED", "True").lower() in ("true", "1", "yes")
        self._load_credentials()
        
    def _load_credentials(self) -> None:
        """Load credentials from environment variables"""
        self.credentials = {}
        
        if not self.auth_enabled:
            logger.info("Authentication is disabled")
            return
        
        # Parse credentials from environment variable
        # Format: "username1:password1,username2:password2"
        creds_str = os.getenv("AUTH_CREDENTIALS", "admin:admin123")
        
        try:
            for cred_pair in creds_str.split(","):
                if ":" not in cred_pair:
                    logger.warning(f"Invalid credential format: {cred_pair}")
                    continue
                    
                username, password = cred_pair.strip().split(":", 1)
                self.credentials[username] = password
                
            logger.info(f"Loaded {len(self.credentials)} user credentials")
            
        except Exception as e:
            logger.error(f"Error parsing credentials: {str(e)}")
            # Set default admin user if parsing fails
            self.credentials = {"admin": "admin123"}
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            True if authentication succeeds, False otherwise
        """
        if not self.auth_enabled:
            return True
            
        if username not in self.credentials:
            logger.warning(f"Authentication failed: User '{username}' not found")
            return False
            
        if self.credentials[username] != password:
            logger.warning(f"Authentication failed: Invalid password for user '{username}'")
            return False
            
        logger.info(f"User '{username}' authenticated successfully")
        return True
    
    def get_auth_middleware(self) -> Optional[Tuple[List[str], str]]:
        """
        Get Gradio authentication middleware configuration.
        
        Returns:
            Tuple of (usernames, message) if auth is enabled, None otherwise
        """
        if not self.auth_enabled:
            return None
            
        return (list(self.credentials.keys()), "Enter your username and password")