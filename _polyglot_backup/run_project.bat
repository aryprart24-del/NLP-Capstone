@echo off
echo ========================================================
echo   PolyGlot NLP - Multilingual Translation Assistant
echo   Presented by: Aryan ^| D.Y. Patil University
echo ========================================================
echo.
echo Starting FastAPI Backend on http://localhost:8000 ...
start "PolyGlot Backend (FastAPI)" cmd /k "cd backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Starting React Vite Frontend on http://localhost:5173 ...
start "PolyGlot Frontend (Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are launching!
echo Backend API Docs: http://localhost:8000/docs
echo Frontend Web App: http://localhost:5173
echo ========================================================
pause
