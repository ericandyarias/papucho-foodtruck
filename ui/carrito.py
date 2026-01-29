"""
Módulo para el carrito de compras (barra derecha)
Muestra items seleccionados, cantidad, total y botón de confirmación
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.orden import leer_numero_orden, incrementar_orden
from utils.tickets import generar_tickets_pedido
from utils.productos import calcular_precio_con_ingredientes


class Carrito(ttk.Frame):
    """Frame lateral derecho para el carrito de compras"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.items = []  # Lista de items en el carrito
        self.numero_orden = leer_numero_orden()  # Cargar número de orden
        self.configurar_carrito()
    
    def configurar_carrito(self):
        """Configura el diseño del carrito"""
        # Configurar estilo del frame y grid
        self.config(relief='sunken', borderwidth=2, width=300)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Frame para el encabezado del carrito
        frame_encabezado = ttk.Frame(self)
        frame_encabezado.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        frame_encabezado.columnconfigure(1, weight=1)
        
        # Título del carrito (izquierda)
        titulo = ttk.Label(
            frame_encabezado,
            text="🛒 Carrito",
            font=('Arial', 14, 'bold')
        )
        titulo.grid(row=0, column=0, sticky='w')
        
        # Número de pedido (derecha)
        self.label_numero_pedido = ttk.Label(
            frame_encabezado,
            text=f"Pedido #{self.numero_orden:04d}",
            font=('Arial', 11, 'bold'),
            foreground='#3498db'
        )
        self.label_numero_pedido.grid(row=0, column=1, sticky='e', padx=10)
        
        # Frame para la lista de items
        frame_lista = ttk.Frame(self)
        frame_lista.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)
        
        # Canvas con scrollbar para items
        canvas = tk.Canvas(frame_lista)
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        self.frame_items = ttk.Frame(canvas)
        
        self.frame_items.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Crear ventana del canvas y configurar para que se expanda
        canvas_window = canvas.create_window((0, 0), window=self.frame_items, anchor="nw")
        
        # Función para ajustar el ancho del frame cuando el canvas cambie de tamaño
        def ajustar_ancho_frame(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', ajustar_ancho_frame)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar scroll con rueda del mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Vincular el evento de scroll al canvas y al frame
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.frame_items.bind_all("<MouseWheel>", on_mousewheel)
        
        # Guardar referencia al canvas para poder accederlo desde otros métodos
        self.canvas_carrito = canvas
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Frame para el total
        frame_total = ttk.Frame(self)
        frame_total.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        frame_total.columnconfigure(0, weight=1)
        
        ttk.Separator(frame_total, orient='horizontal').grid(row=0, column=0, sticky='ew', pady=5)
        
        self.label_total = ttk.Label(
            frame_total,
            text="Total: $0.00",
            font=('Arial', 14, 'bold'),
            foreground='#2c3e50'
        )
        self.label_total.grid(row=1, column=0, pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)
        
        # Botón Borrar Carrito (usando tk.Button para mejor control de hover)
        self.btn_borrar = tk.Button(
            frame_botones,
            text="🗑️ Borrar Todo",
            command=self.on_borrar_carrito,
            font=('Arial', 12),
            relief='flat',
            cursor='hand2',
            borderwidth=0,
            compound='left',
            anchor='center'
        )
        self.btn_borrar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Botón Confirmar (usando tk.Button para mejor control de hover)
        self.btn_confirmar = tk.Button(
            frame_botones,
            text="✅ Confirmar Pedido",
            command=self.on_confirmar,
            font=('Arial', 12),
            relief='flat',
            cursor='hand2',
            borderwidth=0
        )
        self.btn_confirmar.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Configurar estilos iniciales de los botones
        self.actualizar_estilo_boton_confirmar()
        self.actualizar_estilo_boton_borrar()
        
        # Mostrar mensaje inicial
        self.mostrar_mensaje_vacio()
    
    def mostrar_mensaje_vacio(self):
        """Muestra un mensaje cuando el carrito está vacío"""
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        mensaje = ttk.Label(
            self.frame_items,
            text="El carrito está vacío\nSelecciona productos para comenzar",
            font=('Arial', 10),
            foreground='gray',
            justify='center'
        )
        mensaje.pack(pady=50)
        
        # Actualizar estilos de los botones cuando está vacío
        self.actualizar_estilo_boton_confirmar()
        self.actualizar_estilo_boton_borrar()
    
    def agregar_item(self, producto, cantidad=1):
        """Agrega un item al carrito"""
        # Buscar si el producto ya está en el carrito
        for item in self.items:
            if item['producto']['id'] == producto['id']:
                item['cantidad'] += cantidad
                self.actualizar_vista()
                return
        
        # Recargar el producto desde el JSON para obtener la versión más actualizada con ingredientes
        from utils.productos import buscar_producto_por_id
        resultado = buscar_producto_por_id(producto['id'])
        if resultado:
            # Usar el producto actualizado del JSON
            producto = resultado['producto'].copy()
            producto['categoria'] = resultado.get('categoria', '')
        else:
            # Si no se encuentra, usar el producto original pero asegurar que tenga categoría
            if 'categoria' not in producto:
                producto['categoria'] = ''
        
        # Inicializar modificaciones_ingredientes: dict con {nombre_ingrediente: cantidad_actual}
        modificaciones_ingredientes = {}
        ingredientes = producto.get("ingredientes", [])
        for ingrediente in ingredientes:
            nombre = ingrediente.get("nombre", "")
            cantidad_base = ingrediente.get("cantidad_base", 1)
            modificaciones_ingredientes[nombre] = cantidad_base
        
        self.items.append({
            'producto': producto,
            'cantidad': cantidad,
            'modificaciones_ingredientes': modificaciones_ingredientes
        })
        self.actualizar_vista()
    
    def eliminar_item(self, producto_id):
        """Elimina un item del carrito"""
        self.items = [item for item in self.items if item['producto']['id'] != producto_id]
        self.actualizar_vista()
    
    def actualizar_cantidad(self, producto_id, nueva_cantidad):
        """Actualiza la cantidad de un item"""
        for item in self.items:
            if item['producto']['id'] == producto_id:
                if nueva_cantidad <= 0:
                    self.eliminar_item(producto_id)
                else:
                    item['cantidad'] = nueva_cantidad
                break
        self.actualizar_vista()
    
    def calcular_total(self):
        """Calcula el total del carrito considerando modificaciones de ingredientes"""
        total = 0
        for item in self.items:
            producto = item['producto']
            cantidad = item['cantidad']
            modificaciones = item.get('modificaciones_ingredientes', {})
            
            # Calcular precio unitario con ingredientes
            precio_unitario = calcular_precio_con_ingredientes(producto, modificaciones)
            total += precio_unitario * cantidad
        return total
    
    def actualizar_estilo_boton_confirmar(self):
        """Actualiza el estilo del botón de confirmar según el estado del carrito"""
        if not self.items or len(self.items) == 0:
            # Carrito vacío: gris con letras blancas
            self.btn_confirmar.config(
                bg='#95a5a6',
                fg='white',
                activebackground='#7f8c8d',
                activeforeground='white'
            )
        else:
            # Carrito con contenido: verde con letras blancas
            self.btn_confirmar.config(
                bg='#27ae60',
                fg='white',
                activebackground='#2ecc71',  # Verde clarito para hover
                activeforeground='white'
            )
        
        # Configurar eventos de hover
        self.configurar_hover_confirmar()
    
    def configurar_hover_confirmar(self):
        """Configura los efectos hover para el botón de confirmar"""
        def on_enter(event):
            if self.items and len(self.items) > 0:
                # Verde clarito cuando hay contenido
                self.btn_confirmar.config(bg='#2ecc71')
            else:
                # Gris más claro cuando está vacío
                self.btn_confirmar.config(bg='#bdc3c7')
        
        def on_leave(event):
            # Restaurar color original
            if self.items and len(self.items) > 0:
                self.btn_confirmar.config(bg='#27ae60')
            else:
                self.btn_confirmar.config(bg='#95a5a6')
        
        self.btn_confirmar.bind('<Enter>', on_enter)
        self.btn_confirmar.bind('<Leave>', on_leave)
    
    def actualizar_estilo_boton_borrar(self):
        """Actualiza el estilo del botón de borrar según el estado del carrito"""
        if not self.items or len(self.items) == 0:
            # Carrito vacío: gris con letras blancas
            self.btn_borrar.config(
                bg='#95a5a6',
                fg='white',
                activebackground='#7f8c8d',
                activeforeground='white'
            )
        else:
            # Carrito con contenido: rojo con letras blancas
            self.btn_borrar.config(
                bg='#e74c3c',
                fg='white',
                activebackground='#ec7063',  # Rojo clarito para hover
                activeforeground='white'
            )
        
        # Configurar eventos de hover
        self.configurar_hover_borrar()
    
    def configurar_hover_borrar(self):
        """Configura los efectos hover para el botón de borrar"""
        def on_enter(event):
            if self.items and len(self.items) > 0:
                # Rojo clarito cuando hay contenido
                self.btn_borrar.config(bg='#ec7063')
            else:
                # Gris más claro cuando está vacío
                self.btn_borrar.config(bg='#bdc3c7')
        
        def on_leave(event):
            # Restaurar color original
            if self.items and len(self.items) > 0:
                self.btn_borrar.config(bg='#e74c3c')
            else:
                self.btn_borrar.config(bg='#95a5a6')
        
        self.btn_borrar.bind('<Enter>', on_enter)
        self.btn_borrar.bind('<Leave>', on_leave)
    
    def actualizar_vista(self):
        """Actualiza la vista del carrito"""
        # Limpiar items actuales
        for widget in self.frame_items.winfo_children():
            widget.destroy()
        
        if not self.items:
            self.mostrar_mensaje_vacio()
            self.label_total.config(text="Total: $0.00")
            self.btn_confirmar.config(state='normal')
            self.actualizar_estilo_boton_confirmar()
            self.actualizar_estilo_boton_borrar()
            return
        
        # Configurar grid del frame de items para que ocupen todo el ancho
        self.frame_items.columnconfigure(0, weight=1)
        
        # Mostrar cada item
        for idx, item in enumerate(self.items):
            frame_item = ttk.Frame(self.frame_items, relief='raised', borderwidth=1)
            frame_item.grid(row=idx, column=0, sticky='ew', padx=5, pady=5)
            frame_item.columnconfigure(0, weight=1)
            
            # Información del producto
            info_frame = ttk.Frame(frame_item)
            info_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
            info_frame.columnconfigure(0, weight=1)
            
            ttk.Label(
                info_frame,
                text=item['producto']['nombre'],
                font=('Arial', 10, 'bold')
            ).grid(row=0, column=0, sticky='w')
            
            # Calcular precio unitario y subtotal considerando ingredientes
            modificaciones = item.get('modificaciones_ingredientes', {})
            precio_unitario = calcular_precio_con_ingredientes(item['producto'], modificaciones)
            subtotal = precio_unitario * item['cantidad']
            
            # Mostrar precio base y ajustes si hay modificaciones
            precio_base = item['producto']['precio']
            if precio_unitario != precio_base:
                ttk.Label(
                    info_frame,
                    text=f"Base: ${precio_base:.2f} → ${precio_unitario:.2f} x {item['cantidad']} = ${subtotal:.2f}",
                    font=('Arial', 9),
                    foreground='#e67e22'
                ).grid(row=1, column=0, sticky='w')
            else:
                ttk.Label(
                    info_frame,
                    text=f"${precio_unitario:.2f} x {item['cantidad']} = ${subtotal:.2f}",
                    font=('Arial', 11),
                    foreground='gray'
                ).grid(row=1, column=0, sticky='w')
            
            # Controles de cantidad
            controles_frame = ttk.Frame(frame_item)
            controles_frame.grid(row=0, column=1, padx=5, pady=5, sticky='e')
            
            # Guardar referencia al producto_id para los callbacks (usando default parameter para capturar el valor)
            producto_id = item['producto']['id']
            
            # Crear funciones con closure correcto usando default parameters
            def crear_callback_menos(pid):
                """Crea un callback para disminuir cantidad con el producto_id correcto"""
                def callback():
                    # Buscar la cantidad actual del producto específico
                    for it in self.items:
                        if it['producto']['id'] == pid:
                            self.actualizar_cantidad(pid, it['cantidad'] - 1)
                            break
                return callback
            
            def crear_callback_mas(pid):
                """Crea un callback para aumentar cantidad con el producto_id correcto"""
                def callback():
                    # Buscar la cantidad actual del producto específico
                    for it in self.items:
                        if it['producto']['id'] == pid:
                            self.actualizar_cantidad(pid, it['cantidad'] + 1)
                            break
                return callback
            
            # Botón editar ingredientes (a la izquierda del botón menos)
            # SOLO mostrar el botón si el producto tiene ingredientes definidos
            ingredientes = item['producto'].get('ingredientes', [])
            
            # Obtener categoría del producto si no está en el item (para uso futuro)
            categoria = item['producto'].get('categoria', '')
            if not categoria:
                # Buscar la categoría del producto
                from utils.productos import buscar_producto_por_id
                resultado = buscar_producto_por_id(producto_id)
                if resultado:
                    categoria = resultado.get('categoria', '')
                    item['producto']['categoria'] = categoria
            
            # SOLO mostrar botón si tiene ingredientes (sin lógica hardcodeada)
            columna_actual = 0
            if ingredientes and len(ingredientes) > 0:
                btn_editar = ttk.Button(
                    controles_frame,
                    text="✏️",
                    width=3,
                    command=lambda pid=producto_id: self.editar_ingredientes(pid)
                )
                btn_editar.grid(row=0, column=columna_actual, padx=2)
                columna_actual += 1
            
            # Botón menos
            btn_menos = ttk.Button(
                controles_frame,
                text="-",
                width=3,
                command=crear_callback_menos(producto_id)
            )
            btn_menos.grid(row=0, column=columna_actual, padx=2)
            columna_actual += 1
            
            ttk.Label(
                controles_frame,
                text=str(item['cantidad']),
                width=3
            ).grid(row=0, column=columna_actual, padx=2)
            columna_actual += 1
            
            # Botón más
            btn_mas = ttk.Button(
                controles_frame,
                text="+",
                width=3,
                command=crear_callback_mas(producto_id)
            )
            btn_mas.grid(row=0, column=columna_actual, padx=2)
            columna_actual += 1
            
            # Botón eliminar
            btn_eliminar = ttk.Button(
                controles_frame,
                text="🗑️",
                width=3,
                command=lambda pid=producto_id: self.eliminar_item(pid)
            )
            btn_eliminar.grid(row=0, column=columna_actual, padx=2)
        
        # Actualizar total
        total = self.calcular_total()
        self.label_total.config(text=f"Total: ${total:.2f}")
        self.btn_confirmar.config(state='normal')
        
        # Actualizar estilos de los botones cuando hay contenido
        self.actualizar_estilo_boton_confirmar()
        self.actualizar_estilo_boton_borrar()
    
    def editar_ingredientes(self, producto_id):
        """Abre una ventana para editar los ingredientes de un producto"""
        # Buscar el item en el carrito
        item = None
        for it in self.items:
            if it['producto']['id'] == producto_id:
                item = it
                break
        
        if not item:
            return
        
        # Recargar el producto desde el JSON para obtener ingredientes actualizados
        from utils.productos import buscar_producto_por_id
        resultado = buscar_producto_por_id(producto_id)
        if resultado:
            # Actualizar el producto en el item con la versión más reciente
            producto_actualizado = resultado['producto']
            item['producto'] = producto_actualizado
            # Si hay nuevos ingredientes, inicializar sus modificaciones
            modificaciones = item.get('modificaciones_ingredientes', {})
            ingredientes_actuales = producto_actualizado.get('ingredientes', [])
            for ingrediente in ingredientes_actuales:
                nombre = ingrediente.get('nombre', '')
                if nombre not in modificaciones:
                    # Inicializar con cantidad_base si es un ingrediente nuevo
                    modificaciones[nombre] = ingrediente.get('cantidad_base', 1)
            item['modificaciones_ingredientes'] = modificaciones
        
        producto = item['producto']
        ingredientes = producto.get('ingredientes', [])
        
        if not ingredientes or len(ingredientes) == 0:
            mensaje = "Este producto no tiene ingredientes configurables.\n\n"
            mensaje += "Para agregar ingredientes a este producto:\n"
            mensaje += "1. Ve al panel de Administración\n"
            mensaje += "2. Selecciona el producto en la pestaña 'Productos'\n"
            mensaje += "3. Asigna ingredientes al producto desde el formulario"
            messagebox.showinfo("Sin Ingredientes", mensaje)
            return
        
        # Crear ventana modal (diseño más simple)
        ventana = tk.Toplevel(self)
        ventana.title(f"Editar Ingredientes - {producto['nombre']}")
        ventana.geometry("550x650")
        ventana.resizable(True, True)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")

        # Frame principal
        frame_principal = ttk.Frame(ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(2, weight=1)  # Área de ingredientes con scroll

        # Título
        ttk.Label(
            frame_principal,
            text="Editar Ingredientes",
            font=('Arial', 14, 'bold')
        ).grid(row=0, column=0, pady=(0, 5))

        ttk.Label(
            frame_principal,
            text=producto['nombre'],
            font=('Arial', 12),
            foreground='gray'
        ).grid(row=1, column=0, pady=(0, 10))

        # Frame para ingredientes con scroll
        frame_scroll = ttk.Frame(frame_principal)
        frame_scroll.grid(row=2, column=0, sticky='nsew', pady=10)
        frame_scroll.columnconfigure(0, weight=1)
        frame_scroll.rowconfigure(0, weight=1)

        canvas_frame = tk.Canvas(frame_scroll)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_frame.yview)
        frame_ingredientes = ttk.Frame(canvas_frame)

        frame_ingredientes.bind(
            "<Configure>",
            lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))
        )

        canvas_window = canvas_frame.create_window((0, 0), window=frame_ingredientes, anchor="nw")

        def ajustar_ancho_frame(event):
            canvas_width = event.width
            canvas_frame.itemconfig(canvas_window, width=canvas_width)

        canvas_frame.bind('<Configure>', ajustar_ancho_frame)
        canvas_frame.configure(yscrollcommand=scrollbar.set)

        canvas_frame.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Variables para almacenar las cantidades actuales
        variables_cantidad = {}
        modificaciones_actuales = item.get('modificaciones_ingredientes', {}).copy()

        # Frame para precio total (debajo de los ingredientes)
        frame_precio_total = ttk.Frame(frame_principal)
        frame_precio_total.grid(row=3, column=0, sticky='ew', pady=10)

        ttk.Separator(frame_precio_total, orient='horizontal').pack(fill='x', pady=5)

        label_precio_base = ttk.Label(
            frame_precio_total,
            text=f"Precio base: ${producto['precio']:.2f}",
            font=('Arial', 10)
        )
        label_precio_base.pack()

        label_precio_final = ttk.Label(
            frame_precio_total,
            text="",
            font=('Arial', 12, 'bold'),
            foreground='#27ae60'
        )
        label_precio_final.pack()

        # Función para calcular precio total
        def actualizar_precio_total():
            precio_base = producto.get('precio', 0.0)
            ajuste_total = 0.0

            for idx_var, var in variables_cantidad.items():
                if isinstance(idx_var, int) and idx_var < len(ingredientes):
                    ingrediente = ingredientes[idx_var]
                    cantidad_base = ingrediente.get('cantidad_base', 1)
                    precio_extra = ingrediente.get('precio_extra', 0.0)
                    precio_resta = ingrediente.get('precio_resta', 0.0)
                    cantidad_actual = var.get()

                    if cantidad_actual > cantidad_base:
                        extras = cantidad_actual - cantidad_base
                        ajuste_total += extras * precio_extra
                    elif cantidad_actual < cantidad_base:
                        quitados = cantidad_base - cantidad_actual
                        ajuste_total -= quitados * precio_resta

            precio_final = precio_base + ajuste_total
            ajuste = precio_final - precio_base

            if ajuste != 0:
                signo = "+" if ajuste > 0 else ""
                label_precio_final.config(
                    text=f"Precio final: ${precio_final:.2f} ({signo}${ajuste:.2f})"
                )
            else:
                label_precio_final.config(text=f"Precio final: ${precio_final:.2f}")

        # Debug: verificar ingredientes
        print(f"DEBUG: Producto {producto['nombre']} tiene {len(ingredientes)} ingredientes")
        for ing in ingredientes:
            print(f"  - {ing.get('nombre', 'SIN NOMBRE')}")

        # Layout de dos columnas para los ingredientes
        frame_ingredientes.columnconfigure(0, weight=1)
        frame_ingredientes.columnconfigure(1, weight=1)

        # Mostrar cada ingrediente
        if not ingredientes:
            ttk.Label(
                frame_ingredientes,
                text="Este producto no tiene ingredientes configurables.",
                font=('Arial', 10),
                foreground='gray'
            ).grid(row=0, column=0, padx=20, pady=20)

        for idx, ingrediente in enumerate(ingredientes):
            nombre = ingrediente.get('nombre', '')
            cantidad_base = ingrediente.get('cantidad_base', 1)
            precio_extra = ingrediente.get('precio_extra', 0.0)
            precio_resta = ingrediente.get('precio_resta', 0.0)

            # Obtener cantidad actual (o base si no hay modificación)
            cantidad_actual = modificaciones_actuales.get(nombre, cantidad_base)

            # Posición en dos columnas
            fila = idx // 2
            columna = idx % 2

            # Frame para cada ingrediente (diseño simple)
            frame_ing = ttk.LabelFrame(frame_ingredientes, text=nombre, padding=10)
            frame_ing.grid(row=fila, column=columna, sticky='nsew', padx=5, pady=5)
            frame_ing.columnconfigure(1, weight=1)

            # Variable para la cantidad (usar índice para manejar duplicados)
            var_cantidad = tk.IntVar(value=cantidad_actual)
            variables_cantidad[idx] = var_cantidad

            # Label cantidad
            ttk.Label(frame_ing, text="Cantidad:").grid(row=0, column=0, padx=5, sticky='w')

            # Frame para controles de cantidad
            frame_controles = ttk.Frame(frame_ing)
            frame_controles.grid(row=0, column=1, sticky='w', padx=5)

            # Botón menos
            btn_menos = ttk.Button(
                frame_controles,
                text="-",
                width=3,
                command=lambda v=var_cantidad: v.set(max(0, v.get() - 1))
            )
            btn_menos.pack(side='left', padx=2)

            # Label cantidad actual
            label_cantidad = ttk.Label(frame_controles, textvariable=var_cantidad, width=5)
            label_cantidad.pack(side='left', padx=5)

            # Botón más
            btn_mas = ttk.Button(
                frame_controles,
                text="+",
                width=3,
                command=lambda v=var_cantidad: v.set(v.get() + 1)
            )
            btn_mas.pack(side='left', padx=2)

            # Información de precios
            info_text = f"Base: {cantidad_base}"
            if precio_extra > 0:
                info_text += f" | Extra: +${precio_extra:.2f}"
            if precio_resta > 0:
                info_text += f" | Quitar: -${precio_resta:.2f}"

            ttk.Label(
                frame_ing,
                text=info_text,
                font=('Arial', 8),
                foreground='black'
            ).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=2)

            # Label impacto en precio
            label_impacto = ttk.Label(frame_ing, text="", font=('Arial', 9, 'bold'))
            label_impacto.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=2)

            # Callback para actualizar impacto y precio total
            def on_cambio_cantidad(*_args,
                                   var_ref=var_cantidad,
                                   label_ref=label_impacto,
                                   base=cantidad_base,
                                   p_extra=precio_extra,
                                   p_resta=precio_resta):
                cantidad = var_ref.get()
                if cantidad > base:
                    impacto = (cantidad - base) * p_extra
                    label_ref.config(text=f"Impacto: +${impacto:.2f}", foreground='#e67e22')
                elif cantidad < base:
                    impacto = (base - cantidad) * p_resta
                    label_ref.config(text=f"Impacto: -${impacto:.2f}", foreground='#e67e22')
                else:
                    label_ref.config(text="", foreground='gray')
                actualizar_precio_total()

            # Vincular cambios de cantidad
            var_cantidad.trace_add('write', on_cambio_cantidad)
            # Inicializar impacto para el estado actual
            on_cambio_cantidad()

        # Asegurar que el frame_ingredientes tenga el ancho correcto
        frame_ingredientes.update_idletasks()
        canvas_frame.update_idletasks()

        # Inicializar precio total al abrir la ventana
        actualizar_precio_total()

        # Frame para botones (simple)
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.grid(row=4, column=0, pady=15, sticky='ew')
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        # Botón Cancelar
        btn_cancelar = tk.Button(
            frame_botones,
            text="❌ Cancelar",
            command=ventana.destroy,
            width=18,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2',
            activebackground='#7f8c8d',
            activeforeground='white'
        )
        btn_cancelar.grid(row=0, column=0, padx=5, sticky='ew')
        
        # Botón Guardar/Aceptar
        def guardar_modificaciones():
            # Convertir modificaciones a formato por nombre (sumando duplicados)
            modificaciones_por_nombre = {}
            
            for idx_var, var in variables_cantidad.items():
                if isinstance(idx_var, int) and idx_var < len(ingredientes):
                    ingrediente = ingredientes[idx_var]
                    nombre = ingrediente.get('nombre', '')
                    cantidad_base = ingrediente.get('cantidad_base', 1)
                    cantidad_actual = var.get()
                    
                    if nombre in modificaciones_por_nombre:
                        diferencia_anterior = modificaciones_por_nombre[nombre] - cantidad_base
                        diferencia_nueva = cantidad_actual - cantidad_base
                        modificaciones_por_nombre[nombre] = cantidad_base + diferencia_anterior + diferencia_nueva
                    else:
                        modificaciones_por_nombre[nombre] = cantidad_actual
            
            item['modificaciones_ingredientes'] = modificaciones_por_nombre
            self.actualizar_vista()
            ventana.destroy()
        
        btn_guardar = tk.Button(
            frame_botones,
            text="✅ Aceptar",
            command=guardar_modificaciones,
            width=18,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            cursor='hand2',
            activebackground='#2ecc71',
            activeforeground='white'
        )
        btn_guardar.grid(row=0, column=1, padx=5, sticky='ew')
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")
    
    def on_confirmar(self):
        """Callback cuando se confirma el pedido"""
        if not self.items:
            return
        
        # Abrir ventana de confirmación
        self.mostrar_ventana_confirmacion()
    
    def mostrar_ventana_confirmacion(self):
        """Muestra una ventana secundaria para confirmar el pedido"""
        ventana = tk.Toplevel(self)
        ventana.title("Confirmar Pedido")
        ventana.geometry("450x550")
        ventana.resizable(False, False)
        
        # Centrar la ventana
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Frame principal con scroll si es necesario
        frame_principal = ttk.Frame(ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(
            frame_principal,
            text="Confirmar Pedido",
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 10))
        
        # Número de orden
        ttk.Label(
            frame_principal,
            text=f"Orden #{self.numero_orden:04d}",
            font=('Arial', 12, 'bold'),
            foreground='#3498db'
        ).pack(pady=(0, 20))
        
        # Frame para información del cliente
        frame_cliente = ttk.LabelFrame(frame_principal, text="Datos del Cliente", padding=10)
        frame_cliente.pack(fill='x', pady=5)
        
        # Campo nombre del cliente
        ttk.Label(frame_cliente, text="Nombre del Cliente:", font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        entry_nombre = ttk.Entry(frame_cliente, width=40, font=('Arial', 10))
        entry_nombre.pack(fill='x', pady=(0, 15))
        entry_nombre.focus()
        
        # Frame para input de domicilio (inicialmente oculto)
        frame_domicilio = ttk.Frame(frame_cliente)
        
        ttk.Label(frame_domicilio, text="Dirección:", font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        entry_domicilio = ttk.Entry(frame_domicilio, width=40, font=('Arial', 10))
        entry_domicilio.pack(fill='x')
        
        # Ocultar inicialmente el frame de domicilio
        frame_domicilio.pack_forget()
        
        # Checkbox para pedido a domicilio
        self.var_domicilio = tk.BooleanVar()
        checkbox_domicilio = ttk.Checkbutton(
            frame_cliente,
            text="Pedido a domicilio",
            variable=self.var_domicilio,
            command=lambda: self.toggle_domicilio_input(frame_domicilio)
        )
        checkbox_domicilio.pack(anchor='w', pady=5)
        
        # Guardar referencias para acceso desde callbacks
        self.entry_domicilio = entry_domicilio
        self.frame_domicilio = frame_domicilio
        
        # Frame para forma de pago
        frame_pago = ttk.LabelFrame(frame_principal, text="Forma de Pago", padding=10)
        frame_pago.pack(fill='x', pady=10)
        
        # Variable para forma de pago
        self.var_forma_pago = tk.StringVar(value="Efectivo")
        
        # Opciones de pago
        opciones_pago = [
            ("Efectivo", "Efectivo"),
            ("Tarjeta", "Tarjeta"),
            ("Transferencia", "Transferencia")
        ]
        
        for texto, valor in opciones_pago:
            ttk.Radiobutton(
                frame_pago,
                text=texto,
                variable=self.var_forma_pago,
                value=valor
            ).pack(anchor='w', pady=3)
        
        # Frame para el total
        frame_total = ttk.Frame(frame_principal)
        frame_total.pack(pady=(10, 5))
        
        # Calcular y mostrar el total
        total = self.calcular_total()
        ttk.Label(
            frame_total,
            text=f"Total: ${total:.2f}",
            font=('Arial', 14, 'bold'),
            foreground='#2c3e50'
        ).pack()
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=15)
        
        # Botón Cancelar (usando tk.Button para mejor control de hover) - PRIMERO
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
        
        # Configurar hover para botón Cancelar (rojo clarito)
        def on_enter_cancelar(event):
            btn_cancelar.config(bg='#ec7063')
        def on_leave_cancelar(event):
            btn_cancelar.config(bg='#e74c3c')
        btn_cancelar.bind('<Enter>', on_enter_cancelar)
        btn_cancelar.bind('<Leave>', on_leave_cancelar)
        
        # Botón Aceptar (usando tk.Button para mejor control de hover) - SEGUNDO
        btn_aceptar = tk.Button(
            frame_botones,
            text="Aceptar",
            command=lambda: self.procesar_confirmacion(ventana, entry_nombre.get(), entry_domicilio.get()),
            width=15,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#2ecc71',
            activeforeground='white'
        )
        btn_aceptar.pack(side='left', padx=5)
        
        # Configurar hover para botón Aceptar
        def on_enter_aceptar(event):
            btn_aceptar.config(bg='#2ecc71')
        def on_leave_aceptar(event):
            btn_aceptar.config(bg='#27ae60')
        btn_aceptar.bind('<Enter>', on_enter_aceptar)
        btn_aceptar.bind('<Leave>', on_leave_aceptar)
        
        # Centrar la ventana en la pantalla
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")
    
    def toggle_domicilio_input(self, frame_domicilio):
        """Muestra u oculta el input de domicilio según el checkbox"""
        if self.var_domicilio.get():
            frame_domicilio.pack(fill='x', pady=(5, 0), before=None)
        else:
            frame_domicilio.pack_forget()
    
    def procesar_confirmacion(self, ventana, nombre_cliente, domicilio):
        """Procesa la confirmación del pedido"""
        # Validar que se haya ingresado el nombre del cliente
        if not nombre_cliente or not nombre_cliente.strip():
            messagebox.showwarning(
                "Campo Requerido",
                "Por favor, ingrese el nombre del cliente."
            )
            return
        
        # Validar domicilio si es pedido a domicilio
        if self.var_domicilio.get():
            if not domicilio or not domicilio.strip():
                messagebox.showwarning(
                    "Campo Requerido",
                    "Por favor, ingrese la dirección de entrega."
                )
                return
        
        # Obtener tipo de pedido
        tipo_pedido = "Domicilio" if self.var_domicilio.get() else "Mesa/Llevar"
        
        # Obtener forma de pago
        forma_pago = self.var_forma_pago.get()
        
        # Guardar información completa del pedido (para tickets)
        total = self.calcular_total()
        pedido_info = {
            'numero': self.numero_orden,
            'nombre_cliente': nombre_cliente.strip(),
            'tipo': tipo_pedido,
            'domicilio': domicilio.strip() if self.var_domicilio.get() else None,
            'forma_pago': forma_pago,
            'items': self.items.copy(),
            'total': total
        }
        
        # Cerrar ventana de confirmación
        ventana.destroy()
        
        # Generar tickets (COCINA y CLIENTE) e imprimir automáticamente
        # Los tickets se imprimen directamente usando Win32Raw sin previsualización
        try:
            resultado = generar_tickets_pedido(pedido_info, imprimir_automatico=True, guardar_respaldo=True)
            
            # Construir mensaje sobre tickets generados
            if resultado.get('cocina') and resultado.get('cliente'):
                mensaje_tickets = f"\n\nTickets generados:\n• {os.path.basename(resultado['cocina'])}\n• {os.path.basename(resultado['cliente'])}"
            else:
                mensaje_tickets = "\n\nTickets generados"
            
            # Informar sobre el estado de la impresión
            if resultado.get('impresion_cocina') and resultado.get('impresion_cliente'):
                mensaje_tickets += "\n\n✅ Tickets enviados a la impresora"
            elif resultado.get('impresion_cocina') or resultado.get('impresion_cliente'):
                mensaje_tickets += "\n\n⚠ Algunos tickets no se pudieron imprimir"
            else:
                mensaje_tickets += "\n\n⚠ No se pudo imprimir (verifique la impresora)"
        except Exception as e:
            mensaje_tickets = f"\n\n⚠ Error al generar/imprimir tickets: {str(e)}"
        
        # Mostrar messagebox
        messagebox.showinfo(
            "Pedido Confirmado",
            f"Pedido #{self.numero_orden:04d} confirmado.\n"
            f"Cliente: {nombre_cliente.strip()}\n"
            f"Total: ${total:.2f}"
            f"{mensaje_tickets}"
        )
        
        # Limpiar el carrito
        self.items = []
        self.actualizar_vista()
        
        # Generar nuevo número de pedido
        self.numero_orden = incrementar_orden()
        self.label_numero_pedido.config(text=f"Pedido #{self.numero_orden:04d}")
        
        # Actualizar estilos de los botones después de limpiar
        self.actualizar_estilo_boton_confirmar()
        self.actualizar_estilo_boton_borrar()
    
    def on_borrar_carrito(self):
        """Callback cuando se quiere borrar todo el carrito"""
        if not self.items:
            return
        
        # Mostrar ventana de confirmación
        self.mostrar_ventana_confirmacion_borrar()
    
    def mostrar_ventana_confirmacion_borrar(self):
        """Muestra una ventana de confirmación para borrar el carrito"""
        ventana = tk.Toplevel(self)
        ventana.title("Confirmar Borrado")
        ventana.geometry("350x150")
        ventana.resizable(False, False)
        
        # Centrar la ventana
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        
        # Frame principal
        frame_principal = ttk.Frame(ventana, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        # Mensaje de confirmación
        ttk.Label(
            frame_principal,
            text="¿Está seguro de borrar todo el carrito?",
            font=('Arial', 12),
            justify='center'
        ).pack(pady=10)
        
        ttk.Label(
            frame_principal,
            text="Esta acción no se puede deshacer.",
            font=('Arial', 9),
            foreground='gray',
            justify='center'
        ).pack(pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=15)
        
        # Botón Confirmar (usando tk.Button para mejor compatibilidad de estilos)
        btn_confirmar = tk.Button(
            frame_botones,
            text="Sí, Borrar",
            command=lambda: self.borrar_carrito_completo(ventana),
            width=15,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#ec7063',
            activeforeground='white'
        )
        btn_confirmar.pack(side='left', padx=5)
        
        # Configurar hover para botón Confirmar borrado (rojo clarito)
        def on_enter_confirmar_borrar(event):
            btn_confirmar.config(bg='#ec7063')
        def on_leave_confirmar_borrar(event):
            btn_confirmar.config(bg='#e74c3c')
        btn_confirmar.bind('<Enter>', on_enter_confirmar_borrar)
        btn_confirmar.bind('<Leave>', on_leave_confirmar_borrar)
        
        # Botón Cancelar (usando tk.Button para mejor compatibilidad de estilos)
        btn_cancelar = tk.Button(
            frame_botones,
            text="Cancelar",
            command=ventana.destroy,
            width=15,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#7f8c8d',
            activeforeground='white'
        )
        btn_cancelar.pack(side='left', padx=5)
        
        # Configurar hover para botón Cancelar
        def on_enter_cancelar_borrar(event):
            btn_cancelar.config(bg='#bdc3c7')
        def on_leave_cancelar_borrar(event):
            btn_cancelar.config(bg='#95a5a6')
        btn_cancelar.bind('<Enter>', on_enter_cancelar_borrar)
        btn_cancelar.bind('<Leave>', on_leave_cancelar_borrar)
        
        # Centrar la ventana en la pantalla
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")
    
    def borrar_carrito_completo(self, ventana):
        """Borra todo el contenido del carrito"""
        # Limpiar items
        self.items = []
        
        # Actualizar vista
        self.actualizar_vista()
        
        # Cerrar ventana de confirmación
        ventana.destroy()
        
        # Mostrar mensaje de confirmación
        messagebox.showinfo(
            "Carrito Borrado",
            "El carrito ha sido borrado correctamente."
        )
