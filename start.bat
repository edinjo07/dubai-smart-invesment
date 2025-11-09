@echo off
echo ========================================
echo   Dubai Smart Invest - Starting Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Starting Flask Server...
echo ========================================
echo.
echo Server will be available at:
echo   - Local:   http://localhost:5000
echo   - Network: http://192.168.0.103:5000
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.

REM Start the Flask application
python app.py

REM If app exits, pause to show any errors
if errorlevel 1 (
    echo.
    echo Server stopped with errors!
    pause
)
