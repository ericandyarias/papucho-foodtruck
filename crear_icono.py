"""
Script para crear el icono de la aplicación Papucho Foodtruck
Genera un archivo icono.ico que se usará en el ejecutable y el instalador
"""
from PIL import Image, ImageDraw, ImageFont
import os

def crear_icono():
    """Crea un icono .ico para la aplicación"""
    
    # Tamaños estándar para iconos de Windows (ICO puede contener múltiples tamaños)
    tamanos = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Crear lista de imágenes para el ICO
    imagenes = []
    
    for tamano in tamanos:
        # Crear imagen con fondo
        img = Image.new('RGB', tamano, color='#FF6B35')  # Color naranja para foodtruck
        draw = ImageDraw.Draw(img)
        
        # Dibujar un círculo/plato como fondo
        margin = tamano[0] // 8
        draw.ellipse(
            [margin, margin, tamano[0] - margin, tamano[1] - margin],
            fill='#FFFFFF',
            outline='#2c3e50',
            width=max(1, tamano[0] // 32)
        )
        
        # Intentar dibujar texto "P" o símbolo de comida
        try:
            # Calcular tamaño de fuente apropiado
            font_size = tamano[0] // 2
            # Intentar usar una fuente del sistema
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Dibujar "P" en el centro
            texto = "P"
            bbox = draw.textbbox((0, 0), texto, font=font)
            texto_width = bbox[2] - bbox[0]
            texto_height = bbox[3] - bbox[1]
            
            x = (tamano[0] - texto_width) // 2
            y = (tamano[1] - texto_height) // 2 - bbox[1]
            
            draw.text((x, y), texto, fill='#FF6B35', font=font)
        except Exception as e:
            # Si falla el texto, dibujar un símbolo simple
            center = tamano[0] // 2
            radius = tamano[0] // 4
            draw.ellipse(
                [center - radius, center - radius, center + radius, center + radius],
                fill='#FF6B35'
            )
        
        imagenes.append(img)
    
    # Guardar como ICO
    imagenes[0].save(
        'icono.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in imagenes]
    )
    
    print("Icono creado exitosamente: icono.ico")
    print(f"   Tamanos incluidos: {', '.join([f'{w}x{h}' for w, h in tamanos])}")

if __name__ == "__main__":
    try:
        crear_icono()
    except ImportError:
        print("Error: Pillow no esta instalado.")
        print("   Instala con: python -m pip install Pillow")
    except Exception as e:
        print(f"Error al crear el icono: {e}")
