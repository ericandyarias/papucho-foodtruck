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
        
        # Si no existe, agregarlo
        self.items.append({
            'producto': producto,
            'cantidad': cantidad
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
        """Calcula el total del carrito"""
        total = 0
        for item in self.items:
            total += item['producto']['precio'] * item['cantidad']
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
            
            subtotal = item['producto']['precio'] * item['cantidad']
            ttk.Label(
                info_frame,
                text=f"${item['producto']['precio']:.2f} x {item['cantidad']} = ${subtotal:.2f}",
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
            
            # Botón menos
            btn_menos = ttk.Button(
                controles_frame,
                text="-",
                width=3,
                command=crear_callback_menos(producto_id)
            )
            btn_menos.grid(row=0, column=0, padx=2)
            
            ttk.Label(
                controles_frame,
                text=str(item['cantidad']),
                width=3
            ).grid(row=0, column=1, padx=2)
            
            # Botón más
            btn_mas = ttk.Button(
                controles_frame,
                text="+",
                width=3,
                command=crear_callback_mas(producto_id)
            )
            btn_mas.grid(row=0, column=2, padx=2)
            
            # Botón eliminar
            btn_eliminar = ttk.Button(
                controles_frame,
                text="🗑️",
                width=3,
                command=lambda pid=producto_id: self.eliminar_item(pid)
            )
            btn_eliminar.grid(row=0, column=3, padx=2)
        
        # Actualizar total
        total = self.calcular_total()
        self.label_total.config(text=f"Total: ${total:.2f}")
        self.btn_confirmar.config(state='normal')
        
        # Actualizar estilos de los botones cuando hay contenido
        self.actualizar_estilo_boton_confirmar()
        self.actualizar_estilo_boton_borrar()
    
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
        
        # Imprimir información del pedido (para depuración y futura implementación de tickets)
        print("=" * 50)
        print(f"PEDIDO #{self.numero_orden:04d} CONFIRMADO")
        print("=" * 50)
        print(f"Cliente: {pedido_info['nombre_cliente']}")
        print(f"Tipo: {tipo_pedido}")
        if pedido_info['domicilio']:
            print(f"Domicilio: {pedido_info['domicilio']}")
        print(f"Forma de Pago: {forma_pago}")
        print("-" * 50)
        print("Items:")
        for item in pedido_info['items']:
            subtotal = item['producto']['precio'] * item['cantidad']
            print(f"  - {item['producto']['nombre']} x{item['cantidad']} = ${subtotal:.2f}")
        print("-" * 50)
        print(f"TOTAL: ${total:.2f}")
        print("=" * 50)
        
        # TODO: Aquí se puede guardar en archivo JSON o base de datos para generar tickets
        # Por ejemplo: guardar_pedido(pedido_info)
        
        # Cerrar ventana de confirmación
        ventana.destroy()
        
        # Mostrar previsualización de tickets
        self.mostrar_previsualizacion_tickets(pedido_info)
        
        # Mostrar messagebox
        messagebox.showinfo(
            "Pedido Confirmado",
            f"Pedido #{self.numero_orden:04d} confirmado.\n"
            f"Cliente: {nombre_cliente.strip()}\n"
            f"Total: ${total:.2f}\n\n"
            f"Previsualización de tickets mostrada."
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
    
    def mostrar_previsualizacion_tickets(self, pedido_info):
        """Muestra una previsualización de los tickets (cocina y cliente)"""
        ventana_tickets = tk.Toplevel(self)
        ventana_tickets.title("Previsualización de Tickets")
        ventana_tickets.geometry("700x900")
        ventana_tickets.resizable(True, True)
        
        # Centrar la ventana
        ventana_tickets.transient(self.winfo_toplevel())
        
        # Frame principal con scroll
        frame_principal = ttk.Frame(ventana_tickets, padding=20)
        frame_principal.pack(fill='both', expand=True)
        
        # Título de la ventana
        ttk.Label(
            frame_principal,
            text="Previsualización de Tickets (8 cm de ancho)",
            font=('Arial', 12, 'bold')
        ).pack(pady=(0, 20))
        
        # Frame para los dos tickets lado a lado
        frame_tickets = tk.Frame(frame_principal, bg='lightgray')
        frame_tickets.pack(fill='both', expand=True, pady=10)
        
        # Ancho del ticket: 8 cm (para impresora térmica de 80mm)
        # 8 cm = aproximadamente 302 píxeles a 96 DPI
        ancho_ticket = 302
        
        # Frame para centrar los tickets (usando grid)
        frame_centro = tk.Frame(frame_tickets, bg='lightgray')
        frame_centro.pack(expand=True)
        frame_centro.grid_columnconfigure(0, weight=1)
        frame_centro.grid_columnconfigure(1, weight=1)
        
        # Ticket para COCINA
        self.crear_ticket_preview(
            frame_centro,
            pedido_info,
            "COCINA",
            ancho_ticket,
            columna=0
        )
        
        # Ticket para CLIENTE
        self.crear_ticket_preview(
            frame_centro,
            pedido_info,
            "CLIENTE",
            ancho_ticket,
            columna=1
        )
        
        # Botón cerrar
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=20)
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="Cerrar",
            command=ventana_tickets.destroy,
            width=20,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            relief='flat',
            cursor='hand2',
            activebackground='#7f8c8d',
            activeforeground='white'
        )
        btn_cerrar.pack()
        
        # Configurar hover para botón cerrar
        def on_enter_cerrar(event):
            btn_cerrar.config(bg='#bdc3c7')
        def on_leave_cerrar(event):
            btn_cerrar.config(bg='#95a5a6')
        btn_cerrar.bind('<Enter>', on_enter_cerrar)
        btn_cerrar.bind('<Leave>', on_leave_cerrar)
        
        # Centrar la ventana
        ventana_tickets.update_idletasks()
        x = (ventana_tickets.winfo_screenwidth() // 2) - (ventana_tickets.winfo_width() // 2)
        y = (ventana_tickets.winfo_screenheight() // 2) - (ventana_tickets.winfo_height() // 2)
        ventana_tickets.geometry(f"+{x}+{y}")
    
    def crear_ticket_preview(self, parent, pedido_info, tipo_ticket, ancho, columna):
        """Crea la previsualización de un ticket individual"""
        # Frame del ticket con borde
        frame_ticket = tk.Frame(
            parent,
            relief='solid',
            borderwidth=2,
            bg='white'
        )
        frame_ticket.grid(row=0, column=columna, padx=10, pady=10, sticky='n')
        
        # Frame interno con padding reducido para 8 cm
        frame_contenido = tk.Frame(frame_ticket, bg='white', padx=8, pady=8, width=ancho-16)
        frame_contenido.pack(fill='both', expand=True)
        
        # Configurar ancho mínimo del frame_ticket
        frame_ticket.config(width=ancho)
        
        # Título del puesto (centrado, fuente más pequeña)
        label_titulo = tk.Label(
            frame_contenido,
            text="PAPUCHO FOODTRUCK",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        label_titulo.pack(pady=(0, 5))
        
        # Separador
        tk.Frame(frame_contenido, height=1, bg='#2c3e50').pack(fill='x', pady=(0, 8))
        
        # Número de orden (centrado, fuente más pequeña)
        label_orden = tk.Label(
            frame_contenido,
            text=f"Orden #{pedido_info['numero']:04d}",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#3498db'
        )
        label_orden.pack(pady=(0, 5))
        
        # Cliente
        frame_cliente = tk.Frame(frame_contenido, bg='white')
        frame_cliente.pack(fill='x', pady=(0, 4))
        
        tk.Label(
            frame_cliente,
            text="Cliente:",
            font=('Arial', 8, 'bold'),
            bg='white',
            anchor='w'
        ).pack(side='left')
        
        tk.Label(
            frame_cliente,
            text=pedido_info['nombre_cliente'],
            font=('Arial', 8),
            bg='white',
            anchor='w'
        ).pack(side='left', padx=(3, 0))
        
        # Domicilio (si existe)
        if pedido_info['domicilio']:
            frame_domicilio = tk.Frame(frame_contenido, bg='white')
            frame_domicilio.pack(fill='x', pady=(0, 4))
            
            tk.Label(
                frame_domicilio,
                text="Domicilio:",
                font=('Arial', 8, 'bold'),
                bg='white',
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_domicilio,
                text=pedido_info['domicilio'],
                font=('Arial', 8),
                bg='white',
                anchor='w',
                wraplength=ancho-40,
                justify='left'
            ).pack(side='left', padx=(3, 0), fill='x')
        
        # Separador
        tk.Frame(frame_contenido, height=1, bg='#bdc3c7').pack(fill='x', pady=6)
        
        # Items del pedido
        tk.Label(
            frame_contenido,
            text="PEDIDO:",
            font=('Arial', 9, 'bold'),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(0, 4))
        
        # Frame para items con scroll si es necesario
        frame_items = tk.Frame(frame_contenido, bg='white')
        frame_items.pack(fill='both', expand=True)
        
        for item in pedido_info['items']:
            frame_item = tk.Frame(frame_items, bg='white')
            frame_item.pack(fill='x', pady=2)
            
            # Primera línea: Nombre del producto y cantidad (de izquierda a derecha)
            nombre_cantidad = f"{item['producto']['nombre']} x{item['cantidad']}"
            tk.Label(
                frame_item,
                text=nombre_cantidad,
                font=('Arial', 8),
                bg='white',
                anchor='w'
            ).pack(fill='x', pady=(0, 2))
            
            # Segunda línea: Monto total del item (alineado a la derecha)
            subtotal = item['producto']['precio'] * item['cantidad']
            tk.Label(
                frame_item,
                text=f"${subtotal:.2f}",
                font=('Arial', 8, 'bold'),
                bg='white',
                anchor='e'
            ).pack(fill='x')
        
        # Separador
        tk.Frame(frame_contenido, height=1, bg='#bdc3c7').pack(fill='x', pady=6)
        
        # Total a pagar
        frame_total = tk.Frame(frame_contenido, bg='white')
        frame_total.pack(fill='x', pady=(0, 4))
        
        tk.Label(
            frame_total,
            text="TOTAL A PAGAR:",
            font=('Arial', 9, 'bold'),
            bg='white',
            anchor='w'
        ).pack(side='left')
        
        tk.Label(
            frame_total,
            text=f"${pedido_info['total']:.2f}",
            font=('Arial', 9, 'bold'),
            bg='white',
            anchor='e'
        ).pack(side='right')
        
        # Forma de pago
        tk.Label(
            frame_contenido,
            text=f"Forma de Pago: {pedido_info['forma_pago']}",
            font=('Arial', 8),
            bg='white',
            anchor='w'
        ).pack(fill='x', pady=(3, 0))
        
        # Separador final
        tk.Frame(frame_contenido, height=1, bg='#2c3e50').pack(fill='x', pady=(8, 0))
        
        # Marca del ticket (COCINA o CLIENTE)
        color_marca = '#e74c3c' if tipo_ticket == 'COCINA' else '#27ae60'
        tk.Label(
            frame_contenido,
            text=f"═══ {tipo_ticket} ═══",
            font=('Arial', 9, 'bold'),
            bg='white',
            fg=color_marca
        ).pack(pady=(6, 0))
        
        # Actualizar el frame para que se muestre correctamente
        frame_ticket.update_idletasks()
    
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
