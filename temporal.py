


import cv2
import tempfile
import flet as ft
import pathlib
import time

from sistema_archivos.archivos_temporales import  crear_directorio_temporal
from sistema_archivos.imagen_temporal import crear_imagen_temporal


def principal(page: ft.Page):

    global imagen_temporal

    imagen = ft.Image(
        src = imagen_temporal.name,
        height = 512,
        width  = 512, 
        )

    page.add(imagen)
    page.window_height = 600
    page.window_width  = 600

    page.update()







if __name__ == "__main__":


    # ruta_archivo = "manejo_imagenes/ejemplo2.jpg"
    ruta_archivo = "manejo_imagenes/ejemplo.jpg"

    carpeta_temporal = crear_directorio_temporal("ensayo")
    print("carpeta temporal: ", carpeta_temporal.name)

    inicio = time.time()
    imagen_temporal = crear_imagen_temporal(ruta_archivo, carpeta_temporal)
    fin = time.time()

    print("archivo temporal: ",imagen_temporal.name)
    print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")


    ft.app(target=principal)

    
    # elimina la carpeta temporal y sus archivos internos
    carpeta_temporal.cleanup()
