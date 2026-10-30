@echo off
chcp 65001 >nul
title Text Extractor Launcher
color 07

:: Change directory to the folder where this .bat file is located
cd /d "%~dp0"

:ASK_PATH
cls
echo Enter the folder path you want to scan (or drag ^& drop it here):
echo Type "q" to quit.
set /p "USER_PATH=Path: "

:: Exit if user types q
if /i "%USER_PATH%"=="q" exit /b

:: Remove quotes if the path was dragged and dropped
set USER_PATH=%USER_PATH:"=%

:: Check if path is empty
if "%USER_PATH%"=="" (
    echo [ERROR] Path cannot be empty. Try again.
    timeout /t 2 >nul
    goto ASK_PATH
)

:: Check if the folder exists
if not exist "%USER_PATH%\" (
    echo [ERROR] The specified path does not exist. Try again.
    timeout /t 2 >nul
    goto ASK_PATH
)

echo.

:: Run Python script
python extractor.py "%USER_PATH%"

echo.
echo -------------------------------------------------------
if %errorlevel% neq 0 (
    echo [ERROR] Script finished with an error.
)

echo.
echo Press any key to scan another folder...
pause >nul
goto ASK_PATH