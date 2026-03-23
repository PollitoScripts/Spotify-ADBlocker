Markdown
# 🎵 Spotify Ad-Muter (Pollito Edition) 🐥

Un script inteligente y ligero para Windows que detecta automáticamente los anuncios de Spotify y los silencia en segundo plano, sin interrumpir el resto de tus sonidos (Discord, juegos, navegadores, etc.).

## ✨ Características

* **Silencio selectivo:** Solo mutea el proceso `Spotify.exe`. Tu música se detiene, pero tu charla en Discord sigue viva.
* **Detección por Título:** Utiliza expresiones regulares (Regex) para identificar anuncios, promociones y pausas, incluso con caracteres especiales o guiones largos.
* **Segundo Plano Total:** Se ejecuta en la bandeja del sistema (System Tray) con un icono personalizado.
* **Sin Foco:** No necesita que la ventana de Spotify esté activa ni visible.

## 🚀 Cómo usarlo

### Opción 1: Ejecutable (Recomendado para usuarios)
Si solo quieres que funcione sin instalar nada:
1. Descarga el archivo `spotify_muter.exe`.
2. Ejecútalo (requiere permisos de administrador para controlar el mezclador de sonido).
3. Busca el icono del **Pollito** en la barra de tareas (junto al reloj).
4. Para cerrar, haz clic derecho en el pollito y selecciona **Salir**.

### Opción 2: Desde el código fuente (Para desarrolladores)
Si prefieres ejecutar el archivo `.py`, necesitarás Python 3.10+ y las siguientes librerías:

```bash
pip install pycaw comtypes pygetwindow pystray Pillow psutil pywin32
Luego simplemente ejecuta:

Bash
python spotify_muter.py
🛠️ Cómo se construyó
El proyecto utiliza:

PyCaw: Para el control granular del volumen por procesos.

PyWin32: Para interceptar los títulos de las ventanas nativas de Windows.

PyStray: Para la interfaz en la bandeja del sistema.

Regex: Para filtrar los títulos que no siguen el patrón Artista - Canción.

📂 Estructura del Repositorio
spotify_muter.py: El código fuente documentado.

spotify_muter.exe: El ejecutable listo para usar.

pollito_discord_CON_MARCA_DE_AGUA.ico: El icono personalizado del proyecto.

Nota: Este proyecto es para uso personal y educativo. No está afiliado a Spotify.
