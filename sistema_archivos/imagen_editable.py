# test:
# py -m sistema_archivos.imagen_editable
import cv2
import numpy as np
import flet as ft
import pathlib
from typing import IO
import tempfile

from . archivos_temporales import crear_directorio_temporal
from . imagen_temporal import crear_imagen_temporal


class ImagenEditable:
    """Imagen creada como archivo temporal actualizable. Al cambiar su contenido se elimina el archivo temporal original y se crea uno nuevo como sustituto."""
    def __init__(self,
        directorio: str|None = None,
        extension : str =".bmp"
        ):
        self.imagen_actual: IO|None = None
        self.imagen_vieja : IO|None = None
        self.directorio = directorio
        self.extension  = extension

    @property
    def ruta(self):
        """Muestra la ruta del contenido actual."""
        return self.imagen_actual.name

    def subir(self, ruta: str):
        """Carga una nueva imagen desde archivo y elimina el anterior."""
        # reemplazo de contenido
        self.imagen_vieja = self.imagen_actual
        self.imagen_actual = crear_imagen_temporal(ruta, directorio=self.directorio, extension=self.extension)
        # cierre y eliminacion de la version previa
        if self.imagen_vieja != None:
            if pathlib.Path(self.imagen_vieja.name).exists():
                self.imagen_vieja.close()
                pathlib.Path(self.imagen_vieja.name).unlink()

    def crear(self, opencv_data: np.ndarray, extension:str=".bmp"):
        """Crea una imagen temporal desde objetos de OpenCV y elimina el anterior."""
        # reemplazo de contenido
        self.imagen_vieja = self.imagen_actual
        # cracion archivo vacio
        self.imagen_actual = tempfile.NamedTemporaryFile( 
            prefix = "img_",    # parte del nombre de archivo
            suffix = extension,    # extensión añadida de archivo
            dir = self.directorio,
            # configuracion recomendada Windows (en POSIX no molesta)
            delete = True,
            delete_on_close= False,
            )
        # codificacion y cargade contenido
        cv2.imwrite(self.imagen_actual.name, opencv_data)
        # cierre y eliminacion de la version previa
        if self.imagen_vieja != None:
            if pathlib.Path(self.imagen_vieja.name).exists():
                self.imagen_vieja.close()
                pathlib.Path(self.imagen_vieja.name).unlink()
        
    def cerrar(self):
        """Cierra todo el contenido actual"""
        if self.imagen_actual != None:
            if pathlib.Path(self.imagen_actual.name).exists():
                self.imagen_actual.close()
                pathlib.Path(self.imagen_actual.name).unlink()
        if self.imagen_vieja != None:
            if pathlib.Path(self.imagen_vieja.name).exists():
                self.imagen_vieja.close()
                pathlib.Path(self.imagen_vieja.name).unlink()



def main(page: ft.Page):

    global archivo_editable

    #inicializacion imagen
    archivo_editable.subir(rutas[0])

    imagen = ft.Image(
        src= archivo_editable.ruta,
        height=512,
        width=512,
        fit=ft.ImageFit.CONTAIN,
        gapless_playback=True,  # previene parpadeo al reemplazar imagen
    )

    def cambiar_imagen(e:ft.ControlEvent):
        if e.control==boton_1:
            archivo_editable.subir(rutas[0])
            imagen.src = archivo_editable.ruta
            imagen.update()
        else:
            archivo_editable.subir(rutas[1])
            imagen.src = archivo_editable.ruta
            imagen.update()

    boton_1 = ft.ElevatedButton("imagen 1", on_click=cambiar_imagen, bgcolor=ft.colors.BLUE_800 )
    boton_2 = ft.ElevatedButton("imagen 2", on_click=cambiar_imagen, bgcolor=ft.colors.RED_800 )


    page.add(imagen)
    page.add(ft.Row(
        [boton_1, boton_2],
        width=500,
        )
    )
    page.theme_mode=ft.ThemeMode.DARK
    page.window_height=700
    page.window_width=500
    page.update()



if __name__ == "__main__":

    import sys

    if len(sys.argv) == 3:

        rutas = [sys.argv[1],  sys.argv[2]]

        carpeta_temporal = crear_directorio_temporal("ensayo")
        print("carpeta temporal: ", carpeta_temporal.name)
        archivos = []

        # creacion de estructura de imagenes temporales
        archivo_editable = ImagenEditable(carpeta_temporal.name)

        # llamado de interfaz grafica
        ft.app(target=main)

        # elimina archivos temporales internos
        archivo_editable.cerrar()

        # elimina la carpeta temporal y sus archivos internos
        carpeta_temporal.cleanup()


    else:
        print('uso programa: py -m componentes.imagen_editable  "ruta_archivo_1" "ruta_archivo_2" ')
