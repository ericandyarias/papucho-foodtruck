"""
Script para asignar ingredientes a todos los productos de hamburguesas
"""
import json
import os

def asignar_ingredientes_hamburguesas():
    """Asigna ingredientes disponibles a todos los productos de hamburguesas"""
    ruta_productos = os.path.join('data', 'productos.json')
    ruta_ingredientes = os.path.join('data', 'ingredientes.json')
    
    # Cargar productos
    with open(ruta_productos, 'r', encoding='utf-8') as f:
        productos_data = json.load(f)
    
    # Cargar ingredientes
    with open(ruta_ingredientes, 'r', encoding='utf-8') as f:
        ingredientes_data = json.load(f)
    
    # Obtener todos los ingredientes disponibles para Hamburguesas
    ingredientes_hamburguesas = []
    for ingrediente in ingredientes_data.get("ingredientes", []):
        if "Hamburguesas" in ingrediente.get("categorias", []):
            ingredientes_hamburguesas.append(ingrediente)
    
    print(f"Encontrados {len(ingredientes_hamburguesas)} ingredientes para Hamburguesas")
    
    # Buscar categoría de Hamburguesas
    for categoria in productos_data.get("categorias", []):
        if categoria["nombre"] == "Hamburguesas":
            productos_actualizados = 0
            for producto in categoria.get("productos", []):
                # Solo agregar ingredientes si el producto no los tiene ya
                if "ingredientes" not in producto or len(producto.get("ingredientes", [])) == 0:
                    producto["ingredientes"] = []
                    
                    # Agregar todos los ingredientes disponibles con cantidad_base = 1
                    for ingrediente in ingredientes_hamburguesas:
                        ingrediente_producto = {
                            "nombre": ingrediente["nombre"],
                            "cantidad_base": 1,
                            "precio_extra": ingrediente["precio_extra"],
                            "precio_resta": ingrediente["precio_resta"]
                        }
                        producto["ingredientes"].append(ingrediente_producto)
                    
                    productos_actualizados += 1
                    print(f"  - Ingredientes asignados a: {producto['nombre']}")
            
            print(f"\nTotal: {productos_actualizados} productos actualizados")
            break
    
    # Guardar productos actualizados
    with open(ruta_productos, 'w', encoding='utf-8') as f:
        json.dump(productos_data, f, indent=2, ensure_ascii=False)
    
    print("\nIngredientes asignados correctamente")
    print("Ahora todos los productos de hamburguesas deberían mostrar el botón de editar")

if __name__ == "__main__":
    asignar_ingredientes_hamburguesas()
