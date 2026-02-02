# Solución: Error de Windows Security con Pillow

## Problema
Windows Security bloquea `_imagingtk.cp314-win_amd64.pyd` (módulo de Pillow) porque no puede verificar el editor.

## Soluciones

### Opción 1: Agregar exclusión en Windows Security (RECOMENDADO)

1. Abre **Seguridad de Windows** (buscar en el menú Inicio)
2. Ve a **Protección contra virus y amenazas**
3. Haz clic en **"Administrar configuración"** (en Configuración de protección contra virus y amenazas)
4. Desplázate hasta **"Exclusiones"**
5. Haz clic en **"Agregar o quitar exclusiones"**
6. Haz clic en **"Agregar una exclusión"** → **"Carpeta"**
7. Agrega la carpeta completa del proyecto:
   ```
   C:\Users\erica\Documents\papucho-foodtruck
   ```

### Opción 2: Permitir desde la notificación

1. Haz clic en **"Más información"** en la notificación
2. Selecciona **"Ejecutar de todos modos"** o **"Permitir"**

### Opción 3: Reinstalar Pillow (si persiste)

```bash
pip uninstall Pillow
pip install Pillow
```

## Verificación

Después de agregar la exclusión, reinicia la aplicación. El error no debería aparecer nuevamente.

## Nota

Este es un falso positivo de Windows Security. Pillow es una librería segura y ampliamente usada en Python. El bloqueo ocurre porque los archivos `.pyd` son módulos compilados y Windows no puede verificar su firma digital automáticamente.
