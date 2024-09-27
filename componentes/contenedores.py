from typing import TypeVar
import flet as ft

from estilos.estilos_contenedores import EstiloContenedor


class Imagen(ft.Image):
    """Esta clase auxiliar permite inicializar imagenes de forma simplificada."""""
    def __init__(self, ruta: str, ancho=256, alto=256, redondeo=0):
        super().__init__(
            src = ruta,
            width = ancho,
            height = alto,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(redondeo),
        )


# Subclase del container de FLET, manejo simplificado e imagen interior
class Contenedor(ft.Container):
    """'Contenedor' es una implementacion simplificada del componente 'ft.Container' de FLET"""
    # Inicializacion
    def __init__(self, ancho=256, alto=256, redondeo=0, margen=4):
        """Crea el objeto contenedor con valores preestablecidos."""
        # herencia de atributos y asignaciones valores predeterminados
        super().__init__(
            margin  = margen,
            padding = 10,
            width   = ancho,
            height  = alto,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            border = ft.border.all(0, ft.colors.WHITE),
            border_radius=redondeo ,  
            image_fit = ft.ImageFit.CONTAIN,       
            animate=ft.animation.Animation(
                1000, 
                ft.AnimationCurve.BOUNCE_OUT # acomodamiento con "rebotes"
                # ft.AnimationCurve.EASE    # acomodamiento gradual
                ),
            )

    
    # Metodos
    def estilo(self, estilo: EstiloContenedor):
        """ Permite actualizar el aspecto del contenedor ingresando el objeto con los valores deseados. Su uso es opcional"""
        self.width  = estilo.width
        self.height = estilo.height
        self.border_radius = estilo.border_radius
        self.bgcolor = estilo.bgcolor
        self.border = estilo.border
        self.margin  = estilo.margin
        self.padding = estilo.padding


    def eventos(self, click=None, hover=None, longpress=None):
        """Carga las funciones de eventos del contenedor de forma simplificada. Su uso es opcional"""
        if click != None :
            self.on_click = click 
        if hover != None :
            self.on_hover = hover
        if longpress != None :
            self.on_long_press = longpress


# nuevos tipados para contenedor y sus subclases
Cont     = TypeVar('Cont'     , bound=Contenedor)


class ContenedorImagen(Contenedor):
    """ 'ContenedorImagen' permite manejar una iumagen interna de forma simplificada."""
    # Inicializacion
    def __init__(self, ruta, ancho=256, alto=256, redondeo=0):
        """Crea el objeto contenedor con valores preestablecidos."""
        # herencia de atributos y asignaciones valores predeterminados
        super().__init__( ancho, alto, redondeo)
        self.imagen = Imagen(ruta, ancho, alto, redondeo)
        self.content= self.imagen


    @property
    def ruta_imagen(self):
        return  self.content.src

    @ruta_imagen.setter
    def ruta_imagen(self, valor: str):
        self.content.src = valor

    @property
    def clave(self):
        return  self.content.key
    
    
    @clave.setter
    def clave(self, valor: str):
        self.content.key = valor


# nuevos tipados para contenedor de imagenes y sus subclases
ContImag = TypeVar('ContImag' , bound=ContenedorImagen)