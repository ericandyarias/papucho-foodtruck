"""
Script simple para probar la impresión de un ticket de prueba
Usa la función imprimir_ticket_prueba() del módulo tickets
"""
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(__file__))

from utils.tickets import imprimir_ticket_prueba

if __name__ == "__main__":
    print("Probando impresion de ticket simple...")
    print("=" * 50)
    
    exito = imprimir_ticket_prueba()
    
    if exito:
        print("\n[OK] Ticket de prueba impreso exitosamente!")
        print("Verifica que el ticket se haya impreso en la impresora XP-80C")
    else:
        print("\n[ERROR] No se pudo imprimir el ticket de prueba")
        print("Revisa los mensajes de error anteriores")
    
    sys.exit(0 if exito else 1)
