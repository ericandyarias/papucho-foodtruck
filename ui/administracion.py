"""
Módulo para la ventana de administración de productos
Permite Alta, Baja y Modificación de productos
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.productos import (
    cargar_productos, CATEGORIAS_FIJAS,
    agregar_producto, modificar_producto, eliminar_producto,
    obtener_todos_los_productos
)
from utils.ingredientes import (
    cargar_ingredientes,
    agregar_ingrediente, modificar_ingrediente, eliminar_ingrediente,
    obtener_todos_los_ingredientes, buscar_ingrediente_por_id
)
from ui.administracion_ingredientes_producto import (
    cargar_ingredientes_por_categoria,
    agregar_ingrediente_a_producto_ui,
    eliminar_ingrediente_de_producto_ui
)


class VentanaAdministracion:
    """Ventana de administración de productos"""
    
    def __init__(self, parent, callback_actualizar=None):
        """
        Inicializa la ventana de administración
        
        Args:
            parent: Ventana padre
            callback_actualizar: Función a llamar cuando se actualicen los productos
        """
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        self.producto_seleccionado = None
        
        self.crear_ventana()
        self.cargar_lista_productos()
    
    def crear_ventana(self):
        """Crea y configura la ventana de administración"""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Administración")
        self.ventana.geometry("1400x700")
        self.ventana.resizable(True, True)
        
        # Centrar la ventana
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(self.ventana, padding=10)
        frame_principal.pack(fill='both', expand=True)
        
        # Título
        titulo = ttk.Label(
            frame_principal,
            text="⚙️ Administración",
            font=('Arial', 16, 'bold')
        )
        titulo.pack(pady=10)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña de Productos
        frame_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame_productos, text="📦 Productos")
        self.crear_pestaña_productos(frame_productos)
        
        # Pestaña de Ingredientes
        frame_ingredientes = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame_ingredientes, text="🥗 Ingredientes")
        self.crear_pestaña_ingredientes(frame_ingredientes)
        
        # Centrar la ventana en la pantalla
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (self.ventana.winfo_width() // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (self.ventana.winfo_height() // 2)
        self.ventana.geometry(f"+{x}+{y}")
    
    def crear_pestaña_productos(self, parent):
        """Crea la pestaña de productos"""
        # Configurar grid
        parent.columnconfigure(0, weight=3)  # Lista más ancha
        parent.columnconfigure(1, weight=2)  # Formulario más estrecho
        parent.rowconfigure(0, weight=1)
        
        # Frame izquierdo: Lista de productos
        self.crear_frame_lista(parent)
        
        # Frame derecho: Formulario
        self.crear_frame_formulario(parent)
    
    def crear_frame_lista(self, parent):
        """Crea el frame con la lista de productos"""
        frame_lista = ttk.LabelFrame(parent, text="Lista de Productos", padding=10)
        frame_lista.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(1, weight=1)
        
        # Frame para filtros
        frame_filtros = ttk.Frame(frame_lista)
        frame_filtros.grid(row=0, column=0, sticky='ew', pady=5)
        frame_filtros.columnconfigure(1, weight=1)
        
        ttk.Label(frame_filtros, text="Categoría:").grid(row=0, column=0, padx=5)
        
        self.var_filtro_categoria = tk.StringVar(value="Todas")
        combo_filtro = ttk.Combobox(
            frame_filtros,
            textvariable=self.var_filtro_categoria,
            values=["Todas"] + CATEGORIAS_FIJAS,
            state='readonly',
            width=15
        )
        combo_filtro.grid(row=0, column=1, padx=5, sticky='w')
        combo_filtro.bind('<<ComboboxSelected>>', lambda e: self.cargar_lista_productos())
        
        # Treeview para lista de productos
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.grid(row=1, column=0, sticky='nsew')
        frame_tree.columnconfigure(0, weight=1)
        frame_tree.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Treeview (sin columna Categoría visible)
        self.tree = ttk.Treeview(
            frame_tree,
            columns=('ID', 'Categoría', 'Nombre', 'Precio', 'Descripción'),
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Descripción', text='Descripción')
        
        self.tree.column('ID', width=0, stretch=False)  # Ocultar columna ID
        self.tree.column('Categoría', width=0, stretch=False)  # Ocultar columna Categoría
        self.tree.column('Nombre', width=250)
        self.tree.column('Precio', width=120)
        self.tree.column('Descripción', width=400)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.on_seleccionar_producto)
        
        # Botones de acción
        frame_botones_lista = ttk.Frame(frame_lista)
        frame_botones_lista.grid(row=2, column=0, pady=10)
        
        btn_nuevo = ttk.Button(
            frame_botones_lista,
            text="➕ Nuevo Producto",
            command=self.nuevo_producto,
            width=20
        )
        btn_nuevo.pack(side='left', padx=5)
    
    def crear_frame_formulario(self, parent):
        """Crea el frame con el formulario de producto"""
        frame_formulario = ttk.LabelFrame(parent, text="Datos del Producto", padding=10)
        frame_formulario.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        frame_formulario.columnconfigure(1, weight=1)
        
        # Categoría
        ttk.Label(frame_formulario, text="Categoría:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.var_categoria = tk.StringVar()
        combo_categoria = ttk.Combobox(
            frame_formulario,
            textvariable=self.var_categoria,
            values=CATEGORIAS_FIJAS,
            state='readonly',
            width=20
        )
        combo_categoria.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        # Nombre
        ttk.Label(frame_formulario, text="Nombre:").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.entry_nombre = ttk.Entry(frame_formulario, width=30)
        self.entry_nombre.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        # Precio
        ttk.Label(frame_formulario, text="Precio:").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.entry_precio = ttk.Entry(frame_formulario, width=30)
        self.entry_precio.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        
        # Descripción
        ttk.Label(frame_formulario, text="Descripción:").grid(row=3, column=0, sticky='nw', pady=5, padx=5)
        self.text_descripcion = tk.Text(frame_formulario, width=30, height=5, wrap='word')
        self.text_descripcion.grid(row=3, column=1, sticky='ew', pady=5, padx=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_formulario)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón Guardar
        self.btn_guardar = ttk.Button(
            frame_botones,
            text="💾 Guardar",
            command=self.guardar_producto,
            width=15
        )
        self.btn_guardar.pack(side='left', padx=5)
        
        # Botón Modificar
        self.btn_modificar = ttk.Button(
            frame_botones,
            text="✏️ Modificar",
            command=self.modificar_producto_actual,
            width=15,
            state='disabled'
        )
        self.btn_modificar.pack(side='left', padx=5)
        
        # Botón Eliminar
        self.btn_eliminar = ttk.Button(
            frame_botones,
            text="❌ Eliminar",
            command=self.eliminar_producto_actual,
            width=15,
            state='disabled'
        )
        self.btn_eliminar.pack(side='left', padx=5)
        
        # Botón Limpiar
        btn_limpiar = ttk.Button(
            frame_botones,
            text="🔄 Limpiar",
            command=self.limpiar_formulario,
            width=15
        )
        btn_limpiar.pack(side='left', padx=5)
        
        # Sección de Ingredientes del Producto
        frame_ingredientes_producto = ttk.LabelFrame(frame_formulario, text="Ingredientes del Producto", padding=10)
        frame_ingredientes_producto.grid(row=5, column=0, columnspan=2, sticky='ew', pady=10, padx=5)
        frame_ingredientes_producto.columnconfigure(0, weight=1)
        
        # Frame para agregar ingrediente
        frame_agregar_ing = ttk.Frame(frame_ingredientes_producto)
        frame_agregar_ing.grid(row=0, column=0, sticky='ew', pady=5)
        frame_agregar_ing.columnconfigure(1, weight=1)
        
        ttk.Label(frame_agregar_ing, text="Ingrediente:").grid(row=0, column=0, padx=5, sticky='w')
        self.combo_ingrediente = ttk.Combobox(frame_agregar_ing, state='readonly', width=20)
        self.combo_ingrediente.grid(row=0, column=1, padx=5, sticky='ew')
        
        ttk.Label(frame_agregar_ing, text="Cantidad Base:").grid(row=0, column=2, padx=5, sticky='w')
        self.entry_cantidad_ing = ttk.Entry(frame_agregar_ing, width=10)
        self.entry_cantidad_ing.grid(row=0, column=3, padx=5)
        self.entry_cantidad_ing.insert(0, "1")
        
        btn_agregar_ing = ttk.Button(
            frame_agregar_ing,
            text="➕ Agregar",
            command=self.agregar_ingrediente_producto,
            width=12
        )
        btn_agregar_ing.grid(row=0, column=4, padx=5)
        
        # Treeview para ingredientes del producto
        frame_tree_ing = ttk.Frame(frame_ingredientes_producto)
        frame_tree_ing.grid(row=1, column=0, sticky='nsew', pady=5)
        frame_tree_ing.columnconfigure(0, weight=1)
        frame_tree_ing.rowconfigure(0, weight=1)
        
        scrollbar_ing = ttk.Scrollbar(frame_tree_ing)
        scrollbar_ing.grid(row=0, column=1, sticky='ns')
        
        self.tree_ingredientes_producto = ttk.Treeview(
            frame_tree_ing,
            columns=('Nombre', 'Cantidad', 'Precio Extra', 'Precio Resta'),
            show='headings',
            yscrollcommand=scrollbar_ing.set,
            height=5
        )
        scrollbar_ing.config(command=self.tree_ingredientes_producto.yview)
        
        self.tree_ingredientes_producto.heading('Nombre', text='Nombre')
        self.tree_ingredientes_producto.heading('Cantidad', text='Cantidad Base')
        self.tree_ingredientes_producto.heading('Precio Extra', text='Precio Extra')
        self.tree_ingredientes_producto.heading('Precio Resta', text='Precio Resta')
        
        self.tree_ingredientes_producto.column('Nombre', width=150)
        self.tree_ingredientes_producto.column('Cantidad', width=100)
        self.tree_ingredientes_producto.column('Precio Extra', width=100)
        self.tree_ingredientes_producto.column('Precio Resta', width=100)
        
        self.tree_ingredientes_producto.grid(row=0, column=0, sticky='nsew')
        
        # Botón eliminar ingrediente
        btn_eliminar_ing = ttk.Button(
            frame_ingredientes_producto,
            text="❌ Eliminar Ingrediente",
            command=self.eliminar_ingrediente_producto,
            width=20
        )
        btn_eliminar_ing.grid(row=2, column=0, pady=5)
        
        # Actualizar combo cuando cambia la categoría
        combo_categoria.bind('<<ComboboxSelected>>', self.on_categoria_changed)
    
    def cargar_lista_productos(self):
        """Carga la lista de productos en el treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        productos = obtener_todos_los_productos()
        
        # Filtrar por categoría si es necesario
        filtro_categoria = self.var_filtro_categoria.get()
        if filtro_categoria != "Todas":
            productos = [p for p in productos if p["categoria"] == filtro_categoria]
        
        # Agregar productos al treeview
        for producto in productos:
            self.tree.insert(
                '',
                'end',
                values=(
                    producto['id'],
                    producto['categoria'],
                    producto['nombre'],
                    f"${producto['precio']:.2f}",
                    producto.get('descripcion', '')
                )
            )
    
    def on_seleccionar_producto(self, event):
        """Callback cuando se selecciona un producto en la lista"""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = self.tree.item(seleccion[0])
        producto_id = int(item['values'][0])
        
        # Buscar el producto completo
        from utils.productos import buscar_producto_por_id
        resultado = buscar_producto_por_id(producto_id)
        
        if resultado:
            self.producto_seleccionado = resultado['producto']
            
            # Llenar formulario
            self.var_categoria.set(resultado['categoria'])
            self.entry_nombre.delete(0, 'end')
            self.entry_nombre.insert(0, self.producto_seleccionado['nombre'])
            self.entry_precio.delete(0, 'end')
            self.entry_precio.insert(0, str(self.producto_seleccionado['precio']))
            self.text_descripcion.delete('1.0', 'end')
            self.text_descripcion.insert('1.0', self.producto_seleccionado.get('descripcion', ''))
            
            # Habilitar botones de modificar y eliminar
            self.btn_modificar.config(state='normal')
            self.btn_eliminar.config(state='normal')
            self.btn_guardar.config(state='disabled')
            
            # Cargar ingredientes del producto
            self.cargar_ingredientes_producto()
            # Cargar ingredientes disponibles según la categoría
            self.on_categoria_changed()
    
    def nuevo_producto(self):
        """Prepara el formulario para un nuevo producto"""
        self.limpiar_formulario()
        self.producto_seleccionado = None
        self.btn_guardar.config(state='normal')
        self.btn_modificar.config(state='disabled')
        self.btn_eliminar.config(state='disabled')
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.var_categoria.set('')
        self.entry_nombre.delete(0, 'end')
        self.entry_precio.delete(0, 'end')
        self.text_descripcion.delete('1.0', 'end')
        self.producto_seleccionado = None
        self.tree.selection_remove(self.tree.selection())
    
    def validar_formulario(self):
        """Valida que el formulario esté completo"""
        if not self.var_categoria.get():
            messagebox.showerror("Error", "Debe seleccionar una categoría")
            return False
        
        if not self.entry_nombre.get().strip():
            messagebox.showerror("Error", "Debe ingresar un nombre")
            return False
        
        try:
            precio = float(self.entry_precio.get())
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return False
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return False
        
        return True
    
    def guardar_producto(self):
        """Guarda un nuevo producto"""
        if not self.validar_formulario():
            return
        
        categoria = self.var_categoria.get()
        nombre = self.entry_nombre.get().strip()
        precio = float(self.entry_precio.get())
        descripcion = self.text_descripcion.get('1.0', 'end').strip()
        
        try:
            agregar_producto(categoria, nombre, precio, descripcion)
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.cargar_lista_productos()
            self.limpiar_formulario()
            
            # Notificar actualización
            if self.callback_actualizar:
                self.callback_actualizar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def modificar_producto_actual(self):
        """Modifica el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return
        
        if not self.validar_formulario():
            return
        
        producto_id = self.producto_seleccionado['id']
        categoria = self.var_categoria.get()
        nombre = self.entry_nombre.get().strip()
        precio = float(self.entry_precio.get())
        descripcion = self.text_descripcion.get('1.0', 'end').strip()
        
        try:
            if modificar_producto(producto_id, categoria, nombre, precio, descripcion):
                messagebox.showinfo("Éxito", "Producto modificado correctamente")
                self.cargar_lista_productos()
                
                # Preparar formulario para crear un nuevo producto
                self.nuevo_producto()
                
                # Notificar actualización
                if self.callback_actualizar:
                    self.callback_actualizar()
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar producto: {str(e)}")
    
    def eliminar_producto_actual(self):
        """Elimina el producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto '{self.producto_seleccionado['nombre']}'?"
        )
        
        if not respuesta:
            return
        
        try:
            if eliminar_producto(self.producto_seleccionado['id']):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.cargar_lista_productos()
                self.limpiar_formulario()
                
                # Notificar actualización
                if self.callback_actualizar:
                    self.callback_actualizar()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    
    def crear_pestaña_ingredientes(self, parent):
        """Crea la pestaña de administración de ingredientes"""
        # Configurar grid
        parent.columnconfigure(0, weight=3)  # Lista más ancha
        parent.columnconfigure(1, weight=2)  # Formulario más estrecho
        parent.rowconfigure(0, weight=1)
        
        # Frame izquierdo: Lista de ingredientes
        frame_lista = ttk.LabelFrame(parent, text="Lista de Ingredientes", padding=10)
        frame_lista.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(1, weight=1)
        
        # Treeview para lista de ingredientes
        frame_tree = ttk.Frame(frame_lista)
        frame_tree.grid(row=1, column=0, sticky='nsew')
        frame_tree.columnconfigure(0, weight=1)
        frame_tree.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Treeview
        self.tree_ingredientes = ttk.Treeview(
            frame_tree,
            columns=('ID', 'Nombre', 'Categorías', 'Precio Extra', 'Precio Resta'),
            show='headings',
            yscrollcommand=scrollbar.set,
            selectmode='browse'
        )
        scrollbar.config(command=self.tree_ingredientes.yview)
        
        # Configurar columnas
        self.tree_ingredientes.heading('ID', text='ID')
        self.tree_ingredientes.heading('Nombre', text='Nombre')
        self.tree_ingredientes.heading('Categorías', text='Categorías')
        self.tree_ingredientes.heading('Precio Extra', text='Precio Extra')
        self.tree_ingredientes.heading('Precio Resta', text='Precio Resta')
        
        self.tree_ingredientes.column('ID', width=0, stretch=False)  # Ocultar
        self.tree_ingredientes.column('Nombre', width=200)
        self.tree_ingredientes.column('Categorías', width=250)
        self.tree_ingredientes.column('Precio Extra', width=120)
        self.tree_ingredientes.column('Precio Resta', width=120)
        
        self.tree_ingredientes.grid(row=0, column=0, sticky='nsew')
        self.tree_ingredientes.bind('<<TreeviewSelect>>', self.on_seleccionar_ingrediente)
        
        # Botones de acción
        frame_botones_lista = ttk.Frame(frame_lista)
        frame_botones_lista.grid(row=2, column=0, pady=10)
        
        btn_nuevo_ing = ttk.Button(
            frame_botones_lista,
            text="➕ Nuevo Ingrediente",
            command=self.nuevo_ingrediente,
            width=20
        )
        btn_nuevo_ing.pack(side='left', padx=5)
        
        # Frame derecho: Formulario de ingrediente
        frame_formulario_ing = ttk.LabelFrame(parent, text="Datos del Ingrediente", padding=10)
        frame_formulario_ing.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        frame_formulario_ing.columnconfigure(1, weight=1)
        
        # Nombre
        ttk.Label(frame_formulario_ing, text="Nombre:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.entry_nombre_ing = ttk.Entry(frame_formulario_ing, width=30)
        self.entry_nombre_ing.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        
        # Categorías (checkboxes)
        ttk.Label(frame_formulario_ing, text="Categorías:").grid(row=1, column=0, sticky='nw', pady=5, padx=5)
        frame_categorias_ing = ttk.Frame(frame_formulario_ing)
        frame_categorias_ing.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        
        self.vars_categorias_ing = {}
        for idx, categoria in enumerate(CATEGORIAS_FIJAS):
            var = tk.BooleanVar()
            self.vars_categorias_ing[categoria] = var
            checkbox = ttk.Checkbutton(
                frame_categorias_ing,
                text=categoria,
                variable=var
            )
            checkbox.grid(row=idx // 2, column=idx % 2, sticky='w', padx=5, pady=2)
        
        # Precio Extra
        ttk.Label(frame_formulario_ing, text="Precio Extra:").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.entry_precio_extra = ttk.Entry(frame_formulario_ing, width=30)
        self.entry_precio_extra.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        
        # Precio Resta
        ttk.Label(frame_formulario_ing, text="Precio Resta:").grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.entry_precio_resta = ttk.Entry(frame_formulario_ing, width=30)
        self.entry_precio_resta.grid(row=3, column=1, sticky='ew', pady=5, padx=5)
        
        # Frame para botones
        frame_botones_ing = ttk.Frame(frame_formulario_ing)
        frame_botones_ing.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Botón Guardar
        self.btn_guardar_ing = ttk.Button(
            frame_botones_ing,
            text="💾 Guardar",
            command=self.guardar_ingrediente,
            width=15
        )
        self.btn_guardar_ing.pack(side='left', padx=5)
        
        # Botón Modificar
        self.btn_modificar_ing = ttk.Button(
            frame_botones_ing,
            text="✏️ Modificar",
            command=self.modificar_ingrediente_actual,
            width=15,
            state='disabled'
        )
        self.btn_modificar_ing.pack(side='left', padx=5)
        
        # Botón Eliminar
        self.btn_eliminar_ing = ttk.Button(
            frame_botones_ing,
            text="❌ Eliminar",
            command=self.eliminar_ingrediente_actual,
            width=15,
            state='disabled'
        )
        self.btn_eliminar_ing.pack(side='left', padx=5)
        
        # Botón Limpiar
        btn_limpiar_ing = ttk.Button(
            frame_botones_ing,
            text="🔄 Limpiar",
            command=self.limpiar_formulario_ingrediente,
            width=15
        )
        btn_limpiar_ing.pack(side='left', padx=5)
        
        # Cargar lista inicial
        self.cargar_lista_ingredientes()
        self.ingrediente_seleccionado = None
    
    def cargar_lista_ingredientes(self):
        """Carga la lista de ingredientes en el treeview"""
        # Limpiar treeview
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)
        
        # Obtener ingredientes
        ingredientes = obtener_todos_los_ingredientes()
        
        # Agregar ingredientes al treeview
        for ingrediente in ingredientes:
            categorias_str = ", ".join(ingrediente.get("categorias", []))
            self.tree_ingredientes.insert(
                '',
                'end',
                values=(
                    ingrediente['id'],
                    ingrediente['nombre'],
                    categorias_str,
                    f"${ingrediente['precio_extra']:.2f}",
                    f"${ingrediente['precio_resta']:.2f}"
                )
            )
    
    def on_seleccionar_ingrediente(self, event):
        """Callback cuando se selecciona un ingrediente en la lista"""
        seleccion = self.tree_ingredientes.selection()
        if not seleccion:
            return
        
        item = self.tree_ingredientes.item(seleccion[0])
        ingrediente_id = int(item['values'][0])
        
        # Buscar el ingrediente completo
        ingrediente = buscar_ingrediente_por_id(ingrediente_id)
        
        if ingrediente:
            self.ingrediente_seleccionado = ingrediente
            
            # Llenar formulario
            self.entry_nombre_ing.delete(0, 'end')
            self.entry_nombre_ing.insert(0, ingrediente['nombre'])
            
            # Limpiar checkboxes
            for var in self.vars_categorias_ing.values():
                var.set(False)
            
            # Marcar categorías del ingrediente
            categorias = ingrediente.get("categorias", [])
            for categoria in categorias:
                if categoria in self.vars_categorias_ing:
                    self.vars_categorias_ing[categoria].set(True)
            
            self.entry_precio_extra.delete(0, 'end')
            self.entry_precio_extra.insert(0, str(ingrediente['precio_extra']))
            
            self.entry_precio_resta.delete(0, 'end')
            self.entry_precio_resta.insert(0, str(ingrediente['precio_resta']))
            
            # Habilitar botones de modificar y eliminar
            self.btn_modificar_ing.config(state='normal')
            self.btn_eliminar_ing.config(state='normal')
            self.btn_guardar_ing.config(state='disabled')
    
    def nuevo_ingrediente(self):
        """Prepara el formulario para un nuevo ingrediente"""
        self.limpiar_formulario_ingrediente()
        self.ingrediente_seleccionado = None
        self.btn_guardar_ing.config(state='normal')
        self.btn_modificar_ing.config(state='disabled')
        self.btn_eliminar_ing.config(state='disabled')
    
    def limpiar_formulario_ingrediente(self):
        """Limpia el formulario de ingrediente"""
        self.entry_nombre_ing.delete(0, 'end')
        for var in self.vars_categorias_ing.values():
            var.set(False)
        self.entry_precio_extra.delete(0, 'end')
        self.entry_precio_resta.delete(0, 'end')
        self.ingrediente_seleccionado = None
        self.tree_ingredientes.selection_remove(self.tree_ingredientes.selection())
    
    def validar_formulario_ingrediente(self):
        """Valida que el formulario de ingrediente esté completo"""
        if not self.entry_nombre_ing.get().strip():
            messagebox.showerror("Error", "Debe ingresar un nombre")
            return False
        
        # Verificar que al menos una categoría esté seleccionada
        categorias_seleccionadas = [cat for cat, var in self.vars_categorias_ing.items() if var.get()]
        if not categorias_seleccionadas:
            messagebox.showerror("Error", "Debe seleccionar al menos una categoría")
            return False
        
        try:
            precio_extra = float(self.entry_precio_extra.get())
            if precio_extra < 0:
                messagebox.showerror("Error", "El precio extra debe ser mayor o igual a 0")
                return False
        except ValueError:
            messagebox.showerror("Error", "El precio extra debe ser un número válido")
            return False
        
        try:
            precio_resta = float(self.entry_precio_resta.get())
            if precio_resta < 0:
                messagebox.showerror("Error", "El precio de resta debe ser mayor o igual a 0")
                return False
        except ValueError:
            messagebox.showerror("Error", "El precio de resta debe ser un número válido")
            return False
        
        return True
    
    def guardar_ingrediente(self):
        """Guarda un nuevo ingrediente"""
        if not self.validar_formulario_ingrediente():
            return
        
        nombre = self.entry_nombre_ing.get().strip()
        categorias = [cat for cat, var in self.vars_categorias_ing.items() if var.get()]
        precio_extra = float(self.entry_precio_extra.get())
        precio_resta = float(self.entry_precio_resta.get())
        
        try:
            agregar_ingrediente(nombre, categorias, precio_extra, precio_resta)
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente")
            self.cargar_lista_ingredientes()
            self.limpiar_formulario_ingrediente()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar ingrediente: {str(e)}")
    
    def modificar_ingrediente_actual(self):
        """Modifica el ingrediente seleccionado"""
        if not self.ingrediente_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un ingrediente")
            return
        
        if not self.validar_formulario_ingrediente():
            return
        
        ingrediente_id = self.ingrediente_seleccionado['id']
        nombre = self.entry_nombre_ing.get().strip()
        categorias = [cat for cat, var in self.vars_categorias_ing.items() if var.get()]
        precio_extra = float(self.entry_precio_extra.get())
        precio_resta = float(self.entry_precio_resta.get())
        
        try:
            if modificar_ingrediente(ingrediente_id, nombre, categorias, precio_extra, precio_resta):
                messagebox.showinfo("Éxito", "Ingrediente modificado correctamente")
                self.cargar_lista_ingredientes()
                self.nuevo_ingrediente()
            else:
                messagebox.showerror("Error", "No se pudo modificar el ingrediente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar ingrediente: {str(e)}")
    
    def eliminar_ingrediente_actual(self):
        """Elimina el ingrediente seleccionado"""
        if not self.ingrediente_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un ingrediente")
            return
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el ingrediente '{self.ingrediente_seleccionado['nombre']}'?"
        )
        
        if not respuesta:
            return
        
        try:
            if eliminar_ingrediente(self.ingrediente_seleccionado['id']):
                messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente")
                self.cargar_lista_ingredientes()
                self.limpiar_formulario_ingrediente()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ingrediente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar ingrediente: {str(e)}")
    
    # Métodos para gestionar ingredientes de productos
    def on_categoria_changed(self, event=None):
        """Actualiza el combo de ingredientes cuando cambia la categoría del producto"""
        categoria = self.var_categoria.get()
        if categoria:
            cargar_ingredientes_por_categoria(self.combo_ingrediente, categoria)
        else:
            self.combo_ingrediente['values'] = []
    
    def cargar_ingredientes_producto(self):
        """Carga los ingredientes del producto seleccionado en el treeview"""
        # Limpiar treeview
        for item in self.tree_ingredientes_producto.get_children():
            self.tree_ingredientes_producto.delete(item)
        
        if not self.producto_seleccionado:
            return
        
        ingredientes = self.producto_seleccionado.get('ingredientes', [])
        for ingrediente in ingredientes:
            self.tree_ingredientes_producto.insert(
                '',
                'end',
                values=(
                    ingrediente.get('nombre', ''),
                    ingrediente.get('cantidad_base', 0),
                    f"${ingrediente.get('precio_extra', 0):.2f}",
                    f"${ingrediente.get('precio_resta', 0):.2f}"
                )
            )
    
    def agregar_ingrediente_producto(self):
        """Agrega un ingrediente al producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto primero")
            return
        
        producto_id = self.producto_seleccionado['id']
        nombre_ingrediente = self.combo_ingrediente.get()
        cantidad_base = self.entry_cantidad_ing.get()
        
        agregar_ingrediente_a_producto_ui(
            producto_id,
            nombre_ingrediente,
            cantidad_base,
            self.combo_ingrediente,
            self.tree_ingredientes_producto,
            self.entry_cantidad_ing
        )
        
        # Recargar el producto para actualizar los ingredientes
        from utils.productos import buscar_producto_por_id
        resultado = buscar_producto_por_id(producto_id)
        if resultado:
            self.producto_seleccionado = resultado['producto']
            self.cargar_ingredientes_producto()
    
    def eliminar_ingrediente_producto(self):
        """Elimina un ingrediente del producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto primero")
            return
        
        producto_id = self.producto_seleccionado['id']
        eliminar_ingrediente_de_producto_ui(producto_id, self.tree_ingredientes_producto)
        
        # Recargar el producto para actualizar los ingredientes
        from utils.productos import buscar_producto_por_id
        resultado = buscar_producto_por_id(producto_id)
        if resultado:
            self.producto_seleccionado = resultado['producto']
            self.cargar_ingredientes_producto()