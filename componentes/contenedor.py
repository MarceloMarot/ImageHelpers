import flet as ft
from functools import partial

from sys import getsizeof



# Clase auxiliar para configurar contenedores
class Estilo_Contenedor:
    def __init__(self, border_radius=0, bgcolor=ft.colors.WHITE, 
        border=ft.border.all(0, ft.colors.WHITE)):
        self.border_radius = border_radius
        self.bgcolor = bgcolor
        self.border = border


# Subclase del container de FLET, manejo simplificado
class Contenedor(ft.Container):
    # INICIALIZACION
    def build(self):
        self.id = 0
        super().__init__()
    
    # METODOS
    def setup(self, base=256, altura=256 ):
        # estilo predefinido
        self.margin=10
        self.padding=10
        self.width   = base
        self.height  = altura
        self.alignment=ft.alignment.center
        self.bgcolor=ft.colors.WHITE
        self.border = ft.border.all(0, ft.colors.WHITE)
        self.border_radius=0          
        self.animate=ft.animation.Animation(1000, "bounceOut")
        self.content=None
        self.update()

    def estilo(self, e: Estilo_Contenedor):
        self.border_radius = e.border_radius
        self.bgcolor = e.bgcolor
        self.border = e.border
        self.update()

    # def eventos(self, click=None, hover=None, longpress=None ):
    #     self.on_click = click  
    #     self.on_hover = hover
    #     self.on_long_press = longpress
    #     self.update()

    def click(self, funcion):
        self.on_click = partial(funcion, self)  

    def hover(self, funcion):
        self.on_hover = partial(funcion, self)  

    def longpress(self, funcion):
        self.on_long_press = partial(funcion, self)  


# Sub-subclase del container de FLET, con imagen interna
class Contenedor_Imagen(Contenedor):
    # INICIALIZACION
    def build(self):
        super().__init__()

    # Lee una imagen y la carga en un objeto FLET 
    # def crear_imagen(self, ruta: str, base=256, altura=256, redondeo=0):
    def crear_imagen(self, ruta: str, redondeo=0):
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
        self.update()



# FUNCION MAIN

def pagina(page: ft.Page):

    # creacion del contenedor y agregado a la página
    contenedor = Contenedor_Imagen()

    fila = ft.Row([contenedor])
    page.add(fila)

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

    # Eventos que producirán un cambio de estilo del contenedor
    def funcion_click(cont, e):
        cont.estilo(estilo_click)

    def funcion_hover(cont, e):
        cont.estilo(estilo_hover)

    def funcion_longpress(cont, e):        
        cont.estilo(estilo_defecto)

    # La configuracion del contenedor se puede hacer:
    # - durante inicializacion;
    # - Despues del agregado a página
    # Hacerlo en la definición de clase NO SIRVE
    # cambio de tamaño
    dimension = 512
    contenedor.setup(dimension, dimension)

    # estilos, eventos e imagen
    contenedor.estilo(estilo_defecto)
    # contenedor.eventos(funcion_click, funcion_hover, funcion_longpress)
    contenedor.crear_imagen(
        "https://picsum.photos/200/200?0",
        100
        )
    contenedor.click(funcion_click)
    contenedor.hover(funcion_hover)
    contenedor.longpress(funcion_longpress)

    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.update()


if __name__ == "__main__":
    ft.app(target = pagina)