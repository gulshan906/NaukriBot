@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Runner
color 0B

echo ============================================================
echo                 NAUKRIBOT RUNNER
echo ============================================================
echo.

echo [1/5] Checking Python...

py -3.13 --version >nul 2>&1

if errorlevel 1 (
    color 0C
    echo ERROR : Python 3.13 Not Installed.
    pause
    exit /b
)

echo Python OK

echo.
echo [2/5] Checking Chrome...

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo Chrome OK
) else (
    color 0C
    echo Chrome Not Installed.
    pause
    exit /b
)

echo.
echo [3/5] Checking Test Script...

if not exist test_selenium.py (
    color 0C
    echo test_selenium.py Not Found.
    pause
    exit /b
)

echo Test Script OK

echo.
echo [4/5] Starting Selenium...

py -3.13 test_selenium.py

if errorlevel 1 (
    color 0C
    echo.
    echo Selenium Test Failed.
    pause
    exit /b
)

echo.
echo [5/5] Completed Successfully.

echo.
echo ===========================================
echo        NAUKRIBOT TEST PASSED
echo ===========================================

pause