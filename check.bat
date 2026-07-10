@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Health Check
color 0B

echo ============================================================
echo                 NAUKRIBOT HEALTH CHECK
echo ============================================================
echo.

:: --------------------------------------------------
:: Python
:: --------------------------------------------------
echo [1/10] Python

py -3.13 --version >nul 2>&1

if errorlevel 1 (
    echo [FAIL] Python Not Installed
) else (
    echo [PASS] Python Installed
)

echo.

:: --------------------------------------------------
:: pip
:: --------------------------------------------------
echo [2/10] pip

py -3.13 -m pip --version >nul 2>&1

if errorlevel 1 (
    echo [FAIL] pip Missing
) else (
    echo [PASS] pip Installed
)

echo.

:: --------------------------------------------------
:: Chrome
:: --------------------------------------------------
echo [3/10] Google Chrome

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [PASS] Chrome Installed
) else (
    echo [FAIL] Chrome Missing
)

echo.

:: --------------------------------------------------
:: Selenium
:: --------------------------------------------------
echo [4/10] Selenium

py -3.13 -c "import selenium" >nul 2>&1

if errorlevel 1 (
    echo [FAIL] Selenium Missing
) else (
    echo [PASS] Selenium Installed
)

echo.

:: --------------------------------------------------
:: ChromeDriver
:: --------------------------------------------------
echo [5/10] ChromeDriver

py -3.13 -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()" >nul 2>&1

if errorlevel 1 (
    echo [FAIL] ChromeDriver
) else (
    echo [PASS] ChromeDriver
)

echo.

:: --------------------------------------------------
:: Resume
:: --------------------------------------------------
echo [6/10] Resume Folder

if exist Resume (
    echo [PASS] Resume Folder
) else (
    echo [FAIL] Resume Folder
)

echo.

:: --------------------------------------------------
:: Chrome Profile
:: --------------------------------------------------
echo [7/10] Chrome Profile

if exist ChromeProfile (
    echo [PASS] Chrome Profile
) else (
    echo [FAIL] Chrome Profile
)

echo.

:: --------------------------------------------------
:: Internet
:: --------------------------------------------------
echo [8/10] Internet

ping google.com -n 1 >nul

if errorlevel 1 (
    echo [FAIL] Internet
) else (
    echo [PASS] Internet
)

echo.

:: --------------------------------------------------
:: Disk Space
:: --------------------------------------------------
echo [9/10] Disk Space

wmic logicaldisk where "DeviceID='C:'" get FreeSpace,Size

echo.

:: --------------------------------------------------
:: Windows Version
:: --------------------------------------------------
echo [10/10] Windows Version

ver

echo.
echo ============================================================
echo              HEALTH CHECK COMPLETED
echo ============================================================

pause