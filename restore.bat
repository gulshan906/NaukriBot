@echo off
setlocal
cd /d "%~dp0"

title NaukriBot Restore Utility v2.0
color 0A

echo ============================================================
echo             NAUKRIBOT RESTORE v2.0
echo ============================================================
echo.

:: ---------------------------------------------------------
:: Find Latest Backup
:: ---------------------------------------------------------

set "LATEST="

for /f "delims=" %%i in ('dir /ad /b /o-d Backup') do (
    set "LATEST=%%i"
    goto :FOUND
)

:FOUND

if "%LATEST%"=="" (
    color 0C
    echo ERROR : No Backup Found.
    pause
    exit /b
)

echo Latest Backup Found:
echo.
echo %LATEST%
echo.

choice /C YN /M "Restore this backup"

if errorlevel 2 exit /b

set BACKUP=Backup\%LATEST%

echo.
echo Starting Restore...
echo.

:: =========================================================
:: Resume
:: =========================================================

echo [1/5] Resume

if exist "%BACKUP%\Resume" (

    xcopy "%BACKUP%\Resume" "Resume\" /E /I /Y >nul

    echo PASS

) else (

    echo SKIPPED

)

echo.

:: =========================================================
:: Chrome Profile
:: =========================================================

echo [2/5] Chrome Profile

if exist "%BACKUP%\ChromeProfile" (

    xcopy "%BACKUP%\ChromeProfile" "ChromeProfile\" /E /I /Y >nul

    echo PASS

) else (

    echo SKIPPED

)

echo.

:: =========================================================
:: .env
:: =========================================================

echo [3/5] Environment

if exist "%BACKUP%\.env" (

    copy "%BACKUP%\.env" ".env" >nul

    echo PASS

) else (

    echo SKIPPED

)

echo.

:: =========================================================
:: Cookies
:: =========================================================

echo [4/5] Cookies

if exist "%BACKUP%\cookies.pkl" (

    copy "%BACKUP%\cookies.pkl" "." >nul

    echo PASS

) else (

    echo SKIPPED

)

echo.

:: =========================================================
:: Logs
:: =========================================================

echo [5/5] Logs

if exist "%BACKUP%\Logs" (

    xcopy "%BACKUP%\Logs" "Logs\" /E /I /Y >nul

    echo PASS

) else (

    echo SKIPPED

)

echo.

echo ============================================================
echo              RESTORE FINISHED
echo ============================================================

echo.
echo Backup Used :
echo %LATEST%

echo.
pause