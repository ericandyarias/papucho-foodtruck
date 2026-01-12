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
        self.ventana.title("Administración de Productos")
        self.ventana.geometry("900x600")
        self.ventana.resizable(True, True)
        
        # Centrar la ventana
        self.ventana.transient(self.parent)
        self.ventana.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(self.ventana, padding=10)
        frame_principal.pack(fill='both', expand=True)
        
        # Configurar grid
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(
            frame_principal,
            text="⚙️ Administración de Productos",
            font=('Arial', 16, 'bold')
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Frame izquierdo: Lista de productos
        self.crear_frame_lista(frame_principal)
        
        # Frame derecho: Formulario
        self.crear_frame_formulario(frame_principal)
        
        # Centrar la ventana en la pantalla
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - (self.ventana.winfo_width() // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (self.ventana.winfo_height() // 2)
        self.ventana.geometry(f"+{x}+{y}")
    
    def crear_frame_lista(self, parent):
        """Crea el frame con la lista de productos"""
        frame_lista = ttk.LabelFrame(parent, text="Lista de Productos", padding=10)
        frame_lista.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
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
        
        # Treeview
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
        
        self.tree.column('ID', width=50)
        self.tree.column('Categoría', width=120)
        self.tree.column('Nombre', width=150)
        self.tree.column('Precio', width=80)
        self.tree.column('Descripción', width=200)
        
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
        frame_formulario.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
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
                self.limpiar_formulario()
                
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
