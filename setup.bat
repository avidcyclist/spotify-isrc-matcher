@echo off
echo ========================================
echo   Spotify ISRC Matcher Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

REM Check if virtual environment exists
if not exist ".venv" (
    echo.
    echo 🔄 Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo.
echo 🔄 Installing dependencies...
call .venv\Scripts\activate.bat
pip install requests>=2.31.0 openpyxl>=3.1.0 pandas>=2.0.0

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Setup config file
echo.
echo 🔧 Setting up configuration...

if exist "config.json" (
    echo ✅ config.json already exists
    goto :test_config
)

echo Creating config.json...
echo {> config.json
echo   "client_id": "YOUR_CLIENT_ID",>> config.json
echo   "client_secret": "YOUR_CLIENT_SECRET">> config.json
echo }>> config.json

:test_config
REM Check if config has been updated
findstr "YOUR_CLIENT_ID" config.json >nul
if %errorlevel% equ 0 (
    echo.
    echo ⚠️  You need to update your Spotify API credentials!
    echo.
    echo Please follow these steps:
    echo 1. Go to: https://developer.spotify.com/dashboard
    echo 2. Log in with your Spotify account
    echo 3. Click "Create App"
    echo 4. Fill in app details and use redirect URI: https://localhost:8888/callback
    echo 5. Copy your Client ID and Client Secret
    echo.
    
    set /p client_id="Enter your Spotify Client ID: "
    set /p client_secret="Enter your Spotify Client Secret: "
    
    echo {> config.json
    echo   "client_id": "%client_id%",>> config.json
    echo   "client_secret": "%client_secret%">> config.json
    echo }>> config.json
    
    echo ✅ Configuration updated
) else (
    echo ✅ Configuration looks good
)

REM Test the setup
echo.
echo 🧪 Testing setup...
call .venv\Scripts\activate.bat
python test_basic.py

if %errorlevel% neq 0 (
    echo ❌ Setup test failed
    pause
    exit /b 1
)

echo.
echo =========================================
echo   🎉 Setup Complete! 🎉
echo =========================================
echo.
echo Your Spotify ISRC Matcher is ready to use!
echo.
echo To run the program:
echo   - Double-click 'run_program.bat'
echo   - Or run: python excel_runner.py
echo.
echo Happy ISRC matching! 🎵
echo.
pause
