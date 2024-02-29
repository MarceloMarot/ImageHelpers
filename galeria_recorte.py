import cv2
from rich import print as print
import flet as ft
from typing import TypeVar
from cortar_imagen import ImagenOpenCV , ParametrosVentana
import pathlib

from componentes.galeria_imagenes import Galeria, Contenedor_Imagen, imagen_clave
from sistema_archivos.buscar_extension import buscar_imagenes
from componentes.estilos_contenedores import estilos_galeria

# import threading
from  threading import Thread


def nada( e ):
    pass


class ContenedorRecortes( Contenedor_Imagen):
    def __init__(self, ruta, clave: str, ancho=768, alto=768, redondeo=0,):
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        # flags para el coloreo de bordes
        self.__marcada = False
        self.__guardada = False
        self.__defectuosa = False
        # datos de la ventana emergente
        self.parametros = ParametrosVentana(ruta_origen=ruta, clave=clave)


    def ruta_recorte(self, ruta_directorio: str):
        """Este metodo asigna una ruta de destino para el recorte dentro del directorio indicado"""
        directorio = pathlib.Path(ruta_directorio)
        nombre_archivo = pathlib.Path(self.ruta_imagen).name
        # composicion del archivo de salida
        ruta_recorte = pathlib.Path(directorio, nombre_archivo)
        # asignacion de ruta de salida
        self.parametros.ruta_recorte = str(ruta_recorte)


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


    def ruta_recortes(self, ruta_directorio: str):
        # contenedor: ContenedorRecortes
        for contenedor in self.controls:
            contenedor.ruta_recorte(ruta_directorio)    


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


# Variable global: requerida para inicializar correctamente la ventana emergente
clickeos = 0

hilo = None


def main(page: ft.Page):

    ancho_pagina = 900
    altura_pagina = 800

    ruta_recorte = "recorte.webp"

    # Botones
    ancho_botones = 200
    altura_botones = 40


    # Botones apertura de ventana emergente
    boton_carpeta_origen = ft.ElevatedButton(
        text = "Carpeta capturas",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.BLUE_900,
        color= ft.colors.WHITE,
        height = altura_botones,
        width  = ancho_botones,
        ## manejador
        on_click=lambda _: dialogo_directorio_origen.get_directory_path(
            dialog_title="Elegir carpeta con las capturas de imagen"
        ),
    )

    boton_carpeta_destino = ft.ElevatedButton(

        text = "Carpeta recortes",
        icon=ft.icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_destino.get_directory_path(
            dialog_title="Elegir carpeta para los recortes",
            ),
        disabled = True,       
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.RED_900,
        color = ft.colors.WHITE,
    )


    page.add(ft.Row([
        boton_carpeta_origen,
        boton_carpeta_destino
        ]))

    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):
        if e.path:
            # acceso a elementos globales
            global imagenes_galeria
            # busqueda 
            directorio = e.path
            # print(f"[bold green]{directorio}")
            rutas_imagen = buscar_imagenes(directorio)
            # Creacion y carga de imagenes del directorio
            imagenes_galeria = cargar_imagenes_recortes(rutas_imagen)
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_galeria)
            galeria.estilo(estilos_galeria["predefinido"])
            galeria.update()
            # desbloquea el boton de recortes
            boton_carpeta_destino.disabled=False
            boton_carpeta_destino.update()


    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        if e.path:
            directorio = e.path
            # asignacion de rutas de salida
            galeria.ruta_recortes(directorio)


    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen   = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino   = ft.FilePicker(on_result = resultado_directorio_destino )
   
    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio_origen, dialogo_directorio_destino
        ])


    def puntero_ventana_opencv( evento ):
        global ventana_emergente
        clave = ventana_emergente.clave

        imagen_seleccionada: ContenedorRecortes
        imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
        imagen_seleccionada.parametros = ventana_emergente.copiar_estados()

        # if evento==cv2.EVENT_LBUTTONDOWN or evento==cv2.EVENT_RBUTTONDOWN:
        #     imagen_seleccionada: ContenedorRecortes
        #     imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
        #     imagen_seleccionada.parametros = ventana_emergente.copiar_estados()


    def crear_ventana_opencv( parametros):
        global ventana_emergente
        ventana_emergente = ImagenOpenCV()
        ventana_emergente.interfaz_edicion(
            parametros,
            [512,512],[768,768],
            texto_consola=False, escape_teclado=False, 
            funcion_mouse=puntero_ventana_opencv
            )  #tamaño recorte predefinido


    def click_galeria(e: ft.ControlEvent):
        global clickeos
        clickeos += 1
        global ventana_emergente
        global imagenes_galeria

        contenedor = e.control     # es ft.Container
        clave = contenedor.clave

        imagen = imagen_clave(clave, imagenes_galeria)
        parametros = imagen.parametros

        global hilo

        if hilo == None or hilo.is_alive() == False:
            hilo = Thread(
                target = crear_ventana_opencv,
                args   = [parametros]
                )
            hilo.start()
        else:
            ventana_emergente.leer_estados(parametros)


    # manejador del teclado
    def teclado_galeria(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")
  

    galeria = GaleriaRecortes(estilos_galeria)
    page.add(galeria)

    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = teclado_galeria

    page.title="Galeria Recorte"
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    page.update()



if __name__=="__main__":
    ft.app(target=main)


