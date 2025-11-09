@echo off
echo ========================================
echo Le Blanc Dubai - GitHub Setup
echo ========================================
echo.

REM Initialize Git repository
echo [1/6] Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo ERROR: Git not found. Please close and reopen PowerShell, then run this script again.
    pause
    exit /b 1
)

REM Configure Git (update with your details)
echo.
echo [2/6] Configuring Git...
set /p GIT_NAME="Enter your name: "
set /p GIT_EMAIL="Enter your email: "
git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"

REM Add all files
echo.
echo [3/6] Adding files...
git add .

REM Initial commit
echo.
echo [4/6] Creating initial commit...
git commit -m "Initial commit - Le Blanc Dubai Real Estate Website"

REM Create GitHub repository instructions
echo.
echo [5/6] GitHub Repository Setup
echo ========================================
echo.
echo Please create a new repository on GitHub:
echo 1. Go to: https://github.com/new
echo 2. Repository name: leblanc-dubai
echo 3. Make it PUBLIC or PRIVATE
echo 4. DO NOT initialize with README
echo 5. Click "Create repository"
echo.
set /p GITHUB_URL="Enter your GitHub repository URL (e.g., https://github.com/username/leblanc-dubai.git): "

REM Add remote and push
echo.
echo [6/6] Pushing to GitHub...
git branch -M main
git remote add origin %GITHUB_URL%
git push -u origin main

echo.
echo ========================================
echo SUCCESS! Your code is now on GitHub!
echo ========================================
echo.
echo Next steps:
echo 1. Go to: https://railway.app
echo 2. Sign in with GitHub
echo 3. Click "New Project"
echo 4. Select "Deploy from GitHub repo"
echo 5. Choose "leblanc-dubai"
echo 6. Railway will deploy automatically!
echo.
pause
