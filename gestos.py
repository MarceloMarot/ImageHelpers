
import cv2
from rich import print as print
import flet as ft

# import re

# from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor
from componentes.menu_navegacion import  MenuNavegacion
# from componentes.etiquetador_botones import EtiquetadorBotones
# from componentes.lista_desplegable import crear_lista_desplegable,convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
# from sistema_archivos.buscar_extension import buscar_imagenes

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen


from cortar_imagen import Redimensionar_Imagen


def nada(e):
    pass


class ImagenCooordenadas(ft.Column):
    def __init__(self, escala_inicial=80):
        self.ancho_archivo = 500
        self.alto_archivo  = 500
        self.ancho_grafica = 500
        self.alto_grafica  = 500
        self.escala_grafica = escala_inicial
        self.escala_opencv  = escala_inicial
        self.ruta = ""
        self.imagen = ft.Image(
            width  = self.ancho_archivo,
            height = self.alto_archivo, 
            ) 
        self.contenedor = ft.Container(
            content = self.imagen,
            bgcolor=ft.colors.GREEN, 
            width  = self.ancho_archivo,
            height = self.alto_archivo, 
            padding=0,
            margin=0,
            )
        self.detector_gestos = ft.GestureDetector(
            content = self.contenedor,
            on_pan_start=self.coordenadas_grafica,
            on_pan_update=self.coordenadas_grafica,
            )   
        self.funcion_arrastre = nada
        self.barra_ampliacion = ft.Slider(
            min=20, 
            max=200, 
            divisions=50, 
            label="{value}%", 
            on_change=self.handler_ampliar,
            # thumb_color=ft.colors.RED,
            width=500,
            value=escala_inicial,
            )
        self.texto_ampliacion = ft.Text(
            value=f"Escala: {escala_inicial}"
        )
        super().__init__([
            self.detector_gestos, 
            self.texto_ampliacion,
            self.barra_ampliacion,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            )
        self.imagen_opencv: cv2.UMat


    def leer_imagen(self, ruta: str, escala=100 ):
        self.ruta = ruta 
        dimensiones = dimensiones_imagen(ruta)
        self.escala_grafica = escala
        self.ancho_archivo = dimensiones[1]
        self.alto_archivo  = dimensiones[0] 
        self.imagen.src = ruta
        self.cambio_escala_grafica(escala)
        self.imagen_ampliada(self.escala_opencv)



    def cambio_escala_grafica(self, escala=100):
        p = escala/100
        self.escala_grafica = escala
        self.ancho_grafica = int( p * self.ancho_archivo )
        self.alto_grafica  = int( p * self.alto_archivo  )

        self.imagen.width  = self.ancho_grafica
        self.imagen.height = self.alto_grafica
        self.contenedor.width =  self.ancho_grafica
        self.contenedor.height = self.alto_grafica


    def handler_ampliar(self, e : ft.ControlEvent):
        escala = e.control.value
        self.escala_opencv = escala
        self.imagen_ampliada(escala)
        self.texto_ampliacion.value=f"Escala: {escala}"
        self.texto_ampliacion.update()


    def imagen_ampliada(self, escala):
        imag = cv2.imread(self.ruta)
        self.imagen_opencv = Redimensionar_Imagen(imag, escala/100)
        # print(self.imagen_opencv.shape)
        # img =  self.imagen_opencv 
        # cv2.imshow("Display window", img)
        # cv2.waitKey(0)

    def coordenadas_grafica(self, e):
        xi = e.local_x
        yi = e.local_y
        alto  = self.alto_grafica
        ancho = self.ancho_grafica

        # Prevencion desbordes
        xi=0 if xi<0 else xi
        xi=ancho-1 if xi>=ancho else xi
        yi=0 if yi<0 else yi        
        yi=alto-1 if yi>=alto else yi

        #reescritura valores evento
        e.local_x = xi
        e.local_y = yi
        # funcion de usuario (se elige externamente)
        self.funcion_arrastre(e)











def main(pagina:ft.Page):

    ancho_pagina  = 1000
    altura_pagina = 900

    ruta_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
    ruta_imagen = '1686469590.png'

    ############## HANDLERS ####################

    def coordenadas(e):
        valor = f" lx: {e.local_x}, ly: {e.local_y}"
        print(valor)
        texto.value = valor
        texto.update()


    def cambio_escala(e):
        escala = e.control.value
        print(f"Escala: {escala} %")
        texto_escala.value = f"Escala: {escala} %"
        imagen_gestos.cambio_escala_grafica( escala)
        pagina.update()


    ################# COMPONENTES ##################3


    imagen_gestos = ImagenCooordenadas()
    texto = ft.Text("")


    texto_escala = ft.Text("")
    barra_escala = ft.Slider(
            min=20, 
            max=100, 
            divisions=50, 
            label="{value}%", 
            on_change=cambio_escala,
            thumb_color=ft.colors.RED,
            width=500,
            value= 60,
            )

    escala = barra_escala.value
    # barra_escala.active_color=ft.colors.RED
    # barra_escala.thumb_color=ft.colors.RED
    # barra_escala.inactive_color=ft.colors.GREEN

    imagen_gestos.funcion_arrastre = coordenadas
    imagen_gestos.leer_imagen(ruta_imagen, escala)




    # imagen_opencv = cv2.imread(ruta_imagen)
    # ampliado = Redimensionar_Imagen(imagen_opencv,0.6)
    # cv2.imshow('Original',ampliado) 
    # cv2.waitKey(0)


    ####################### Maquetado #########################

    fila_imagen = ft.Row(
        [imagen_gestos],
        width=ancho_pagina,
        alignment=ft.MainAxisAlignment.CENTER
        )
    fila_texto = ft.Row(
        [texto],
        width=ancho_pagina,
        alignment=ft.MainAxisAlignment.CENTER
        )

    pagina.add(ft.Row(
        [texto_escala],
        width=ancho_pagina,
        alignment=ft.MainAxisAlignment.CENTER
        ))
    pagina.add(ft.Row(
        [barra_escala],
        width=ancho_pagina,
        alignment=ft.MainAxisAlignment.CENTER
        ))

    pagina.add(fila_texto)
    pagina.add(fila_imagen)

    ################## PROPIDADES PAGINA ###################

    # Propiedades pagina 
    pagina.title = "Gestos"
    pagina.window_width  = ancho_pagina
    pagina.window_height = altura_pagina
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()


    


if __name__ == "__main__":
    ft.app(target=main)