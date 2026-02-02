"""
Módulo para gestión de imágenes de productos e ingredientes
Maneja carga, guardado, redimensionamiento y eliminación de imágenes
"""
import os
import shutil
from PIL import Image, ImageTk


# Formatos de imagen permitidos
FORMATOS_PERMITIDOS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']


def obtener_ruta_imagenes():
    """Obtiene la ruta de la carpeta de imágenes"""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'imagenes'
    )


def obtener_ruta_imagenes_productos():
    """Obtiene la ruta de la carpeta de imágenes de productos"""
    ruta = os.path.join(obtener_ruta_imagenes(), 'productos')
    os.makedirs(ruta, exist_ok=True)
    return ruta


def obtener_ruta_imagenes_ingredientes():
    """Obtiene la ruta de la carpeta de imágenes de ingredientes"""
    ruta = os.path.join(obtener_ruta_imagenes(), 'ingredientes')
    os.makedirs(ruta, exist_ok=True)
    return ruta


def validar_formato_imagen(ruta_archivo):
    """Valida que el archivo sea una imagen con formato permitido"""
    if not os.path.exists(ruta_archivo):
        return False
    
    extension = os.path.splitext(ruta_archivo)[1].lower()
    return extension in FORMATOS_PERMITIDOS


def guardar_imagen_producto(ruta_origen, producto_id):
    """
    Guarda una imagen para un producto
    
    Args:
        ruta_origen: Ruta del archivo de imagen original
        producto_id: ID del producto
    
    Returns:
        str: Ruta relativa de la imagen guardada (ej: "productos/producto_1.jpg")
    """
    if not validar_formato_imagen(ruta_origen):
        raise ValueError("Formato de imagen no permitido")
    
    # Obtener extensión del archivo original
    extension = os.path.splitext(ruta_origen)[1].lower()
    
    # Nombre del archivo destino
    nombre_archivo = f"producto_{producto_id}{extension}"
    ruta_destino = os.path.join(obtener_ruta_imagenes_productos(), nombre_archivo)
    
    # Copiar archivo
    shutil.copy2(ruta_origen, ruta_destino)
    
    # Retornar ruta relativa para guardar en JSON
    return f"productos/{nombre_archivo}"


def guardar_imagen_ingrediente(ruta_origen, ingrediente_id):
    """
    Guarda una imagen para un ingrediente
    
    Args:
        ruta_origen: Ruta del archivo de imagen original
        ingrediente_id: ID del ingrediente
    
    Returns:
        str: Ruta relativa de la imagen guardada (ej: "ingredientes/ingrediente_1.jpg")
    """
    if not validar_formato_imagen(ruta_origen):
        raise ValueError("Formato de imagen no permitido")
    
    # Obtener extensión del archivo original
    extension = os.path.splitext(ruta_origen)[1].lower()
    
    # Nombre del archivo destino
    nombre_archivo = f"ingrediente_{ingrediente_id}{extension}"
    ruta_destino = os.path.join(obtener_ruta_imagenes_ingredientes(), nombre_archivo)
    
    # Copiar archivo
    shutil.copy2(ruta_origen, ruta_destino)
    
    # Retornar ruta relativa para guardar en JSON
    return f"ingredientes/{nombre_archivo}"


def obtener_ruta_completa_imagen(ruta_relativa):
    """
    Obtiene la ruta completa de una imagen desde su ruta relativa
    
    Args:
        ruta_relativa: Ruta relativa guardada en JSON (ej: "productos/producto_1.jpg")
    
    Returns:
        str: Ruta completa del archivo o None si no existe
    """
    if not ruta_relativa:
        return None
    
    ruta_completa = os.path.join(obtener_ruta_imagenes(), ruta_relativa)
    if os.path.exists(ruta_completa):
        return ruta_completa
    return None


def eliminar_imagen(ruta_relativa):
    """
    Elimina una imagen del sistema de archivos
    
    Args:
        ruta_relativa: Ruta relativa de la imagen (ej: "productos/producto_1.jpg")
    """
    if not ruta_relativa:
        return
    
    ruta_completa = obtener_ruta_completa_imagen(ruta_relativa)
    if ruta_completa and os.path.exists(ruta_completa):
        try:
            os.remove(ruta_completa)
        except Exception:
            pass  # Ignorar errores al eliminar


def redimensionar_imagen(ruta_imagen, ancho, alto):
    """
    Redimensiona una imagen manteniendo su aspecto
    
    Args:
        ruta_imagen: Ruta completa de la imagen
        ancho: Ancho deseado en píxeles
        alto: Alto deseado en píxeles
    
    Returns:
        PIL.Image: Imagen redimensionada
    """
    if not os.path.exists(ruta_imagen):
        return None
    
    try:
        imagen = Image.open(ruta_imagen)
        # Redimensionar manteniendo aspecto
        imagen.thumbnail((ancho, alto), Image.Resampling.LANCZOS)
        return imagen
    except Exception:
        return None


def cargar_imagen_tkinter(ruta_imagen, ancho=None, alto=None):
    """
    Carga una imagen para usar en Tkinter
    
    Args:
        ruta_imagen: Ruta completa o relativa de la imagen
        ancho: Ancho deseado (opcional)
        alto: Alto deseado (opcional)
    
    Returns:
        ImageTk.PhotoImage: Imagen lista para usar en Tkinter o None si hay error
    """
    # Si es ruta relativa, obtener ruta completa
    if not os.path.isabs(ruta_imagen):
        ruta_imagen = obtener_ruta_completa_imagen(ruta_imagen)
    
    if not ruta_imagen or not os.path.exists(ruta_imagen):
        return None
    
    try:
        if ancho and alto:
            imagen = redimensionar_imagen(ruta_imagen, ancho, alto)
            if imagen:
                return ImageTk.PhotoImage(imagen)
        else:
            imagen = Image.open(ruta_imagen)
            return ImageTk.PhotoImage(imagen)
    except Exception:
        return None
