"""
Script para asignar ingredientes a productos de ejemplo
Este script muestra cómo agregar ingredientes a productos
"""
import json
import os

def asignar_ingredientes_ejemplo():
    """Asigna ingredientes de ejemplo a la Hamburguesa Completa"""
    ruta_productos = os.path.join('data', 'productos.json')
    ruta_ingredientes = os.path.join('data', 'ingredientes.json')
    
    # Cargar productos
    with open(ruta_productos, 'r', encoding='utf-8') as f:
        productos_data = json.load(f)
    
    # Cargar ingredientes
    with open(ruta_ingredientes, 'r', encoding='utf-8') as f:
        ingredientes_data = json.load(f)
    
    # Buscar Hamburguesa Completa (id: 1)
    for categoria in productos_data.get("categorias", []):
        if categoria["nombre"] == "Hamburguesas":
            for producto in categoria.get("productos", []):
                if producto.get("id") == 1:  # Hamburguesa Completa
                    # Agregar ingredientes
                    producto["ingredientes"] = []
                    
                    # Buscar ingredientes disponibles para Hamburguesas
                    for ingrediente in ingredientes_data.get("ingredientes", []):
                        if "Hamburguesas" in ingrediente.get("categorias", []):
                            ingrediente_producto = {
                                "nombre": ingrediente["nombre"],
                                "cantidad_base": 1,
                                "precio_extra": ingrediente["precio_extra"],
                                "precio_resta": ingrediente["precio_resta"]
                            }
                            producto["ingredientes"].append(ingrediente_producto)
                    
                    break
    
    # Guardar productos actualizados
    with open(ruta_productos, 'w', encoding='utf-8') as f:
        json.dump(productos_data, f, indent=2, ensure_ascii=False)
    
    print("Ingredientes asignados a Hamburguesa Completa")
    print("Ahora el botón de editar debería aparecer en el carrito")

if __name__ == "__main__":
    asignar_ingredientes_ejemplo()
