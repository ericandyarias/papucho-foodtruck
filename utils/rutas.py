"""
Módulo para obtener rutas correctas de archivos
Funciona tanto en desarrollo como en ejecutable empaquetado
Usa AppData del usuario para archivos modificables cuando está instalado
"""
import os
import sys


def obtener_ruta_base():
    """
    Obtiene la ruta base de la aplicación.
    Funciona tanto en desarrollo como cuando está empaquetado con PyInstaller.
    
    Returns:
        str: Ruta base de la aplicación
    """
    # Si estamos ejecutando desde un ejecutable empaquetado (PyInstaller)
    if getattr(sys, 'frozen', False):
        # sys.executable apunta al .exe
        # La carpeta base es el directorio donde está el .exe
        return os.path.dirname(sys.executable)
    else:
        # En desarrollo, la carpeta base es el directorio raíz del proyecto
        # (dos niveles arriba desde utils/)
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def obtener_ruta_appdata():
    """
    Obtiene la ruta de AppData del usuario para archivos modificables.
    Solo se usa cuando la aplicación está instalada (empaquetada).
    
    Returns:
        str: Ruta completa de AppData\Papucho Foodtruck
    """
    appdata = os.getenv('APPDATA')
    if not appdata:
        # Fallback si APPDATA no está definido
        appdata = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
    
    ruta_appdata = os.path.join(appdata, 'Papucho Foodtruck')
    # Crear la carpeta si no existe
    os.makedirs(ruta_appdata, exist_ok=True)
    return ruta_appdata


def obtener_ruta_data():
    """
    Obtiene la ruta de la carpeta data.
    En desarrollo usa la carpeta del proyecto.
    Cuando está instalado, usa AppData para archivos modificables.
    
    Returns:
        str: Ruta completa de la carpeta data
    """
    # Si está empaquetado, usar AppData para archivos modificables
    if getattr(sys, 'frozen', False):
        return obtener_ruta_appdata()
    else:
        # En desarrollo, usar la carpeta del proyecto
        return os.path.join(obtener_ruta_base(), 'data')


def obtener_ruta_data_instalacion():
    """
    Obtiene la ruta de la carpeta data en la instalación (solo lectura).
    Se usa para leer archivos iniciales como imágenes.
    
    Returns:
        str: Ruta completa de la carpeta data en la instalación
    """
    return os.path.join(obtener_ruta_base(), 'data')


def obtener_ruta_json(nombre_archivo):
    """
    Obtiene la ruta de un archivo JSON.
    Cuando está instalado, los JSON se guardan en AppData (modificables).
    En desarrollo, se guardan en la carpeta data del proyecto.
    
    Args:
        nombre_archivo: Nombre del archivo JSON (ej: 'productos.json', 'ingredientes.json')
    
    Returns:
        str: Ruta completa del archivo JSON
    """
    ruta_data = obtener_ruta_data()
    ruta_json = os.path.join(ruta_data, nombre_archivo)
    
    # Si está instalado y el archivo no existe en AppData, copiarlo desde la instalación
    if getattr(sys, 'frozen', False):
        ruta_instalacion = obtener_ruta_data_instalacion()
        ruta_json_instalacion = os.path.join(ruta_instalacion, nombre_archivo)
        
        # Si el archivo no existe en AppData pero sí en la instalación, copiarlo
        if not os.path.exists(ruta_json) and os.path.exists(ruta_json_instalacion):
            import shutil
            try:
                shutil.copy2(ruta_json_instalacion, ruta_json)
            except Exception:
                pass  # Si falla la copia, continuar de todas formas
    
    return ruta_json
