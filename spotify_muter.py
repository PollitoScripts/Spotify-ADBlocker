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

# --- LÓGICA DE DETECCIÓN POR FORMATO "A - B" ---

def is_spotify_playing_music():
    """
    Revisa todas las ventanas de Spotify. 
    Si encuentra al menos UNA que tenga el formato 'Artista - Canción', devuelve True.
    """
    found_music = False
    
    def callback(hwnd, extra):
        nonlocal found_music
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                if "spotify" in proc.name().lower():
                    title = win32gui.GetWindowText(hwnd)
                    # La regla de oro: ¿Tiene el guion de separación?
                    if re.search(r".+ [\-\u2010\u2011\u2012\u2013\u2014\u2015] .+", title):
                        found_music = True
            except: pass
        return True

    win32gui.EnumWindows(callback, None)
    return found_music

def set_spotify_mute(mute_state):
    """Muteo total para atravesar SteelSeries Sonar."""
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and "spotify" in session.Process.name().lower():
                # 1. Muteo estándar
                session.SimpleAudioVolume.SetMute(mute_state, None)
                # 2. Muteo de volumen maestro (para asegurar en Sonar)
                vol = 0.0 if mute_state == 1 else 1.0
                session.SimpleAudioVolume.SetMasterVolume(vol, None)
    except: pass

# --- CONTROL Y BUCLE ---

running = True

def main_loop(icon):
    global running
    is_muted = False
    while running:
        try:
            # Si NO hay música con formato "A - B", entonces es un anuncio
            if not is_spotify_playing_music():
                if not is_muted:
                    set_spotify_mute(1)
                    is_muted = True
            else:
                # Si hay formato "A - B", es música, quitamos mute
                if is_muted:
                    set_spotify_mute(0)
                    is_muted = False
        except: pass
        time.sleep(0.7) # Un poco más rápido para no oír ni el "Hola" del anuncio

def quit_action(icon, item):
    global running
    running = False
    set_spotify_mute(0)
    icon.stop()

def create_image():
    image = Image.new('RGB', (64, 64), color=(30, 215, 96))
    d = ImageDraw.Draw(image)
    d.ellipse((15, 15, 49, 49), fill=(0, 0, 0))
    return image

icon = pystray.Icon("SpotifyMuter", create_image(), "Pollito Muter (Vigilando)", menu=pystray.Menu(
    item('Salir', quit_action)
))

# Ocultar consola
hWnd = ctypes.windll.kernel32.GetConsoleWindow()
if hWnd: ctypes.windll.user32.ShowWindow(hWnd, 0)

thread = threading.Thread(target=main_loop, args=(icon,))
thread.daemon = True
thread.start()

icon.run()
