
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


from manejo_imagenes.cortar_imagen import ImagenOpenCV , ParametrosVentana
from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
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
        self.parametros = ParametrosVentana(
            ruta_origen=ruta, 
            clave=clave,
            )


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
        ancho=128,
        alto=128, 
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


# reasignacion de dimensiones para las imagenes de galeria
estilos_galeria["predefinido"]. width   = 128
estilos_galeria["predefinido"]. height  = 128
estilos_galeria["guardado"].    width   = 128
estilos_galeria["guardado"].    height  = 128
estilos_galeria["modificado"].  width   = 128
estilos_galeria["modificado"].  height  = 128
estilos_galeria["erroneo"].     width   = 128
estilos_galeria["erroneo"].     height  = 128




def pagina_galeria(page: ft.Page, tuberias, candado_recorte):
    """Funcion gráfica para crear la galería de Flet"""
    # lista completa de tuberias disponibles
    [tuberia_datos_recorte , tuberia_apertura_ventana ] = tuberias 

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

    barra_zoom = ft.Slider(min=20,value=50, max=200, divisions=40, label="{value}%")
    texto_zoom = ft.Text(f"Zoom: {barra_zoom.value:5}%")

    page.add(ft.Row([
        boton_carpeta_origen,
        boton_carpeta_destino,
        texto_zoom,
        barra_zoom,
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
            # asignacion de dimensiones y ubicacion de ventana emergente
            for img in imagenes_galeria:
                ruta = img.parametros.ruta_origen
                [altura, base, _ ] = dimensiones_imagen(ruta)
                # lectura de dimensiones
                img.parametros.dimensiones_original = [base, altura]

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


    def recepcion_datos_ventana(tuberia_datos_recorte):
        while True:
            # se espera a recibir data emitida por los eventos del mouse
            [parametros] = tuberia_datos_recorte[1].recv()
            imagen_seleccionada = imagen_clave(parametros.clave, imagenes_galeria)
            imagen_seleccionada: ContenedorRecortes
            parametros: ParametrosVentana
            imagen_seleccionada.parametros = parametros

            if parametros.coordenadas_guardado != [0,0,0,0] :
                # marcado de propiedades y actualizacion grafica
                imagen_seleccionada.guardada = True
                imagen_seleccionada.marcada = False 
                imagen_seleccionada.update()
                # 
                candado_recorte.acquire()
                imagen_seleccionada.ruta_imagen = parametros.ruta_recorte
                candado_recorte.release()
                # actualizacion grafica
                imagen_seleccionada.update()

            if parametros.coordenadas_recorte != [0,0,0,0] and parametros.coordenadas_recorte != parametros.coordenadas_guardado :
                imagen_seleccionada.marcada = True
                imagen_seleccionada.update()

            # actualizacion de bordes
            galeria.actualizar_estilos()
            galeria.update()


    def click_galeria(e: ft.ControlEvent):
        global imagenes_galeria
        global clave_actual        
        # lectura de datos de la imagen elegida
        contenedor = e.control     # es ft.Container
        clave_actual = contenedor.clave
        enviar_imagen_clave(clave_actual)


    def enviar_imagen_clave(clave):
        """Esta funcion envia los parametros de la imagen con la clave indicada para visualizarla en la ventana emergente."""
        global imagenes_galeria
        imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
        parametros = imagen_seleccionada.parametros
        # Forzar dimensiones y ubicacion de ventana emergente
        #movimiento
        page.update()
        x = int(page.window_left + page.window_width)
        y = int(page.window_top)
        parametros.coordenadas_ventana = [x, y]  
        zoom = barra_zoom.value
        base   = int(zoom * parametros.dimensiones_original[0] / 100)
        altura = int(zoom * parametros.dimensiones_original[1] / 100 )
        parametros.dimensiones_ventana = [base, altura]   
        tuberia_apertura_ventana[1].send([parametros])


    def cambio_zoom(e: ft.ControlEvent):
        valor = e.control.value
        texto_zoom.value=f"Zoom: {int(valor):5}%"
        texto_zoom.update()

        global clave_actual
        enviar_imagen_clave(clave_actual)

    barra_zoom.on_change = cambio_zoom

    # hilo perpetuo para recibir datos de la seleccion del recorte
    hilo_recepcion_datos = Thread(
        target=recepcion_datos_ventana, args=[tuberia_datos_recorte,])
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



def apertura_ventana_opencv( tuberias, candado_recorte ):
    """Esta rutina llama a la ventana de edicion hecha en OpenCV. Se ejecuta en un subproceso."""

    [tuberia_datos_recorte , tuberia_apertura_ventana ] = tuberias 

    ventana_emergente = ImagenOpenCV(
        candado = candado_recorte,
        canal_recepcion = tuberia_apertura_ventana,
        canal_transmision = tuberia_datos_recorte,
        )    
    
    # llamado a la ventana grafica (bucle condicional, se sale por teclado)
    ventana_emergente.interfaz_edicion( 
        texto_consola = False, 
        escape_teclado = True, 
        # escape_teclado = False, 
        )    # Tamaño predefinido 
     


def crear_galeria(tuberias, candado):
    """Esta funcion auxiliar permite llamar a la pagina de FLET .
    Al mismo tiempo le adjunta como argumentos los pipes y locks necesarios para que funcionw el sistema.
    Se ejecuta en un subproceso."""
    principal_tuberias = lambda pagina: pagina_galeria(pagina, tuberias, candado)
    ft.app(target=principal_tuberias)



if __name__=="__main__":

    #(requerido para los  subprocesos en Windows)
    freeze_support() # requerido para crear ejecutables en Windows

    # candado para proteger el acceso a archivos
    candado_recorte = Lock()
    # Pipe (tuberia) para interconectar interfases graficas
    extremo_interno, extremo_externo = Pipe()
    tuberia_datos_recorte = [extremo_interno, extremo_externo]
    # Pipe (tuberia) para sincronizar la creacion de ventanas
    extremo_interno, extremo_externo = Pipe()
    tuberia_apertura_ventana = [extremo_interno, extremo_externo]

    tuberias = [tuberia_datos_recorte , tuberia_apertura_ventana ]

    subproceso_galeria = Process(
        target=crear_galeria, args=[tuberias, candado_recorte  ])
    subproceso_galeria.start()

    subproceso_solicitud_ventana =  Process(
        target=apertura_ventana_opencv, args=[tuberias, candado_recorte  ])
    subproceso_solicitud_ventana.start()


    # se espera al cierre de la galeria para forzar el cierre de la ventana 
    subproceso_galeria.join()
    subproceso_solicitud_ventana.terminate()

