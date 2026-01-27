"""
Script de prueba para verificar el cálculo de precios con ingredientes
"""
from utils.productos import calcular_precio_con_ingredientes

# Producto de ejemplo
producto = {
    "id": 1,
    "nombre": "Hamburguesa Completa",
    "precio": 8800.0,
    "ingredientes": [
        {
            "nombre": "Medallón",
            "cantidad_base": 1,
            "precio_extra": 1000.0,
            "precio_resta": 500.0
        },
        {
            "nombre": "Tomáte",
            "cantidad_base": 1,
            "precio_extra": 500.0,
            "precio_resta": 500.0
        }
    ]
}

# Caso 1: Sin modificaciones (debería retornar precio base)
modificaciones1 = {"Medallón": 1, "Tomáte": 1}
precio1 = calcular_precio_con_ingredientes(producto, modificaciones1)
print(f"Caso 1 - Sin modificaciones: ${precio1:.2f} (esperado: $8800.00)")

# Caso 2: Agregar 1 medallón extra
modificaciones2 = {"Medallón": 2, "Tomáte": 1}
precio2 = calcular_precio_con_ingredientes(producto, modificaciones2)
print(f"Caso 2 - 1 medallón extra: ${precio2:.2f} (esperado: $9800.00)")

# Caso 3: Quitar 1 tomáte
modificaciones3 = {"Medallón": 1, "Tomáte": 0}
precio3 = calcular_precio_con_ingredientes(producto, modificaciones3)
print(f"Caso 3 - Quitar 1 tomáte: ${precio3:.2f} (esperado: $8300.00)")

# Caso 4: Sin modificaciones dict (debería usar cantidad_base)
precio4 = calcular_precio_con_ingredientes(producto, None)
print(f"Caso 4 - Sin dict modificaciones: ${precio4:.2f} (esperado: $8800.00)")

# Caso 5: Modificaciones vacías
precio5 = calcular_precio_con_ingredientes(producto, {})
print(f"Caso 5 - Dict vacío: ${precio5:.2f} (esperado: $8800.00)")
