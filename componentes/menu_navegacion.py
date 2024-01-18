# Ejecutar demo como:
# py -m componentes.menu_navegacion

import pathlib
# import time 
import flet as ft
from functools import partial       # usado para los handlers

from . contenedor import Contenedor, Contenedor_Imagen, Estilo_Contenedor



# class MenuNavegacion(ft.UserControl):
class MenuNavegacion(ft.Column):

    def __init__(self):
        # inicializacion
        self.indice = 0
        self.maximo = 0
        self.incremento = 10
        self.ancho_boton = 200
        self.rutas_imagen = []
        self.funcion_botones = lambda _ : nada(_)
        self.estilo_contenedor = Estilo_Contenedor(        
            border_radius = 0, 
            bgcolor = ft.colors.WHITE,
            border=ft.border.all(0, ft.colors.WHITE)
            )
        self.titulo = ft.Text(
            value="", 
            size=30,
            height=50, 
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            )
        self.fila_titulo = ft.Row(
            # expand = True,
            controls = [self.titulo],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        # Se invoca un contenedor hijo
        self.contenedor = Contenedor_Imagen()
        self.fila_contenedor = ft.Row(
            controls = [self.contenedor],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        adelantar       = partial(self.cambiar_indice, 1)
        adelantar_fast  = partial(self.cambiar_indice, self.incremento)
        retroceder      = partial(self.cambiar_indice, -1)
        retroceder_fast = partial(self.cambiar_indice, -1*self.incremento)


        # botones de navegacion
        self.boton_next      = ft.ElevatedButton(text="Siguiente",     on_click=adelantar ,width=self.ancho_boton)
        self.boton_prev      = ft.ElevatedButton(text="Anterior" ,     on_click=retroceder ,width=self.ancho_boton)
        self.boton_next_fast = ft.ElevatedButton(text=f"Siguiente + {self.incremento}", on_click=adelantar_fast ,width=self.ancho_boton)
        self.boton_prev_fast = ft.ElevatedButton(text=f"Anterior  - {self.incremento}", on_click=retroceder_fast ,width=self.ancho_boton)

        self.lista_botones_navegacion_1 =[self.boton_prev     , self.boton_next     ]
        self.lista_botones_navegacion_2 =[self.boton_prev_fast, self.boton_next_fast]

        self.fila_botones_navegacion_1 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = self.lista_botones_navegacion_1,
            alignment=ft.MainAxisAlignment.CENTER,
            # width=self.contenedor.width
        )

        self.fila_botones_navegacion_2 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = self.lista_botones_navegacion_2,
            alignment=ft.MainAxisAlignment.CENTER,
            # width=self.contenedor.width
        )

        # self.columna_navegacion = ft.Column(
        super().__init__(
            wrap=False,
            # spacing=10,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [ 
                self.fila_titulo,
                self.fila_contenedor, 
                self.fila_botones_navegacion_1, 
                self.fila_botones_navegacion_2
                ] 
        )
            # self.columna_navegacion = ft.Column(
        # self.wrap=False
        #     # spacing=10,       # espaciado horizontal entre contenedores
        # self.run_spacing=50     # espaciado vertical entre filas
        # self.controls = [ 
        #         fila_titulo,
        #         fila_contenedor, 
        #         fila_botones_navegacion_1, 
        #         fila_botones_navegacion_2
        #         ] 
        # )
        # return self.columna_navegacion


    # Metodo actualizacion
    def cargar_imagen(self):
        imagen = self.rutas_imagen[self.indice]
        nombre_imagen = pathlib.Path(imagen).name
        radio = self.contenedor.border_radius 
        # radio = 0
        self.contenedor.imagen(imagen, radio)

        self.titulo.value = f"{self.indice} - {nombre_imagen}"
        self.estilo()
        self.update()

    def estilo(self):
        self.contenedor.estilo(self.estilo_contenedor)
        self.fila_titulo.width=self.contenedor.width
        self.fila_botones_navegacion_1.width=self.contenedor.width
        self.fila_botones_navegacion_2.width=self.contenedor.width
        self.fila_contenedor.width=self.contenedor.width
        self.update()


    # def incrementar(self, numero):
    def cambiar_indice(self, incremento, _):
        numero = self.indice + incremento
        previo = self.indice 
        if numero <0:
            self.indice = 0
        elif numero >= self.maximo:
            self.indice = self.maximo -1
        else:
            self.indice = numero
        # se actualiza solo si hubo cambio de indice          
        if previo != self.indice:    
            self.cargar_imagen()
            self.funcion_botones(self.indice)


    def imagenes(self, rutas: list):
        self.rutas_imagen = rutas
        self.maximo= len(rutas)
    

    def eventos(self, click = None, hover = None, longpress = None ):
        # for contenedor in self.controls:
        self.contenedor.eventos(click, hover, longpress)

# funcion auxiliar con formato para los botones del menu
def nada( indice ):
    pass






def pagina_etiquetado(page: ft.Page ):

    numero_imagenes = 20

    dimensiones = 768

    rutas_imagen = []
    for i in range(numero_imagenes):
        rutas_imagen.append(f"https://picsum.photos/400/400?{i}")


    # estilos para el contenedor 
    estilo_defecto = Estilo_Contenedor(
        width = 768,
        height = 768,
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100)
        )

    estilo_click = Estilo_Contenedor(
        width = 768,
        height = 768,
        border_radius = 5,
        bgcolor = ft.colors.RED_900,
        border = ft.border.all(20, ft.colors.PURPLE_900),
        )   

    estilo_hover = Estilo_Contenedor(
        width = 768,
        height = 768,
        border_radius = 50, 
        bgcolor = ft.colors.AMBER_400,
        border=ft.border.all(20, ft.colors.ORANGE_600),
        )


    def funcion_click(cont, e):
        cont.estilo(estilo_click)
        cont.update()

    def funcion_hover(cont, e):
        cont.estilo(estilo_hover)
        cont.update()

    def funcion_longpress(cont, e):        
        cont.estilo(estilo_defecto)
        cont.update()


    menu = MenuNavegacion()
    page.add(menu)
    menu.imagenes(rutas_imagen)
    # menu.contenedor.setup(dimensiones, dimensiones)

    # menu.contenedor.estilo(estilo_defecto)
    menu.estilo_contenedor = estilo_defecto

    # menu.contenedor.click(funcion_click)
    # menu.contenedor.hover(funcion_hover)
    # menu.contenedor.longpress(funcion_longpress)

    menu.eventos(funcion_click, funcion_hover, funcion_longpress)
    menu.contenedor.imagen(
        f"https://picsum.photos/400/400?0",
        100
        )
    menu.estilo()
    menu.cargar_imagen()

    # Estilos 
    # Tema_Pagina(page)

    page.title = "Navegación Imágenes"
    page.window_width=1200
    page.window_height=1000
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False

    # print("Listo")
    page.update()



# # Tema aplicado globalmente
# def Tema_Pagina(pagina: ft.Page):
#     pagina.theme = ft.Theme(
#         scrollbar_theme=ft.ScrollbarTheme(
#             track_color={
#                 ft.MaterialState.HOVERED: ft.colors.AMBER,
#                 ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
#             },
#             track_visibility=True,
#             track_border_color=ft.colors.BLUE,
#             thumb_visibility=True,
#             thumb_color={
#                 ft.MaterialState.HOVERED: ft.colors.RED,
#                 ft.MaterialState.DEFAULT: ft.colors.GREY_300,
#             },
#             thickness=30,
#             radius=15,
#             main_axis_margin=5,
#             cross_axis_margin=10,
#         )
#     )



# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)


