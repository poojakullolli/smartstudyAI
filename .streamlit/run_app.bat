@echo off
cd /d "%~dp0"

echo ========================================
echo       SmartStudy AI - Auto Launcher
echo ========================================

echo [1/3] Installing dependencies...
python -m pip install -r requirements.txt --quiet

echo [2/3] Starting FastAPI Backend (Port 8042)...
start "" cmd /k "title SmartStudyAI - Backend && cd /d C:\Users\Admin\Desktop\smartstudyAI\smartstudyAI-main && python -m uvicorn backend.main:app --port 8042 --reload"

echo [3/3] Waiting for backend to initialize...
timeout /t 4 /nobreak > nul

echo [4/4] Starting Streamlit Frontend...
start "" cmd /k "title SmartStudyAI - Frontend && cd /d C:\Users\Admin\Desktop\smartstudyAI\smartstudyAI-main && python -m streamlit run frontend/app.py"

echo ========================================
echo  Both servers launching!
echo  Frontend: http://localhost:8501
echo  Backend:  http://localhost:8042/docs
echo ========================================

timeout /t 5 /nobreak > nul
start "" "http://localhost:8501"
