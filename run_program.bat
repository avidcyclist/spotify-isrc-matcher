@echo off
echo ========================================
echo   Spotify ISRC Matcher
echo ========================================
echo.

REM Check if setup has been run
if not exist ".venv" (
    echo ❌ Setup not complete!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

if not exist "config.json" (
    echo ❌ Configuration missing!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run the program
call .venv\Scripts\activate.bat
python excel_runner.py

echo.
echo Press any key to exit...
pause >nul
