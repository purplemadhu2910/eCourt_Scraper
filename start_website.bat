@echo off
echo Starting eCourts Legal Services Website...
echo.

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
echo.

echo Starting Flask backend server...
start "Flask Backend" cmd /k "python app.py"
echo Backend started on http://localhost:5000
echo.

echo Installing frontend dependencies...
cd ..\frontend
call npm install
echo.

echo Starting React frontend server...
start "React Frontend" cmd /k "npm start"
echo Frontend will start on http://localhost:3000
echo.

echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause