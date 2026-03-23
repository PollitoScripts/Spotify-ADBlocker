@echo off
title Instalador de Spotify Muter
echo === Instalando librerias de Python ===
pip install -r requirements.txt

echo.
echo === Verificando Componentes de Windows ===
echo Si el programa no abre, instala el siguiente componente de Microsoft:
start https://aka.ms/vs/17/release/vc_redist.x64.exe

echo.
echo === TODO LISTO ===
echo Ya puedes ejecutar spotify_muter.py o el .exe
pause
