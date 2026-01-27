"""
Script para limpiar todos los ingredientes de los productos
"""
import json
import os

def limpiar_ingredientes():
    """Elimina todos los ingredientes de todos los productos"""
    ruta_productos = os.path.join('data', 'productos.json')
    
    # Cargar productos
    with open(ruta_productos, 'r', encoding='utf-8') as f:
        productos_data = json.load(f)
    
    productos_limpiados = 0
    
    # Recorrer todas las categorías y productos
    for categoria in productos_data.get("categorias", []):
        for producto in categoria.get("productos", []):
            if "ingredientes" in producto:
                del producto["ingredientes"]
                productos_limpiados += 1
                print(f"  - Limpiado: {producto.get('nombre', 'Sin nombre')}")
    
    # Guardar productos actualizados
    with open(ruta_productos, 'w', encoding='utf-8') as f:
        json.dump(productos_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nTotal: {productos_limpiados} productos limpiados")
    print("Todos los ingredientes han sido eliminados de los productos")

if __name__ == "__main__":
    limpiar_ingredientes()
