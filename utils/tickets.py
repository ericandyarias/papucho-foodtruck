"""
Módulo para generar tickets de pedidos usando python-escpos con Win32Raw
Genera tickets en formato ESC/POS para impresoras térmicas (80mm)
Impresión directa sin previsualización, ocupando todo el ancho del papel
Usa Win32Raw para imprimir por nombre de impresora en Windows
"""
import os
import sys
import json
from datetime import datetime

try:
    from escpos.printer import Win32Raw
    from escpos.exceptions import Error
    ESCPOS_AVAILABLE = True
except ImportError:
    ESCPOS_AVAILABLE = False
    print("Advertencia: python-escpos no está instalado. Ejecuta: pip install python-escpos")


def obtener_ruta_tickets():
    """Obtiene la ruta del directorio de tickets"""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'tickets'
    )


def obtener_ruta_config():
    """Obtiene la ruta del archivo de configuración"""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'config.json'
    )


def cargar_configuracion():
    """Carga la configuración desde el archivo JSON"""
    ruta_config = obtener_ruta_config()
    try:
        with open(ruta_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        # Configuración por defecto si no existe el archivo
        config_default = {
            "impresora": {
                "ancho_ticket": 80,
                "modelo": "Xprinter EX-E200M",
                "nombre_impresora": "XP-80C"  # Nombre de la impresora en Windows
            },
            "tickets": {
                "incluir_fecha_hora": True,
                "lineas_corte": 3
            }
        }
        # Crear el archivo de configuración
        os.makedirs(os.path.dirname(ruta_config), exist_ok=True)
        with open(ruta_config, 'w', encoding='utf-8') as f:
            json.dump(config_default, f, indent=2, ensure_ascii=False)
        return config_default
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        # Retornar configuración por defecto
        return {
            "impresora": {
                "ancho_ticket": 80,
                "modelo": "Xprinter EX-E200M",
                "nombre_impresora": "XP-80C"
            },
            "tickets": {"incluir_fecha_hora": True, "lineas_corte": 3}
        }


def listar_impresoras_windows():
    """
    Lista todas las impresoras disponibles en Windows
    Retorna lista de nombres de impresoras
    """
    if sys.platform != 'win32':
        return []
    
    try:
        import win32print
        impresoras = []
        impresoras_raw = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        for impresora in impresoras_raw:
            impresoras.append(impresora[2])  # El nombre está en el índice 2
        return impresoras
    except ImportError:
        print("Advertencia: pywin32 no está instalado. Ejecuta: pip install pywin32")
        return []
    except Exception as e:
        print(f"Error al listar impresoras: {e}")
        return []


def verificar_impresora_existe(nombre_impresora):
    """
    Verifica si una impresora existe en Windows
    Retorna True si existe, False en caso contrario
    """
    if sys.platform != 'win32':
        return False
    
    try:
        import win32print
        impresoras = listar_impresoras_windows()
        return nombre_impresora in impresoras
    except Exception as e:
        print(f"Error al verificar impresora: {e}")
        return False


def obtener_impresora():
    """
    Obtiene la conexión a la impresora usando Win32Raw
    Retorna objeto printer o None si hay error
    """
    if not ESCPOS_AVAILABLE:
        print("Error: python-escpos no está disponible")
        return None
    
    if sys.platform != 'win32':
        print("Error: Win32Raw solo está disponible en Windows")
        return None
    
    config = cargar_configuracion()
    nombre_impresora = config.get('impresora', {}).get('nombre_impresora', 'XP-80C')
    
    if not nombre_impresora:
        print("Error: No se ha configurado el nombre de la impresora")
        print("Configura 'nombre_impresora' en data/config.json")
        return None
    
    # Verificar que la impresora existe
    if not verificar_impresora_existe(nombre_impresora):
        print(f"Error: La impresora '{nombre_impresora}' no se encuentra en el sistema")
        print("\nImpresoras disponibles:")
        impresoras = listar_impresoras_windows()
        if impresoras:
            for imp in impresoras:
                print(f"  - {imp}")
        else:
            print("  (No se pudieron listar las impresoras)")
        print(f"\nActualiza 'nombre_impresora' en data/config.json con el nombre correcto")
        return None
    
    try:
        printer = Win32Raw(nombre_impresora)
        return printer
    except Error as e:
        print(f"Error al conectar con la impresora '{nombre_impresora}': {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al conectar con la impresora: {e}")
        return None


def formatear_texto_centrado(texto, ancho=48):
    """
    Formatea texto centrado para impresora térmica
    ancho: ancho en caracteres (48 para impresora de 80mm)
    """
    texto = str(texto)
    if len(texto) >= ancho:
        return texto[:ancho]
    
    espacios_izq = (ancho - len(texto)) // 2
    espacios_der = ancho - len(texto) - espacios_izq
    return ' ' * espacios_izq + texto + ' ' * espacios_der


def formatear_linea_producto(nombre, cantidad, precio, ancho=48):
    """
    Formatea una línea de producto con nombre a la izquierda y precio a la derecha
    ancho: ancho total en caracteres
    """
    nombre_cantidad = f"{nombre} x{cantidad}"
    precio_str = f"${precio:,.2f}"
    
    # Calcular espacios necesarios
    espacio_total = ancho - len(nombre_cantidad) - len(precio_str)
    
    if espacio_total < 1:
        # Si no cabe, truncar nombre
        max_nombre = ancho - len(precio_str) - 10  # 10 para " x1" y espacios
        nombre_cantidad = nombre_cantidad[:max_nombre] + "..."
        espacio_total = ancho - len(nombre_cantidad) - len(precio_str)
    
    return nombre_cantidad + ' ' * espacio_total + precio_str


def tiene_modificaciones_reales(producto, modificaciones):
    """
    Verifica si un producto tiene modificaciones reales de ingredientes
    (es decir, si alguna cantidad difiere de la cantidad base)
    
    Args:
        producto: Diccionario del producto con ingredientes
        modificaciones: Dict con {nombre_ingrediente: cantidad_actual}
    
    Returns:
        bool: True si hay modificaciones reales, False en caso contrario
    """
    if not modificaciones or not producto.get('ingredientes'):
        return False
    
    ingredientes = producto.get('ingredientes', [])
    for ingrediente in ingredientes:
        nombre = ingrediente.get('nombre', '')
        cantidad_base = ingrediente.get('cantidad_base', 1)
        cantidad_actual = modificaciones.get(nombre, cantidad_base)
        
        if cantidad_actual != cantidad_base:
            return True
    
    return False


def formatear_linea_ingrediente(nombre_ing, cantidad_mod, es_extra, ajuste, ancho=48):
    """
    Formatea una línea de ingrediente modificado con precio alineado a la derecha
    Formato:   + Nombre xCant              +$Precio
    o:         - Nombre                    -$Precio
    
    Args:
        nombre_ing: Nombre del ingrediente
        cantidad_mod: Cantidad modificada (extras o quitados)
        es_extra: True si es extra, False si es quitado
        ajuste: Precio del ajuste (positivo para extra, negativo para quitar)
        ancho: Ancho total en caracteres
    
    Returns:
        str: Línea formateada con precio alineado a la derecha
    """
    # Prefijo: "  + " o "  - "
    prefijo = "  + " if es_extra else "  - "
    
    # Construir parte izquierda: prefijo + nombre + cantidad (si aplica)
    parte_izq = prefijo + nombre_ing
    if cantidad_mod > 1:
        parte_izq += f" x{cantidad_mod}"
    
    # Parte derecha: precio con signo
    if es_extra:
        precio_str = f"+${abs(ajuste):,.2f}"
    else:
        precio_str = f"-${abs(ajuste):,.2f}"
    
    # Columna fija para precios: 38-48 (10 caracteres)
    columna_precio_inicio = 38
    max_ancho_parte_izq = columna_precio_inicio - 1
    
    # Si la parte izquierda es muy larga, truncar
    if len(parte_izq) > max_ancho_parte_izq:
        parte_izq = parte_izq[:max_ancho_parte_izq - 3] + "..."
    
    # Calcular espacios para alinear precio a la derecha
    espacios = max(1, columna_precio_inicio - len(parte_izq))
    
    return parte_izq + ' ' * espacios + precio_str


def formatear_linea_subtotal(precio_unitario, cantidad, subtotal, ancho=48):
    """
    Formatea la línea de subtotal para productos editados
    Formato: $ precio_unitario   x cantidad     =     $ subtotal
    El precio unitario se alinea a la derecha
    
    Args:
        precio_unitario: Precio unitario del producto (con modificaciones)
        cantidad: Cantidad del producto
        subtotal: Total del producto (precio_unitario * cantidad)
        ancho: Ancho total en caracteres
    
    Returns:
        str: Línea formateada
    """
    precio_str = f"${precio_unitario:,.2f}"
    cantidad_str = f"x {cantidad}"
    subtotal_str = f"=     ${subtotal:,.2f}"
    
    # Calcular espacios para alinear precio a la derecha
    # Estructura: espacios_izq + precio_str + espacios1 + cantidad_str + espacios2 + subtotal_str
    # El precio debe quedar alineado a la derecha, luego espacios, luego cantidad, luego espacios, luego subtotal
    
    # Calcular el ancho necesario para precio + espacios + cantidad
    ancho_precio_cantidad = len(precio_str) + 3 + len(cantidad_str)  # 3 espacios entre precio y cantidad
    
    # Calcular espacios para alinear el precio a la derecha
    # Queremos que el precio esté cerca del centro-izquierda, pero alineado
    espacios_izq = max(0, ancho - len(precio_str) - 3 - len(cantidad_str) - len(subtotal_str) - 5)
    espacios1 = 3  # Espacios fijos entre precio y cantidad
    espacios2 = 5  # Espacios fijos entre cantidad y "="
    
    return ' ' * espacios_izq + precio_str + ' ' * espacios1 + cantidad_str + ' ' * espacios2 + subtotal_str


def imprimir_ticket_escpos(pedido_info, tipo_ticket):
    """
    Imprime un ticket directamente usando ESC/POS con Win32Raw
    
    Args:
        pedido_info: Diccionario con la información del pedido
        tipo_ticket: 'COCINA' o 'CLIENTE'
    
    Returns:
        bool: True si la impresión fue exitosa, False en caso contrario
    """
    if not ESCPOS_AVAILABLE:
        print("Error: python-escpos no está disponible")
        return False
    
    if sys.platform != 'win32':
        print("Error: Win32Raw solo está disponible en Windows")
        return False
    
    printer = None
    try:
        printer = obtener_impresora()
        if not printer:
            return False
        
        config = cargar_configuracion()
        ancho_caracteres = 48  # Ancho estándar para impresora de 80mm
        
        # Inicializar impresora
        printer.set(align='center', font='a', width=2, height=2, bold=True)
        printer.text("PAPUCHO FOODTRUCK\n")
        
        # Separador grueso
        printer.set(align='center')
        printer.text("=" * ancho_caracteres + "\n")
        
        # Número de orden
        printer.set(align='center', font='a', width=2, height=1, bold=True)
        printer.text(f"Orden #{pedido_info['numero']:04d}\n")
        
        # Separador
        printer.set(align='center')
        printer.text("=" * ancho_caracteres + "\n")
        
        # Cliente
        printer.set(align='left', font='a', width=1, height=1, bold=False)
        printer.text(f"Cliente: {pedido_info['nombre_cliente']}\n")
        
        # Domicilio si existe
        if pedido_info.get('domicilio'):
            domicilio = pedido_info['domicilio']
            # Si el domicilio es muy largo, dividirlo en líneas
            if len(domicilio) > ancho_caracteres - 12:
                palabras = domicilio.split()
                linea = "Domicilio: "
                for palabra in palabras:
                    if len(linea) + len(palabra) + 1 > ancho_caracteres:
                        printer.text(linea + "\n")
                        linea = "  " + palabra
                    else:
                        linea += " " + palabra if linea != "Domicilio: " else palabra
                printer.text(linea + "\n")
            else:
                printer.text(f"Domicilio: {domicilio}\n")
        
        # Separador
        printer.text("-" * ancho_caracteres + "\n")
        
        # PEDIDO
        printer.set(align='left', bold=True)
        printer.text("PEDIDO:\n")
        printer.set(bold=False)
        printer.text("-" * ancho_caracteres + "\n")
        
        # Items del pedido
        for item in pedido_info['items']:
            producto = item['producto']
            nombre = producto['nombre']
            cantidad = item['cantidad']
            modificaciones = item.get('modificaciones_ingredientes', {})
            
            # Calcular precio unitario y subtotal considerando ingredientes
            from utils.productos import calcular_precio_con_ingredientes
            precio_unitario = calcular_precio_con_ingredientes(producto, modificaciones)
            subtotal = precio_unitario * cantidad
            
            # Verificar si tiene modificaciones reales
            tiene_modificaciones = tiene_modificaciones_reales(producto, modificaciones)
            
            if tiene_modificaciones:
                # Formato especial para productos editados
                # Mostrar solo el nombre del producto
                printer.text(nombre + "\n")
                
                # Mostrar modificaciones de ingredientes
                ingredientes = producto.get('ingredientes', [])
                if ingredientes and modificaciones:
                    for ingrediente in ingredientes:
                        nombre_ing = ingrediente.get('nombre', '')
                        cantidad_base = ingrediente.get('cantidad_base', 1)
                        cantidad_actual = modificaciones.get(nombre_ing, cantidad_base)
                        precio_extra = ingrediente.get('precio_extra', 0.0)
                        precio_resta = ingrediente.get('precio_resta', 0.0)
                        
                        if cantidad_actual > cantidad_base:
                            # Extras agregados
                            extras = cantidad_actual - cantidad_base
                            ajuste = extras * precio_extra
                            texto_ing = formatear_linea_ingrediente(
                                nombre_ing, extras, True, ajuste, ancho_caracteres
                            )
                            printer.text(texto_ing + "\n")
                        elif cantidad_actual < cantidad_base:
                            # Ingredientes quitados
                            quitados = cantidad_base - cantidad_actual
                            ajuste = quitados * precio_resta
                            texto_ing = formatear_linea_ingrediente(
                                nombre_ing, quitados, False, ajuste, ancho_caracteres
                            )
                            printer.text(texto_ing + "\n")
                
                # Mostrar línea de subtotal: precio_unitario x cantidad = subtotal
                linea_subtotal = formatear_linea_subtotal(precio_unitario, cantidad, subtotal, ancho_caracteres)
                printer.text(linea_subtotal + "\n")
            else:
                # Formato normal para productos sin editar
                linea = formatear_linea_producto(nombre, cantidad, subtotal, ancho_caracteres)
                printer.text(linea + "\n")
        
        # Separador
        printer.text("-" * ancho_caracteres + "\n")
        
        # Total a pagar
        total = pedido_info['total']
        printer.set(align='left', bold=True)
        printer.text("TOTAL A PAGAR:")
        printer.set(align='right', bold=True)
        printer.text(f"${total:,.2f}\n")
        
        # Separador
        printer.set(align='center')
        printer.text("-" * ancho_caracteres + "\n")
        
        # Forma de pago
        printer.set(align='left', bold=False)
        printer.text(f"Forma de Pago: {pedido_info['forma_pago']}\n")
        
        # Separador grueso
        printer.set(align='center')
        printer.text("=" * ancho_caracteres + "\n")
        
        # Marca del ticket (COCINA o CLIENTE)
        printer.set(align='center', font='a', width=1, height=1, bold=True)
        printer.text(f"=== {tipo_ticket} ===\n")
        
        # Fecha y hora si está habilitado
        if config.get('tickets', {}).get('incluir_fecha_hora', True):
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            printer.set(align='center', font='a', width=1, height=1, bold=False)
            printer.text(fecha_hora + "\n")
        
        # Separador final
        printer.set(align='center')
        printer.text("=" * ancho_caracteres + "\n")
        
        # Espacios antes del corte
        lineas_corte = config.get('tickets', {}).get('lineas_corte', 3)
        for _ in range(lineas_corte):
            printer.text("\n")
        
        # Cortar papel
        printer.cut()
        
        # Cerrar conexión
        printer.close()
        
        return True
        
    except Error as e:
        print(f"Error ESC/POS al imprimir ticket: {e}")
        if printer:
            try:
                printer.close()
            except:
                pass
        return False
    except Exception as e:
        print(f"Error inesperado al imprimir ticket: {e}")
        if printer:
            try:
                printer.close()
            except:
                pass
        return False


def guardar_ticket_texto(pedido_info, tipo_ticket):
    """
    Guarda el ticket en un archivo de texto plano (opcional, para respaldo)
    
    Args:
        pedido_info: Diccionario con la información del pedido
        tipo_ticket: 'COCINA' o 'CLIENTE'
    
    Returns:
        str: Ruta del archivo guardado
    """
    # Asegurar que el directorio existe
    directorio_tickets = obtener_ruta_tickets()
    os.makedirs(directorio_tickets, exist_ok=True)
    
    # Generar nombre del archivo
    numero_orden = pedido_info['numero']
    nombre_archivo = f"ticket_{tipo_ticket.lower()}_{numero_orden:04d}.txt"
    ruta_archivo = os.path.join(directorio_tickets, nombre_archivo)
    
    # Generar contenido del ticket en texto plano
    config = cargar_configuracion()
    ancho_caracteres = 48
    
    contenido = []
    contenido.append("=" * ancho_caracteres)
    contenido.append(formatear_texto_centrado("PAPUCHO FOODTRUCK", ancho_caracteres))
    contenido.append("=" * ancho_caracteres)
    contenido.append(formatear_texto_centrado(f"Orden #{pedido_info['numero']:04d}", ancho_caracteres))
    contenido.append("=" * ancho_caracteres)
    contenido.append(f"Cliente: {pedido_info['nombre_cliente']}")
    
    if pedido_info.get('domicilio'):
        contenido.append(f"Domicilio: {pedido_info['domicilio']}")
    
    contenido.append("-" * ancho_caracteres)
    contenido.append("PEDIDO:")
    contenido.append("-" * ancho_caracteres)
    
    for item in pedido_info['items']:
        producto = item['producto']
        nombre = producto['nombre']
        cantidad = item['cantidad']
        modificaciones = item.get('modificaciones_ingredientes', {})
        
        # Calcular precio unitario y subtotal considerando ingredientes
        from utils.productos import calcular_precio_con_ingredientes
        precio_unitario = calcular_precio_con_ingredientes(producto, modificaciones)
        subtotal = precio_unitario * cantidad
        
        # Verificar si tiene modificaciones reales
        tiene_modificaciones = tiene_modificaciones_reales(producto, modificaciones)
        
        if tiene_modificaciones:
            # Formato especial para productos editados
            # Mostrar solo el nombre del producto
            contenido.append(nombre)
            
            # Mostrar modificaciones de ingredientes
            ingredientes = producto.get('ingredientes', [])
            if ingredientes and modificaciones:
                for ingrediente in ingredientes:
                    nombre_ing = ingrediente.get('nombre', '')
                    cantidad_base = ingrediente.get('cantidad_base', 1)
                    cantidad_actual = modificaciones.get(nombre_ing, cantidad_base)
                    precio_extra = ingrediente.get('precio_extra', 0.0)
                    precio_resta = ingrediente.get('precio_resta', 0.0)
                    
                    if cantidad_actual > cantidad_base:
                        # Extras agregados
                        extras = cantidad_actual - cantidad_base
                        ajuste = extras * precio_extra
                        texto_ing = formatear_linea_ingrediente(
                            nombre_ing, extras, True, ajuste, ancho_caracteres
                        )
                        contenido.append(texto_ing)
                    elif cantidad_actual < cantidad_base:
                        # Ingredientes quitados
                        quitados = cantidad_base - cantidad_actual
                        ajuste = quitados * precio_resta
                        texto_ing = formatear_linea_ingrediente(
                            nombre_ing, quitados, False, ajuste, ancho_caracteres
                        )
                        contenido.append(texto_ing)
            
            # Mostrar línea de subtotal: precio_unitario x cantidad = subtotal
            linea_subtotal = formatear_linea_subtotal(precio_unitario, cantidad, subtotal, ancho_caracteres)
            contenido.append(linea_subtotal)
        else:
            # Formato normal para productos sin editar
            linea = formatear_linea_producto(nombre, cantidad, subtotal, ancho_caracteres)
            contenido.append(linea)
    
    contenido.append("-" * ancho_caracteres)
    total = pedido_info['total']
    linea_total = "TOTAL A PAGAR:" + " " * (ancho_caracteres - len("TOTAL A PAGAR:") - len(f"${total:,.2f}")) + f"${total:,.2f}"
    contenido.append(linea_total)
    contenido.append("-" * ancho_caracteres)
    contenido.append(f"Forma de Pago: {pedido_info['forma_pago']}")
    contenido.append("=" * ancho_caracteres)
    contenido.append(formatear_texto_centrado(f"=== {tipo_ticket} ===", ancho_caracteres))
    
    if config.get('tickets', {}).get('incluir_fecha_hora', True):
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        contenido.append(formatear_texto_centrado(fecha_hora, ancho_caracteres))
    
    contenido.append("=" * ancho_caracteres)
    
    # Guardar en archivo
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write('\n'.join(contenido))
    
    return ruta_archivo


def generar_tickets_pedido(pedido_info, imprimir_automatico=True, guardar_respaldo=True):
    """
    Genera ambos tickets (COCINA y CLIENTE) para un pedido e imprime directamente
    
    Args:
        pedido_info: Diccionario con la información del pedido
        imprimir_automatico: Si es True, imprime automáticamente los tickets
        guardar_respaldo: Si es True, guarda archivos .txt de respaldo
    
    Returns:
        dict: Diccionario con las rutas de los archivos generados (si aplica) y estado de impresión
    """
    resultado = {
        'cocina': None,
        'cliente': None,
        'impresion_cocina': False,
        'impresion_cliente': False
    }
    
    # Guardar respaldo en archivos de texto si está habilitado
    if guardar_respaldo:
        try:
            resultado['cocina'] = guardar_ticket_texto(pedido_info, 'COCINA')
            resultado['cliente'] = guardar_ticket_texto(pedido_info, 'CLIENTE')
        except Exception as e:
            print(f"Error al guardar tickets de respaldo: {e}")
    
    # Imprimir automáticamente si está habilitado
    if imprimir_automatico:
        resultado['impresion_cocina'] = imprimir_ticket_escpos(pedido_info, 'COCINA')
        # Pequeña pausa entre impresiones
        import time
        time.sleep(0.5)
        resultado['impresion_cliente'] = imprimir_ticket_escpos(pedido_info, 'CLIENTE')
    
    return resultado


def imprimir_ticket_prueba():
    """
    Imprime un ticket de prueba simple
    Retorna True si fue exitoso, False en caso contrario
    """
    if not ESCPOS_AVAILABLE:
        print("Error: python-escpos no está disponible")
        return False
    
    if sys.platform != 'win32':
        print("Error: Win32Raw solo está disponible en Windows")
        return False
    
    printer = None
    try:
        printer = obtener_impresora()
        if not printer:
            return False
        
        printer.set(align='center', font='a', width=1, height=1, bold=True)
        printer.text("TICKET DE PRUEBA\n")
        printer.text("Impresora XP-80C\n")
        printer.text("\n\n")
        printer.cut()
        
        printer.close()
        print("Ticket de prueba impreso exitosamente")
        return True
        
    except Error as e:
        print(f"Error ESC/POS al imprimir ticket de prueba: {e}")
        if printer:
            try:
                printer.close()
            except:
                pass
        return False
    except Exception as e:
        print(f"Error inesperado al imprimir ticket de prueba: {e}")
        if printer:
            try:
                printer.close()
            except:
                pass
        return False
