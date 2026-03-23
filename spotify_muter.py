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

# --- LÓGICA DE DETECCIÓN ULTRA-AGRESIVA ---

def get_spotify_info():
    """Detecta si hay un anuncio basado en el título de la ventana."""
    titles = []
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                if "spotify" in proc.name().lower():
                    text = win32gui.GetWindowText(hwnd)
                    if text: hwnds.append(text)
            except: pass
        return True
    
    win32gui.EnumWindows(callback, titles)
    
    # Palabras clave que SIEMPRE son anuncios
    blacklist = ["spotify", "anuncio", "advertisement", "escucha música sin anuncios", "spotify free", "spotify premium"]
    
    for t in titles:
        t_lower = t.lower()
        # 1. Si el título está en la lista negra, es anuncio.
        if any(bad_word in t_lower for bad_word in blacklist):
            return "Anuncio"
        # 2. Si tiene el formato "Artista - Canción", es MÚSICA.
        if re.search(r".+ [\-\u2010\u2011\u2012\u2013\u2014\u2015] .+", t):
            return t
            
    # Si llegamos aquí y hay una ventana de Spotify pero no parece música clara, muteamos por si acaso.
    return "Anuncio" if titles else "Nada"

def set_spotify_mute(mute_state):
    """Mutea Spotify buscando en todas las tarjetas de sonido (ideal para Sonar/SteelSeries)."""
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            # Buscamos por nombre de proceso o por el identificador de la sesión
            if session.Process and "spotify" in session.Process.name().lower():
                session.SimpleAudioVolume.SetMute(mute_state, None)
    except: pass

# --- CONTROL Y BUCLE ---

running = True

def main_loop(icon):
    global running
    is_muted = False
    while running:
        try:
            info = get_spotify_info()
            
            # Si el título indica anuncio o no detectamos música clara...
            if info == "Anuncio":
                if not is_muted:
                    set_spotify_mute(1)
                    is_muted = True
            elif info != "Nada":
                # Si detectamos música (título con guion), desmuteamos.
                if is_muted:
                    set_spotify_mute(0)
                    is_muted = False
        except: pass
        time.sleep(0.8) # Más rápido para que el anuncio no suene nada

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

icon = pystray.Icon("SpotifyMuter", create_image(), "Pollito Muter Activo", menu=pystray.Menu(
    item('Salir', quit_action)
))

# Ocultar la consola negra al arrancar
hWnd = ctypes.windll.kernel32.GetConsoleWindow()
if hWnd: ctypes.windll.user32.ShowWindow(hWnd, 0)

thread = threading.Thread(target=main_loop, args=(icon,))
thread.daemon = True
thread.start()

icon.run()
