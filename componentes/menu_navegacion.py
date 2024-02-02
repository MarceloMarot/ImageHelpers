# Ejecutar demo como:
# py -m componentes.menu_navegacion

import pathlib
# import time 
import flet as ft
from functools import partial       # usado para los handlers

# from . contenedor import Contenedor, Contenedor_Imagen, Estilo_Contenedor
from . galeria_imagenes import  Contenedor_Imagen, Estilo_Contenedor, leer_imagenes, Imagen, rutas_imagenes_picsum



# class MenuNavegacion(ft.UserControl):
class MenuNavegacion(ft.Column):

    def __init__(self):
        # inicializacion
        self.__indice = 0
        self.__maximo = 0
        self.incremento = 10
        self.ancho_boton = 200
        self.__imagenes = []
        self.funcion_botones = lambda _ : nada(_)
        self.estilo_contenedor = Estilo_Contenedor(        
            border_radius = 0, 
            bgcolor = ft.colors.WHITE,
            border=ft.border.all(0, ft.colors.WHITE)
            )
        self.__titulo= ft.Text(
            value="", 
            size=20,
            height=30, 
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            )
        self.__fila_titulo = ft.Row(
            controls = [self.__titulo],
            alignment=ft.MainAxisAlignment.CENTER,
            height=self.__titulo.height,
        )
        self.__subtitulo = ft.Text(
            value="", 
            size=15,
            height=40, 
            weight=ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.CENTER,
            )
        self.__fila_subtitulo = ft.Row(
            controls = [self.__subtitulo],
            alignment=ft.MainAxisAlignment.CENTER,
            height=self.__subtitulo.height,
            wrap=True,
        )
        # Se invoca un contenedor hijo
        self.__contenedor = Contenedor_Imagen()
        self.__fila_contenedor = ft.Row(
            controls = [self.__contenedor],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        adelantar       = partial(self.cambiar_indice, 1)
        adelantar_fast  = partial(self.cambiar_indice, self.incremento)
        retroceder      = partial(self.cambiar_indice, -1)
        retroceder_fast = partial(self.cambiar_indice, -1*self.incremento)


        # botones de navegacion
        self.__boton_next      = ft.ElevatedButton(text="Siguiente",     on_click=adelantar ,width=self.ancho_boton)
        self.__boton_prev      = ft.ElevatedButton(text="Anterior" ,     on_click=retroceder ,width=self.ancho_boton)
        self.__boton_next_fast = ft.ElevatedButton(text=f"Siguiente + {self.incremento}", on_click=adelantar_fast ,width=self.ancho_boton)
        self.__boton_prev_fast = ft.ElevatedButton(text=f"Anterior  - {self.incremento}", on_click=retroceder_fast ,width=self.ancho_boton)

        self.__botones_1 =[self.__boton_prev     , self.__boton_next     ]
        self.__botones_2 =[self.__boton_prev_fast, self.__boton_next_fast]


        self.__altura_filas_botones = 40
        self.__fila_botones_navegacion_1 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = self.__botones_1,
            alignment=ft.MainAxisAlignment.CENTER,
            height = self.__altura_filas_botones,
        )
        self.__fila_botones_navegacion_2 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = self.__botones_2,
            alignment=ft.MainAxisAlignment.CENTER,
            height = self.__altura_filas_botones,
        )
        self.__divisor = ft.Divider(height = 10)
        super().__init__(
            wrap=False,
            # spacing=10,       # espaciado horizontal entre contenedores
            # run_spacing=30,     # espaciado vertical entre filas
            controls = [ 
                self.__fila_titulo,
                self.__fila_contenedor, 
                self.__fila_subtitulo,
                self.__divisor,
                self.__fila_botones_navegacion_1, 
                self.__fila_botones_navegacion_2,
                self.__divisor,
                ] 
        )

    # metodos habilitar / dehabilitar controles
    def deshabilitar(self):
        """Anula manualmente los controles del selector"""
        self.__boton_prev_fast  .disabled = True
        self.__boton_prev       .disabled = True
        self.__boton_next_fast  .disabled = True
        self.__boton_next       .disabled = True
        self.__contenedor       .disabled = True
        # self.update()

    def habilitar(self):
        """Habilita manualmente los controles del selector"""
        self.__boton_prev_fast  .disabled = False
        self.__boton_prev       .disabled = False
        self.__boton_next_fast  .disabled = False
        self.__boton_next       .disabled = False
        self.__contenedor       .disabled = False
        # self.update()



    # Metodo actualizacion
    def cargar_imagen(self):
        """Este metodo lee la imagen correspondiente al indice actual."""
        # visualizar imagen con el indice actual
        imagen = self.__imagenes[self.__indice]
        self.__contenedor.content = imagen
        nombre_imagen = pathlib.Path(imagen.src).name
        ruta_imagen = imagen.src
        self.__titulo.value = f"{self.__indice + 1 } - {nombre_imagen}"
        self.__subtitulo.value = f"Ruta archivo: {ruta_imagen}"
        # carga de estilo de contenedor y actualizacion visual
        self.estilo()
        self.update()


    # def estilo(self):
    def estilo(self, estilo=None):
        """Carga o restablecimiento de aspecto para el contenedor de imagen."""
        if estilo != None:
            self.estilo_contenedor = estilo
        self.__contenedor.estilo(self.estilo_contenedor)
        # self.__fila_titulo.width=self.__contenedor.width
        # self.__fila_subtitulo.width=self.__contenedor.width
        # self.__fila_botones_navegacion_1.width=self.__contenedor.width
        # self.__fila_botones_navegacion_2.width=self.__contenedor.width
        # self.__fila_contenedor.width=self.__contenedor.width
        self.update()

    @property
    def alto(self):
        return self.height

    @alto.setter
    def alto(self, valor):
        self.height = valor

    @property
    def ancho(self):
        return self.width

    @ancho.setter
    def ancho(self, valor):
        self.width = valor
        self.__fila_titulo.width = valor
        self.__fila_subtitulo.width = valor
        self.__fila_botones_navegacion_1.width = valor
        self.__fila_botones_navegacion_2.width = valor
        self.__fila_contenedor.width = valor 


    @property 
    def indice(self):
        return self.__indice   

    @indice.setter
    def indice(self, valor: int):
        if valor >= 0 and valor < self.__maximo:
            self.__indice = valor 
        elif valor >= self.__maximo:
            self.__indice = self.__maximo
        else:
            self.__indice = 0
        self.cargar_imagen()
        self.update()


    # def incrementar(self, numero):
    def cambiar_indice(self, incremento, _):
        """Refresca el indice de imagen actual."""
        numero = self.__indice + incremento
        previo = self.__indice 
        if numero <0:
            self.__indice = 0
        elif numero >= self.__maximo:
            self.__indice = self.__maximo -1
        else:
            self.__indice = numero
        # se actualiza solo si hubo cambio de indice          
        if previo != self.__indice:    
            self.cargar_imagen()
            self.funcion_botones(self.__indice)

    
    def imagenes(self, imagenes: list[ft.Image]):
        """Asigna imagenes (ft.Image) ya creadas al componente."""
        self.__imagenes = imagenes
        self.__maximo = len(imagenes)
        self.cargar_imagen()


    def eventos(self, click = None, hover = None, longpress = None, funcion_botones = None ):
        """Eventos para el contenedor de imagen. Pueden ser 'None'"""
        self.__contenedor.eventos(click, hover, longpress)
        if funcion_botones != None:
            self.funcion_botones = funcion_botones
            

# funcion auxiliar con formato para los botones del menu
def nada( indice ):
    pass






def pagina_etiquetado(page: ft.Page ):

    numero_imagenes = 20
    rutas_imagen = rutas_imagenes_picsum(numero_imagenes, 200) 

    dimension = 512
    imagenes_picsum = leer_imagenes(rutas_imagen, ancho=dimension, alto=dimension, redondeo=50 )


    # estilos para el contenedor 
    estilo_defecto = Estilo_Contenedor(
        width = dimension,
        height = dimension,
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100)
        )

    estilo_click = Estilo_Contenedor(
        width = dimension,
        height = dimension,
        border_radius = 5,
        bgcolor = ft.colors.RED_900,
        border = ft.border.all(20, ft.colors.PURPLE_900),
        )   

    estilo_hover = Estilo_Contenedor(
        width = dimension,
        height = dimension,
        border_radius = 50, 
        bgcolor = ft.colors.AMBER_400,
        border=ft.border.all(20, ft.colors.ORANGE_600),
        )


    def funcion_click(e : ft.ControlEvent):
        cont = e.control    
        cont.estilo(estilo_click)
        cont.update()

    def funcion_hover( e: ft.ControlEvent):
        cont = e.control
        cont.estilo(estilo_hover)
        cont.update()

    def funcion_longpress( e: ft.ControlEvent):   
        cont = e.control     
        cont.estilo(estilo_defecto)
        cont.update()


    menu = MenuNavegacion()
    page.add(menu)
    menu.imagenes(imagenes_picsum)
    # menu.estilo_contenedor = estilo_defecto
    menu.eventos(funcion_click, funcion_hover, funcion_longpress)

    menu.estilo(estilo_defecto)

    menu.alto = 800
    menu.ancho = 800

    page.title = "Navegación Imágenes"
    page.window_width=1200
    page.window_height=1000
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False
    page.update()


# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)



