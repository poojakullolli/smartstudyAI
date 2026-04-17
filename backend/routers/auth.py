<<<<<<< HEAD
"""
backend/routers/auth.py

Authentication routes using Firebase Admin SDK (for user management)
combined with JWT tokens (for stateless API session management).

Flow:
  ┌─ POST /auth/signup ──► Creates user in Firebase + local DB
  ├─ POST /auth/login  ──► Verifies Firebase user exists → issues JWT
  └─ GET  /auth/me     ──► Returns current user info from JWT claim
"""

from datetime import timedelta
import os

import firebase_admin.auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from backend import models, schemas, auth_utils
from backend.database import get_db
=======
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend import models, schemas, auth_utils
from backend.database import get_db
import os
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

<<<<<<< HEAD

# ─────────────────────────────────────────────
# Request schemas (JSON body — not form data)
# ─────────────────────────────────────────────
class SignupRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─────────────────────────────────────────────
# Helper – get or create local DB user
# ─────────────────────────────────────────────
def _get_or_create_local_user(db: Session, email: str, firebase_uid: str, full_name: str = None) -> models.User:
    """
    Ensure a matching row exists in the local users table.
    The hashed_password column stores the Firebase UID (prefixed) so existing
    code that reads the column doesn't break.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            full_name=full_name,
            hashed_password=f"firebase:{firebase_uid}",  # not used for auth
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif full_name and not user.full_name:
        user.full_name = full_name
        db.commit()
        db.refresh(user)
    return user


# ─────────────────────────────────────────────
# POST /auth/signup
# ─────────────────────────────────────────────
@router.post("/signup", status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user in Firebase and mirror into the local DB.
    Firebase enforces unique emails and password strength.
    """
    # 1. Create Firebase user
    try:
        firebase_user = firebase_auth.create_user(
            email=payload.email,
            password=payload.password,
        )
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )
    except FirebaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Firebase error: {exc.message}",
        )
    except Exception as exc:
        # Firebase not initialized (key file missing) → fall back to local-only
        # Allow signup so the app doesn't break during development
        local_user = db.query(models.User).filter(models.User.email == payload.email).first()
        if local_user:
            raise HTTPException(status_code=400, detail="Email already registered.")
        hashed = auth_utils.get_password_hash(payload.password)
        local_user = models.User(email=payload.email, full_name=payload.full_name, hashed_password=hashed)
        db.add(local_user)
        db.commit()
        db.refresh(local_user)
        return {"message": "Account created (local fallback).", "email": payload.email}

    # 2. Mirror into local DB (so JWT-protected routes can look up user_id)
    _get_or_create_local_user(db, payload.email, firebase_user.uid, payload.full_name)

    return {
        "message": "Account created successfully.",
        "email": firebase_user.email,
        "firebase_uid": firebase_user.uid,
    }


# ─────────────────────────────────────────────
# POST /auth/login
# ─────────────────────────────────────────────
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Verify the user exists in Firebase, then issue:
      - a Firebase custom token  (for front-end Firebase SDK use)
      - a JWT access token       (for direct API bearer auth)

    Note: Firebase Admin cannot verify passwords server-side.
    Password verification is the responsibility of the Firebase client SDK.
    Here we confirm the account exists and produce tokens.
    """
    # 1. Look up Firebase user by email
    try:
        firebase_user = firebase_auth.get_user_by_email(payload.email)
    except firebase_auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No account found for this email.",
        )
    except FirebaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Firebase error: {exc.message}",
        )
    except Exception:
        # Firebase not initialized → fall back to local password check
        local_user = db.query(models.User).filter(models.User.email == payload.email).first()
        if not local_user or not auth_utils.verify_password(
            payload.password, local_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
        access_token = auth_utils.create_access_token(
            data={"sub": local_user.email}, expires_delta=expire
        )
        return {
            "message": "Login successful (local fallback).",
            "access_token": access_token,
            "token_type": "bearer",
            "token": access_token,
        }

    # 2. Ensure local DB row exists (for JWT-protected routes)
    _get_or_create_local_user(db, firebase_user.email, firebase_user.uid)

    # 3. Generate Firebase custom token (bytes → decode to str)
    try:
        custom_token_bytes = firebase_auth.create_custom_token(firebase_user.uid)
        custom_token = custom_token_bytes.decode("utf-8")
    except Exception:
        custom_token = None

    # 4. Generate our own JWT so all protected API routes keep working
    expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
    access_token = auth_utils.create_access_token(
        data={"sub": firebase_user.email}, expires_delta=expire
    )

    return {
        "message": "Login successful.",
        # access_token is what the Streamlit frontend stores and sends as Bearer
        "access_token": access_token,
        "token_type": "bearer",
        # token is the Firebase custom token (for Firebase client SDK exchange)
        "token": custom_token or access_token,
        "firebase_uid": firebase_user.uid,
    }


# ─────────────────────────────────────────────
# GET /auth/me
# ─────────────────────────────────────────────
@router.get("/me")
def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    """Return the logged-in user's profile info."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }

# ─────────────────────────────────────────────
# POST /auth/google
# ─────────────────────────────────────────────
class GoogleLoginRequest(BaseModel):
    id_token: str

@router.post("/google")
def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    from fastapi.responses import JSONResponse
    try:
        # Verify the Firebase ID token
        decoded_token = firebase_auth.verify_id_token(payload.id_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        picture = decoded_token.get("picture")

        # Mirror user into local DB so JWT-reliant routes might work if integrated later 
        # (Does not break existing flows)
        if email and uid:
            _get_or_create_local_user(db, email, uid, name)

        return {
            "message": "Google login successful",
            "uid": uid,
            "email": email,
            "name": name,
            "picture": picture
        }
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid Google token"}
        )

# ─────────────────────────────────────────────
# GET /auth/google/login (Backend-controlled OAuth Initiation)
# ─────────────────────────────────────────────
from fastapi.responses import RedirectResponse
from backend.google_oauth import get_google_flow
import requests
import uuid

# Memory-store for PKCE code verifiers (solves invalid_grant on callback)
OAUTH_STATES = {}

@router.get("/google/login")
def google_login_redirect():
    """
    Step 1 of OAuth Flow:
    Redirects the user directly to the Google OAuth consent screen.
    """
    try:
        flow = get_google_flow()
        # Generate the authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        # Store the PKCE verifier securely in backend memory using 'state' as the key
        OAUTH_STATES[state] = getattr(flow, 'code_verifier', None)
        
        # Redirect user browser to Google
        return RedirectResponse(url=authorization_url)
    except Exception as exc:
        # Return clean HTTP error, avoid crashing server
        raise HTTPException(status_code=500, detail=f"OAuth setup failed: {str(exc)}")

# ─────────────────────────────────────────────
# GET /auth/google/callback (OAuth Callback Handler)
# ─────────────────────────────────────────────
@router.get("/google/callback")
def google_login_callback(state: str, code: str, db: Session = Depends(get_db)):
    """
    Step 2 of OAuth Flow:
    Google redirects back here with a "code". We exchange it for tokens,
    extract the user profile, mirror to our DB, and generate our custom JWT.
    """
    try:
        # 1. Exchange the authorization code for an OAuth token
        flow = get_google_flow()
        
        # Retrieve the PKCE verifier we saved in /login
        code_verifier = OAUTH_STATES.pop(state, None)
        if code_verifier:
            flow.fetch_token(code=code, code_verifier=code_verifier)
        else:
            flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # 2. Get user info from Google's Userinfo API
        userinfo_response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo?alt=json',
            headers={'Authorization': f'Bearer {credentials.token}'}
        )
        user_info = userinfo_response.json()
        
        # 3. Extract requested fields
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")
        
        if not email:
            raise HTTPException(status_code=400, detail="Google authentication did not provide an email.")
            
        # 4. If user does not exist -> mirror/create new user
        # We use Google's subject ID (or a UUID fallback) strictly to satisfy the DB schema (hashed_password).
        google_subject_id = user_info.get("id", str(uuid.uuid4()))
        _get_or_create_local_user(db, email, f"google_oauth:{google_subject_id}", name)
        
        # 5. Generate app JWT (our existing JWT system)
        expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
        access_token = auth_utils.create_access_token(
            data={"sub": email}, expires_delta=expire
        )
        
        # 6. Redirect to frontend with token
        # Using Streamlit default port 8501. The frontend can pick up the token from URL query params.
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8501")
        return RedirectResponse(url=f"{frontend_url}/?token={access_token}")
        
    except Exception as exc:
        print(f"\n[!] OAUTH ERROR DETECTED: {str(exc)}\n")
        import traceback
        traceback.print_exc()
        
        # Proper error handling: Custom HTTP exception without crashing the entire FastAPI app
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth callback failed: {str(exc)}"
        )
=======
@router.post("/signup", response_model=schemas.UserDisplay)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_utils.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.get("/me", response_model=schemas.UserDisplay)
def get_me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return current_user
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
