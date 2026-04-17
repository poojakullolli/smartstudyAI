"""
backend/google_oauth.py
Handles backend-controlled Google OAuth 2.0 Flow configuration.
"""
import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()

# Allow OAuth testing over local HTTP (required for oauthlib to not crash on 127.0.0.1)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def get_google_flow():
    """
    Configures and returns the Google OAuth flow object
    based on environment variables.
    """
    # Load OAuth Credentials from environment variables
    # We use a dynamically created client config dictionary 
    # instead of a static JSON file for better security.
    client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8042/auth/google/callback")
    
    # Validation to prevent runtime crashes if variables aren't set
    if not client_id or not client_secret:
        raise ValueError("Google OAuth credentials missing in environment variables.")

    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri]
        }
    }
    
    # Initialize the OAuth Flow with requested scopes
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    )
    
    # Explicitly set the redirect URI
    flow.redirect_uri = redirect_uri
    
    return flow
