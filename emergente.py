
import flet as ft
import cv2
from cortar_imagen import ImagenOpenCV
# from cortar_imagen import interfaz_edicion
# from cortar_imagen import coordenadas_recorte, coordenadas_seleccion, escala_minima, escala_maxima, xmouse, ymouse 


# Variables globales de la interfaz de edicion de opencv
# coordenadas_recorte = [0,0,0,0]
# coordenadas_seleccion = [0,0,0,0]
# escala_minima = 100     #inicializacion por defecto 
# escala_maxima = 200     #inicializacion por defecto 
# xmouse = ymouse =0

clickeos = 0

def main(page: ft.Page):


    base = 768
    altura = 768
    

    ruta_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
    ruta_imagen = '1686469590.png'

    ruta_recorte = "recorte.webp"
    img = ImagenOpenCV(ruta_imagen, ruta_recorte)

    # clickeos = 0

    def clickeo(e):
        global clickeos
        clickeos += 1
        print(f"Nº clicks: {clickeos}")
        # ruta_recorte = "recorte.webp"
        # archivo_recorte = "recorte.webp"
        # interfaz_edicion(ruta_imagen , archivo_recorte, True , 512,512)    # Recorte pequeño
        # img = ImagenOpenCV(ruta_imagen, ruta_recorte)
        img.interfaz_edicion()  #tamaño recorte predefinido
        # Cierre de ventanas
        # cv2.destroyAllWindows()
        cv2.destroyWindow(img.nombre_ventana)


    imagen = ft.Image(
        src = ruta_imagen,
        width  = base,
        height = altura, 
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        ) 
    contenedor = ft.Container(
        content = imagen,
        # bgcolor=ft.colors.GREEN, 
        width  = base,
        height = altura, 
        padding=0,
        margin=0,
        on_click= clickeo
        )


    page.add(contenedor)
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height=800
    page.window_width=800

    page.update()







if __name__=="__main__":
    ft.app(target=main)


