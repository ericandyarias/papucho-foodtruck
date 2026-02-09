"""
Sistema de Caja para Foodtruck - PAPUCHO FOODTRUCK
Aplicación principal que integra todos los componentes de la UI
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import time

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.encabezado import Encabezado
from ui.navegador import Navegador
from ui.seleccion import Seleccion
from ui.carrito import Carrito
from ui.administracion import VentanaAdministracion
from ui.splash import SplashScreen
from utils.productos import cargar_productos, guardar_productos
from utils.ingredientes import cargar_ingredientes, guardar_ingredientes


class AplicacionCaja:
    """Clase principal de la aplicación de caja"""
    
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.configurar_cierre()
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
    
    def configurar_cierre(self):
        """Configura el handler para cuando se cierra la ventana"""
        def on_closing():
            """Handler que se ejecuta al cerrar la aplicación"""
            # Mostrar ventana de confirmación
            respuesta = messagebox.askyesno(
                "Confirmar cierre",
                "¿Está seguro que desea cerrar el sistema?",
                icon='question'
            )
            
            # Si el usuario confirma, proceder con el cierre
            if respuesta:
                try:
                    # Forzar guardado de todos los datos
                    self.guardar_todos_los_datos()
                except Exception as e:
                    # Si hay error al guardar, mostrar mensaje pero permitir cerrar
                    print(f"Error al guardar datos: {e}")
                finally:
                    # Cerrar la aplicación
                    self.root.destroy()
            # Si el usuario cancela, no hacer nada (la ventana permanece abierta)
        
        # Vincular el evento de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
    
    def guardar_todos_los_datos(self):
        """Fuerza el guardado de todos los datos (productos e ingredientes)"""
        try:
            # Recargar y guardar productos (fuerza sincronización)
            productos_data = cargar_productos()
            guardar_productos(productos_data)
            
            # Recargar y guardar ingredientes (fuerza sincronización)
            ingredientes_data = cargar_ingredientes()
            guardar_ingredientes(ingredientes_data)
        except Exception as e:
            print(f"Error al guardar datos al cerrar: {e}")
            raise
    
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
        self.frame_principal.columnconfigure(1, weight=5)  # Selección (centro) - más espacio
        self.frame_principal.columnconfigure(0, weight=1)  # Navegador - más estrecho
        self.frame_principal.columnconfigure(2, weight=2)  # Carrito
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
    # Crear ventana principal pero ocultarla inmediatamente (debe existir para el splash)
    root = tk.Tk()
    root.withdraw()  # Ocultar inmediatamente, no se verá hasta que se muestre explícitamente
    
    # Crear splash screen PRIMERO (aparecerá antes que todo)
    splash = SplashScreen(root=root)
    
    # Forzar que el splash se muestre y esté al frente
    splash.splash.update()
    splash.splash.lift()
    splash.splash.attributes('-topmost', True)
    
    # Simular progreso inicial
    splash.actualizar_progreso(5, "Iniciando sistema...")
    splash.splash.update()
    time.sleep(0.3)
    
    def inicializar_aplicacion():
        """Función que inicializa la aplicación"""
        # Actualizar progreso
        splash.actualizar_progreso(15, "Cargando productos...")
        splash.splash.update()
        time.sleep(0.2)
        
        # Asegurar que las categorías fijas existan al iniciar
        cargar_productos()
        
        splash.actualizar_progreso(35, "Cargando ingredientes...")
        splash.splash.update()
        time.sleep(0.2)
        
        # Cargar ingredientes para verificar que todo esté bien
        cargar_ingredientes()
        
        splash.actualizar_progreso(50, "Inicializando componentes...")
        splash.splash.update()
        time.sleep(0.2)
        
        # Crear la aplicación (pero la ventana sigue oculta)
        splash.actualizar_progreso(65, "Creando interfaz...")
        splash.splash.update()
        app = AplicacionCaja(root)
        
        splash.actualizar_progreso(85, "Preparando interfaz...")
        splash.splash.update()
        time.sleep(0.2)
        
        splash.actualizar_progreso(95, "Finalizando...")
        splash.splash.update()
        time.sleep(0.2)
        
        return app
    
    # Inicializar aplicación con splash screen
    try:
        app = inicializar_aplicacion()
        splash.actualizar_progreso(100, "¡Listo!")
        splash.splash.update()
        time.sleep(0.3)
        
        # Cerrar splash después de un pequeño delay para que se vea el progreso
        def cerrar_splash_y_mostrar():
            splash.cerrar()
            # Asegurar que la ventana principal esté visible y al frente
            root.deiconify()
            root.lift()
            root.focus_set()
        
        splash.splash.after(200, cerrar_splash_y_mostrar)
    except Exception as e:
        splash.cerrar()
        if root:
            root.deiconify()
        raise
    
    # Iniciar el loop principal (ahora la ventana principal está visible)
    root.mainloop()


if __name__ == "__main__":
    main()
