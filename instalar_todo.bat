@echo off
title Lanzador Maestro Spotify Muter
:: 1. Localizamos el ejecutable real de Python (saltando el Launcher)
set PY_PATH=%LocalAppData%\Programs\Python\Python314\python.exe

echo === REVISANDO LIBRERIAS ===
"%PY_PATH%" -m pip install pycaw psutil pystray Pillow pywin32 comtypes --quiet

echo.
echo === ARRANCANDO SCRIPT ===
:: Ejecutamos directamente con el motor de Python
"%PY_PATH%" spotify_muter.py

echo.
echo Si ves esto, el script se ha cerrado. Error detectado:
pause
