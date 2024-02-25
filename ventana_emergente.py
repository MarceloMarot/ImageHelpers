
import flet as ft
import cv2
from cortar_imagen import ImagenOpenCV


clickeos = 0

ventana = None


def main(page: ft.Page):

    ancho_pagina = 800
    altura_pagina = 800

    base = 768
    altura = 768

    # ruta_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
    ruta_imagen = '1686469590.png'

    ruta_recorte = "recorte.webp"
    # ventana = ImagenOpenCV()



    def clickeo(e):
        global clickeos
        clickeos += 1
        print(f"Nº clicks: {clickeos}")
        global ventana

        if clickeos ==1: 
            ventana = ImagenOpenCV()

        if clickeos >=1: 
            ventana.interfaz_edicion(ruta_imagen, ruta_recorte,[512,512],[768,768],texto_consola=False, escape_teclado=False)  #tamaño recorte predefinido
        
        # Cierre de ventanas
        # cv2.destroyWindow(img.nombre_ventana)
        # ventana.cerrar_ventana()


    imagen = ft.Image(
        src = ruta_imagen,
        width  = base,
        height = altura, 
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        ) 
    contenedor = ft.Container(
        content = imagen,
        width  = base,
        height = altura, 
        padding=0,
        margin=0,
        on_click= clickeo
        )


    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")
        # # Avance y retroseso de imagenes en seleccion y galeria
        # incremento = 0
        # if tecla == "Arrow Left" or tecla == "A":
        #     incremento = - 1     # retroceso
        # elif tecla == "Arrow Right" or tecla == "D":
        #     incremento = 1      # avance



    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = desplazamiento_teclado

    texto = ft.Text(
        "Click en Imagen", 
        size=20,
        width=200,
        )
    fila_texto = ft.Row(
        [texto],
        alignment=ft.MainAxisAlignment.CENTER,
        )
    page.add(fila_texto)

    page.add(contenedor)
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    page.update()







if __name__=="__main__":
    ft.app(target=main)


