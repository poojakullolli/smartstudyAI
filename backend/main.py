import os
import threading
import time
import logging
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
from backend.routers import auth
from backend.auth_utils import get_current_user
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from fastapi import Depends, HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# 🔥 Load Environment Variables FIRST
# ─────────────────────────────────────────────
load_dotenv()   # This loads your .env file




# ─────────────────────────────────────────────
# 🔥 Firebase Initialization
# ─────────────────────────────────────────────
def init_firebase():
    if not firebase_admin._apps:
        base_dir = os.path.dirname(__file__)
        key_file = os.path.join(base_dir, "firebase_key.json")

        if key_file:
            cred = credentials.Certificate(key_file)
            firebase_admin.initialize_app(cred)
            print(f"[Firebase] Initialized with key: {os.path.basename(key_file)}")
        else:
            print(
                "[Firebase] WARNING: No service account key file found. "
                "Place firebase_key.json inside backend/ folder."
            )


init_firebase()


# ─────────────────────────────────────────────
# Create SQLAlchemy tables
# ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)




# ─────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────
app = FastAPI(title="SmartStudy AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the SmartStudy AI API!", "status": "online"}



# ─────────────────────────────────────────────
# Run App
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8042, reload=True)
