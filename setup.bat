@echo off
REM Le Blanc Dubai Real Estate - Windows Setup Script

echo Setting up Le Blanc Dubai Real Estate Backend...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create environment file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your actual email configuration.
)

REM Create leads file if it doesn't exist
if not exist leads.json (
    echo Creating leads.json file...
    echo [] > leads.json
)

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your email configuration
echo 2. Run 'python app.py' to start the server
echo 3. Visit http://localhost:5000 to view the website
echo.
echo To activate virtual environment in future sessions:
echo venv\Scripts\activate.bat

pause