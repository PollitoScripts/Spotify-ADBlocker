import ctypes
import time
import threading
import win32gui
import win32process
import psutil
import unicodedata
import pythoncom # <--- NUEVA IMPORTACIÓN
from pycaw.pycaw import AudioUtilities
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item

def eliminar_tildes(texto):
    return "".join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn').lower()

def get_spotify_status():
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
    
    if not titles: return "Inactivo"

    blacklist = [
        "gillette", "escuchar musica", "escucha musica", "sin anuncios", 
        "anuncio", "advertisement", "spotify free", "spotify premium",
        "video ad", "sponsored", "patrocinado", "disfruta", "spotify"
    ]

    es_anuncio = False
    tiene_formato_musica = False
    
    # Imprimimos solo si hay cambio o algo relevante para no saturar
    for t in titles:
        t_limpio = eliminar_tildes(t).strip()
        if t_limpio == "spotify" or any(bad in t_limpio for bad in blacklist):
            es_anuncio = True
            break
        if " - " in t or " – " in t:
            tiene_formato_musica = True

    if es_anuncio: return "Anuncio"
    if tiene_formato_musica: return "Musica"
    return "Anuncio"

def set_spotify_mute(mute_state):
    """Barre todas las sesiones de audio y silencia Spotify"""
    try:
        # CRUCIAL: Inicializar COM para este hilo
        pythoncom.CoInitialize()
        
        sessions = AudioUtilities.GetAllSessions()
        found = False
        for session in sessions:
            name = ""
            if session.Process:
                name = session.Process.name().lower()
            
            if "spotify" in name or "spotify" in session.Identifier.lower():
                volume = session.SimpleAudioVolume
                volume.SetMute(mute_state, None)
                level = 0.0 if mute_state else 1.0
                volume.SetMasterVolume(level, None)
                found = True
        
        # Opcional: Liberar COM
        # pythoncom.CoUninitialize() 
    except Exception as e:
        print(f"⚠️ Error en muteo: {e}")

running = True

def main_loop(icon):
    global running
    last_status = None
    
    print("🔍 Buscando anuncios de Spotify...")
    
    while running:
        status = get_spotify_status()
        
        if status != last_status:
            if status == "Anuncio":
                print("🚩 ANUNCIO DETECTADO -> 🔇 MUTE")
                set_spotify_mute(True)
            else:
                print("🎵 MÚSICA DETECTADA -> 🔊 UNMUTE")
                set_spotify_mute(False)
            last_status = status
            
        # Refuerzo constante si es anuncio
        if status == "Anuncio":
            set_spotify_mute(True)
            
        time.sleep(0.8)

def quit_action(icon, item):
    global running
    running = False
    # Intentar desmutear antes de salir
    try:
        pythoncom.CoInitialize()
        set_spotify_mute(False)
    except: pass
    icon.stop()

def create_image():
    image = Image.new('RGB', (64, 64), color=(30, 215, 96))
    d = ImageDraw.Draw(image)
    d.ellipse((10, 10, 54, 54), fill=(0, 0, 0))
    return image

icon = pystray.Icon("SpotifyMuter", create_image(), "Spotify Muter v7 By Pollito", 
                    menu=pystray.Menu(item('Cerrar', quit_action)))

thread = threading.Thread(target=main_loop, args=(icon,))
thread.daemon = True
thread.start()

icon.run()
