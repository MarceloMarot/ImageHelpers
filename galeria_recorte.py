
import cv2
from rich import print as print
import flet as ft
from typing import TypeVar
import pathlib
from  threading import Thread
# INSTALAR
# pip install psutil
import psutil
import os
import gc
from multiprocessing import Process, Pipe, freeze_support, Lock


from cortar_imagen import ImagenOpenCV , ParametrosVentana
from componentes.galeria_imagenes import ContImag, Galeria, Contenedor_Imagen, imagen_clave, imagen_nombre
from sistema_archivos.buscar_extension import buscar_imagenes
from componentes.estilos_contenedores import estilos_galeria,estilos_seleccion


def nada( e ):
    pass


class ContenedorRecortes( Contenedor_Imagen):
    def __init__(self, ruta, clave: str, ancho=768, alto=768, redondeo=0,):
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        # flags para el coloreo de bordes
        self.marcada = False
        self.guardada = False
        self.defectuosa = False
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

        self.actualizar_estilos( )  


    def ruta_recortes(self, ruta_directorio: str):

        for contenedor in self.controls:
            contenedor.ruta_recorte(ruta_directorio)    


    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    


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


def actualizar_estilo_estado(
    contenedores: list[ContenedorRecortes], estilos : dict ):
    for contenedor in contenedores:
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.marcada :
            estilo = estilos["modificado"]
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        else: 
            estilo = estilos["predefinido"]

        contenedor.estilo( estilo )



def memory_usage_psutil( x=""):
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / float(2 ** 20)
    print(f"[bold green]Espacio en memoria: {mem}")
    return mem



def liberar_memoria():
    gc.collect(0)



# Nuevo proceso: ventana de OpenCV
def crear_ventana_opencv(tuberias, candado_recorte):
    
    [tuberia_galeria, tuberia_ventana, tuberia_click, tuberia_apertura ] = tuberias

    global ventana_emergente
    
    [data] =  tuberia_ventana.recv()
    parametros = data 
    
    # funcion adicional para el mouse --> envio datos
    def puntero_ventana_emergente( evento ):
        clave = ventana_emergente.clave
        if evento==cv2.EVENT_LBUTTONDOWN or evento==cv2.EVENT_RBUTTONDOWN:
            # envio de datos al proceso principal
            parametros = ventana_emergente.copiar_estados()
            clave = ventana_emergente.clave
            tuberia_ventana.send([clave, parametros])

            # monitoreo uso memoria
            memory_usage_psutil()

        liberar_memoria()

    ventana_emergente = ImagenOpenCV(candado=candado_recorte)
    ventana_emergente.interfaz_edicion(
        parametros,
        [512,512],[768,768],
        texto_consola=False, escape_teclado=False, 
        funcion_mouse=puntero_ventana_emergente,
        funcion_trackbar=memory_usage_psutil
        )  #tamaño recorte predefinido


# Variable global: requerida para inicializar correctamente la ventana emergente
subproceso_ventana = None


def pagina_galeria(page: ft.Page, tuberias, candado_recorte):
    """Funcion gráfica para crear la galería de Flet"""
    # lista completa de tuberias disponibles
    [tuberia_galeria, tuberia_ventana, tuberia_click, extremo_apertura ] = tuberias 

    ancho_pagina = 900
    altura_pagina = 800

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
            # busqueda de recortes preexistentes
            rutas_recortes = buscar_imagenes(directorio)

            nombres_recortes = []

            for recorte in rutas_recortes:
                nombres_recortes.append(str(pathlib.Path(recorte).name))

            global imagenes_galeria

            nombres_imagen = []

            for imagen in imagenes_galeria:
                ruta_imagen = imagen.ruta_imagen
                nombres_imagen.append(str(pathlib.Path(ruta_imagen).name))

            for nombre in nombres_imagen:
                if nombre in nombres_recortes:

                    imagen_seleccionada = imagen_nombre(nombre, imagenes_galeria)
                    indice = nombres_recortes.index(nombre)
                    imagen_seleccionada.guardada = True
                    imagen_seleccionada.update()

                    candado_recorte.acquire()
                    imagen_seleccionada.ruta_imagen = rutas_recortes[indice]
                    candado_recorte.release()

                    imagen_seleccionada.update()

            # actualizar graficas con los recortes 
            galeria.actualizar_estilos()
            galeria.update()



    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen   = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino   = ft.FilePicker(on_result = resultado_directorio_destino )
   
    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio_origen, dialogo_directorio_destino
        ])


    def recepcion_datos_ventana(tuberia):
        # global galeria
        while True:
            # se espera a recibir data emitida por los eventos del mouse
            [clave, parametros] = tuberia.recv()
            imagen_seleccionada = imagen_clave(clave, imagenes_galeria)

            imagen_seleccionada: ContenedorRecortes
            parametros: ParametrosVentana

            imagen_seleccionada.parametros = parametros

            if parametros.coordenadas_guardado != [0,0,0,0] :

                imagen_seleccionada.guardada = True
                imagen_seleccionada.marcada = False

                imagen_seleccionada.update()

                candado_recorte.acquire()
                imagen_seleccionada.ruta_imagen = parametros.ruta_recorte
                candado_recorte.release()

                imagen_seleccionada.update()


            if parametros.coordenadas_recorte != [0,0,0,0] and parametros.coordenadas_recorte != parametros.coordenadas_guardado :

                imagen_seleccionada.marcada = True
                # imagen_seleccionada.ruta_imagen = parametros.ruta_recorte
                imagen_seleccionada.update()

            # actualizacion de bordes
            galeria.actualizar_estilos()
            galeria.update()


    def click_galeria(e: ft.ControlEvent):

        global imagenes_galeria

        # lectura de datos de la imagen elegida
        contenedor = e.control     # es ft.Container
        clave = contenedor.clave
        imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
        parametros = imagen_seleccionada.parametros

        tuberia_click.send([parametros])


    # hilo perpetuo para recibir datos de la seleccion del recorte
    hilo_recepcion_datos = Thread(
        target=recepcion_datos_ventana, args=[tuberia_galeria,])
    hilo_recepcion_datos.start()

    # (NO USADO AUN) manejador del teclado
    def teclado_galeria(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")
  
    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = teclado_galeria

    galeria = GaleriaRecortes(estilos_galeria)
    page.add(galeria)

    liberar_memoria()
    memory_usage_psutil()

    page.title="Galeria Recorte"
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    page.update()



def apertura_ventana( tuberias, candado_recorte ):

    [tuberia_galeria, tuberia_ventana, tuberia_click, tuberia_apertura ] = tuberias
 
    global subproceso_ventana

    while True:
        # se espera hasta que se pida una nueva apertura
        [parametros] = tuberia_apertura.recv()
        # caso primera seleccion: crear ventana desde cero
        if subproceso_ventana==None:
            subproceso_ventana = Process(target=crear_ventana_opencv, args=(tuberias, candado_recorte,))
            subproceso_ventana.daemon=True
            subproceso_ventana.start()

            tuberia_galeria.send([parametros])  

        # caso contrario: destruir ventana y recrearla desde cero
        elif subproceso_ventana.is_alive():
            subproceso_ventana.terminate()
            subproceso_ventana = Process(target=crear_ventana_opencv, args=(tuberias, candado_recorte,))
            subproceso_ventana.daemon=True
            subproceso_ventana.start()
            tuberia_galeria.send([parametros])  
     


def crear_galeria(tuberias, candado):

    principal_tuberias = lambda pagina: pagina_galeria(pagina, tuberias, candado)
    ft.app(target=principal_tuberias)



if __name__=="__main__":

    #(requerido para los  subprocesos en Windows)
    freeze_support() # requerido para crear ejecutables en Windows

    # candado para proteger el acceso a archivos
    candado_recorte = Lock()
    # Pipe (tuberia) para interconectar interfases graficas
    tuberia_galeria, tuberia_ventana = Pipe()
    # Pipe (tuberia) para sincronizar la creacion de ventanas
    tuberia_click, tuberia_apertura = Pipe()

    tuberias = [tuberia_galeria, tuberia_ventana, tuberia_click, tuberia_apertura ]

    subproceso_solicitud_ventana =  Process(
        target=apertura_ventana, args=[tuberias, candado_recorte  ])
    subproceso_solicitud_ventana.start()

    subproceso_galeria = Process(
        target=crear_galeria, args=[tuberias, candado_recorte  ])
    subproceso_galeria.start()

    # se espera al cierre de la galeria para forzar el cierre de la ventana 
    subproceso_galeria.join()
    subproceso_solicitud_ventana.terminate()

