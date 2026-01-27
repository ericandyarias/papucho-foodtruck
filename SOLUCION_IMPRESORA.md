# Solución: Error "No backend available" en Windows

## Problema
El error "No backend available" significa que pyusb no tiene un driver USB instalado para comunicarse con la impresora.

## Soluciones (en orden de recomendación)

### Solución 1: Instalar libusb usando Zadig (RECOMENDADO)

1. Descarga Zadig desde: https://zadig.akeo.ie/
2. Conecta tu impresora Xprinter EX-E200M por USB
3. Abre Zadig
4. En "Options", marca "List All Devices"
5. Selecciona tu impresora de la lista
6. En el campo derecho, selecciona "libusb-win32" o "WinUSB"
7. Haz clic en "Install Driver" o "Replace Driver"
8. Espera a que termine la instalación
9. Reinicia tu computadora (recomendado)
10. Prueba nuevamente: `python utils/probar_impresora.py`

### Solución 2: Instalar libusb usando pip (si está disponible)

```bash
pip install libusb-package
```

Nota: Esto puede no funcionar en todas las versiones de Windows.

### Solución 3: Usar el nombre de la impresora en lugar de USB directo

Si las soluciones anteriores no funcionan, podemos modificar el código para usar el nombre de la impresora de Windows en lugar de USB directo.

### Solución 4: Usar puerto COM (si la impresora tiene modo serial)

Algunas impresoras Xprinter pueden funcionar como puerto COM. Verifica en el Administrador de dispositivos si aparece como puerto COM.

## Verificación

Después de aplicar cualquier solución, ejecuta:
```bash
python utils/probar_impresora.py
```

Si funciona, deberías ver un ticket de prueba impreso.
