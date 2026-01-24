# 🔧 SOLUCIÓN RÁPIDA: Python no encontrado

## El Problema

Si ves este error:
```
no se encontró Python; ejecutar sin argumentos para instalar desde el Microsoft Store
```

Significa que Python no está instalado o no está en el PATH del sistema.

---

## ✅ SOLUCIÓN RÁPIDA (5 minutos)

### Opción 1: Instalar Python (RECOMENDADO)

1. **Descarga Python:**
   - Ve a: https://www.python.org/downloads/
   - Click en "Download Python 3.x.x" (la última versión)

2. **Instala Python:**
   - Ejecuta el instalador descargado
   - **MUY IMPORTANTE:** Marca la casilla "☑ Add Python to PATH" (abajo en la ventana)
   - Click en "Install Now"
   - Espera a que termine la instalación

3. **Verifica la instalación:**
   - Cierra TODAS las ventanas de terminal/CMD/PowerShell
   - Abre una NUEVA terminal
   - Escribe: `python --version`
   - Deberías ver algo como: `Python 3.14.x`

4. **Continúa con el instalador:**
   - Ahora puedes ejecutar: `python -m pip install pyinstaller`

---

### Opción 2: Si Python ya está instalado (pero no funciona)

1. **Busca dónde está Python:**
   - Presiona `Win + R`
   - Escribe: `%LOCALAPPDATA%\Programs\Python`
   - O busca manualmente en: `C:\Users\TuUsuario\AppData\Local\Programs\Python`

2. **Agrega Python al PATH:**
   - Presiona `Win + X` → Click en "Sistema"
   - Click en "Configuración avanzada del sistema" (lado derecho)
   - Click en "Variables de entorno" (botón abajo)
   - En "Variables del sistema", busca "Path" y click en "Editar"
   - Click en "Nuevo" y agrega la ruta de Python (ejemplo: `C:\Users\erica\AppData\Local\Programs\Python\Python314`)
   - Click en "Nuevo" otra vez y agrega: `C:\Users\erica\AppData\Local\Programs\Python\Python314\Scripts`
   - Click "Aceptar" en todas las ventanas

3. **Reinicia la terminal:**
   - Cierra TODAS las ventanas de terminal
   - Abre una NUEVA terminal
   - Prueba: `python --version`

---

### Opción 3: Deshabilitar el alias de Microsoft Store

Si Windows te redirige a Microsoft Store cuando escribes `python`:

1. Presiona `Win + I` (abre Configuración)
2. Ve a: **Aplicaciones** → **Configuración avanzada de aplicaciones** → **Alias de ejecución de aplicaciones**
3. Busca "App Installer" y desactiva los alias para:
   - `python.exe`
   - `python3.exe`
4. Cierra y vuelve a abrir la terminal

---

## 🎯 Después de solucionar

Una vez que `python --version` funcione, continúa con:

```bash
python -m pip install pyinstaller
```

Y luego ejecuta el script:
```bash
build_installer.bat
```

---

## ❓ ¿Aún no funciona?

Si después de todo esto aún no funciona:

1. **Verifica que Python esté realmente instalado:**
   - Busca "Python" en el menú de inicio
   - Si aparece, haz click derecho → "Abrir ubicación del archivo"
   - Copia esa ruta

2. **Usa la ruta completa:**
   ```bash
   # Reemplaza con tu ruta real
   C:\Users\erica\AppData\Local\Programs\Python\Python314\python.exe -m pip install pyinstaller
   ```

3. **O ejecuta Python directamente:**
   - Abre Python desde el menú de inicio
   - Escribe: `import sys; print(sys.executable)`
   - Esto te mostrará la ruta exacta de Python

---

## 📞 Resumen

1. ✅ Instala Python desde python.org (marca "Add to PATH")
2. ✅ Cierra y vuelve a abrir la terminal
3. ✅ Verifica con: `python --version`
4. ✅ Instala PyInstaller: `python -m pip install pyinstaller`
5. ✅ Ejecuta: `build_installer.bat`

¡Eso es todo! 🎉
