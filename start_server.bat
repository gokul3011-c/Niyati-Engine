@echo off
echo ============================================
echo   Niyati Engine - Starting Backend Server
echo ============================================
echo.
echo Installing dependencies...
pip install flask flask-cors
echo.
echo Starting Flask API server on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python api_server.py
pause
