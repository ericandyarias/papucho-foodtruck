# 🖨️ CONFIGURAR IMPRESORA POS-80

## Configuración del Ancho de Impresión

El archivo `data\config.json` controla cómo se imprimen los tickets.

### Ubicación del archivo
```
papucho-foodtruck\
└── data\
    └── config.json  ← Editar este archivo
```

### Configuración actual

```json
{
  "impresora": {
    "ancho_ticket": 48,
    "modelo": "POS-80",
    "comentarios": "Para impresoras térmicas de 80mm. Valores típicos: 42-48 caracteres"
  },
  "tickets": {
    "incluir_fecha_hora": true,
    "lineas_corte": 3
  }
}
```

---

## 📏 Ajustar el Ancho del Ticket

### Para impresora POS-80 (80mm)

Tu impresora puede imprimir entre **42 y 48 caracteres por línea**.

**Valores recomendados para probar:**

1. **48 caracteres** (aprovecha todo el ancho, recomendado)
   ```json
   "ancho_ticket": 48
   ```

2. **42 caracteres** (más conservador, con márgenes)
   ```json
   "ancho_ticket": 42
   ```

3. **45 caracteres** (equilibrado)
   ```json
   "ancho_ticket": 45
   ```

### Cómo cambiar el ancho

1. Abre `data\config.json`
2. Cambia el valor de `"ancho_ticket"`:
   ```json
   "ancho_ticket": 48
   ```
3. Guarda el archivo
4. **No necesitas reiniciar la aplicación** - el cambio se aplica inmediatamente

---

## 🧪 Probar Diferentes Anchos

### Método rápido

1. Cambia `"ancho_ticket"` en `config.json`
2. Haz un pedido de prueba
3. Observa cómo se imprime
4. Si el texto se corta o se sale del papel, ajusta el valor

### Señales de que el ancho está mal

❌ **Ancho muy grande:**
- El texto se corta en los bordes
- Las líneas salen del papel

❌ **Ancho muy pequeño:**
- Mucho espacio en blanco a los lados
- El texto se ve muy angosto

✅ **Ancho correcto:**
- El texto usa todo el ancho del papel
- Pequeños márgenes a los lados
- Nada se corta

---

## 🔧 Otras Configuraciones

### Líneas de corte

Controla cuántas líneas en blanco se agregan al final (para el cortador de papel):

```json
"lineas_corte": 3
```

- **Menos líneas (1-2):** Ahorra papel, pero puede cortar el texto final
- **Más líneas (4-5):** Más espacio, asegura que el cortador no toque el texto

### Incluir fecha y hora

Controla si se imprime la fecha y hora al final del ticket:

```json
"incluir_fecha_hora": true
```

- `true`: Incluye fecha y hora
- `false`: No incluye fecha y hora

---

## 📋 VALORES TÍPICOS POR IMPRESORA

| Modelo | Ancho de papel | Caracteres por línea |
|--------|----------------|---------------------|
| POS-58 | 58mm | 32-35 |
| POS-80 | 80mm | 42-48 |
| POS-82 | 82mm | 44-50 |

---

## ⚙️ Configuración Recomendada para POS-80

```json
{
  "impresora": {
    "ancho_ticket": 48,
    "modelo": "POS-80"
  },
  "tickets": {
    "incluir_fecha_hora": true,
    "lineas_corte": 3
  }
}
```

---

## 🐛 Solución de Problemas

### El ticket no usa todo el ancho del papel

**Solución:** Aumenta el `ancho_ticket` de a poco:
- Prueba con 42, luego 45, luego 48
- Encuentra el valor que mejor se ajusta

### El texto se sale del papel

**Solución:** Reduce el `ancho_ticket`:
- Prueba con 45, luego 42, luego 40

### La impresora corta parte del texto al final

**Solución:** Aumenta las `lineas_corte`:
```json
"lineas_corte": 5
```

### Los tickets no se cortan automáticamente

- Tu impresora debe tener cortador automático
- Verifica que esté habilitado en la configuración de la impresora
- Algunas impresoras requieren comandos especiales (ESC/POS)

---

## 💡 Consejo

**Empieza con 48 caracteres** y reduce si es necesario. Es el valor más común para impresoras de 80mm.

Si cambias de impresora, solo edita `config.json` - no necesitas tocar el código.
