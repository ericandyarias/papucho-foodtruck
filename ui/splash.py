"""
Módulo para la pantalla de carga (splash screen)
Se muestra mientras se inicializa la aplicación
"""
import tkinter as tk
from tkinter import ttk
import threading
import time


class SplashScreen:
    """Pantalla de carga que se muestra al iniciar la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.splash = None
        self.progress_var = None
        self.label_status = None
        self.crear_splash()
    
    def crear_splash(self):
        """Crea la ventana de splash screen"""
        # Crear ventana de splash
        self.splash = tk.Toplevel(self.root)
        self.splash.title("Cargando...")
        self.splash.geometry("500x350")
        self.splash.resizable(False, False)
        
        # Remover decoraciones de ventana (opcional, puede causar problemas en algunos sistemas)
        # self.splash.overrideredirect(True)
        
        # Centrar la ventana
        self.splash.transient(self.root)
        self.splash.grab_set()
        
        # Frame principal
        frame_principal = tk.Frame(self.splash, bg='#2c3e50')
        frame_principal.pack(fill='both', expand=True)
        
        # Título
        label_titulo = tk.Label(
            frame_principal,
            text="🍔 PAPUCHO FOODTRUCK",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        label_titulo.pack(pady=(50, 10))
        
        # Subtítulo
        label_subtitulo = tk.Label(
            frame_principal,
            text="Sistema de Caja",
            font=('Arial', 14),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        label_subtitulo.pack(pady=(0, 30))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            frame_principal,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        progress_bar.pack(pady=20)
        
        # Label de estado
        self.label_status = tk.Label(
            frame_principal,
            text="Inicializando...",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        self.label_status.pack(pady=10)
        
        # Centrar la ventana en la pantalla
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (self.splash.winfo_width() // 2)
        y = (self.splash.winfo_screenheight() // 2) - (self.splash.winfo_height() // 2)
        self.splash.geometry(f"+{x}+{y}")
        
        # Ocultar la ventana principal mientras se carga
        self.root.withdraw()
    
    def actualizar_progreso(self, valor, mensaje=""):
        """Actualiza el progreso de la barra de carga"""
        if self.progress_var:
            self.progress_var.set(valor)
        if self.label_status and mensaje:
            self.label_status.config(text=mensaje)
        if self.splash:
            self.splash.update()
    
    def cerrar(self):
        """Cierra la pantalla de carga y muestra la ventana principal"""
        if self.splash:
            self.splash.destroy()
        self.root.deiconify()  # Mostrar la ventana principal
        self.root.focus_set()


def mostrar_splash_con_carga(root, funcion_carga, *args, **kwargs):
    """
    Muestra la pantalla de carga mientras se ejecuta una función de carga
    
    Args:
        root: Ventana raíz de Tkinter
        funcion_carga: Función que se ejecutará para cargar datos
        *args, **kwargs: Argumentos para la función de carga
    
    Returns:
        Resultado de la función de carga
    """
    splash = SplashScreen(root)
    
    resultado = None
    error = None
    
    def cargar_en_thread():
        """Ejecuta la carga en un thread separado"""
        nonlocal resultado, error
        try:
            # Simular progreso inicial
            splash.actualizar_progreso(10, "Cargando productos...")
            time.sleep(0.1)
            
            splash.actualizar_progreso(30, "Cargando ingredientes...")
            time.sleep(0.1)
            
            splash.actualizar_progreso(50, "Inicializando componentes...")
            time.sleep(0.1)
            
            # Ejecutar la función de carga real
            splash.actualizar_progreso(70, "Preparando interfaz...")
            resultado = funcion_carga(*args, **kwargs)
            
            splash.actualizar_progreso(100, "¡Listo!")
            time.sleep(0.2)
        except Exception as e:
            error = e
        finally:
            # Cerrar splash después de un pequeño delay
            root.after(100, splash.cerrar)
    
    # Ejecutar carga en thread separado
    thread = threading.Thread(target=cargar_en_thread, daemon=True)
    thread.start()
    
    # Mantener la ventana de splash activa hasta que termine
    while thread.is_alive():
        root.update()
        time.sleep(0.01)
    
    # Cerrar splash
    splash.cerrar()
    
    if error:
        raise error
    
    return resultado
