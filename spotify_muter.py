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

# --- LÓGICA DE DETECCIÓN MEJORADA ---

def get_spotify_info():
    """Busca la ventana de Spotify y extrae su título y si está emitiendo audio."""
    spotify_windows = []
    
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
        
    win32gui.EnumWindows(callback, spotify_windows)
    
    # Filtramos títulos inútiles
    titulos_limpios = [t for t in spotify_windows if t not in ["", "Spotify", "Spotify Free", "Spotify Premium", "Advertisement", "Anuncio"]]
    
    # Si no hay títulos limpios, es un anuncio fijo (o está pausado)
    if not titulos_limpios:
        return "Anuncio"
        
    # Spotify suele poner el título de la canción en la ventana principal.
    # Buscamos el que tenga el formato "Artista - Canción"
    for t in titulos_limpios:
        # Regex mejorada para detectar guiones normales, largos y cortos
        if re.search(r".+ [\-\u2010\u2011\u2012\u2013\u2014\u2015] .+", t):
            return t
            
    # Si hay un título pero no tiene guion (como "SUDHGFB MOTOR"), 
    # y Spotify está en la lista de ventanas, lo tratamos como anuncio.
    return "Anuncio"

def set_spotify_mute(mute_state):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == "spotify.exe":
                volume = session.SimpleAudioVolume
                if volume.GetMute() != mute_state:
                    volume.SetMute(mute_state, None)
    except: pass

# --- CONTROL DEL ICONO Y BUCLE ---

running = True

def main_loop(icon):
    global running
    is_muted = False
    
    while running:
        try:
            title = get_spotify_info()
            
            # LÓGICA DEFINITIVA:
            # Si el título es "Anuncio" o "Spotify" o no tiene el formato "Artista - Canción" -> MUTE
            es_musica = re.search(r".+ [\-\u2010\u2011\u2012\u2013\u2014\u2015] .+", title)
            
            # Si NO es música clara, es anuncio.
            if not es_musica:
                if not is_muted:
                    set_spotify_mute(1)
                    is_muted = True
            else:
                # Es música, quitamos el mute
                if is_muted:
                    set_spotify_mute(0)
                    is_muted = False
                    
        except Exception as e:
            pass
        time.sleep(1.0) # Bajamos a 1 segundo para ser más rápidos

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

icon = pystray.Icon("SpotifyMuter", create_image(), "Spotify Ad Muter Activo", menu=pystray.Menu(
    item('Salir', quit_action)
))

# Ocultar consola
hWnd = ctypes.windll.kernel32.GetConsoleWindow()
if hWnd: ctypes.windll.user32.ShowWindow(hWnd, 0)

thread = threading.Thread(target=main_loop, args=(icon,))
thread.daemon = True
thread.start()

icon.run()
