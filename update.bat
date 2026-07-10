@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Update Utility
color 0E

echo ============================================================
echo                NAUKRIBOT UPDATE
echo ============================================================
echo.

:: -------------------------------------------------
:: Python
:: -------------------------------------------------

echo [1/8] Checking Python...

py -3.13 --version

if errorlevel 1 (
    color 0C
    echo Python Not Installed.
    pause
    exit /b
)

echo.

:: -------------------------------------------------
:: Upgrade pip
:: -------------------------------------------------

echo [2/8] Updating pip...

py -3.13 -m pip install --upgrade pip setuptools wheel

echo.

:: -------------------------------------------------
:: Update Packages
:: -------------------------------------------------

echo [3/8] Updating Python Packages...

py -3.13 -m pip install --upgrade -r requirements.txt

echo.

:: -------------------------------------------------
:: ChromeDriver
:: -------------------------------------------------

echo [4/8] Updating ChromeDriver...

py -3.13 -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())"

echo.

:: -------------------------------------------------
:: Selenium Test
:: -------------------------------------------------

echo [5/8] Testing Selenium...

py -3.13 -c "import selenium; print('Selenium OK')"

echo.

:: -------------------------------------------------
:: Folder Check
:: -------------------------------------------------

echo [6/8] Checking Folder Structure...

if not exist Resume mkdir Resume
if not exist ChromeProfile mkdir ChromeProfile
if not exist Logs mkdir Logs
if not exist Backup mkdir Backup
if not exist Screenshots mkdir Screenshots
if not exist Temp mkdir Temp
if not exist src mkdir src
if not exist config mkdir config

echo Folder Structure OK

echo.

:: -------------------------------------------------
:: Internet
:: -------------------------------------------------

echo [7/8] Internet Check...

ping google.com -n 1 >nul

if errorlevel 1 (
    echo Internet : FAIL
) else (
    echo Internet : PASS
)

echo.

:: -------------------------------------------------
:: Completed
:: -------------------------------------------------

echo [8/8] Update Complete

echo.
echo ============================================================
echo            UPDATE COMPLETED SUCCESSFULLY
echo ============================================================

pause