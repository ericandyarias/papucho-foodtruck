"""
Sistema de Caja para Foodtruck - PAPUCHO FOODTRUCK
Aplicación principal que integra todos los componentes de la UI
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.encabezado import Encabezado
from ui.navegador import Navegador
from ui.seleccion import Seleccion
from ui.carrito import Carrito
from ui.administracion import VentanaAdministracion
from utils.productos import cargar_productos


class AplicacionCaja:
    """Clase principal de la aplicación de caja"""
    
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.crear_componentes()
        self.configurar_layout()
    
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("PAPUCHO FOODTRUCK - Sistema de Caja")
        # Pantalla completa
        self.root.state('zoomed')  # Windows
        # Alternativa para Linux/Mac: self.root.attributes('-zoomed', True)
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar colores personalizados
        estilo.configure('Accent.TButton', foreground='white')
    
    def crear_componentes(self):
        """Crea todos los componentes de la UI"""
        # Encabezado (arriba, ancho completo)
        self.encabezado = Encabezado(self.root)
        
        # Frame principal para el contenido
        self.frame_principal = ttk.Frame(self.root)
        
        # Navegador (izquierda)
        self.navegador = Navegador(self.frame_principal)
        
        # Selección de productos (centro)
        self.seleccion = Seleccion(self.frame_principal)
        
        # Carrito (derecha)
        self.carrito = Carrito(self.frame_principal)
        
        # Conectar componentes
        self.conectar_componentes()
    
    def conectar_componentes(self):
        """Conecta los componentes entre sí"""
        # Hacer que la selección pueda agregar items al carrito
        self.seleccion.callback_agregar_carrito = self.carrito.agregar_item
        
        # Conectar navegador con administración
        self.navegador.callback_administracion = self.abrir_administracion
    
    def abrir_administracion(self):
        """Abre la ventana de administración"""
        VentanaAdministracion(
            self.root,
            callback_actualizar=self.actualizar_productos
        )
    
    def actualizar_productos(self):
        """Actualiza los productos en la selección cuando se modifican en administración"""
        self.seleccion.recargar_productos()
    
    def configurar_layout(self):
        """Configura el layout usando grid"""
        # Encabezado en la fila 0, columnas 0-2
        self.encabezado.grid(row=0, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # Frame principal en la fila 1
        self.frame_principal.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        
        # Configurar grid del frame principal
        self.frame_principal.columnconfigure(1, weight=3)  # Selección (centro) - reducido
        self.frame_principal.columnconfigure(0, weight=2)  # Navegador
        self.frame_principal.columnconfigure(2, weight=2)  # Carrito - más ancho
        self.frame_principal.rowconfigure(0, weight=1)
        
        # Navegador (columna 0)
        self.navegador.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Selección (columna 1)
        self.seleccion.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Carrito (columna 2)
        self.carrito.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        
        # Configurar grid de la ventana principal
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)


def main():
    """Función principal"""
    # Asegurar que las categorías fijas existan al iniciar
    cargar_productos()
    
    root = tk.Tk()
    app = AplicacionCaja(root)
    root.mainloop()


if __name__ == "__main__":
    main()
