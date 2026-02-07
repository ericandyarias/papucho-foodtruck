"""
Módulo para la selección de productos (centro)
Incluye buscador, categorías y botones de productos
"""
import tkinter as tk
from tkinter import ttk
import os
import sys
import threading

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.productos import cargar_productos
from utils.imagenes import cargar_imagen_tkinter


class Seleccion(ttk.Frame):
    """Frame central para selección de productos"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.productos_data = self.cargar_productos()
        self.categoria_actual = None
        self._imagenes_productos = []  # Lista para mantener referencias de imágenes
        self._imagenes_cargando = {}  # Dict para rastrear qué imágenes se están cargando
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
        frame_buscador = ttk.Frame(self)
        frame_buscador.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        frame_buscador.columnconfigure(1, weight=1)
        
        ttk.Label(
            frame_buscador,
            text="🔍 Buscar:",
            font=('Arial', 10)
        ).grid(row=0, column=0, padx=5)
        
        self.entry_buscador = ttk.Entry(frame_buscador, width=30)
        self.entry_buscador.grid(row=0, column=1, sticky='ew', padx=5)
        self.entry_buscador.bind('<KeyRelease>', self.on_buscar)
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
            
            # Comportamiento especial para "Otros"
            if categoria["nombre"].lower() == "personalizados":
                btn = ttk.Button(
                    self.frame_categorias_btns,
                    text=categoria["nombre"],
                    command=self.mostrar_ventana_producto_personalizado,
                    width=15
                )
            else:
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
        
        # Limpiar referencias de imágenes anteriores
        self._imagenes_productos.clear()
        self._imagenes_cargando.clear()
        
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
        
        # Mostrar productos de la categoría
        self.mostrar_lista_productos(categoria.get("productos", []))
    
    def mostrar_lista_productos(self, productos):
        """Muestra una lista de productos (usado tanto para categorías como para búsqueda)"""
        # Limpiar productos actuales
        for widget in self.frame_productos.winfo_children():
            widget.destroy()
        
        # Limpiar referencias de imágenes anteriores
        self._imagenes_productos.clear()
        self._imagenes_cargando.clear()
        
        # Actualizar el scrollregion del canvas
        self.canvas_productos.update_idletasks()
        self.canvas_productos.configure(scrollregion=self.canvas_productos.bbox("all"))
        
        # Configurar grid del frame de productos para que ocupen todo el ancho
        self.frame_productos.columnconfigure(0, weight=1)
        
        # Tamaño fijo para las imágenes (cuadrado 80x80 píxeles)
        TAMANO_IMAGEN = 80
        
        # Mostrar productos
        for idx, producto in enumerate(productos):
            frame_producto = ttk.Frame(self.frame_productos, relief='raised', borderwidth=1)
            frame_producto.grid(row=idx, column=0, sticky='ew', padx=5, pady=5)
            frame_producto.columnconfigure(1, weight=1)  # Columna de información con peso
            
            # Frame para imagen (tamaño fijo a la izquierda)
            frame_imagen = tk.Frame(frame_producto, width=TAMANO_IMAGEN, height=TAMANO_IMAGEN, bg='#d3d3d3', relief='sunken', borderwidth=1)
            frame_imagen.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
            frame_imagen.grid_propagate(False)  # Mantener tamaño fijo
            frame_imagen.pack_propagate(False)
            
            # Label para imagen (siempre ocupa el mismo espacio)
            label_imagen = tk.Label(
                frame_imagen,
                text="Cargando...",
                font=('Arial', 8),
                foreground='gray',
                background='#d3d3d3',
                anchor='center',
                justify='center'
            )
            label_imagen.pack(fill='both', expand=True)
            
            # Cargar imagen de forma diferida (lazy loading)
            ruta_imagen = producto.get("imagen")
            producto_id = producto.get("id", idx)
            
            if ruta_imagen:
                # Marcar como cargando
                self._imagenes_cargando[producto_id] = True
                # Cargar imagen en thread separado
                self.cargar_imagen_diferida(label_imagen, ruta_imagen, TAMANO_IMAGEN, producto_id)
            else:
                # No hay imagen, mostrar placeholder
                label_imagen.config(text="Sin\nimagen")
            
            # Información del producto (se mueve a la derecha)
            info_frame = ttk.Frame(frame_producto)
            info_frame.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
            info_frame.columnconfigure(0, weight=1)
            
            ttk.Label(
                info_frame,
                text=producto["nombre"],
                font=('Arial', 11, 'bold')
            ).grid(row=0, column=0, sticky='w')
            
            ttk.Label(
                info_frame,
                text=producto.get("descripcion", ""),
                font=('Arial', 10),
                foreground='gray'
            ).grid(row=1, column=0, sticky='w')
            
            ttk.Label(
                info_frame,
                text=f"${producto['precio']:,.2f}",
                font=('Arial', 12, 'bold'),
                foreground='#27ae60'
            ).grid(row=2, column=0, sticky='w')
            
            # Botón agregar
            btn_agregar = ttk.Button(
                frame_producto,
                text="➕ Agregar",
                command=lambda p=producto: self.on_agregar_producto(p)
            )
            btn_agregar.grid(row=0, column=2, padx=10, pady=5, sticky='e')
    
    def cargar_imagen_diferida(self, label_imagen, ruta_imagen, tamano, producto_id):
        """
        Carga una imagen de forma diferida en un thread separado
        
        Args:
            label_imagen: Label donde se mostrará la imagen
            ruta_imagen: Ruta de la imagen a cargar
            tamano: Tamaño de la imagen (ancho y alto)
            producto_id: ID del producto para rastrear
        """
        def cargar():
            """Función que se ejecuta en el thread separado"""
            try:
                # Cargar la imagen
                imagen_tk = cargar_imagen_tkinter(ruta_imagen, tamano, tamano)
                
                if imagen_tk:
                    # Actualizar el label en el thread principal
                    self.after(0, lambda img=imagen_tk: self.actualizar_imagen_label(
                        label_imagen, img, producto_id
                    ))
                else:
                    # Si no se pudo cargar, mostrar placeholder
                    self.after(0, lambda: self.actualizar_imagen_error(label_imagen, producto_id))
            except Exception as e:
                # En caso de error, mostrar placeholder
                print(f"Error al cargar imagen {ruta_imagen}: {e}")
                self.after(0, lambda: self.actualizar_imagen_error(label_imagen, producto_id))
            finally:
                # Marcar como no cargando
                if producto_id in self._imagenes_cargando:
                    del self._imagenes_cargando[producto_id]
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=cargar, daemon=True)
        thread.start()
    
    def actualizar_imagen_label(self, label_imagen, imagen_tk, producto_id):
        """Actualiza el label con la imagen cargada (se ejecuta en el thread principal)"""
        try:
            label_imagen.config(image=imagen_tk, text='', background='white')
            # Mantener referencia para evitar que se elimine por el garbage collector
            self._imagenes_productos.append(imagen_tk)
        except Exception as e:
            print(f"Error al actualizar imagen del producto {producto_id}: {e}")
            label_imagen.config(text="Sin\nimagen")
    
    def actualizar_imagen_error(self, label_imagen, producto_id):
        """Actualiza el label cuando hay error al cargar la imagen"""
        label_imagen.config(text="Sin\nimagen")
    
    def on_agregar_producto(self, producto):
        """Callback cuando se agrega un producto al carrito"""
        print(f"Agregando producto: {producto['nombre']}")
        # El callback será asignado desde main.py para conectar con el carrito
        if hasattr(self, 'callback_agregar_carrito'):
            self.callback_agregar_carrito(producto)
    
    def on_buscar(self, event=None):
        """Callback cuando se escribe en el buscador"""
        busqueda = self.entry_buscador.get().strip().lower()
        
        # Si no hay búsqueda, mostrar la categoría actual
        if not busqueda:
            if self.categoria_actual:
                self.mostrar_productos(self.categoria_actual)
            elif self.productos_data.get("categorias"):
                self.mostrar_productos(self.productos_data["categorias"][0]["nombre"])
            return
        
        # Buscar en todos los productos de todas las categorías
        productos_encontrados = []
        for categoria in self.productos_data.get("categorias", []):
            for producto in categoria.get("productos", []):
                nombre = producto.get("nombre", "").lower()
                descripcion = producto.get("descripcion", "").lower()
                
                # Buscar en nombre o descripción
                if busqueda in nombre or busqueda in descripcion:
                    productos_encontrados.append(producto)
        
        # Mostrar productos encontrados
        self.mostrar_lista_productos(productos_encontrados)
    
    def mostrar_ventana_producto_personalizado(self):
        """Muestra una ventana para crear un producto personalizado"""
        ventana = tk.Toplevel(self)
        ventana.title("Producto Personalizado")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        
        # Centrar la ventana
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(
            frame_principal,
            text="Producto Personalizado",
            font=('Arial', 14, 'bold')
        ).pack(pady=(0, 15))
        
        # Campo Nombre
        frame_nombre = ttk.Frame(frame_principal)
        frame_nombre.pack(fill='x', pady=5)
        
        ttk.Label(frame_nombre, text="Nombre del Producto:", font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        entry_nombre = ttk.Entry(frame_nombre, width=40, font=('Arial', 10))
        entry_nombre.pack(fill='x', pady=(0, 10))
        entry_nombre.focus()
        
        # Campo Precio
        frame_precio = ttk.Frame(frame_principal)
        frame_precio.pack(fill='x', pady=5)
        
        ttk.Label(frame_precio, text="Precio:", font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        entry_precio = ttk.Entry(frame_precio, width=40, font=('Arial', 10))
        entry_precio.pack(fill='x', pady=(0, 15))
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana.destroy,
            width=15,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#ec7063',
            activeforeground='white'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Configurar hover para botón Cancelar
        def on_enter_cancelar(event):
            btn_cancelar.config(bg='#ec7063')
        def on_leave_cancelar(event):
            btn_cancelar.config(bg='#e74c3c')
        btn_cancelar.bind('<Enter>', on_enter_cancelar)
        btn_cancelar.bind('<Leave>', on_leave_cancelar)
        
        # Botón Agregar
        btn_agregar = tk.Button(
            frame_botones,
            text="Agregar",
            command=lambda: self.agregar_producto_personalizado(ventana, entry_nombre.get(), entry_precio.get()),
            width=15,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#2ecc71',
            activeforeground='white'
        )
        btn_agregar.pack(side='left', padx=5)
        
        # Configurar hover para botón Agregar
        def on_enter_agregar(event):
            btn_agregar.config(bg='#2ecc71')
        def on_leave_agregar(event):
            btn_agregar.config(bg='#27ae60')
        btn_agregar.bind('<Enter>', on_enter_agregar)
        btn_agregar.bind('<Leave>', on_leave_agregar)
        
        # Centrar la ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")
        
        # Permitir Enter para agregar
        entry_precio.bind('<Return>', lambda e: self.agregar_producto_personalizado(ventana, entry_nombre.get(), entry_precio.get()))
    
    def agregar_producto_personalizado(self, ventana, nombre, precio_str):
        """Agrega un producto personalizado al carrito"""
        from tkinter import messagebox
        
        # Validar nombre
        if not nombre or not nombre.strip():
            messagebox.showwarning("Campo Requerido", "Por favor, ingrese el nombre del producto.")
            return
        
        # Validar precio
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showwarning("Precio Inválido", "El precio debe ser mayor a 0.")
                return
        except ValueError:
            messagebox.showwarning("Precio Inválido", "Por favor, ingrese un precio válido.")
            return
        
        # Crear producto personalizado (sin ID, será temporal)
        producto_personalizado = {
            'id': -1,  # ID negativo para identificar productos personalizados
            'nombre': nombre.strip(),
            'precio': precio,
            'descripcion': 'Producto personalizado'
        }
        
        # Agregar al carrito
        if hasattr(self, 'callback_agregar_carrito'):
            self.callback_agregar_carrito(producto_personalizado)
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo agregar el producto al carrito.")