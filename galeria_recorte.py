from cv2 import EVENT_LBUTTONDOWN, EVENT_RBUTTONDOWN
from rich import print as print
import flet as ft
from typing import TypeVar
# import cv2
from cortar_imagen import ImagenOpenCV , ParametrosVentana



# from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor, imagen_clave
# from componentes.menu_navegacion import  MenuNavegacion
# from componentes.etiquetador_botones import EtiquetadorBotones

# from componentes.lista_desplegable import crear_lista_desplegable,convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from sistema_archivos.buscar_extension import buscar_imagenes

# from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
from componentes.estilos_contenedores import estilos_galeria


# from componentes.galeria_imagenes import Cont, ContImag


def nada( e ):
    pass


class ContenedorRecortes( Contenedor_Imagen):
    def __init__(self, ruta, clave: str, ancho=768, alto=768, redondeo=0,):
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        # self.__etiquetada = False
        self.__marcada = False
        self.__guardada = False
        self.__defectuosa = False
        # datos de la ventana emergente
        self.parametros = ParametrosVentana(ruta_origen=ruta, clave=clave)


    @property
    def defectuosa(self):
        return self.__defectuosa


    @property
    def guardada(self):
        return self.__guardada 


    @property
    def marcada(self):
        return self.__marcada


# nuevos tipados para contenedor y sus subclases
ContRec = TypeVar('ContRec', bound=ContenedorRecortes)


class GaleriaRecortes( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.imagenes: list[ContenedorRecortes]


    # def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
    #     self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        
    #     contenedores = leer_imagenes_etiquetadas(rutas_imagen, ancho, alto, redondeo)
    #     self.numero = len(contenedores)
    #     self.controls = contenedores

    #     actualizar_estilo_estado( contenedores, self.estilos)


    def cargar_imagenes(self, 
        imagenes: list[ContRec ], 
        cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        # actualizar_estilo_estado( imagenes, self.estilos)  # FIX
        self.actualizar_estilos( )  # FIX



    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    


def actualizar_estilo_estado(
    contenedores: list[ContRec], estilos : dict ):
    for contenedor in contenedores:
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        elif contenedor.marcada :
            estilo = estilos["modificado"]
        else: 
            estilo = estilos["predefinido"]

        contenedor.estilo( estilo )


def leer_imagenes_recortes(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        clave = f"imag_{i}"
        contenedor = ContenedorRecortes(rutas_imagen[i], clave, ancho, alto, redondeo)
        contenedor.clave = clave
        contenedores.append(contenedor)
    return contenedores


def cargar_imagenes_recortes(rutas: list[str]):
    # replica de imagenes para la galeria - menor resolucion
    galeria = []
    galeria = leer_imagenes_recortes(
        rutas,
        ancho=256,
        alto=256, 
        redondeo=10
        )
    return galeria




clickeos = 0



def main(page: ft.Page):

    ancho_pagina = 800
    altura_pagina = 800

    ruta_recorte = "recorte.webp"

    # Botones apertura de ventana emergente
    boton_carpeta = ft.ElevatedButton(
        text = "Abrir carpeta",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.RED,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_directorio.get_directory_path(
            dialog_title="Elegir carpeta con todas las imágenes"
        ),
    )

    page.add(boton_carpeta)


    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        if e.path:

            # acceso a elementos globales
            global imagenes_galeria
            # busqueda 
            directorio = e.path
            rutas_imagen = buscar_imagenes(directorio)
            # Carga de imagenes del directorio
            imagenes_galeria = cargar_imagenes_recortes(rutas_imagen)

            for img in imagenes_galeria:
                print(f"imag: {img.clave}")

            # Objeto galeria
            # galeria.leer_imagenes(rutas_imagen, redondeo = 30)
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_galeria)
            galeria.estilo(estilos_galeria["predefinido"])
            galeria.update()


    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   = ft.FilePicker(on_result = resultado_directorio )
   
    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio
        ])


    def click_ventana_emergente( evento ):
        global ventana_emergente
        clave =  ventana_emergente.clave

        if evento==EVENT_LBUTTONDOWN or evento==EVENT_RBUTTONDOWN:
            imagen_seleccionada: ContenedorRecortes
            # print(f"[bold cyan]Ventana --> Clave imagen: {clave}")
            imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
            imagen_seleccionada.parametros = ventana_emergente.parametros


    def click_galeria(e):
        global clickeos
        clickeos += 1
        global ventana_emergente
        global imagen
        global imagenes_galeria

        contenedor = e.control     # es ft.Container
        clave = contenedor.clave

        if clickeos ==1: 
            imagen = e.control 
            # print("[bold blue]Galeria -> clave imagen: ", clave)
            ventana_emergente = ImagenOpenCV()
            ventana_emergente.interfaz_edicion(
                imagen.ruta_imagen, ruta_recorte,clave ,
                [512,512],[768,768],
                texto_consola=False, escape_teclado=False, 
                funcion_mouse=click_ventana_emergente
                )  #tamaño recorte predefinido

        if clickeos >1: 
            # print("[bold blue]Galeria -> clave imagen: ",clave)
            imagen = imagen_clave(clave, imagenes_galeria)
            parametros = imagen.parametros
            ventana_emergente.recuperar_estados(parametros)



    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")
  

    galeria = GaleriaRecortes(estilos_galeria)
    page.add(galeria)

    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = desplazamiento_teclado

    page.title="Galeria Recorte"
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    page.update()








if __name__=="__main__":
    ft.app(target=main)


