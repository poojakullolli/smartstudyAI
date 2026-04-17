# AI Study Planner + Smart Doubt Explainer

A full-stack application leveraging FastAPI (backend), Streamlit (frontend), and OpenAI to provide intelligent study scheduling and on-demand doubt explanation.

## Features

- **User Authentication**: Secure signup and login.
- **AI Study Planner**: Generate tailored daily and weekly plans based on exams and weak subjects.
- **Smart Doubt Explainer**: Explain topics using simple logic, real-world analogies, and difficulty modes.
- **Study Tracker**: Monitor completed subjects and overall progress.
- **Pomodoro Timer**: Embedded timer for focused study sessions.

## Setup Instructions

1. **Install Requirements**
   Ensure you have Python 3.9+ installed. Run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Rename `.env.example` to `.env` and fill in your variables. If you don't have an OpenAI key, the app will use mock responses.

3. **Database**
   The application uses SQLite (`database.db`). It will be created automatically upon the first run.

4. **Run the Backend (FastAPI)**
   Open a terminal and run:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

5. **Run the Frontend (Streamlit)**
   Open a second terminal and run:
   ```bash
   streamlit run frontend/app.py
   ```
   
The Streamlit app will open in your browser automatically (usually at `http://localhost:8501`).
