<<<<<<< HEAD
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


def get_user_stats(token: str):
    """GET /user/stats — fetch user XP and level stats."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/user/stats",
        headers={"Authorization": f"Bearer {token}"},
    )


# ─────────────────────────────────────────────
# Study Planner endpoints
# ─────────────────────────────────────────────
def create_study_plan(token: str, subject: str, exam_date, daily_hours: float, is_weak: bool):
    return _safe_request(
        "POST",
        f"{BASE_URL}/planner/create",
        json={
            "subject": subject,
            "exam_date": exam_date.isoformat(),
            "daily_available_hours": daily_hours,
            "is_weak_subject": is_weak,
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def get_my_plans(token: str):
    return _safe_request(
        "GET",
        f"{BASE_URL}/planner/my-plans",
        headers={"Authorization": f"Bearer {token}"},
    )


def delete_study_plan(token: str, plan_id: int):
    return _safe_request(
        "DELETE",
        f"{BASE_URL}/planner/delete/{plan_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


def toggle_complete(token: str, plan_id: int):
    return _safe_request(
        "PUT",
        f"{BASE_URL}/planner/toggle-complete/{plan_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


# ─────────────────────────────────────────────
# Study Tracker endpoints
# ─────────────────────────────────────────────
def create_task(token: str, subject: str, topic: str, duration: int) -> bool:
    res = _safe_request(
        "POST",
        f"{BASE_URL}/tracker/tasks",
        json={"subject": subject, "topic": topic, "duration_minutes": duration},
        headers={"Authorization": f"Bearer {token}"},
    )
    return res.status_code == 200


def get_tasks(token: str) -> list:
    res = _safe_request(
        "GET",
        f"{BASE_URL}/tracker/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )
=======
import os
import requests
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8042").replace("localhost", "127.0.0.1")

def signup_user(email, password):
    url = f"{BACKEND_URL}/auth/signup"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload)
    return response

def login_user(email, password):
    url = f"{BACKEND_URL}/auth/login"
    payload = {"username": email, "password": password}
    response = requests.post(url, data=payload)
    return response

def get_me(token):
    url = f"{BACKEND_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response

def create_study_plan(token, subject, exam_date, daily_hours, is_weak):
    url = f"{BACKEND_URL}/planner/create"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "subject": subject,
        "exam_date": exam_date.isoformat(),
        "daily_available_hours": daily_hours,
        "is_weak_subject": is_weak
    }
    return requests.post(url, json=payload, headers=headers)

def get_my_plans(token):
    url = f"{BACKEND_URL}/planner/my-plans"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers)

def delete_study_plan(token, plan_id):
    url = f"{BACKEND_URL}/planner/delete/{plan_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.delete(url, headers=headers)

def toggle_complete(token, plan_id):
    url = f"{BACKEND_URL}/planner/toggle-complete/{plan_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.put(url, headers=headers)

def create_task(token, subject, topic, duration):
    url = f"{BACKEND_URL}/tracker/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"subject": subject, "topic": topic, "duration_minutes": duration}
    res = requests.post(url, json=payload, headers=headers)
    return res.status_code == 200

def get_tasks(token):
    url = f"{BACKEND_URL}/tracker/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    if res.status_code == 200:
        return res.json()
    return []

<<<<<<< HEAD

def toggle_task(token: str, task_id: int):
    _safe_request(
        "PUT",
        f"{BASE_URL}/tracker/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


def delete_task(token: str, task_id: int):
    _safe_request(
        "DELETE",
        f"{BASE_URL}/tracker/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
    )


# ─────────────────────────────────────────────
# AI Explainer endpoints
# ─────────────────────────────────────────────
def get_history(token: str) -> list:
    res = _safe_request(
        "GET",
        f"{BASE_URL}/explainer/history",
        headers={"Authorization": f"Bearer {token}"},
    )
=======
def toggle_task(token, task_id):
    url = f"{BACKEND_URL}/tracker/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    requests.put(url, headers=headers)

def delete_task(token, task_id):
    url = f"{BACKEND_URL}/tracker/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {token}"}
    requests.delete(url, headers=headers)

def get_history(token):
    url = f"{BACKEND_URL}/explainer/history"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    if res.status_code == 200:
        return res.json()
    return []

<<<<<<< HEAD

def explain_doubt(token: str, question: str, difficulty: str):
    res = _safe_request(
        "POST",
        f"{BASE_URL}/explainer/explain",
        json={"question": question, "difficulty": difficulty},
        headers={"Authorization": f"Bearer {token}"},
    )
    if res.status_code == 200:
        return res.json()
    return None


def get_study_pattern(token: str):
    """GET /analytics/study-pattern — fetch study pattern analytics."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/analytics/study-pattern",
        headers={"Authorization": f"Bearer {token}"},
    )


def get_weak_analysis(token: str):
    """POST /ai/weak-analysis — get AI weak subject analysis."""
    return _safe_request(
        "POST",
        f"{BASE_URL}/ai/weak-analysis",
        headers={"Authorization": f"Bearer {token}"},
    )


def get_global_leaderboard(token: str):
    """GET /leaderboard/global — get global XP leaderboard."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/leaderboard/global",
        headers={"Authorization": f"Bearer {token}"},
    )


def get_weekly_leaderboard(token: str):
    """GET /leaderboard/weekly — get weekly XP leaderboard."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/leaderboard/weekly",
        headers={"Authorization": f"Bearer {token}"},
    )


def create_challenge(token: str, opponent_email: str, goal: str, duration_days: int):
    """POST /challenge/create — create a new challenge."""
    return _safe_request(
        "POST",
        f"{BASE_URL}/challenge/create",
        params={"opponent_email": opponent_email, "goal": goal, "duration_days": duration_days},
        headers={"Authorization": f"Bearer {token}"},
    )


def accept_challenge(token: str, challenge_id: int, accept: bool):
    """POST /challenge/accept — accept or decline a challenge."""
    return _safe_request(
        "POST",
        f"{BASE_URL}/challenge/accept",
        params={"challenge_id": challenge_id, "accept": accept},
        headers={"Authorization": f"Bearer {token}"},
    )


def get_challenges(token: str):
    """GET /challenge/status — get all user challenges."""
    return _safe_request(
        "GET",
        f"{BASE_URL}/challenge/status",
        headers={"Authorization": f"Bearer {token}"},
    )
=======
def explain_doubt(token, question, difficulty):
    url = f"{BACKEND_URL}/explainer/explain"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": question, "difficulty": difficulty}
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()
    return None
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
