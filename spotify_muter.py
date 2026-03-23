import ctypes
import time
import re
import threading
import win32gui
import win32process
import psutil
from pycaw.pycaw import AudioUtilities
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

# --- LÓGICA DE DETECCIÓN (La que ya funciona) ---

def get_spotify_window_title():
    titles = []
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                if proc.name().lower() == "spotify.exe":
                    text = win32gui.GetWindowText(hwnd)
                    if text: hwnds.append(text)
            except: pass
        return True
    win32gui.EnumWindows(callback, titles)
    for t in titles:
        if re.search(r".+ [\-\u2013\u2014] .+", t): return t
    return titles[0] if titles else None

def set_spotify_mute(mute_state):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == "spotify.exe":
                session.SimpleAudioVolume.SetMute(mute_state, None)
    except: pass

# --- CONTROL DEL ICONO Y BUCLE ---

running = True

def main_loop(icon):
    global running
    is_muted = False
    while running:
        try:
            title = get_spotify_window_title()
            if title:
                es_musica = re.search(r".+ [\-\u2013\u2014] .+", title)
                titulos_ad = ["Spotify", "Spotify Free", "Spotify Premium", "Advertisement", "Anuncio"]
                es_anuncio = not es_musica or any(ad == title for ad in titulos_ad)

                if es_anuncio and not is_muted:
                    set_spotify_mute(1)
                    is_muted = True
                elif not es_anuncio and is_muted:
                    set_spotify_mute(0)
                    is_muted = False
        except: pass
        time.sleep(1.5)

def quit_action(icon, item):
    global running
    running = False
    set_spotify_mute(0) # Asegurar que queda desmuteado al salir
    icon.stop()

# Crear un icono simple (un cuadrado verde)
def create_image():
    image = Image.new('RGB', (64, 64), color=(30, 215, 96)) # Color Spotify
    d = ImageDraw.Draw(image)
    d.ellipse((10, 10, 54, 54), fill=(0, 0, 0)) # Un círculo negro dentro
    return image

# Configurar el menú del icono
icon = pystray.Icon("SpotifyMuter", create_image(), "Spotify Ad Muter", menu=pystray.Menu(
    item('Salir', quit_action)
))

# Ocultar consola al inicio
hWnd = ctypes.windll.kernel32.GetConsoleWindow()
if hWnd: ctypes.windll.user32.ShowWindow(hWnd, 0)

# Ejecutar el bucle de detección en un hilo separado
thread = threading.Thread(target=main_loop, args=(icon,))
thread.daemon = True
thread.start()

# Ejecutar el icono
icon.run()
