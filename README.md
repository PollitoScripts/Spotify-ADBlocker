Markdown
# 🎵 Spotify Muter v7 (Anti-Ads)

Este script de Python detecta automáticamente cuando Spotify está reproduciendo un anuncio y silencia el proceso de audio de forma inteligente, restaurando el volumen en cuanto vuelve la música.

## ✨ Características
* **Detección por Título:** Analiza las ventanas activas para diferenciar entre canciones y publicidad.
* **Muteo Selectivo:** Usa `PyCaw` para silenciar solo a Spotify, sin afectar al resto del sistema.
* **Thread-Safe:** Corregido el error de `CoInitialize` mediante `pythoncom` para ejecución estable en hilos.
* **Icono en Bandeja:** Se ejecuta en segundo plano con un icono en la barra de tareas (System Tray).

## 🛠️ Requisitos previos

Antes de empezar, asegúrate de tener instalado **Python 3.10 o superior**. (Testeado en 3.14)

### Librerías necesarias
El script depende de las siguientes librerías de terceros:
* `pywin32` (Manejo de API de Windows y COM)
* `psutil` (Gestión de procesos)
* `pycaw` (Control de audio de Windows)
* `pillow` (Generación del icono)
* `pystray` (Menú en la barra de tareas)

## 🚀 Instalación y Uso

1. **Clona o descarga** este repositorio.
2. **Instala las dependencias** ejecutando el siguiente comando en tu terminal (En la ruta del script):
   ```bash
   pip install -r requirements.txt
Ejecuta el script:

Puedes usar el archivo .bat incluido para automatizar el arranque.

O directamente desde la terminal:

Bash
python spotify_muter.py
## 📂 Estructura del Proyecto
spotify_muter.py: El código principal del script.

requirements.txt: Lista de dependencias de Python.

lanzador.bat: Script de Windows para instalar dependencias y arrancar el muter con un clic.

## ⚙️ Configuración (Blacklist)
Si detectas un anuncio que el script no silencia, puedes añadir palabras clave en la lista blacklist dentro de la función get_spotify_status():

Python
blacklist = ["gillette", "escuchar musica", "escucha musica", "sin anuncios", "anuncio", "advertisement", "spotify free", "spotify premium", "video ad", "sponsored", "patrocinado", "disfruta", "spotify"]
## ⚠️ Notas importantes
Ejecución como Administrador: En algunas versiones de Windows, es necesario ejecutar el script (o el CMD/Terminal) como Administrador para que tenga permisos de modificar el volumen de otros procesos.

Spotify de la Microsoft Store: El script es compatible con la versión de escritorio clásica y la de la Store.

Creado con 🎧 por [Alejandro Tineo Morales/PollitoScripts]


---
