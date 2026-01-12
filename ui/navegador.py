"""
Módulo para la barra de navegación lateral izquierda
Contiene los botones principales: Pedidos y Administración
"""
import tkinter as tk
from tkinter import ttk


class Navegador(ttk.Frame):
    """Frame de navegación lateral con botones principales"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.callback_administracion = None
        self.configurar_navegador()
    
    def configurar_navegador(self):
        """Configura el diseño del navegador"""
        # Configurar estilo del frame
        self.config(relief='sunken', borderwidth=2, width=200)
        
        # Título de la sección
        titulo_seccion = ttk.Label(
            self,
            text="Menú Principal",
            font=('Arial', 12, 'bold')
        )
        titulo_seccion.pack(pady=10)
        
        # Botón Pedidos
        self.btn_pedidos = ttk.Button(
            self,
            text="📋 Pedidos",
            width=20,
            command=self.on_pedidos_click
        )
        self.btn_pedidos.pack(pady=10, padx=10)
        
        # Botón Administración
        self.btn_administracion = ttk.Button(
            self,
            text="⚙️ Administración",
            width=20,
            command=self.on_administracion_click
        )
        self.btn_administracion.pack(pady=10, padx=10)
        
        # Espaciador
        ttk.Label(self, text="").pack(expand=True)
    
    def on_pedidos_click(self):
        """Callback cuando se hace clic en Pedidos"""
        print("Navegando a: Pedidos")
        # TODO: Implementar lógica de navegación
    
    def on_administracion_click(self):
        """Callback cuando se hace clic en Administración"""
        if self.callback_administracion:
            self.callback_administracion()
