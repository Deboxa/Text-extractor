@echo off
chcp 65001 >nul
title Text Extractor Launcher
color 07

:: Переход в папку, где лежит этот .bat файл
cd /d "%~dp0"

:ASK_PATH
echo Enter the folder path you want to scan (or drag ^& drop it here):
set /p "USER_PATH=Path: "

:: Убираем кавычки, если путь был перетащен мышкой
set USER_PATH=%USER_PATH:"=%

:: Проверка, что путь не пустой
if "%USER_PATH%"=="" (
    echo [ERROR] Path cannot be empty. Try again.
    echo.
    goto ASK_PATH
)

:: Проверка, что папка существует
if not exist "%USER_PATH%\" (
    echo [ERROR] The specified path does not exist. Try again.
    echo.
    goto ASK_PATH
)

echo.

:: Запуск Python скрипта
python extractor.py "%USER_PATH%"

echo.
echo -------------------------------------------------------
if %errorlevel% neq 0 (
    echo [ERROR] Script finished with an error.
)

echo Press any key to close this window...
pause >nul