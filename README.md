Markdown
# 🎵 Spotify Ad-Muter (Lite Edition) 🐥

Un script inteligente para Windows que detecta anuncios de Spotify y los silencia automáticamente, manteniendo el resto de tus sonidos (Discord, juegos, etc.) intactos.

## ✨ Características
* **Silencio Selectivo:** Solo afecta a `Spotify.exe`.
* **Modo Invisible:** Se ejecuta en la bandeja del sistema (junto al reloj).
* **Sin Dependencias de Imagen:** El icono se genera por código, evitando errores de rutas de archivos.

## 🚀 Guía de Instalación Rápida

Si el programa no abre o da errores, sigue estos pasos en orden:

### 1. Preparar el Sistema (Obligatorio)
Muchos errores se deben a la falta de componentes de Windows. Instala el siguiente paquete oficial de Microsoft:
* 🔗 [Descargar Visual C++ Redistributable X64](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### 2. Instalación Automática
He incluido un archivo llamado `instalar_todo.bat`. 
1. Haz clic derecho sobre `instalar_todo.bat`.
2. Selecciona **Ejecutar como administrador**.
3. Esto instalará todas las librerías necesarias (`psutil`, `pycaw`, `pystray`, etc.) automáticamente.

## 📂 Contenido del Repositorio
* `spotify_muter.py`: El código fuente principal.
* `spotify_muter.exe`: Ejecutable listo para usar (sin consola).
* `requirements.txt`: Lista de librerías de Python necesarias.
* `instalar_todo.bat`: Script de automatización para preparar el PC.

## 🛠️ Cómo ejecutar el programa
* **Doble clic en `spotify_muter.exe`**: Se abrirá directamente en la bandeja del sistema.
* **Desde la consola**: Si quieres ver qué ocurre, usa `python spotify_muter.py`.

> **Nota Importante:** Algunos antivirus pueden detectar el `.exe` como falso positivo. Si ocurre, añade el archivo a la lista de **Exclusiones** de tu antivirus o Windows Defender.

---
*Proyecto creado para uso personal. No oficial de Spotify.*
