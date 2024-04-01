


import cv2
import tempfile
import flet as ft
import pathlib
import time

from sistema_archivos.archivos_temporales import  crear_directorio_temporal
from sistema_archivos.imagen_temporal import crear_imagen_temporal


def principal(page: ft.Page):

    global imagen_temporal

    def cambiar_brillo(e):

        global imagen_temporal

        inicio = time.time()
        # barra_brillo = e.control
        brillo = float(barra_brillo.value)

        # BRILLO OPENCV
        contraste = float(barra_contraste.value/100)
        # copia de salida con brillo y contraste cambiados
        orig = cv2.imread(imagen_temporal_original.name)
        img = cv2.convertScaleAbs(orig, alpha=contraste, beta=brillo)


        # imagen.opacity=0.5
        # imagen.update()
        # contenedor.opacity=0.5
        # contenedor.update()

        global ruta_archivo, carpeta_temporal
        # imagen_temporal.close()
        imagen_temporal = crear_imagen_temporal(ruta_archivo, carpeta_temporal)
        cv2.imwrite(imagen_temporal.name, img)
        # time.sleep(50e-3)

        # return
        imagen.src = imagen_temporal.name   

        # contenedor.opacity=1
        contenedor.update()
        # imagen.opacity=1
        imagen.update()
        fin = time.time()

        print("archivo temporal: ", imagen_temporal.name)
        print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")


    # def actualizar_imagen(e):
    #     global imagen_temporal
    #     imagen.src = imagen_temporal.name   
    #     imagen.update()

    def coordenadas(e):
        print(f" lx: {e.local_x}, ly: {e.local_y}")
        contenedor.opacity=0.3
        imagen.opacity=0.3
        contenedor.update()
        imagen.update()

    def fin_seleccion(e):
        contenedor.opacity=1
        imagen.opacity=1
        contenedor.update()
        imagen.update()


    imagen = ft.Image(
        src = imagen_temporal.name,
        height = 512,
        width  = 512, 
        fit = ft.ImageFit.CONTAIN,
        # opacity=0.5,
        # animate_opacity=
        # animate_opacity=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
        )

    contenedor = ft.Container(
        content = imagen,
        height = 512,
        width  = 512, 
        image_fit = ft.ImageFit.CONTAIN,
        # opacity=0.5,
        # animate=ft.animation.Animation(1000, "bounceOut"),
        animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
        )

    detector_gesto = ft.GestureDetector(
        content= contenedor,
        on_pan_start=coordenadas,
        on_pan_update=coordenadas,
        on_pan_end=fin_seleccion,
        )   

    barra_brillo = ft.Slider(min=-255, max=255, divisions=500,value=0, label="{value}")
    barra_contraste = ft.Slider(min=0, max=300, divisions=300,value=100, label="{value}")
    # barra_brillo.   on_change_start = cambiar_brillo
    # barra_contraste.on_change_start = cambiar_brillo
    # barra_brillo.   on_change = cambiar_brillo
    # barra_contraste.on_change = cambiar_brillo
    barra_brillo.   on_change_end = cambiar_brillo
    barra_contraste.on_change_end = cambiar_brillo

    page.add(detector_gesto)
    page.add(barra_brillo)
    page.add(barra_contraste)
    page.window_height = 650
    page.window_width  = 600

    page.theme_mode = ft.ThemeMode.DARK

    page.update()










if __name__ == "__main__":


    ruta_archivo = "manejo_imagenes/ejemplo2.jpg"
    # ruta_archivo = "manejo_imagenes/ejemplo.jpg"

    carpeta_temporal = crear_directorio_temporal("ensayo")
    print("carpeta temporal: ", carpeta_temporal.name)

    inicio = time.time()
    imagen_temporal          = crear_imagen_temporal(ruta_archivo, carpeta_temporal)
    imagen_temporal_original = crear_imagen_temporal(ruta_archivo, carpeta_temporal)
    fin = time.time()


    print("archivo temporal: ", imagen_temporal.name)
    print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")


    ft.app(target=principal)

    
    # elimina la carpeta temporal y sus archivos internos
    carpeta_temporal.cleanup()
