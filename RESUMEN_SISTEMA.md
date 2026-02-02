# RESUMEN COMPLETO DEL SISTEMA - PAPUCHO FOODTRUCK

## 📋 DESCRIPCIÓN GENERAL

**PAPUCHO FOODTRUCK** es un sistema de punto de venta (POS) desarrollado en Python con Tkinter (ttk) para la gestión de pedidos de un foodtruck. El sistema permite gestionar productos, ingredientes, realizar pedidos personalizados y generar tickets de impresión automática.

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Estructura de Directorios

```
papucho-foodtruck/
├── main.py                          # Aplicación principal
├── requirements.txt                 # Dependencias del proyecto
├── data/                            # Datos persistentes
│   ├── config.json                  # Configuración del sistema
│   ├── productos.json               # Catálogo de productos
│   ├── ingredientes.json            # Catálogo de ingredientes
│   ├── orden_actual.txt             # Número de orden actual
│   ├── tickets/                     # Tickets generados (respaldo)
│   └── imagenes/                    # Imágenes de productos e ingredientes
│       ├── productos/
│       └── ingredientes/
├── ui/                              # Módulos de interfaz de usuario
│   ├── __init__.py
│   ├── encabezado.py                # Header con título
│   ├── navegador.py                 # Barra lateral izquierda (navegación)
│   ├── seleccion.py                 # Selección de productos (centro)
│   ├── carrito.py                   # Carrito de compras (derecha)
│   ├── administracion.py            # Ventana de administración
│   └── administracion_ingredientes_producto.py
└── utils/                           # Módulos de utilidades
    ├── __init__.py
    ├── productos.py                  # Gestión de productos
    ├── ingredientes.py               # Gestión de ingredientes
    ├── orden.py                      # Gestión de números de orden
    ├── tickets.py                    # Generación e impresión de tickets
    ├── imagenes.py                   # Gestión de imágenes
    ├── detectar_impresora.py         # Detección de impresoras
    └── probar_impresora.py           # Pruebas de impresora
```

---

## 🎨 COMPONENTES DE LA INTERFAZ

### 1. **Encabezado** (`ui/encabezado.py`)
- Muestra el título "PAPUCHO FOODTRUCK"
- Ubicado en la parte superior de la ventana
- Diseño con fuente grande y negrita

### 2. **Navegador** (`ui/navegador.py`)
- Barra lateral izquierda
- Botones principales:
  - **📋 Pedidos**: Vista principal (actualmente siempre visible)
  - **⚙️ Administración**: Abre ventana de administración

### 3. **Selección de Productos** (`ui/seleccion.py`)
- Área central de la aplicación
- **Categorías**: Botones para filtrar productos por categoría
  - Categorías fijas: Hamburguesas, Lomitos, Milanesas, Fritas, Empanadas, Bebidas
  - Categoría especial: "Personalizados" (permite crear productos al vuelo)
- **Lista de Productos**: 
  - Muestra imagen (80x80px), nombre, descripción y precio
  - Botón "➕ Agregar" para cada producto
  - Scroll vertical para listas largas
- **Productos Personalizados**: Ventana modal para crear productos temporales con nombre y precio personalizado

### 4. **Carrito** (`ui/carrito.py`)
- Barra lateral derecha
- **Encabezado del Carrito**:
  - Título "🛒 Carrito"
  - Número de pedido actual (formato: Pedido #0001)
- **Lista de Items**:
  - Muestra cada producto con:
    - Nombre del producto
    - Precio unitario y subtotal
    - Detalle de modificaciones de ingredientes (extras/quitados)
    - Controles de cantidad (+/-)
    - Botón "✏️ Editar" (solo si el producto tiene ingredientes)
    - Botón "🗑️ Eliminar"
  - Scroll vertical
- **Total**: Muestra el total calculado considerando modificaciones
- **Botones**:
  - **🗑️ Borrar Todo**: Limpia todo el carrito (con confirmación)
  - **✅ Confirmar Pedido**: Abre ventana de confirmación

### 5. **Ventana de Confirmación** (dentro de `carrito.py`)
- **Datos del Cliente**:
  - Nombre del cliente (obligatorio)
  - Tipo de pedido (radio buttons):
    - Servicio en mesa
    - Domicilio (muestra campo de dirección y hora estimada)
    - Retira en puesto (muestra campo de hora de retiro)
- **Forma de Pago** (radio buttons):
  - Efectivo
  - Tarjeta
  - Transferencia
- **Total**: Muestra el total del pedido
- **Botones**: Cancelar / Aceptar

### 6. **Ventana de Administración** (`ui/administracion.py`)
- Ventana modal con pestañas:
  
  #### **Pestaña Productos**:
  - **Lista de Productos** (izquierda):
    - Filtro por categoría
    - Treeview con: ID, Categoría, Nombre, Precio, Descripción
    - Botón "➕ Nuevo Producto"
  - **Formulario de Producto** (derecha):
    - Categoría (combobox)
    - Nombre
    - Precio
    - Descripción (área de texto)
    - Imagen del producto (preview + botón cargar)
    - **Sección Ingredientes del Producto**:
      - Combo de ingredientes (filtrado por categoría)
      - Cantidad base
      - Botón "➕ Agregar"
      - Treeview de ingredientes asignados
      - Botón "❌ Eliminar Ingrediente"
    - Botones: 💾 Guardar / ✏️ Modificar / ❌ Eliminar / 🔄 Limpiar
  
  #### **Pestaña Ingredientes**:
  - **Lista de Ingredientes** (izquierda):
    - Treeview con: ID, Nombre, Categorías, Precio Extra, Precio Resta
    - Botón "➕ Nuevo Ingrediente"
  - **Formulario de Ingrediente** (derecha):
    - Nombre
    - Categorías (checkboxes múltiples)
    - Precio Extra
    - Precio Resta
    - Imagen del ingrediente (preview + botón cargar)
    - Botones: 💾 Guardar / ✏️ Modificar / ❌ Eliminar / 🔄 Limpiar

---

## 💾 GESTIÓN DE DATOS

### Archivos de Datos

#### 1. **`data/productos.json`**
Estructura:
```json
{
  "categorias": [
    {
      "nombre": "Hamburguesas",
      "productos": [
        {
          "id": 1,
          "nombre": "Hamburguesa Completa",
          "precio": 8800.0,
          "descripcion": "Descripción del producto",
          "imagen": "productos/producto_1.png",
          "ingredientes": [
            {
              "nombre": "Medallón",
              "cantidad_base": 1
            }
          ]
        }
      ]
    }
  ]
}
```

**Características**:
- Categorías fijas garantizadas por el sistema
- IDs autoincrementales
- Soporte para imágenes
- Ingredientes opcionales (sistema de referencias por nombre)

#### 2. **`data/ingredientes.json`**
Estructura:
```json
{
  "ingredientes": [
    {
      "id": 1,
      "nombre": "Medallón",
      "categorias": ["Hamburguesas", "Lomitos"],
      "precio_extra": 1000.0,
      "precio_resta": 500.0,
      "imagen": "ingredientes/ingrediente_1.png"
    }
  ]
}
```

**Características**:
- IDs autoincrementales
- Múltiples categorías por ingrediente
- Precios de extra y resta independientes
- Soporte para imágenes

#### 3. **`data/config.json`**
Estructura:
```json
{
  "impresora": {
    "ancho_ticket": 80,
    "modelo": "Xprinter EX-E200M",
    "nombre_impresora": "XP-80C"
  },
  "tickets": {
    "incluir_fecha_hora": true,
    "lineas_corte": 3
  }
}
```

#### 4. **`data/orden_actual.txt`**
- Archivo de texto simple con el número de orden actual
- Se incrementa automáticamente al confirmar un pedido

---

## 🔧 MÓDULOS PRINCIPALES

### 1. **`utils/productos.py`**
Funcionalidades:
- `cargar_productos()`: Carga productos desde JSON
- `guardar_productos()`: Guarda productos en JSON
- `asegurar_categorias_fijas()`: Garantiza que existan todas las categorías fijas
- `obtener_siguiente_id()`: Genera IDs autoincrementales
- `obtener_todos_los_productos()`: Lista todos los productos con su categoría
- `buscar_producto_por_id()`: Busca producto por ID
- `agregar_producto()`: Crea nuevo producto
- `modificar_producto()`: Modifica producto existente
- `eliminar_producto()`: Elimina producto
- `agregar_ingrediente_a_producto()`: Asigna ingrediente a producto
- `calcular_precio_con_ingredientes()`: Calcula precio final considerando modificaciones

### 2. **`utils/ingredientes.py`**
Funcionalidades:
- `cargar_ingredientes()`: Carga ingredientes desde JSON
- `guardar_ingredientes()`: Guarda ingredientes en JSON
- `obtener_siguiente_id()`: Genera IDs autoincrementales
- `obtener_todos_los_ingredientes()`: Lista todos los ingredientes
- `buscar_ingrediente_por_id()`: Busca por ID
- `buscar_ingrediente_por_nombre()`: Busca por nombre
- `agregar_ingrediente()`: Crea nuevo ingrediente
- `modificar_ingrediente()`: Modifica ingrediente (actualiza referencias en productos)
- `eliminar_ingrediente()`: Elimina ingrediente (elimina referencias en productos)
- `obtener_ingredientes_por_categoria()`: Filtra ingredientes por categoría

### 3. **`utils/tickets.py`**
Funcionalidades:
- `cargar_configuracion()`: Carga configuración de impresora
- `listar_impresoras_windows()`: Lista impresoras disponibles
- `verificar_impresora_existe()`: Verifica si existe una impresora
- `obtener_impresora()`: Obtiene conexión a impresora (Win32Raw)
- `imprimir_ticket_escpos()`: Imprime ticket directamente
- `guardar_ticket_texto()`: Guarda ticket como archivo .txt (respaldo)
- `generar_tickets_pedido()`: Genera tickets COCINA y CLIENTE
- `imprimir_ticket_prueba()`: Imprime ticket de prueba

**Formato de Tickets**:
- Encabezado: "PAPUCHO FOODTRUCK"
- Número de orden
- Datos del cliente
- Tipo de pedido y dirección (si aplica)
- Lista de productos con modificaciones
- Total a pagar
- Forma de pago
- Fecha y hora
- Marca (COCINA o CLIENTE)

### 4. **`utils/orden.py`**
Funcionalidades:
- `leer_numero_orden()`: Lee número actual
- `guardar_numero_orden()`: Guarda número
- `incrementar_orden()`: Incrementa y guarda

### 5. **`utils/imagenes.py`**
Funcionalidades:
- `cargar_imagen_tkinter()`: Carga y redimensiona imágenes para Tkinter
- `guardar_imagen_producto()`: Guarda imagen de producto
- `guardar_imagen_ingrediente()`: Guarda imagen de ingrediente
- `eliminar_imagen()`: Elimina archivo de imagen
- `validar_formato_imagen()`: Valida formato de imagen

---

## 🎯 FLUJO DE TRABAJO PRINCIPAL

### 1. **Inicio de la Aplicación**
1. Se carga `main.py`
2. Se inicializa la ventana principal (pantalla completa)
3. Se cargan productos desde `productos.json`
4. Se aseguran categorías fijas
5. Se carga número de orden actual

### 2. **Realizar un Pedido**
1. Usuario selecciona categoría
2. Usuario hace clic en "➕ Agregar" en un producto
3. Producto se agrega al carrito (con ingredientes en cantidad base)
4. Usuario puede:
   - Modificar cantidad (+/-)
   - Editar ingredientes (si tiene)
   - Eliminar item
5. Usuario hace clic en "✅ Confirmar Pedido"
6. Se abre ventana de confirmación
7. Usuario ingresa:
   - Nombre del cliente
   - Tipo de pedido
   - Forma de pago
8. Usuario hace clic en "Aceptar"
9. Sistema:
   - Genera tickets (COCINA y CLIENTE)
   - Imprime tickets automáticamente
   - Guarda tickets como respaldo (.txt)
   - Incrementa número de orden
   - Limpia el carrito

### 3. **Administración de Productos**
1. Usuario hace clic en "⚙️ Administración"
2. Se abre ventana de administración
3. **Crear Producto**:
   - Clic en "➕ Nuevo Producto"
   - Llenar formulario
   - Asignar ingredientes (opcional)
   - Cargar imagen (opcional)
   - Clic en "💾 Guardar"
4. **Modificar Producto**:
   - Seleccionar producto en lista
   - Modificar campos
   - Clic en "✏️ Modificar"
5. **Eliminar Producto**:
   - Seleccionar producto
   - Clic en "❌ Eliminar"
   - Confirmar

### 4. **Administración de Ingredientes**
1. Pestaña "🥗 Ingredientes"
2. **Crear Ingrediente**:
   - Clic en "➕ Nuevo Ingrediente"
   - Llenar formulario (nombre, categorías, precios)
   - Cargar imagen (opcional)
   - Clic en "💾 Guardar"
3. **Asignar Ingrediente a Producto**:
   - Ir a pestaña "📦 Productos"
   - Seleccionar producto
   - Seleccionar ingrediente del combo
   - Ingresar cantidad base
   - Clic en "➕ Agregar"

### 5. **Editar Ingredientes en el Carrito**
1. Agregar producto con ingredientes al carrito
2. Clic en "✏️ Editar" del item
3. Se abre ventana modal con:
   - Lista de ingredientes del producto
   - Controles +/- para cada ingrediente
   - Impacto en precio en tiempo real
   - Precio final calculado
4. Usuario modifica cantidades
5. Clic en "✅ Aceptar"
6. El precio del item se actualiza automáticamente

---

## 💰 SISTEMA DE PRECIOS

### Cálculo de Precios con Ingredientes

1. **Precio Base**: Precio del producto sin modificaciones

2. **Modificaciones de Ingredientes**:
   - **Extras**: Si `cantidad_actual > cantidad_base`
     - Ajuste = `(cantidad_actual - cantidad_base) × precio_extra`
   - **Quitas**: Si `cantidad_actual < cantidad_base`
     - Ajuste = `(cantidad_base - cantidad_actual) × precio_resta`
   - **Sin cambios**: Si `cantidad_actual == cantidad_base`
     - Ajuste = 0

3. **Precio Final**:
   ```
   Precio Final = Precio Base + Ajuste Total
   ```

4. **Subtotal por Item**:
   ```
   Subtotal = Precio Final × Cantidad
   ```

5. **Total del Carrito**:
   ```
   Total = Suma de todos los Subtotales
   ```

### Ejemplo:
- Producto: Hamburguesa Completa ($8800)
- Ingrediente: Medallón (cantidad_base: 1, precio_extra: $1000)
- Modificación: Agregar 1 medallón extra
- Precio Final: $8800 + ($1000 × 1) = $9800

---

## 🖨️ SISTEMA DE IMPRESIÓN

### Configuración
- **Tecnología**: python-escpos con Win32Raw (Windows)
- **Formato**: ESC/POS para impresoras térmicas de 80mm
- **Impresión**: Directa sin previsualización
- **Respaldo**: Archivos .txt en `data/tickets/`

### Características
- Detección automática de impresoras Windows
- Validación de existencia de impresora
- Generación de dos tickets por pedido:
  - **COCINA**: Para la cocina
  - **CLIENTE**: Para el cliente
- Formato profesional con:
  - Encabezado centrado
  - Información del pedido
  - Lista de productos con modificaciones
  - Total y forma de pago
  - Fecha y hora
  - Corte automático de papel

---

## 📦 DEPENDENCIAS

### Principales
- **python-escpos** (>=3.1): Impresión de tickets
- **Pillow** (>=10.0.0): Manejo de imágenes
- **pywin32**: Detección de impresoras en Windows (opcional)

### Incluidas en Python
- **tkinter**: Interfaz gráfica
- **json**: Manejo de datos JSON
- **os**: Operaciones del sistema de archivos

---

## 🔐 CARACTERÍSTICAS DE SEGURIDAD Y VALIDACIÓN

### Validaciones Implementadas
1. **Productos**:
   - Nombre obligatorio
   - Precio > 0
   - Categoría obligatoria

2. **Ingredientes**:
   - Nombre obligatorio
   - Al menos una categoría seleccionada
   - Precios >= 0

3. **Pedidos**:
   - Nombre del cliente obligatorio
   - Dirección obligatoria para domicilio
   - Carrito no vacío para confirmar

4. **Imágenes**:
   - Validación de formato
   - Redimensionamiento automático

---

## 🎨 CARACTERÍSTICAS DE DISEÑO

### Interfaz
- Diseño moderno con Tkinter ttk
- Colores personalizados:
  - Verde (#27ae60) para acciones positivas
  - Rojo (#e74c3c) para acciones destructivas
  - Gris (#95a5a6) para estados deshabilitados
- Efectos hover en botones
- Scrollbars donde es necesario
- Ventanas modales centradas
- Layout responsivo con grid

### Imágenes
- Tamaño fijo para productos: 80x80px
- Preview en administración: 100x100px
- Formatos soportados: JPG, PNG, GIF, BMP, WEBP
- Almacenamiento en `data/imagenes/`

---

## 📝 NOTAS IMPORTANTES

### Sistema de Ingredientes
- **Sin lógica hardcodeada**: El botón de editar solo aparece si el producto tiene ingredientes definidos
- **Sin categorías fijas para ingredientes**: Cualquier producto puede tener ingredientes
- **Sistema de referencias**: Los ingredientes en productos se referencian por nombre, los precios se obtienen dinámicamente desde `ingredientes.json`
- **Compatibilidad**: Productos sin ingredientes funcionan normalmente

### Categorías Fijas
Las siguientes categorías están garantizadas por el sistema:
- Hamburguesas
- Lomitos
- Milanesas
- Fritas
- Empanadas
- Bebidas

### Productos Personalizados
- Se pueden crear productos temporales desde la categoría "Personalizados"
- No se guardan en el JSON
- ID negativo (-1) para identificación
- Útiles para pedidos especiales

---

## 🚀 INSTALACIÓN Y USO

### Requisitos
- Python 3.7+
- Windows (para impresión con Win32Raw)
- Impresora térmica compatible ESC/POS (opcional)

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
python main.py
```

### Configuración de Impresora
1. Editar `data/config.json`
2. Configurar `nombre_impresora` con el nombre exacto de la impresora en Windows
3. Verificar con `utils/probar_impresora.py`

---

## 📊 ESTADÍSTICAS DEL SISTEMA

- **Líneas de código**: ~5000+
- **Módulos UI**: 6
- **Módulos Utils**: 7
- **Archivos de datos**: 4
- **Categorías fijas**: 6
- **Formatos de ticket**: 2 (COCINA y CLIENTE)

---

## 🔄 FLUJOS DE DATOS

### Crear Producto con Ingredientes
1. Usuario crea ingrediente → `ingredientes.json`
2. Usuario crea producto → `productos.json`
3. Usuario asigna ingrediente a producto → `productos.json` (referencia por nombre)
4. Al calcular precio → Se busca ingrediente en `ingredientes.json` por nombre

### Modificar Ingrediente
1. Usuario modifica ingrediente → `ingredientes.json`
2. Si cambia el nombre → Se actualizan todas las referencias en `productos.json`
3. Los precios se actualizan automáticamente (referencia dinámica)

### Eliminar Ingrediente
1. Usuario elimina ingrediente → `ingredientes.json`
2. Se eliminan todas las referencias en `productos.json`
3. Los productos quedan sin ese ingrediente

---

## 🎯 CASOS DE USO PRINCIPALES

1. **Tomar Pedido Simple**: Seleccionar productos → Agregar al carrito → Confirmar
2. **Pedido Personalizado**: Crear producto personalizado → Agregar → Confirmar
3. **Pedido con Modificaciones**: Agregar producto → Editar ingredientes → Confirmar
4. **Pedido a Domicilio**: Seleccionar tipo "Domicilio" → Ingresar dirección → Confirmar
5. **Administrar Catálogo**: Agregar/modificar/eliminar productos e ingredientes
6. **Configurar Precios**: Modificar precios de productos e ingredientes

---

## 🔧 MANTENIMIENTO

### Archivos de Respaldo
- Tickets: `data/tickets/` (archivos .txt)
- Orden actual: `data/orden_actual.txt`
- Configuración: `data/config.json`

### Limpieza
- Scripts disponibles:
  - `limpiar_ingredientes_productos.py`: Elimina ingredientes de productos
  - `asignar_ingredientes_hamburguesas.py`: Ejemplo de asignación masiva

---

## 📌 CONCLUSIÓN

El sistema **PAPUCHO FOODTRUCK** es una solución completa de punto de venta diseñada específicamente para foodtrucks. Ofrece:

✅ Gestión completa de productos e ingredientes  
✅ Personalización de pedidos con sistema de precios dinámico  
✅ Impresión automática de tickets  
✅ Interfaz intuitiva y moderna  
✅ Sistema robusto de validaciones  
✅ Almacenamiento persistente en JSON  
✅ Soporte para imágenes  
✅ Múltiples tipos de pedido (mesa, domicilio, retira)  
✅ Múltiples formas de pago  

El sistema está diseñado para ser fácil de usar, mantenible y escalable.
