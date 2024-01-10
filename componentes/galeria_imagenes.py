
import flet as ft
from functools import partial
from . contenedor import  Contenedor_Imagen, Estilo_Contenedor


# Clase 'Galeria' compuesta 
# creada para manejar fácilmente multiples contenedores de imagenes 
# es subclase del objeto 'fila' (ft.Row) de FLET
class Galeria(ft.Row):
    def build(self):
        # self.recuadros = []
        self.numero = 0

        self.expand = True 
        self.wrap = False # version galería (si es 'False' las imagenes van en linea)
        

    def crear(self , numero: int, cuadricula=True):
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        self.numero = numero
        for i in range(0, self.numero):
            c = Contenedor_Imagen()
            self.controls.append(c)


    def setup(self, base = 256 , altura = 256):
        for contenedor in self.controls:
            contenedor.setup(base, altura)


    def estilo(self, estilo: Estilo_Contenedor ): 
        for contenedor in self.controls:
            contenedor.estilo(estilo)


    def imagenes(self,rutas = [], redondeo = 0):
        # prevencion de imagenes sobrantes
        n = len(self.controls) if len(rutas) > len(self.controls) else len(rutas)
        if  len(rutas) > 0:
            for i in range(n):
                self.controls[i].crear_imagen(
                    rutas[i],
                    redondeo
                    )
        else: 
            for i in range(len(self.controls)):
                self.controls[i].crear_imagen(
                    f"https://picsum.photos/200/200?{i}",
                    redondeo
                    )


    def eventos(self, fclick, fhover, flongpress ):
        for contenedor in self.controls:
            contenedor.click(fclick)
            contenedor.hover(fhover)
            contenedor.longpress(flongpress)



def pagina_galeria(page: ft.Page):
    
    # parametros de ejemplo
    numero_imagenes = 30
    lista_imagenes = []     # lista imagenes vacia --> Imagenes online desde Picsum.com

    # estilos para el contenedor 
    estilo_defecto = Estilo_Contenedor(
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100)
        )

    estilo_click = Estilo_Contenedor(
        border_radius = 5,
        bgcolor = ft.colors.RED_900,
        border = ft.border.all(20, ft.colors.PURPLE_900),
        )   

    estilo_hover = Estilo_Contenedor(
        border_radius = 50, 
        bgcolor = ft.colors.AMBER_400,
        border=ft.border.all(20, ft.colors.ORANGE_600),
        )


    # Funciones para los eventos que producirán un cambio de estilo del contenedor
    def funcion_click(c, e):
        c.estilo(estilo_click)

    def funcion_hover(c, e):
        c.estilo(estilo_hover)

    def funcion_longpress(c, e):        
        c.estilo(estilo_defecto)


    # Maquetado
    # componente galeria de contenedores con imágenes
    galeria = Galeria()
    galeria.crear(numero_imagenes)
    # el componente
    page.add(galeria)


    galeria.setup(300, 300)
    galeria.estilo(estilo_defecto)
    galeria.imagenes(lista_imagenes, redondeo=60)
    galeria.eventos(
        funcion_click,
        funcion_hover,
        funcion_longpress
        )

    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=1200
    page.window_height=900
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK

    page.scroll = ft.ScrollMode.AUTO
    page.padding = 10
    # tema_pagina(page)
    page.update()


# creacion de ventana
if __name__ == "__main__":
    ft.app(target = pagina_galeria)
