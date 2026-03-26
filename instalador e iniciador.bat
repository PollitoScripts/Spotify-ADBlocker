@echo off
title Spotify Muter v7 By Pollito
setlocal enabledelayedexpansion

echo ===========================================
echo    SPOTIFY MUTER v7 - BY POLLITO
echo ===========================================
echo.

:: Intentar encontrar el ejecutable real de Python ignorando la Windows Store
set PY_PATH=
for /f "delims=" %%i in ('where python') do (
    set "test_path=%%i"
    :: Si la ruta NO contiene "WindowsApps", es el Python real
    echo !test_path! | findstr /i /v "WindowsApps" >nul
    if !errorlevel! equ 0 (
        set "PY_PATH=!test_path!"
        goto :found
    )
)

:found
if "%PY_PATH%"=="" (
    :: Si no encontro 'python', intentamos con 'py' (Python Launcher)
    where py >nul 2>nul
    if !errorlevel! equ 0 (
        set PY_PATH=py
    ) else (
        echo [ERROR] No se encontro una instalacion valida de Python.
        echo Asegurate de marcar "Add Python to PATH" al instalarlo.
        pause
        exit
    )
)

echo [OK] Python detectado en: "%PY_PATH%"

echo.
echo ===========================================
echo    REVISANDO DEPENDENCIAS...
echo ===========================================
"%PY_PATH%" -m pip install pywin32 psutil pycaw pillow pystray --quiet

echo.
echo ===========================================
echo    ARRANCANDO SPOTIFY MUTER...
echo ===========================================
echo.

:: Ejecutamos el script
"%PY_PATH%" spotify_muter.py

if %errorlevel% neq 0 (
    echo.
    echo [ALERTA] El script se detuvo. 
    echo Asegurate de que el archivo se llame "spotify_muter.py"
    pause
)
