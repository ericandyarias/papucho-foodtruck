# 🔧 AJUSTAR ANCHO DEL TICKET - GUÍA RÁPIDA

## Problema Detectado

El ticket impreso **no usa todo el ancho del papel** - hay mucho espacio en blanco a los lados.

---

## ✅ SOLUCIÓN RÁPIDA (Recomendada)

### Paso 1: Abrir el archivo de configuración

Abre: `data\config.json`

### Paso 2: Cambiar el ancho

Cambia esta línea:
```json
"ancho_ticket": 48,
```

Por esta:
```json
"ancho_ticket": 60,
```

### Paso 3: Guardar y probar

1. Guarda el archivo
2. Haz un pedido de prueba
3. Observa si ahora usa más ancho del papel

---

## 📏 TABLA DE PRUEBAS

Prueba estos valores hasta encontrar el perfecto:

| Valor | Resultado Esperado |
|-------|-------------------|
| **48** | Actual (muy angosto) |
| **55** | Más ancho, conservador |
| **60** | RECOMENDADO - buen balance |
| **65** | Muy ancho, casi todo el papel |
| **70** | Máximo, puede cortarse |

**Cómo probar:**
1. Cambia el valor en `config.json`
2. Guarda
3. Haz un pedido de prueba
4. Si se corta, reduce 5
5. Si sobra espacio, aumenta 5
6. Repite hasta encontrar el perfecto

---

## 🎯 VALORES POR OBSERVACIÓN

Según la foto que compartiste:

- ❌ **48 caracteres**: Muy angosto (lo que tienes ahora)
- ✅ **60-65 caracteres**: Ideal para tu impresora
- ⚠️ **70+ caracteres**: Puede salirse del papel

---

## 🖨️ CONFIGURAR LA IMPRESORA (Opcional)

Si cambiar el ancho no es suficiente:

### Windows:

1. **Panel de Control** → **Dispositivos e impresoras**
2. Click derecho en **POS-80** → **Preferencias de impresión**
3. Busca:
   - **Márgenes**: Ponlos en 0 o mínimo
   - **Tamaño de fuente**: Pequeño/Condensado
   - **Ancho de columna**: Máximo disponible
4. **Aceptar**

### Configuración Avanzada:

Si tu impresora tiene software propio:
1. Abre el software de configuración de la POS-80
2. Busca opciones de **formato** o **layout**
3. Configura:
   - Ancho de caracteres por línea: **Máximo**
   - Márgenes: **Mínimo o 0**
   - Fuente: **Condensada** o **Pequeña**

---

## 🧪 PRUEBA RÁPIDA

Para encontrar el ancho perfecto rápidamente:

1. Pon `"ancho_ticket": 70`
2. Haz un pedido de prueba
3. Si se corta → reduce a 65
4. Si se corta → reduce a 60
5. Si no se corta pero hay espacio → ese es tu máximo
6. Ajusta -2 o -3 para dejar un pequeño margen de seguridad

---

## 💡 RECOMENDACIÓN FINAL

**Empieza con 60 caracteres** y ajusta desde ahí.

Tu impresora POS-80 debería soportar entre 55-70 caracteres dependiendo de la configuración de márgenes.

---

## ⚠️ IMPORTANTE

- **No necesitas reiniciar la app** - los cambios se aplican inmediatamente
- Si generas el instalador, el `config.json` se incluirá con el valor que tengas
- Puedes cambiar el valor cuantas veces quieras sin problemas
