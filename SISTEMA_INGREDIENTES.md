# Sistema de Ingredientes - Documentación

## Concepto General

El sistema de ingredientes permite personalizar productos agregando o quitando ingredientes, con impacto económico en el precio final.

## Estructura de Datos

### Ingredientes Globales (`data/ingredientes.json`)
Define ingredientes reutilizables que pueden asignarse a productos:

```json
{
  "ingredientes": [
    {
      "id": 1,
      "nombre": "Medallón",
      "categorias": ["Hamburguesas", "Lomitos", "Milanesas"],
      "precio_extra": 1000.0,
      "precio_resta": 500.0
    }
  ]
}
```

### Ingredientes en Productos (`data/productos.json`)
Cada producto puede tener ingredientes asignados directamente:

```json
{
  "id": 1,
  "nombre": "Hamburguesa Completa",
  "precio": 8800.0,
  "descripcion": "Hamburguesa completa con fritas.",
  "ingredientes": [
    {
      "nombre": "Medallón",
      "cantidad_base": 1,
      "precio_extra": 1000.0,
      "precio_resta": 500.0
    }
  ]
}
```

## Funcionamiento

### 1. Crear Ingredientes
- Ir a **Administración → Pestaña "Ingredientes"**
- Crear ingredientes con nombre, categorías y precios
- Los ingredientes se guardan en `ingredientes.json`

### 2. Asignar Ingredientes a Productos
- Ir a **Administración → Pestaña "Productos"**
- Seleccionar un producto
- En la sección "Ingredientes del Producto":
  - Seleccionar un ingrediente del combo
  - Definir cantidad base
  - Hacer clic en "Agregar Ingrediente"
- Los ingredientes se guardan directamente en el producto en `productos.json`

### 3. Editar Ingredientes en el Carrito
- Agregar un producto con ingredientes al carrito
- Aparece el botón "✏️ Editar"
- Al hacer clic, se abre una ventana donde se puede:
  - Ver todos los ingredientes del producto
  - Modificar cantidades con botones +/-
  - Ver el impacto en precio en tiempo real
  - Guardar cambios con "✅ Aceptar"

### 4. Cálculo de Precios
- **Precio base**: Precio del producto sin modificaciones
- **Extras**: Si cantidad > cantidad_base → suma `(cantidad - cantidad_base) × precio_extra`
- **Quitas**: Si cantidad < cantidad_base → resta `(cantidad_base - cantidad) × precio_resta`
- **Precio final**: precio_base + ajustes

## Reglas Importantes

1. **NO hay lógica hardcodeada**: El botón de editar solo aparece si el producto tiene ingredientes definidos
2. **Sin categorías fijas**: Cualquier producto puede tener ingredientes, no solo hamburguesas
3. **Ingredientes independientes**: Los ingredientes en `ingredientes.json` son solo referencia; los que importan son los asignados a cada producto
4. **Compatibilidad**: Productos sin ingredientes funcionan normalmente

## Scripts Útiles

- `limpiar_ingredientes_productos.py`: Elimina todos los ingredientes de todos los productos
- `asignar_ingredientes_hamburguesas.py`: Asigna ingredientes a productos de hamburguesas (ejemplo)
