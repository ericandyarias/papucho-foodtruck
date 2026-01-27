# Solución Rápida: Error "No backend available"

## El Problema
El error "No backend available" significa que Windows no tiene el driver USB necesario para que Python se comunique directamente con la impresora.

## Solución (5 minutos)

### Paso 1: Descargar Zadig
1. Ve a: https://zadig.akeo.ie/
2. Descarga la versión más reciente de Zadig
3. Ejecuta `zadig.exe` (puede requerir permisos de administrador)

### Paso 2: Instalar Driver USB
1. **Conecta tu impresora Xprinter EX-E200M por USB** (debe estar encendida)
2. En Zadig, ve al menú **Options** → marca **"List All Devices"**
3. En la lista desplegable superior, **selecciona tu impresora Xprinter**
   - Busca algo como "Xprinter", "USB Printer", o el nombre de tu impresora
4. En el campo derecho (donde dice el driver actual), selecciona:
   - **"libusb-win32"** (recomendado) O
   - **"WinUSB"** (alternativa)
5. Haz clic en **"Install Driver"** o **"Replace Driver"**
6. Espera a que termine (puede tardar 1-2 minutos)
7. Cierra Zadig

### Paso 3: Reiniciar
**Reinicia tu computadora** para que los cambios tengan efecto.

### Paso 4: Probar
Después de reiniciar, ejecuta:
```bash
python utils/probar_impresora.py
```

Si funciona, deberías ver un ticket de prueba impreso.

## ¿Por qué funciona?
Zadig instala el driver `libusb-win32` o `WinUSB` que permite que Python (a través de pyusb) se comunique directamente con dispositivos USB, sin necesidad de drivers específicos del fabricante.

## Notas Importantes
- ✅ **No afecta otros usos de la impresora**: Puedes seguir usándola normalmente desde otras aplicaciones
- ✅ **Es reversible**: Si necesitas volver al driver original, puedes hacerlo desde el Administrador de dispositivos
- ⚠️ **Requiere permisos de administrador**: Zadig necesita ejecutarse como administrador
- ⚠️ **Una vez por impresora**: Solo necesitas hacerlo una vez por impresora

## Alternativa: Si no quieres usar Zadig
Si prefieres no modificar los drivers, podemos cambiar el código para usar el nombre de la impresora de Windows en lugar de USB directo. Esto requiere que la impresora esté instalada como impresora de Windows.
