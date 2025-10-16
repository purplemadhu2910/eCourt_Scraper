@echo off
echo eCourts India Case Scraper
echo ========================
echo.
echo Choose an option:
echo 1. Install dependencies
echo 2. Run CLI interface
echo 3. Start web interface
echo 4. Run tests
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Installing dependencies...
    pip install -r requirements.txt
    pause
    goto :start
)

if "%choice%"=="2" (
    echo.
    echo CLI Usage Examples:
    echo python cli.py --cnr "DLCT01-123456-2023" --today
    echo python cli.py --case "CRL.A" "123" "2023" --tomorrow
    echo python cli.py --causelist
    echo.
    pause
    goto :start
)

if "%choice%"=="3" (
    echo Starting web interface...
    echo Open http://localhost:5000 in your browser
    python web_api.py
    pause
    goto :start
)

if "%choice%"=="4" (
    echo Running tests...
    python test_scraper.py
    pause
    goto :start
)

if "%choice%"=="5" (
    exit
)

:start
cls
goto :start