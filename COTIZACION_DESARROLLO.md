# COTIZACIÓN DE DESARROLLO - SISTEMA PAPUCHO FOODTRUCK

## 📋 INFORMACIÓN DEL PROYECTO

**Cliente**: PAPUCHO FOODTRUCK  
**Proyecto**: Sistema de Punto de Venta (POS) para Foodtruck  
**Fecha de Cotización**: 2024  
**Versión del Sistema**: 1.0  

---

## 📊 RESUMEN EJECUTIVO

Sistema completo de punto de venta desarrollado en Python con Tkinter, incluyendo gestión de productos, ingredientes, personalización de pedidos, impresión automática de tickets y administración completa del catálogo.

**Alcance del Proyecto**:
- ✅ Sistema POS completo y funcional
- ✅ Interfaz gráfica moderna e intuitiva
- ✅ Gestión de productos e ingredientes
- ✅ Sistema de precios dinámico con modificaciones
- ✅ Impresión automática de tickets térmicos
- ✅ Múltiples tipos de pedido y formas de pago
- ✅ Sistema de administración completo
- ✅ Gestión de imágenes
- ✅ Documentación técnica completa

---

## 🔧 DESGLOSE DE DESARROLLO

### 1. ANÁLISIS Y DISEÑO (40 horas)

#### 1.1 Análisis de Requerimientos
- Reuniones con cliente
- Definición de funcionalidades
- Casos de uso
- Especificaciones técnicas
**Horas**: 12 horas

#### 1.2 Diseño de Arquitectura
- Diseño de estructura de datos
- Diseño de base de datos (JSON)
- Diseño de interfaz de usuario
- Diagramas de flujo
**Horas**: 16 horas

#### 1.3 Planificación y Documentación Inicial
- Plan de desarrollo
- Documentación de arquitectura
- Estimación de tiempos
**Horas**: 12 horas

**Subtotal Análisis y Diseño**: 40 horas

---

### 2. DESARROLLO DE INTERFAZ DE USUARIO (80 horas)

#### 2.1 Estructura Principal
- Configuración de ventana principal
- Layout responsivo con grid
- Sistema de navegación
- Integración de componentes
**Horas**: 12 horas

#### 2.2 Módulo de Encabezado
- Diseño de header
- Estilos y tipografía
**Horas**: 2 horas

#### 2.3 Módulo de Navegación
- Barra lateral izquierda
- Botones de navegación
- Callbacks y eventos
**Horas**: 4 horas

#### 2.4 Módulo de Selección de Productos
- Sistema de categorías
- Lista de productos con scroll
- Carga y visualización de imágenes
- Botones de agregar producto
- Ventana de productos personalizados
- Filtrado por categoría
**Horas**: 20 horas

#### 2.5 Módulo de Carrito
- Diseño de carrito lateral
- Lista de items con scroll
- Controles de cantidad (+/-)
- Visualización de precios y subtotales
- Botón de editar ingredientes
- Ventana modal de edición de ingredientes
- Ventana de confirmación de pedido
- Validaciones de formulario
- Efectos hover y estilos
**Horas**: 30 horas

#### 2.6 Módulo de Administración
- Ventana modal de administración
- Sistema de pestañas (Productos/Ingredientes)
- Lista de productos con filtros
- Formulario CRUD de productos
- Lista de ingredientes
- Formulario CRUD de ingredientes
- Gestión de ingredientes por producto
- Preview de imágenes
- Validaciones complejas
- Scrollbars y canvas
**Horas**: 40 horas

**Subtotal Interfaz de Usuario**: 80 horas

---

### 3. DESARROLLO DE LÓGICA DE NEGOCIO (60 horas)

#### 3.1 Gestión de Productos (`utils/productos.py`)
- CRUD completo de productos
- Sistema de categorías fijas
- IDs autoincrementales
- Búsqueda y filtrado
- Gestión de ingredientes en productos
- Cálculo de precios con modificaciones
- Validaciones de datos
**Horas**: 20 horas

#### 3.2 Gestión de Ingredientes (`utils/ingredientes.py`)
- CRUD completo de ingredientes
- Sistema de categorías múltiples
- Búsqueda por ID y nombre
- Actualización de referencias en productos
- Eliminación con limpieza de referencias
- Filtrado por categoría
**Horas**: 16 horas

#### 3.3 Gestión de Órdenes (`utils/orden.py`)
- Sistema de numeración secuencial
- Persistencia de número de orden
- Incremento automático
**Horas**: 4 horas

#### 3.4 Sistema de Cálculo de Precios
- Cálculo de precio base
- Cálculo de modificaciones (extras/quitados)
- Cálculo de subtotales
- Cálculo de totales
- Actualización en tiempo real
**Horas**: 12 horas

#### 3.5 Gestión de Imágenes (`utils/imagenes.py`)
- Carga y redimensionamiento
- Guardado de imágenes
- Eliminación de imágenes
- Validación de formatos
- Integración con Tkinter
**Horas**: 8 horas

**Subtotal Lógica de Negocio**: 60 horas

---

### 4. SISTEMA DE IMPRESIÓN (35 horas)

#### 4.1 Integración con Impresora Térmica
- Investigación de librerías (python-escpos)
- Configuración de Win32Raw
- Detección de impresoras Windows
- Validación de impresora
- Manejo de errores
**Horas**: 12 horas

#### 4.2 Generación de Tickets (`utils/tickets.py`)
- Formato ESC/POS
- Diseño de layout de ticket
- Formateo de texto (centrado, alineado)
- Generación de ticket COCINA
- Generación de ticket CLIENTE
- Manejo de productos con modificaciones
- Cálculo y visualización de totales
- Fecha y hora
- Corte automático de papel
**Horas**: 18 horas

#### 4.3 Respaldo de Tickets
- Guardado en archivos .txt
- Organización de archivos
- Nomenclatura de archivos
**Horas**: 3 horas

#### 4.4 Configuración y Pruebas
- Sistema de configuración (config.json)
- Scripts de prueba
- Documentación de configuración
**Horas**: 2 horas

**Subtotal Sistema de Impresión**: 35 horas

---

### 5. INTEGRACIÓN Y PRUEBAS (40 horas)

#### 5.1 Integración de Componentes
- Conexión entre módulos UI
- Flujo de datos entre componentes
- Callbacks y eventos
- Sincronización de datos
**Horas**: 12 horas

#### 5.2 Pruebas Funcionales
- Pruebas de cada módulo
- Pruebas de flujos completos
- Pruebas de casos límite
- Pruebas de validaciones
**Horas**: 16 horas

#### 5.3 Pruebas de Integración
- Pruebas end-to-end
- Pruebas de impresión
- Pruebas de persistencia de datos
- Pruebas de manejo de errores
**Horas**: 8 horas

#### 5.4 Corrección de Bugs
- Identificación de problemas
- Corrección de errores
- Optimizaciones
**Horas**: 4 horas

**Subtotal Integración y Pruebas**: 40 horas

---

### 6. DOCUMENTACIÓN Y ENTREGA (25 horas)

#### 6.1 Documentación Técnica
- Documentación de código
- Documentación de arquitectura
- Guías de uso
- README completo
**Horas**: 12 horas

#### 6.2 Documentación de Usuario
- Manual de usuario
- Guías de configuración
- Solución de problemas comunes
**Horas**: 8 horas

#### 6.3 Entrega y Capacitación
- Preparación de entregables
- Instalación en ambiente del cliente
- Capacitación básica
- Documentación de instalación
**Horas**: 5 horas

**Subtotal Documentación y Entrega**: 25 horas

---

## 📈 RESUMEN DE HORAS

| Fase | Horas |
|------|-------|
| 1. Análisis y Diseño | 40 |
| 2. Desarrollo de Interfaz de Usuario | 80 |
| 3. Desarrollo de Lógica de Negocio | 60 |
| 4. Sistema de Impresión | 35 |
| 5. Integración y Pruebas | 40 |
| 6. Documentación y Entrega | 25 |
| **TOTAL** | **280 horas** |

---

## 💰 COTIZACIÓN

### Opción 1: Tarifa por Hora Estándar

**Tarifa por hora**: $50 USD / hora  
**Total de horas**: 280 horas  
**Subtotal**: $14,000 USD  
**IVA (si aplica)**: $0 USD  
**TOTAL**: **$14,000 USD**

---

### Opción 2: Tarifa por Hora Premium

**Tarifa por hora**: $75 USD / hora  
**Total de horas**: 280 horas  
**Subtotal**: $21,000 USD  
**IVA (si aplica)**: $0 USD  
**TOTAL**: **$21,000 USD**

---

### Opción 3: Paquete Completo (Recomendado)

**Desarrollo completo del sistema**: $15,000 USD  
**Incluye**:
- ✅ Desarrollo completo
- ✅ Documentación técnica
- ✅ Documentación de usuario
- ✅ 30 días de soporte post-entrega
- ✅ 2 sesiones de capacitación
- ✅ Corrección de bugs críticos

**TOTAL**: **$15,000 USD**

---

## 📦 ENTREGABLES

### Código Fuente
- ✅ Código fuente completo del sistema
- ✅ Estructura de directorios organizada
- ✅ Archivos de configuración
- ✅ Scripts de utilidad

### Documentación
- ✅ README.md con instrucciones de instalación
- ✅ Documentación técnica completa (RESUMEN_SISTEMA.md)
- ✅ Manual de usuario
- ✅ Guías de configuración
- ✅ Documentación de API interna

### Archivos de Configuración
- ✅ requirements.txt
- ✅ Archivos de ejemplo de datos
- ✅ Configuración de impresora

### Soporte
- ✅ 30 días de soporte técnico post-entrega
- ✅ Corrección de bugs críticos
- ✅ 2 sesiones de capacitación (1 hora cada una)

---

## ⏱️ CRONOGRAMA ESTIMADO

| Fase | Duración | Inicio | Fin |
|------|----------|--------|-----|
| Análisis y Diseño | 1 semana | Semana 1 | Semana 1 |
| Desarrollo UI | 2 semanas | Semana 2 | Semana 3 |
| Lógica de Negocio | 1.5 semanas | Semana 3 | Semana 4 |
| Sistema de Impresión | 1 semana | Semana 5 | Semana 5 |
| Integración y Pruebas | 1 semana | Semana 6 | Semana 6 |
| Documentación | 3 días | Semana 7 | Semana 7 |
| **TOTAL** | **7 semanas** | | |

**Tiempo total estimado**: 7 semanas (1.75 meses)

---

## 🎯 FUNCIONALIDADES INCLUIDAS

### ✅ Gestión de Productos
- Crear, modificar, eliminar productos
- Categorización automática
- Gestión de imágenes
- Asignación de ingredientes

### ✅ Gestión de Ingredientes
- Crear, modificar, eliminar ingredientes
- Múltiples categorías por ingrediente
- Precios de extra y resta
- Gestión de imágenes

### ✅ Sistema de Pedidos
- Selección de productos por categoría
- Carrito de compras
- Modificación de ingredientes en tiempo real
- Cálculo automático de precios
- Productos personalizados

### ✅ Confirmación de Pedidos
- Datos del cliente
- Tipos de pedido (mesa, domicilio, retira)
- Formas de pago (efectivo, tarjeta, transferencia)
- Validaciones completas

### ✅ Sistema de Impresión
- Impresión automática de tickets
- Tickets COCINA y CLIENTE
- Formato profesional ESC/POS
- Respaldo en archivos .txt

### ✅ Administración
- Interfaz completa de administración
- Gestión de catálogo
- Filtros y búsquedas
- Validaciones robustas

---

## 🔄 MANTENIMIENTO Y SOPORTE

### Soporte Incluido (30 días)
- Corrección de bugs críticos
- Soporte técnico por email
- 2 sesiones de capacitación

### Soporte Adicional (Opcional)
- **Soporte mensual**: $200 USD/mes
  - Soporte técnico continuo
  - Actualizaciones menores
  - Consultoría

- **Desarrollo de nuevas funcionalidades**: Tarifa por hora
  - Integración con sistemas de pago
  - Reportes y estadísticas
  - Integración con bases de datos
  - Versión web/móvil

---

## 📝 CONDICIONES

### Forma de Pago
- **Opción A**: 50% al inicio, 50% al finalizar
- **Opción B**: 30% al inicio, 40% a mitad del proyecto, 30% al finalizar

### Garantía
- 30 días de garantía para corrección de bugs críticos
- Bugs menores: corrección en actualizaciones futuras

### Propiedad Intelectual
- El código fuente es propiedad del cliente
- El desarrollador puede usar el proyecto como portfolio (sin datos sensibles)

### Modificaciones
- Cambios menores durante desarrollo: incluidos
- Cambios mayores: cotización adicional
- Nuevas funcionalidades: cotización por separado

---

## 📞 CONTACTO

Para consultas sobre esta cotización o para iniciar el proyecto, por favor contactar con el desarrollador.

---

## ✅ VALIDEZ

Esta cotización es válida por **30 días** a partir de la fecha de emisión.

---

**NOTA**: Esta cotización está basada en el análisis del sistema existente. Los precios pueden variar según requerimientos específicos adicionales o modificaciones al alcance del proyecto.
