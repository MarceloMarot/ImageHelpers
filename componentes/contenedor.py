# Ejecutar demo como:
# py -m componentes.contenedor

import flet as ft
from functools import partial


# Clase auxiliar para configurar contenedores
class Estilo_Contenedor:
    def __init__(
        self,
        width=256,
        height=256,
        border_radius=0, 
        bgcolor=ft.colors.WHITE, 
        border=ft.border.all(0, ft.colors.WHITE)):
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.bgcolor = bgcolor
        self.border = border


# Subclase del container de FLET, manejo simplificado
class Contenedor(ft.Container):
    # Inicializacion
    def __init__(self):
        # herencia de atributos y asignaciones valores predeterminados
        super().__init__(
            margin  = 10,
            padding = 10,
            width   = 256,
            height  = 256,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            border = ft.border.all(0, ft.colors.WHITE),
            border_radius=0 ,         
            animate=ft.animation.Animation(
                1000, 
                ft.AnimationCurve.BOUNCE_OUT # acomodamiento con "rebotes"
                # ft.AnimationCurve.EASE    # acomodamiento gradual
                ),
            )
        # nuevo parametro
        # self.id = 0
    
    # Metodos
    def estilo(self, e: Estilo_Contenedor):
        self.width  = e.width
        self.height = e.height
        self.border_radius = e.border_radius
        self.bgcolor = e.bgcolor
        self.border = e.border

    def click(self, funcion = None):
        self.on_click = partial(funcion, self)  if funcion != None else nada

    def hover(self, funcion = None):
        self.on_hover = partial(funcion, self)  if funcion != None else nada

    def longpress(self, funcion = None):
        self.on_long_press = partial(funcion, self)  if funcion != None else nada

    def eventos(self, click, hover, longpress):
        self.click(click)
        self.hover(hover)
        self.longpress(longpress)



def nada( _ ):
    pass


# Sub-subclase del container de FLET, con imagen interna
class Contenedor_Imagen(Contenedor):
    # Incializacion
    def __init__(self):
        # herencia de atributos y asignaciones valores predeterminados
        super().__init__()


    # Metodo
    def imagen(self, ruta: str, redondeo=0):
        # Lee una imagen y la carga en un objeto FLET   
        imagen = ft.Image(
            src = ruta,
            # width = base,
            # height = altura ,
            width = self.width,
            height = self.height ,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(redondeo),
        )
        self.content=imagen



# Objetos de ejemplo
# estilos para el contenedor 
estilo_defecto = Estilo_Contenedor(
    width   = 512,
    height  = 512,
    border_radius = 50, 
    bgcolor = ft.colors.BLUE_400,
    border=ft.border.all(20, ft.colors.INDIGO_100)
    )

estilo_click = Estilo_Contenedor(
    width   = 768,
    height  = 512,
    border_radius = 5,
    bgcolor = ft.colors.RED_900,
    border = ft.border.all(20, ft.colors.PURPLE_900),
    )   

estilo_hover = Estilo_Contenedor(
    width   = 512,
    height  = 768,
    border_radius = 50, 
    bgcolor = ft.colors.AMBER_400,
    border=ft.border.all(20, ft.colors.ORANGE_600),
    )



#  Funcion pagina ("main" para Flet)
def pagina(page: ft.Page):

    # creacion del contenedor y agregado a la página
    contenedor = Contenedor_Imagen()




    # estilos, eventos e imagen
    contenedor.estilo(estilo_defecto)
    contenedor.imagen(
        "https://picsum.photos/200/200?0",
        100
        )
    
    # Funciones para los eventos del mouse que producirán un cambio de estilo del contenedor afectado
    # 'cont' es el contenedor afectado el cual se recibe como parámetro 
    # 'e' es un parámetro residual que envía el manejador de eventos
    def funcion_click(cont, e):
        cont.estilo(estilo_click)
        cont.update()

    def funcion_hover(cont, e):
        cont.estilo(estilo_hover)
        cont.update()

    def funcion_longpress(cont, e):        
        cont.estilo(estilo_defecto)
        cont.update()

    contenedor.eventos(
        funcion_click,
        funcion_hover,
        funcion_longpress
        )


    page.add(contenedor)


    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.update()


if __name__ == "__main__":
    ft.app(target = pagina)