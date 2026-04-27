"""
frontend/api_client.py

Thin HTTP client that talks to the SmartStudy AI FastAPI backend.
All requests are wrapped in try/except so that a missing or offline backend
never crashes the Streamlit frontend — a DummyResponse is returned instead.
"""

import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Base URL — must match the backend's uvicorn port
# ─────────────────────────────────────────────
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8042")

_REQUEST_TIMEOUT = 10  # seconds


# ─────────────────────────────────────────────
# Dummy response — returned when backend is offline
# ─────────────────────────────────────────────
class DummyResponse:
    """Mimics a requests.Response so callers don't need special handling."""

    def __init__(self, status_code: int = 503, detail: str = "Backend is offline. Please try again later."):
        self.status_code = status_code
        self.ok = False
        self.text = detail
        self._detail = detail

    def json(self):
        return {"detail": self._detail}


# ─────────────────────────────────────────────
# Safe request wrapper
# ─────────────────────────────────────────────
def _safe_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Execute an HTTP request and return a DummyResponse on any network error
    so Streamlit pages never see an uncaught exception.
    """
    kwargs.setdefault("timeout", _REQUEST_TIMEOUT)
    try:
        response = requests.request(method, url, **kwargs)
        return response
    except ConnectionError:
        return DummyResponse(503, "Cannot connect to backend. Is the server running on port 8042?")
    except Timeout:
        return DummyResponse(504, "Request timed out. The backend may be overloaded.")
    except RequestException as exc:
        return DummyResponse(500, f"Request failed: {exc}")


# ─────────────────────────────────────────────
# Auth endpoints
# ─────────────────────────────────────────────
def signup_user(email: str, full_name: str, password: str):
    """POST /auth/signup — create a new account (Firebase + local DB)."""
    return _safe_request(
        "POST",
        f"{BASE_URL}/auth/signup",
        json={"email": email, "full_name": full_name, "password": password},
    )


def login_user(email: str, password: str):
    """
    POST /auth/login — authenticate and retrieve a bearer token.

    The backend returns:
        {"access_token": "...", "token_type": "bearer", "token": "...", ...}

    The frontend should store res.json()["access_token"] in session_state.
    """
    return _safe_request(
        "POST",
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
    )


def get_me(token: str):
    """GET /auth/me — fetch the logged-in user's profile."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )



