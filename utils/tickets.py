"""
Módulo para generar tickets de pedidos en HTML
Genera tickets en formato HTML para impresoras térmicas (80mm)
Aprovecha todo el ancho del papel con márgenes mínimos
"""
import os
import subprocess
import sys
import json
from datetime import datetime


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
                "modelo": "POS-80"
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
            "impresora": {"ancho_ticket": 80, "modelo": "POS-80"},
            "tickets": {"incluir_fecha_hora": True, "lineas_corte": 3}
        }


def generar_html_ticket(pedido_info, tipo_ticket):
    """
    Genera el ticket en formato HTML para impresión
    
    Args:
        pedido_info: Diccionario con la información del pedido
        tipo_ticket: 'COCINA' o 'CLIENTE'
    
    Returns:
        str: HTML del ticket formateado
    """
    config = cargar_configuracion()
    color_marca = '#e74c3c' if tipo_ticket == 'COCINA' else '#27ae60'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ticket {tipo_ticket} #{pedido_info['numero']:04d}</title>
    <style>
        @page {{
            size: 80mm auto;
            margin: 2mm 2mm 2mm 2mm;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.3;
            width: 100%;
            padding: 2mm;
        }}
        .ticket {{
            width: 100%;
        }}
        .center {{
            text-align: center;
        }}
        .bold {{
            font-weight: bold;
        }}
        .separador {{
            border-top: 1px solid #000;
            margin: 3px 0;
        }}
        .separador-grueso {{
            border-top: 2px solid #000;
            margin: 3px 0;
        }}
        .titulo {{
            font-size: 11pt;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .orden {{
            font-size: 10pt;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 8px;
        }}
        .item {{
            margin: 8px 0;
        }}
        .item-nombre {{
            margin-bottom: 2px;
        }}
        .item-precio {{
            text-align: right;
            font-weight: bold;
        }}
        .total {{
            margin-top: 8px;
            padding-top: 5px;
        }}
        .total-label {{
            font-weight: bold;
        }}
        .total-monto {{
            text-align: right;
            font-weight: bold;
            font-size: 10pt;
        }}
        .marca {{
            color: {color_marca};
            font-weight: bold;
            font-size: 10pt;
            margin-top: 8px;
        }}
        .fecha {{
            font-size: 8pt;
            color: #666;
            margin-top: 5px;
        }}
        .espaciado {{
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="ticket">
        <div class="center titulo">PAPUCHO FOODTRUCK</div>
        <div class="separador-grueso"></div>
        <div class="center orden">Orden #{pedido_info['numero']:04d}</div>
        
        <div class="espaciado">
            <strong>Cliente:</strong> {pedido_info['nombre_cliente']}
        </div>
"""
    
    # Domicilio si existe
    if pedido_info.get('domicilio'):
        html += f"""        <div>
            <strong>Domicilio:</strong> {pedido_info['domicilio']}
        </div>
"""
    
    html += """        
        <div class="separador"></div>
        <div class="bold espaciado">PEDIDO:</div>
"""
    
    # Items del pedido
    for item in pedido_info['items']:
        subtotal = item['producto']['precio'] * item['cantidad']
        html += f"""        
        <div class="item">
            <div class="item-nombre">{item['producto']['nombre']} x{item['cantidad']}</div>
            <div class="item-precio">${subtotal:.2f}</div>
        </div>
"""
    
    # Total y forma de pago
    html += f"""        
        <div class="separador"></div>
        <div class="total">
            <div class="total-label">TOTAL A PAGAR:</div>
            <div class="total-monto">${pedido_info['total']:.2f}</div>
        </div>
        <div class="espaciado">
            <strong>Forma de Pago:</strong> {pedido_info['forma_pago']}
        </div>
        
        <div class="separador-grueso"></div>
        <div class="center marca">=== {tipo_ticket} ===</div>
"""
    
    # Fecha y hora si está habilitado
    if config.get('tickets', {}).get('incluir_fecha_hora', True):
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        html += f"""        <div class="center fecha">{fecha_hora}</div>
"""
    
    html += """    </div>
</body>
</html>"""
    
    return html


def guardar_ticket(pedido_info, tipo_ticket):
    """
    Guarda el ticket en un archivo HTML
    
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
    nombre_archivo = f"ticket_{tipo_ticket.lower()}_{numero_orden:04d}.html"
    ruta_archivo = os.path.join(directorio_tickets, nombre_archivo)
    
    # Generar HTML del ticket
    html_ticket = generar_html_ticket(pedido_info, tipo_ticket)
    
    # Guardar en archivo
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(html_ticket)
    
    return ruta_archivo


def imprimir_ticket(ruta_archivo, nombre_impresora=None):
    """
    Imprime un ticket HTML directamente de forma completamente invisible
    
    Args:
        ruta_archivo: Ruta del archivo HTML del ticket
        nombre_impresora: Nombre de la impresora (opcional, usa la predeterminada si es None)
    
    Returns:
        bool: True si la impresión fue exitosa, False en caso contrario
    """
    try:
        if sys.platform == 'win32':
            # Windows: usar PowerShell con IE COM completamente oculto
            ruta_absoluta = os.path.abspath(ruta_archivo)
            
            # Script PowerShell mejorado para impresión completamente silenciosa
            ps_script = f'''
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
"@

$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $false
$ie.Silent = $true
$ie.Navigate("{ruta_absoluta}")

while($ie.Busy -or $ie.ReadyState -ne 4) {{ 
    Start-Sleep -Milliseconds 50 
}}

Start-Sleep -Milliseconds 800

try {{
    $ie.ExecWB(6, 2)
}} catch {{}}

Start-Sleep -Milliseconds 800

try {{
    $ie.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ie) | Out-Null
}} catch {{}}

[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
'''
            
            # Ejecutar PowerShell en proceso separado completamente oculto
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-NoProfile', '-NonInteractive', '-Command', ps_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            return True
        else:
            # Linux/Mac: usar lpr con el archivo HTML
            if nombre_impresora:
                subprocess.run(
                    ['lpr', '-P', nombre_impresora, ruta_archivo],
                    check=True,
                    capture_output=True,
                    timeout=10
                )
            else:
                subprocess.run(
                    ['lpr', ruta_archivo],
                    check=True,
                    capture_output=True,
                    timeout=10
                )
            return True
    except Exception as e:
        print(f"Error al imprimir: {e}")
        return False


def generar_tickets_pedido(pedido_info, imprimir_automatico=True, nombre_impresora=None):
    """
    Genera ambos tickets (COCINA y CLIENTE) para un pedido
    
    Args:
        pedido_info: Diccionario con la información del pedido
        imprimir_automatico: Si es True, imprime automáticamente los tickets
        nombre_impresora: Nombre de la impresora (opcional, usa la predeterminada si es None)
    
    Returns:
        dict: Diccionario con las rutas de los archivos generados y estado de impresión
    """
    ruta_cocina = guardar_ticket(pedido_info, 'COCINA')
    ruta_cliente = guardar_ticket(pedido_info, 'CLIENTE')
    
    resultado = {
        'cocina': ruta_cocina,
        'cliente': ruta_cliente,
        'impresion_cocina': False,
        'impresion_cliente': False
    }
    
    # Imprimir automáticamente si está habilitado
    if imprimir_automatico:
        resultado['impresion_cocina'] = imprimir_ticket(ruta_cocina, nombre_impresora)
        resultado['impresion_cliente'] = imprimir_ticket(ruta_cliente, nombre_impresora)
    
    return resultado
