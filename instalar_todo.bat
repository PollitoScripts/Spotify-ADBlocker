@echo off
title Spotify Muter v7 By Pollito
echo ===========================================
echo    SPOTIFY MUTER v7 - BY POLLITO
echo ===========================================
setlocal

:: 1. Intentar localizar Python (ajusta la versión 314 si es necesario)
set PY_PATH=%LocalAppData%\Programs\Python\Python314\python.exe

:: Verificación de seguridad por si la ruta cambió
if not exist "%PY_PATH%" (
    echo [ERROR] No se encontro Python en %PY_PATH%
    echo Intentando comando 'python' global...
    set PY_PATH=python
)

echo ===========================================
echo    REVISANDO DEPENDENCIAS (v7)
echo ===========================================
:: Añadimos 'pywin32' que es el que trae 'pythoncom'
"%PY_PATH%" -m pip install pycaw psutil pystray Pillow pywin32 --quiet

echo.
echo ===========================================
echo    ARRANCANDO SPOTIFY MUTER...
echo    (No cierres esta ventana)
echo ===========================================
echo.

:: Ejecutamos el script. 
:: Nota: Asegurate de que el archivo se llame 'spotify_muter.py'
"%PY_PATH%" spotify_muter.py

echo.
if %errorlevel% neq 0 (
    echo [ALERTA] El script se detuvo con un error.
) else (
    echo [INFO] Script cerrado manualmente.
)

pause
