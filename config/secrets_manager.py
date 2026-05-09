"""
Utility for loading secrets from Streamlit Secrets Manager or .env file.
This allows seamless local development and Streamlit Cloud deployment.
"""

import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()


def get_secret(key: str, default=None) -> str:
    """
    Get a secret from Streamlit Secrets Manager (production) or .env (local).
    
    Args:
        key: Secret key name
        default: Default value if secret not found
        
    Returns:
        Secret value or default
    """
    
    # Try Streamlit Secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            try:
                return st.secrets[key]
            except (KeyError, AttributeError):
                pass
    except ImportError:
        pass
    
    # Fall back to environment variables (for local development)
    return os.getenv(key, default)


def get_fyers_credentials() -> tuple:
    """
    Get Fyers API credentials from secrets.
    
    Returns:
        Tuple of (CLIENT_ID, SECRET_KEY, REDIRECT_URI, ACCESS_TOKEN)
        
    Raises:
        ValueError: If credentials are missing
    """
    
    client_id = get_secret("FYERS_CLIENT_ID")
    secret_key = get_secret("FYERS_SECRET_KEY")
    redirect_uri = get_secret("FYERS_REDIRECT_URI")
    access_token = get_secret("FYERS_ACCESS_TOKEN")
    
    if not all([client_id, secret_key, redirect_uri]):
        raise ValueError(
            "Missing FYERS credentials. Configure in:\n"
            "- Local: .env file\n"
            "- Streamlit Cloud: Settings > Secrets"
        )
    
    return client_id, secret_key, redirect_uri, access_token
