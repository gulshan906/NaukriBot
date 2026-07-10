@echo off
title NaukriBot Setup
color 0A

echo ==========================================
echo         NAUKRIBOT SETUP STARTED
echo ==========================================
echo.

echo [1/9] Checking Python...
py -3.13 --version
if errorlevel 1 (
    echo.
    echo ERROR: Python 3.13 not found.
    pause
    exit /b
)

echo.
echo [2/9] Upgrading pip...
py -3.13 -m pip install --upgrade pip setuptools wheel

echo.
echo [3/9] Installing Required Packages...
py -3.13 -m pip install selenium webdriver-manager requests pandas openpyxl python-dotenv psutil schedule colorama fake-useragent

echo.
echo [4/9] Creating Project Folders...

mkdir C:\NaukriBot 2>nul
mkdir C:\NaukriBot\Resume 2>nul
mkdir C:\NaukriBot\ChromeProfile 2>nul
mkdir C:\NaukriBot\Logs 2>nul
mkdir C:\NaukriBot\Screenshots 2>nul
mkdir C:\NaukriBot\Backup 2>nul
mkdir C:\NaukriBot\Temp 2>nul
mkdir C:\NaukriBot\src 2>nul
mkdir C:\NaukriBot\config 2>nul

echo.
echo [5/9] Checking Google Chrome...

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo Chrome Found.
) else (
    echo.
    echo ERROR : Google Chrome Not Installed.
    pause
    exit /b
)

echo.
echo [6/9] Checking Internet...

ping google.com -n 1 >nul

if errorlevel 1 (
    echo Internet Not Available.
) else (
    echo Internet OK.
)

echo.
echo [7/9] Checking ChromeDriver...

py -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())"

echo.
echo [8/9] Checking Selenium...

py -c "from selenium import webdriver;print('Selenium Installed Successfully')"

echo.
echo [9/9] Setup Completed Successfully.

echo.
echo ==========================================
echo         READY FOR AUTOMATION
echo ==========================================
pause