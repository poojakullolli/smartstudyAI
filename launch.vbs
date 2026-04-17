Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Admin\Desktop\SmartStudyAI"
WshShell.Run "cmd /k ""cd /d C:\Users\Admin\Desktop\SmartStudyAI && python -m uvicorn backend.main:app --port 8042""", 1, False
WshShell.Run "cmd /k ""cd /d C:\Users\Admin\Desktop\SmartStudyAI && python -m streamlit run frontend/app.py""", 1, False
WScript.Sleep 4000
WshShell.Run "http://localhost:8501", 1, False
