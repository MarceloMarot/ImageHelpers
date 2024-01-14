# Ejecutar demo como:
# py -m componentes.galeria_imagenes
from functools import partial
import flet as ft
from . contenedor import Contenedor, Contenedor_Imagen, Estilo_Contenedor


# Clase 'Galeria' compuesta 
# creada para manejar fácilmente multiples contenedores de imagenes 
# es subclase del objeto 'fila' (ft.Row) de FLET
class Galeria(ft.Row):
# class Fila_Imagenes(ft.Row):
    def __init__(self):
        super().__init__(
            expand = True,
            wrap = True, # version galería (si es 'False' las imagenes van en linea)
            scroll=ft.ScrollMode.ALWAYS,
            )
        self.numero = 0


    def crear(self , numero: int, cuadricula=True):
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        self.numero = numero
        for i in range(0, self.numero):
            cont = Contenedor_Imagen()
            # cont.key = str(i)     # asignar la clave anula las animaciones
            self.controls.append(cont)

    def estilo(self, estilo: Estilo_Contenedor ): 
        for contenedor in self.controls:
            contenedor.estilo(estilo)


    def imagenes(self,rutas = [], redondeo = 0):
        # prevencion de imagenes sobrantes
        n = len(self.controls) if len(rutas) > len(self.controls) else len(rutas)
        if  len(rutas) > 0:
            for i in range(n):
                self.controls[i].imagen(
                    rutas[i],
                    redondeo
                    )
                self.controls[i].content.key = str(i)     
        else: 
            for i in range(len(self.controls)):
                self.controls[i].imagen(
                    f"https://picsum.photos/200/200?{i}",
                    redondeo
                    )
                self.controls[i].content.key = str(i)    

    def eventos(self, click = None, hover = None, longpress = None ):
        for contenedor in self.controls:
            contenedor.eventos(click, hover, longpress)




def pagina_galeria(page: ft.Page):
    
    # parametros de ejemplo
    numero_imagenes =  100
    lista_imagenes = []     # lista imagenes vacia --> Imagenes online desde Picsum.com

    # estilos para contenedores 
    estilo_defecto = Estilo_Contenedor(
        width = 300,
        height = 300,
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100)
        )

    estilo_click = Estilo_Contenedor(
        width = 300,
        height = 300,
        border_radius = 5,
        bgcolor = ft.colors.RED_900,
        border = ft.border.all(20, ft.colors.PURPLE_900),
        )   

    estilo_hover = Estilo_Contenedor(
        width = 300,
        height = 300,
        border_radius = 50, 
        bgcolor = ft.colors.AMBER_400,
        border=ft.border.all(20, ft.colors.ORANGE_600),
        )


    # Funciones para los eventos del mouse que producirán un cambio de estilo del contenedor afectado
    # 'cont' es el contenedor afectado el cual se recibe como parámetro 
    # 'e' es un parámetro residual que envía el manejador de eventos
    def funcion_click(cont, e):
        cont.estilo(estilo_click)
        # print(f"Key: {cont.key} clicked")
        # print(f"Key: {cont.content.key} clicked")
        cont.update()

    def funcion_hover(cont, e):
        cont.estilo(estilo_hover)
        # print(f"Key: {cont.key} hoved")
        # print(f"Key: {cont.content.key} hoved")
        cont.update()

    def funcion_longpress(cont, e):        
        cont.estilo(estilo_defecto)
        # print(f"Key: {cont.key} long pressed")
        # print(f"Key: {cont.content.key} long pressed")
        cont.update()

    # Maquetado
    # componente galeria de contenedores con imágenes
    galeria = Galeria()

    galeria.crear(numero_imagenes)
    galeria.estilo(estilo_defecto)
    galeria.imagenes(lista_imagenes, redondeo=60)
    galeria.eventos(
        click = funcion_click,
        hover = funcion_hover,
        longpress = funcion_longpress
        )

    # page.add(galeria)



    def scroll_to_key(n, e):
        galeria.scroll_to(key=str(n), duration=1000)
        print(f"Imagen Nº:{n}")

    def scroll_to_delta(e):
        galeria.scroll_to(delta=40, duration=200)

    m = 0 
    print(m)
    boton_inicio = ft.ElevatedButton(
        # f"Inicio: imagen nº {m}",    
        text="Inicio",    
        bgcolor=ft.colors.RED_400, 
        on_click=partial(scroll_to_key, m)
        )

    m = int(numero_imagenes/2 -1) 
    print(m)
    boton_medio = ft.ElevatedButton(
        # f"Fin: imagen nº {m}",    
        text="Medio",    
        bgcolor=ft.colors.AMBER_400, 
        on_click=partial(scroll_to_key, m)
        )

    m = numero_imagenes - 1 
    print(m)
    boton_fin = ft.ElevatedButton(
        # f"Fin: imagen nº {m}",    
        text="Fin",    
        bgcolor=ft.colors.GREEN_400, 
        on_click=partial(scroll_to_key, m)
        )


    page.add(ft.Row([boton_inicio, boton_medio, boton_fin]))

    page.add(galeria)


    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=1200
    page.window_height=900
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK

    # page.scroll = ft.ScrollMode.AUTO
    page.padding = 10
    # tema_pagina(page)
    page.update()


# creacion de ventana
if __name__ == "__main__":
    ft.app(target = pagina_galeria)
