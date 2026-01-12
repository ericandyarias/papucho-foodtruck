"""
Módulo para la selección de productos (centro)
Incluye buscador, categorías y botones de productos
"""
import tkinter as tk
from tkinter import ttk
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.productos import cargar_productos


class Seleccion(ttk.Frame):
    """Frame central para selección de productos"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.productos_data = self.cargar_productos()
        self.categoria_actual = None
        self.configurar_seleccion()
    
    def recargar_productos(self):
        """Recarga los productos desde el archivo JSON"""
        self.productos_data = self.cargar_productos()
        self.cargar_categorias()
        # Si hay una categoría actual, recargarla
        if self.categoria_actual:
            self.mostrar_productos(self.categoria_actual)
        elif self.productos_data.get("categorias"):
            self.mostrar_productos(self.productos_data["categorias"][0]["nombre"])
    
    def cargar_productos(self):
        """Carga los productos desde el archivo JSON usando el módulo de productos"""
        return cargar_productos()
    
    def configurar_seleccion(self):
        """Configura el diseño de la sección de selección"""
        # Configurar grid del frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Frame para el buscador
        """
        frame_buscador = ttk.Frame(self)
        frame_buscador.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        frame_buscador.columnconfigure(1, weight=1)
        
        ttk.Label(
            frame_buscador,
            text="Buscar:",
            font=('Arial', 10)
        ).grid(row=0, column=0, padx=5)
        
        self.entry_buscador = ttk.Entry(frame_buscador, width=30)
        self.entry_buscador.grid(row=0, column=1, sticky='ew', padx=5)
        self.entry_buscador.bind('<KeyRelease>', self.on_buscar)
        """
        # Frame para categorías
        frame_categorias = ttk.LabelFrame(self, text="Categorías", padding=10)
        frame_categorias.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        frame_categorias.columnconfigure(0, weight=1)
        
        self.frame_categorias_btns = ttk.Frame(frame_categorias)
        self.frame_categorias_btns.grid(row=0, column=0, sticky='ew')
        
        self.cargar_categorias()
        
        # Frame para productos
        frame_productos = ttk.LabelFrame(self, text="Productos", padding=10)
        frame_productos.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        
        # Canvas con scrollbar para productos
        self.canvas_productos = tk.Canvas(frame_productos)
        scrollbar = ttk.Scrollbar(frame_productos, orient="vertical", command=self.canvas_productos.yview)
        self.frame_productos = ttk.Frame(self.canvas_productos)
        
        self.frame_productos.bind(
            "<Configure>",
            lambda e: self.canvas_productos.configure(scrollregion=self.canvas_productos.bbox("all"))
        )
        
        # Crear ventana del canvas y configurar para que se expanda
        self.canvas_window = self.canvas_productos.create_window((0, 0), window=self.frame_productos, anchor="nw")
        
        # Función para ajustar el ancho del frame cuando el canvas cambie de tamaño
        def ajustar_ancho_frame(event):
            canvas_width = event.width
            self.canvas_productos.itemconfig(self.canvas_window, width=canvas_width)
        
        self.canvas_productos.bind('<Configure>', ajustar_ancho_frame)
        self.canvas_productos.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_productos.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Configurar grid del frame_productos
        frame_productos.columnconfigure(0, weight=1)
        frame_productos.rowconfigure(0, weight=1)
        
        # Cargar productos de la primera categoría por defecto
        if self.productos_data.get("categorias"):
            self.mostrar_productos(self.productos_data["categorias"][0]["nombre"])
    
    def cargar_categorias(self):
        """Carga los botones de categorías en dos filas responsivas"""
        for widget in self.frame_categorias_btns.winfo_children():
            widget.destroy()
        
        categorias = self.productos_data.get("categorias", [])
        
        if not categorias:
            return
        
        # Calcular número de columnas (máximo 3 por fila para que quepan bien)
        num_columnas = min(3, len(categorias))
        
        # Calcular número de filas necesarias
        num_filas = (len(categorias) + num_columnas - 1) // num_columnas
        
        # Configurar columnas para distribución uniforme
        for i in range(num_columnas):
            self.frame_categorias_btns.columnconfigure(i, weight=1, uniform='categoria')
        
        # Configurar filas
        for i in range(num_filas):
            self.frame_categorias_btns.rowconfigure(i, weight=1)
        
        # Distribuir categorías en filas
        for idx, categoria in enumerate(categorias):
            # Calcular fila y columna
            fila = idx // num_columnas
            columna = idx % num_columnas
            
            btn = ttk.Button(
                self.frame_categorias_btns,
                text=categoria["nombre"],
                command=lambda c=categoria["nombre"]: self.mostrar_productos(c),
                width=15
            )
            btn.grid(row=fila, column=columna, sticky='ew', padx=5, pady=5)
    
    def mostrar_productos(self, categoria_nombre):
        """Muestra los productos de una categoría"""
        self.categoria_actual = categoria_nombre
        
        # Limpiar productos actuales completamente
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        # Actualizar el scrollregion del canvas para limpiar cualquier artefacto visual
        self.canvas_productos.update_idletasks()
        self.canvas_productos.configure(scrollregion=self.canvas_productos.bbox("all"))
        
        # Buscar la categoría
        categoria = None
        for cat in self.productos_data.get("categorias", []):
            if cat["nombre"] == categoria_nombre:
                categoria = cat
                break
        
        if not categoria:
            return
        
        # Configurar grid del frame de productos para que ocupen todo el ancho
        self.frame_productos.columnconfigure(0, weight=1)
        
        # Mostrar productos
        for idx, producto in enumerate(categoria.get("productos", [])):
            frame_producto = ttk.Frame(self.frame_productos, relief='raised', borderwidth=1)
            frame_producto.grid(row=idx, column=0, sticky='ew', padx=5, pady=5)
            frame_producto.columnconfigure(0, weight=1)
            
            # Información del producto
            info_frame = ttk.Frame(frame_producto)
            info_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
            info_frame.columnconfigure(0, weight=1)
            
            ttk.Label(
                info_frame,
                text=producto["nombre"],
                font=('Arial', 11, 'bold')
            ).grid(row=0, column=0, sticky='w')
            
            ttk.Label(
                info_frame,
                text=producto.get("descripcion", ""),
                font=('Arial', 9),
                foreground='gray'
            ).grid(row=1, column=0, sticky='w')
            
            ttk.Label(
                info_frame,
                text=f"${producto['precio']:.2f}",
                font=('Arial', 10, 'bold'),
                foreground='#27ae60'
            ).grid(row=2, column=0, sticky='w')
            
            # Botón agregar
            btn_agregar = ttk.Button(
                frame_producto,
                text="➕ Agregar",
                command=lambda p=producto: self.on_agregar_producto(p)
            )
            btn_agregar.grid(row=0, column=1, padx=10, pady=5, sticky='e')
    
    def on_agregar_producto(self, producto):
        """Callback cuando se agrega un producto al carrito"""
        print(f"Agregando producto: {producto['nombre']}")
        # El callback será asignado desde main.py para conectar con el carrito
        if hasattr(self, 'callback_agregar_carrito'):
            self.callback_agregar_carrito(producto)
    
    def on_buscar(self, event=None):
        """Callback cuando se escribe en el buscador"""
        busqueda = self.entry_buscador.get().lower()
        print(f"Buscando: {busqueda}")
        # TODO: Implementar lógica de búsqueda
