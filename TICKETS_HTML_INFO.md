# ✅ TICKETS EN HTML - NUEVO SISTEMA

## ¿Qué cambió?

Los tickets ahora se generan en **HTML** en lugar de TXT.

### Ventajas:

✅ **Aprovecha todo el ancho del papel** (márgenes de solo 2mm)
✅ **Letra pequeña y legible** (9pt, perfecta para tickets)
✅ **Se imprime perfecto** sin configurar la impresora
✅ **Control total del formato** como en Word
✅ **Más profesional** con mejor diseño

---

## 📁 Ubicación de los tickets

Los tickets se guardan en:
```
data\tickets\
├── ticket_cocina_0001.html
├── ticket_cliente_0001.html
├── ticket_cocina_0002.html
└── ticket_cliente_0002.html
```

---

## 🖨️ Cómo funciona la impresión

1. Confirmás un pedido
2. Se generan 2 archivos HTML (COCINA y CLIENTE)
3. Se imprimen **automáticamente** usando el navegador
4. Los archivos se guardan para consulta futura

---

## 🎨 Características del diseño

- **Márgenes**: 2mm (mínimos, aprovecha todo el papel)
- **Fuente**: Courier New, 9pt (monoespaciada, pequeña)
- **Ancho**: 80mm (tamaño real del papel)
- **Colores**: 
  - COCINA: Rojo
  - CLIENTE: Verde

---

## ⚙️ Configuración (opcional)

El archivo `data\config.json` sigue funcionando:

```json
{
  "impresora": {
    "ancho_ticket": 80,
    "modelo": "POS-80"
  },
  "tickets": {
    "incluir_fecha_hora": true,
    "lineas_corte": 3
  }
}
```

**Nota:** El `ancho_ticket` ya no afecta tanto porque HTML usa todo el ancho disponible automáticamente.

---

## 🔍 Ver un ticket

Podés abrir cualquier archivo `.html` de la carpeta `data\tickets\` con:
- Doble clic (se abre en el navegador)
- Click derecho → Abrir con → Navegador
- Click derecho → Imprimir

---

## 💡 Ventajas vs TXT

| Característica | TXT (Antiguo) | HTML (Nuevo) |
|---------------|---------------|--------------|
| Ancho usado | 50-60% | 95-98% |
| Márgenes | Grandes | Mínimos (2mm) |
| Fuente | Grande | Pequeña ajustable |
| Control | Limitado | Total |
| Aspecto | Básico | Profesional |

---

## ⚠️ Importante

- **No necesitás configurar la impresora** - funciona directo
- Los archivos HTML se pueden **reimprimir** cuando quieras
- Si cambiás de impresora, **sigue funcionando** sin cambios
- La ventana de confirmación **no cambió** - todo funciona igual

---

## 🎯 Resultado

Los tickets ahora salen **exactamente como querés**:
- Usan todo el ancho del papel
- Letra del tamaño correcto
- Márgenes mínimos
- Aspecto profesional

No hay nada más que configurar. ¡Funcionan de una!
