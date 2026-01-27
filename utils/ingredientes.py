"""
Módulo para gestión de ingredientes en el archivo JSON
Maneja operaciones CRUD de ingredientes y su asignación a categorías
"""
import json
import os


def obtener_ruta_json():
    """Obtiene la ruta del archivo JSON de ingredientes"""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'ingredientes.json'
    )


def cargar_ingredientes():
    """Carga los ingredientes desde el archivo JSON"""
    ruta = obtener_ruta_json()
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Crear estructura inicial
        data = {"ingredientes": []}
        guardar_ingredientes(data)
        return data
    except json.JSONDecodeError:
        print("Error: El archivo ingredientes.json no es válido. Se creará uno nuevo.")
        data = {"ingredientes": []}
        guardar_ingredientes(data)
        return data


def guardar_ingredientes(data):
    """Guarda los ingredientes en el archivo JSON"""
    ruta = obtener_ruta_json()
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def obtener_siguiente_id():
    """Obtiene el siguiente ID disponible para un nuevo ingrediente"""
    data = cargar_ingredientes()
    max_id = 0
    
    for ingrediente in data.get("ingredientes", []):
        if ingrediente.get("id", 0) > max_id:
            max_id = ingrediente.get("id", 0)
    
    return max_id + 1


def obtener_todos_los_ingredientes():
    """Obtiene todos los ingredientes"""
    data = cargar_ingredientes()
    return data.get("ingredientes", [])


def buscar_ingrediente_por_id(ingrediente_id):
    """Busca un ingrediente por su ID"""
    data = cargar_ingredientes()
    
    for ingrediente in data.get("ingredientes", []):
        if ingrediente.get("id") == ingrediente_id:
            return ingrediente
    
    return None


def agregar_ingrediente(nombre, categorias, precio_extra, precio_resta):
    """Agrega un nuevo ingrediente"""
    data = cargar_ingredientes()
    
    nuevo_ingrediente = {
        "id": obtener_siguiente_id(),
        "nombre": nombre,
        "categorias": categorias if isinstance(categorias, list) else [categorias],
        "precio_extra": float(precio_extra),
        "precio_resta": float(precio_resta)
    }
    
    data.setdefault("ingredientes", []).append(nuevo_ingrediente)
    guardar_ingredientes(data)
    return nuevo_ingrediente


def modificar_ingrediente(ingrediente_id, nombre, categorias, precio_extra, precio_resta):
    """Modifica un ingrediente existente"""
    data = cargar_ingredientes()
    
    for ingrediente in data.get("ingredientes", []):
        if ingrediente.get("id") == ingrediente_id:
            ingrediente["nombre"] = nombre
            ingrediente["categorias"] = categorias if isinstance(categorias, list) else [categorias]
            ingrediente["precio_extra"] = float(precio_extra)
            ingrediente["precio_resta"] = float(precio_resta)
            guardar_ingredientes(data)
            return True
    
    return False


def eliminar_ingrediente(ingrediente_id):
    """Elimina un ingrediente por su ID"""
    data = cargar_ingredientes()
    
    for idx, ingrediente in enumerate(data.get("ingredientes", [])):
        if ingrediente.get("id") == ingrediente_id:
            data["ingredientes"].pop(idx)
            guardar_ingredientes(data)
            return True
    
    return False


def obtener_ingredientes_por_categoria(categoria_nombre):
    """Obtiene todos los ingredientes disponibles para una categoría"""
    data = cargar_ingredientes()
    ingredientes = []
    
    for ingrediente in data.get("ingredientes", []):
        categorias = ingrediente.get("categorias", [])
        if categoria_nombre in categorias:
            ingredientes.append(ingrediente)
    
    return ingredientes
