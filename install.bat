@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Production Installer v2.0
color 0A

echo ============================================================
echo          NAUKRIBOT PRODUCTION INSTALLER v2.0
echo ============================================================
echo.

:: --------------------------------------------------
:: Python Check
:: --------------------------------------------------
echo [1/12] Checking Python...

py -3.13 --version >nul 2>&1

if errorlevel 1 (
    color 0C
    echo ERROR : Python 3.13 Not Installed.
    pause
    exit /b
)

echo OK

:: --------------------------------------------------
:: pip Check
:: --------------------------------------------------
echo.
echo [2/12] Checking pip...

py -3.13 -m pip --version >nul 2>&1

if errorlevel 1 (
    color 0C
    echo ERROR : pip Not Installed.
    pause
    exit /b
)

echo OK

:: --------------------------------------------------
:: Upgrade pip
:: --------------------------------------------------
echo.
echo [3/12] Updating pip...

py -3.13 -m pip install --upgrade pip setuptools wheel

:: --------------------------------------------------
:: requirements.txt
:: --------------------------------------------------
echo.
echo [4/12] Installing Python Packages...

if not exist requirements.txt (
    color 0C
    echo ERROR : requirements.txt Missing.
    pause
    exit /b
)

py -3.13 -m pip install -r requirements.txt

if errorlevel 1 (
    color 0C
    echo ERROR : Package Installation Failed.
    pause
    exit /b
)

echo OK

:: --------------------------------------------------
:: Folder Check
:: --------------------------------------------------
echo.
echo [5/12] Creating Project Folder...

mkdir Backup 2>nul
mkdir ChromeProfile 2>nul
mkdir Resume 2>nul
mkdir Logs 2>nul
mkdir Screenshots 2>nul
mkdir Temp 2>nul
mkdir src 2>nul
mkdir config 2>nul

echo OK

:: --------------------------------------------------
:: Chrome
:: --------------------------------------------------
echo.
echo [6/12] Checking Google Chrome...

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo Chrome Installed.
) else (
    color 0C
    echo ERROR : Chrome Not Installed.
    pause
    exit /b
)

:: --------------------------------------------------
:: Internet
:: --------------------------------------------------
echo.
echo [7/12] Checking Internet...

ping google.com -n 1 >nul

if errorlevel 1 (
    color 0E
    echo WARNING : Internet Not Available.
) else (
    echo Internet OK
)

:: --------------------------------------------------
:: Selenium
:: --------------------------------------------------
echo.
echo [8/12] Checking Selenium...

py -3.13 -c "import selenium"

if errorlevel 1 (
    color 0C
    echo Selenium Failed.
    pause
    exit /b
)

echo OK

:: --------------------------------------------------
:: ChromeDriver
:: --------------------------------------------------
echo.
echo [9/12] Checking ChromeDriver...

py -3.13 -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

if errorlevel 1 (
    color 0C
    echo ChromeDriver Failed.
    pause
    exit /b
)

echo OK

:: --------------------------------------------------
:: Resume
:: --------------------------------------------------
echo.
echo [10/12] Resume Folder...

if exist Resume (
    echo Resume Folder OK
) else (
    echo Resume Folder Missing
)

:: --------------------------------------------------
:: Chrome Profile
:: --------------------------------------------------
echo.
echo [11/12] Chrome Profile...

if exist ChromeProfile (
    echo Chrome Profile OK
) else (
    echo Chrome Profile Missing
)

:: --------------------------------------------------
:: Finished
:: --------------------------------------------------
echo.
echo [12/12] Final Status

echo.
echo ============================================
echo Python          : PASS
echo pip             : PASS
echo Packages        : PASS
echo Chrome          : PASS
echo Selenium        : PASS
echo ChromeDriver    : PASS
echo Folder          : PASS
echo ============================================

echo.
echo INSTALLATION SUCCESSFUL
echo.

pause