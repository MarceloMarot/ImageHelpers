
# import cv2 as cv

import flet as ft

# Contenedor con eventos integrados
# pensado para contener imagenes
class Contenedor_Imagen(ft.UserControl):

    def hover(self,e):
        self.contenedor.bgcolor=ft.colors.AMBER
        self.update()


    def click(self, e):
        print(f"{self.contenedor.width} {self.contenedor.height}")
        self.contenedor.bgcolor=ft.colors.GREEN
        self.update()


    def build(self):
        self.borde  = 5
        self.contenedor = ft.Container(
                margin=10,
                padding=10,
                # width   = self.imagen.width + self.borde,
                # height  = self.imagen.height + self.borde,
                width   = 200,
                height  = 200,
                # content = self.imagen,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                border_radius=10,           # redondeo
                animate=ft.animation.Animation(200, "bounceOut"),
                # EVENTOS:  
                # on_long_press = self.longpress,
                on_hover = self.hover,
                on_click = self.click, 
            )
        return self.contenedor
    

    # def setImagen(self, ruta: str):
    #     self.imagen.src  = ruta
        # self.update()

    def setDimensiones(self, dim: int, borde: int):
        # self.imagen.width  = dim
        # self.imagen.height = dim
        # self.borde = borde
        # self.contenedor.width = self.imagen.width + self.borde
        # self.contenedor.height= self.imagen.height + self.borde
        # self.contenedor.width = self.imagen.width + self.borde
        self.contenedor.height= dim+borde
        self.contenedor.width = dim+borde
        self.update()


    def setBGColor(self, color):
        self.contenedor.bgcolor = color
        self.update()
        
 


def pagina(page: ft.Page):

    contenedor = Contenedor_Imagen()
    page.add(contenedor)
    # page.add(contenedor)

    # contenedor.setDimensiones(500,0)
    contenedor.setBGColor(ft.colors.BLUE)

    # contenedor.setImagen("https://picsum.photos/200/200?0")
    contenedor.setDimensiones(400,5)
    # dim_imagen=512




    # contenedor.setContenido(imag)
    # page.add(contenedor)
    page.update()

ft.app(target = pagina)