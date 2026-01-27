"""
Script para agregar la sección de ingredientes del producto en el formulario de administración
Este script modifica ui/administracion.py para agregar la funcionalidad de gestionar ingredientes
de productos directamente desde el formulario de administración.
"""
import re

def aplicar_cambios():
    """Aplica los cambios necesarios al archivo de administración"""
    
    # Leer el archivo
    with open('ui/administracion.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    cambios_aplicados = []
    
    # 1. Agregar imports si no existen
    if 'from ui.administracion_ingredientes_producto import' not in content:
        content = content.replace(
            'from utils.ingredientes import (\n    cargar_ingredientes,\n    agregar_ingrediente, modificar_ingrediente, eliminar_ingrediente,\n    obtener_todos_los_ingredientes, buscar_ingrediente_por_id\n)',
            'from utils.ingredientes import (\n    cargar_ingredientes,\n    agregar_ingrediente, modificar_ingrediente, eliminar_ingrediente,\n    obtener_todos_los_ingredientes, buscar_ingrediente_por_id\n)\nfrom ui.administracion_ingredientes_producto import (\n    cargar_ingredientes_por_categoria,\n    agregar_ingrediente_a_producto_ui,\n    eliminar_ingrediente_de_producto_ui\n)'
        )
        cambios_aplicados.append("✓ Imports agregados")
    
    # 2. Agregar sección de ingredientes después del botón limpiar
    if 'Sección de Ingredientes del Producto' not in content:
        seccion_ingredientes = '''
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
'''
        
        # Buscar el patrón para insertar después del botón limpiar
        patron = r'(btn_limpiar\.pack\(side=\'left\', padx=5)\s+(\n\s+def cargar_lista_productos)'
        reemplazo = r'\1' + seccion_ingredientes + r'\2'
        
        if re.search(patron, content):
            content = re.sub(patron, reemplazo, content)
            cambios_aplicados.append("✓ Sección de ingredientes agregada al formulario")
        else:
            # Intentar con otro patrón
            patron2 = r'(btn_limpiar\.pack\(side=\'left\', padx=5)\s*\n\s*\n\s*(def cargar_lista_productos)'
            reemplazo2 = r'\1' + seccion_ingredientes + r'\n    \2'
            if re.search(patron2, content):
                content = re.sub(patron2, reemplazo2, content)
                cambios_aplicados.append("✓ Sección de ingredientes agregada al formulario")
    
    # 3. Agregar métodos al final de la clase
    if 'def on_categoria_changed' not in content:
        metodos = '''
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
'''
        
        # Buscar el final de la clase (antes del último método o al final)
        patron_metodos = r'(except Exception as e:\s+messagebox\.showerror\("Error", f"Error al eliminar ingrediente: \{str\(e\)\}"\))'
        reemplazo_metodos = r'\1' + metodos
        
        if re.search(patron_metodos, content):
            content = re.sub(patron_metodos, reemplazo_metodos, content)
            cambios_aplicados.append("✓ Métodos para gestionar ingredientes agregados")
        else:
            # Intentar buscar el final del archivo o antes de la última línea
            patron_final = r'(except Exception as e:\s+messagebox\.showerror\("Error", f"Error al eliminar ingrediente: \{str\(e\)\}"\))\s*$'
            if re.search(patron_final, content, re.MULTILINE):
                content = re.sub(patron_final, r'\1' + metodos, content, flags=re.MULTILINE)
                cambios_aplicados.append("✓ Métodos para gestionar ingredientes agregados")
    
    # 4. Actualizar método on_seleccionar_producto para cargar ingredientes
    if 'self.cargar_ingredientes_producto()' not in content:
        patron_seleccion = r'(self\.btn_guardar\.config\(state=\'disabled\'\))\s*\n\s*(def nuevo_producto)'
        reemplazo_seleccion = r'\1\n            \n            # Cargar ingredientes del producto\n            self.cargar_ingredientes_producto()\n            # Cargar ingredientes disponibles según la categoría\n            self.on_categoria_changed()\n    \2'
        
        if re.search(patron_seleccion, content):
            content = re.sub(patron_seleccion, reemplazo_seleccion, content)
            cambios_aplicados.append("✓ Método on_seleccionar_producto actualizado")
    
    # Guardar el archivo
    with open('ui/administracion.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return cambios_aplicados


if __name__ == "__main__":
    print("Aplicando cambios al archivo ui/administracion.py...")
    print()
    
    try:
        cambios = aplicar_cambios()
        
        if cambios:
            print("Cambios aplicados correctamente:")
            for cambio in cambios:
                print(f"  {cambio}")
        else:
            print("No se aplicaron cambios. Es posible que ya estén aplicados.")
        
        print()
        print("✓ Proceso completado")
        
    except Exception as e:
        print(f"❌ Error al aplicar cambios: {e}")
        import traceback
        traceback.print_exc()
