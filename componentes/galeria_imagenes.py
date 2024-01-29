# Ejecutar demo como:
# py -m componentes.galeria_imagenes
from functools import partial
import flet as ft

# Clase auxiliar para configurar contenedores
class Estilo_Contenedor:
    """ 'Estilo_Contenedor' es una estructura de datos creada para guardar parametros de estilo de los contenedores: tamaño, colores, bordes, etc"""
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
    """ 'Contenedor' es una implementacion simplificada del componente 'ft.Container' de FLET"""
    # Inicializacion
    def __init__(self):
        """Crea el objeto contenedor con valores preestablecidos. """
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

    
    # Metodos
    def estilo(self, estilo: Estilo_Contenedor):
        """ Permite actualizar el aspecto del contenedor ingresando el objeto con los valores deseados. Su uso es opcional"""
        self.width  = estilo.width
        self.height = estilo.height
        self.border_radius = estilo.border_radius
        self.bgcolor = estilo.bgcolor
        self.border = estilo.border


    def eventos(self, click=None, hover=None, longpress=None):
        """Carga las funciones de eventos del contenedor de forma simplificada. Su uso es opcional"""
        if click != None :
            self.on_click = click 
        if hover != None :
            self.on_hover = hover
        if longpress != None :
            self.on_long_press = longpress



# Sub-subclase del container de FLET, con imagen interna
class Contenedor_Imagen(Contenedor):
    """Subclase de 'contenedor' con método para leer imagen de archivo agregado."""
    # Incializacion
    def __init__(self):
        # herencia de atributos y asignaciones valores predeterminados
        super().__init__()


    # Metodo
    def ruta_imagen(self, ruta: str, redondeo=0):
        """Este método carga una imagen desde archivo o direccion web y la asigna al contenedor. Uso opcional """
        # Lee una imagen y la carga en un objeto FLET   
        imagen = ft.Image(
            src = ruta,
            width = self.width,
            height = self.height ,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(redondeo),
        )
        self.content=imagen


class Galeria(ft.Row):
    """Clase 'Galeria' compuesta creada para manejar fácilmente multiples contenedores de imagenes. 
    Es subclase del objeto 'fila' (ft.Row) de FLET
    """
    def __init__(self):
        super().__init__(
            expand = True,
            wrap = True, # version galería (si es 'False' las imagenes van en linea)
            scroll=ft.ScrollMode.ALWAYS,
            )
        self.numero = 0


    def crear_contenedores(self , numero: int, cuadricula=True):
        """Crea los contenedores vacios para la galeria"""
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        self.numero = numero
        for i in range(0, self.numero):
            cont = Contenedor_Imagen()
            # cont.key = str(i)     # asignar la clave anula las animaciones
            self.controls.append(cont)


    def estilo(self, estilo: Estilo_Contenedor ): 
        """Asigna un mismo estilo visual a todos los contenedores de la galeria."""
        for contenedor in self.controls:
            contenedor.estilo(estilo)


    def cargar_imagenes(self, imagenes: list[ft.Image],  cuadricula=True):
        """Este metodo carga imagenes de tipo ft.Image creadas externamente"""
        # Crea los contenedores vacios para la galeria y les carga las imagenes
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        self.numero = len(imagenes)
        self.controls = [] 
        for i in range( self.numero):
            imagen = imagenes[i]
            cont = Contenedor_Imagen()
            cont.content =  imagen
            self.controls.append(cont)


    def eventos(self, click = None, hover = None, longpress = None ):
        """Este metodo asigna handlers para todos los componentes de la galeria"""
        for contenedor in self.controls:
            contenedor.eventos(click, hover, longpress)


class Imagen(ft.Image):
    """Esta clase auxiliar permite inicializar imagenes de forma simplificada."""""
    def __init__(self, ruta: str, ancho=256, alto=256, redondeo=0):
        super().__init__(
            src = ruta,
            width = ancho,
            height = alto ,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(redondeo)
        )



def leer_imagenes(rutas: list[str], ancho=256, alto=256, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    imagenes = []
    i = 0 
    for ruta in rutas:
        imagen = Imagen(ruta, ancho, alto, redondeo)
        imagen.key = str(i)
        imagenes.append(imagen)
        i += 1
    return imagenes
  

def rutas_imagenes_picsum(numero: int, dim = 200 ):
    """Funcion auxiliar: busca imagenes online en Picsum.
    Permite elegir el número y tamaño de las imagenes.
    """
    rutas_imagenes = []
    for i in range(numero):
        ruta = f"https://picsum.photos/{dim}/{dim}?{i}"
        rutas_imagenes.append(ruta)
    return rutas_imagenes



def pagina_galeria(page: ft.Page):
    
    # parametros de ejemplo
    numero_imagenes =  15
    rutas_imagenes = rutas_imagenes_picsum(numero_imagenes, 256 )

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
    def funcion_click(e: ft.ControlEvent):
        cont = e.control 
        cont.estilo(estilo_click)
        print("click: ", cont.content.key)
        cont.update()

    def funcion_hover(e: ft.ControlEvent):
        cont = e.control 
        cont.estilo(estilo_hover)
        cont.update()

    def funcion_longpress(e: ft.ControlEvent): 
        cont = e.control        
        cont.estilo(estilo_defecto)
        cont.update()

    # Maquetado
    # componente galeria de contenedores con imágenes
    galeria = Galeria()
    page.add(galeria)
    lista_imagenes  = leer_imagenes(
        rutas = rutas_imagenes, 
        ancho = 400,
        alto  = 400,
        redondeo = 60
        )

    galeria.cargar_imagenes(lista_imagenes)

    galeria.estilo(estilo_defecto)
    galeria.eventos(
        click = funcion_click,
        hover = funcion_hover,
        longpress = funcion_longpress
        )


    def scroll_to_key(n, e):
        galeria.scroll_to(key=str(n), duration=1000)
        print(f"Imagen Nº:{n}")


    m = 0 
    boton_inicio = ft.ElevatedButton(  
        text="Inicio",    
        bgcolor=ft.colors.RED_800, 
        color=ft.colors.WHITE,
        on_click=partial(scroll_to_key, m)
        )

    m = int((numero_imagenes-1)/2)  
    boton_medio = ft.ElevatedButton(
        text="Medio",    
        bgcolor=ft.colors.AMBER_800, 
        color=ft.colors.WHITE, 
        on_click=partial(scroll_to_key, m)
        )

    m = numero_imagenes - 1 
    boton_fin = ft.ElevatedButton(   
        text="Fin",    
        bgcolor=ft.colors.GREEN_800, 
        color=ft.colors.WHITE,
        on_click=partial(scroll_to_key, m)
        )

    page.add(ft.Row([boton_inicio, boton_medio, boton_fin]))


    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=1200
    page.window_height=900
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK

    page.padding = 10
    page.update()


# creacion de ventana
if __name__ == "__main__":
    ft.app(target = pagina_galeria)
