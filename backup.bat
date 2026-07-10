@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Backup Utility
color 0E

echo ============================================================
echo                 NAUKRIBOT BACKUP
echo ============================================================
echo.

:: Create Timestamp
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set TIMESTAMP=%%i

set BACKUP_DIR=Backup\%TIMESTAMP%

echo Creating Backup Folder...
mkdir "%BACKUP_DIR%"

echo.

:: -----------------------------
:: Resume
:: -----------------------------
echo [1/5] Backup Resume...

if exist Resume (
    xcopy Resume "%BACKUP_DIR%\Resume\" /E /I /Y >nul
    echo Resume Backup Completed
) else (
    echo Resume Folder Not Found
)

echo.

:: -----------------------------
:: Chrome Profile
:: -----------------------------
echo [2/5] Backup Chrome Profile...

if exist ChromeProfile (
    xcopy ChromeProfile "%BACKUP_DIR%\ChromeProfile\" /E /I /Y >nul
    echo Chrome Profile Backup Completed
) else (
    echo Chrome Profile Not Found
)

echo.

:: -----------------------------
:: .env
:: -----------------------------
echo [3/5] Backup .env...

if exist .env (
    copy .env "%BACKUP_DIR%" >nul
    echo .env Backup Completed
) else (
    echo .env File Not Found
)

echo.

:: -----------------------------
:: Cookies
:: -----------------------------
echo [4/5] Backup Cookies...

if exist cookies.pkl (
    copy cookies.pkl "%BACKUP_DIR%" >nul
    echo Cookies Backup Completed
) else (
    echo cookies.pkl Not Found
)

echo.

:: -----------------------------
:: Logs
:: -----------------------------
echo [5/5] Backup Logs...

if exist Logs (
    xcopy Logs "%BACKUP_DIR%\Logs\" /E /I /Y >nul
    echo Logs Backup Completed
) else (
    echo Logs Folder Not Found
)

echo.
echo ============================================================
echo Backup Completed Successfully
echo Backup Location:
echo %CD%\%BACKUP_DIR%
echo ============================================================

pause