@echo off
echo Starting Le Blanc Dubai Real Estate Backend...
echo.

REM Check if virtual environment exists
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if errorlevel 1 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
)

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found. Using example configuration.
    echo Please create .env file from .env.example and configure your email settings.
    echo.
)

echo Starting Flask server...
echo Backend will be available at: http://localhost:5000
echo Website will be available at: http://localhost:5000
echo API endpoints available at: http://localhost:5000/api/
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause