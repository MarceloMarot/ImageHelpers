from typing import Sequence
from rich import print as print
import flet as ft

import re

from componentes.procesar_etiquetas import Etiquetas 
from componentes.galeria_imagenes import Galeria, Imagen,Contenedor, Contenedor_Imagen, Estilo_Contenedor
from componentes.menu_navegacion import  MenuNavegacion
from componentes.etiquetador_botones import FilasBotones, EtiquetadorBotones

from sistema_archivos.buscar_extension import buscar_imagenes


class Contenedor_Etiquetado( Etiquetas, Contenedor_Imagen):
    def __init__(self, ruta, ancho=768, alto=768, redondeo=0):
        Etiquetas.__init__(self, ruta)
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        self.__etiquetada = False
        self.__guardada = False
        self.__defectuosa = False
        self.verificar_imagen()
        self.verificar_etiquetado()
        self.verificar_guardado()


    def verificar_imagen(self):
        """Este metodo verificará extension y dimensiones de archivo"""
        pass 

    @property
    def defectuosa(self):
        return self.__defectuosa

    def verificar_etiquetado(self):
        """Verifica si hay etiquetas en la imagen, ya sea guardadas o sin guardar """
        self.__etiquetada = True if len(self.tags) > 0 else False


    @property
    def etiquetada(self):
        return self.__etiquetada 

    def verificar_guardado(self):
        """Comprueba si las etiquetas actuales son las mismas que las guardas en archivo de texto"""
        archivado = Etiquetas(self.ruta)
        self.verificar_etiquetado()
        guardado = set(self.tags) == set(archivado.tags)   # si los tags son iguales da True; en caso contrario da False
        self.__guardada = guardado and self.etiquetada      # se descartan no etiquetados

    @property
    def guardada(self):
        return self.__guardada 



class Etiquetador_Imagenes( EtiquetadorBotones ):
    def __init__(self):
        super().__init__()

    def todas_etiquetas(self, e):
        super().todas_etiquetas(e)
        # codigo agregado

    def ninguna_etiqueta(self, e):
        super().ninguna_etiqueta(e)

    def restablecer_etiquetas(self, e):
        super().restablecer_etiquetas(e)

    def guardar_etiquetas(self, e):
        super().guardar_etiquetas(e)


class MenuEtiquetado( MenuNavegacion):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.alto  = 800
        self.ancho = 600
        

    def cargar_imagen(self):
        """"Este metodo carga la imagen y cambia el estilo del contenedor segun el estado del etiquetado"""
        # Carga de imagen
        super().cargar_imagen()
        # MenuNavegacion.cargar_imagen(self)
        print("imagen cargada")
        indice = self.indice
        contenedor_imagen = self.imagenes[indice]
        # seleccion de estilo segun jerarquia
        actualizar_estilo_estado( [contenedor_imagen], self.estilos)


    def cargar_imagenes(self, imagenes: list[Contenedor]):
        super().cargar_imagenes(imagenes)
        actualizar_estilo_estado( imagenes, self.estilos)


class GaleriaEtiquetado( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos

    def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
        self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        
        contenedores = leer_imagenes_etiquetadas(rutas_imagen, ancho, alto, redondeo)
        self.numero = len(contenedores)
        self.controls = contenedores

        actualizar_estilo_estado( contenedores, self.estilos)


    def cargar_imagenes(self, imagenes: list[Contenedor], cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        actualizar_estilo_estado( imagenes, self.estilos)  # FIX



def actualizar_estilo_estado(
    contenedores: list[Contenedor_Etiquetado], estilos : dict ):
    for contenedor in contenedores:
        # estilo = componente.__estilo_predefinido
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        elif contenedor.etiquetada :
            estilo = estilos["modificado"]
        else: 
            estilo = estilos["predefinido"]

        contenedor.estilo( estilo )



def leer_imagenes_etiquetadas(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    # imagenes = []
    # i = 0 
    # for ruta in rutas:
    #     imagen = Contenedor_Etiquetado(ruta, ancho, alto, redondeo)
    #     imagen.content.key = str(i) # asignacion de indice como clave
    #     imagenes.append(imagen)
    #     i += 1
    # return imagenes
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        contenedor = Contenedor_Etiquetado(rutas_imagen[i], ancho, alto, redondeo)
        # contenedor.content.key = str(i)
        contenedor.content.key = f"imag_{i}"
        contenedores.append(contenedor)
    return contenedores






# estilos para contenedores 
estilo_galeria_defecto = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(5, ft.colors.INDIGO_100)
    )

estilo_galeria_modificado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.AMBER_400,
    border=ft.border.all(5, ft.colors.YELLOW_300)
    )

estilo_galeria_guardado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.LIME_600,
    border=ft.border.all(5, ft.colors.GREEN_500)
    )

estilo_galeria_erroneo = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.RED_400,
    border=ft.border.all(5, ft.colors.BROWN_300)
    )

estilos_galeria = {
    "predefinido" : estilo_galeria_defecto,
    "modificado" : estilo_galeria_modificado,
    "guardado" : estilo_galeria_guardado,
    "erroneo" : estilo_galeria_erroneo
    }


# estilos para el contenedor 
estilo_menu_defecto = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )
estilo_menu_modificado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.AMBER_400,
    border=ft.border.all(10, ft.colors.YELLOW_300)
    )
estilo_menu_guardado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.LIME_600,
    border=ft.border.all(10, ft.colors.GREEN_500)
    )
estilo_menu_erroneo = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_400,
    border=ft.border.all(10, ft.colors.BROWN_300)
    )

estilos_seleccion = {
    "predefinido" : estilo_menu_defecto,
    "modificado" : estilo_menu_modificado,
    "guardado" : estilo_menu_guardado,
    "erroneo" : estilo_menu_erroneo
    }


def main(pagina: ft.Page):


    def cargar_imagenes(rutas: list[str]):
        # Imagenes - objetos ft.Image con etiquetas leidas desde archivo TXT
        etiquetadas = []
        etiquetadas = leer_imagenes_etiquetadas(
            rutas,
            ancho=768,
            alto=768, 
            redondeo=30
            )
        # replica de imagenes para la galeria - menor resolucion
        galeria = []
        galeria = leer_imagenes_etiquetadas(
            rutas,
            ancho=256,
            alto=256, 
            redondeo=10
            )
        return [etiquetadas, galeria]


    ############# COMPONENTES ######################## 

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

    boton_dataset = ft.ElevatedButton(
        text = "Abrir dataset",
        icon=ft.icons.FILE_OPEN,
        bgcolor=ft.colors.BLUE,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_dataset.pick_files(
            dialog_title= "Elegir archivo TXT con todas las etiquetas",
            allowed_extensions=["txt"],
            allow_multiple=False,
        )
    )
    # etiquetas seleccionables
    etiquetador_botones = EtiquetadorBotones()

    galeria = GaleriaEtiquetado( estilos_galeria )

    menu_seleccion = MenuEtiquetado( estilos_seleccion)


    #############  MAQUETADO ############################

    # Fila de botones para abrir carpetas y leer archivos
    pagina.add(ft.Row([
        boton_carpeta,
        boton_dataset
        ]))

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
        )

    # pestaña de etiquetado y navegacion de imagenes
    altura_tab_etiquetado = 800
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            menu_seleccion ,
            ft.VerticalDivider(),
            etiquetador_botones
            ], 
        spacing = 10, 
        height = altura_tab_etiquetado
    ) 

    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=fila_etiquetado_navegacion,
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            tab_galeria   ,
            tab_etiquetado
        ],
        expand=1,
        # disabled=True,        # deshabilita controles internos, no las pestañas en si
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)


    ############## HANDLERS ##################################


    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        if e.path:

            # acceso a elementos globales
            global imagenes_etiquetadas
            global imagenes_galeria
            # busqueda 
            directorio = e.path
            rutas_imagen = buscar_imagenes(directorio)
            # Carga de imagenes del directorio
            imagenes_etiquetadas, imagenes_galeria = cargar_imagenes(rutas_imagen)

            # Objeto galeria
            galeria.cargar_imagenes( imagenes_galeria )
            # galeria.leer_imagenes( rutas_imagen ) 
            # galeria.estilo(estilo_galeria_defecto)
            galeria.eventos(click = click_imagen_galeria)
            galeria.update()

            # Objeto seleccion imagen
            menu_seleccion.cargar_imagenes(imagenes_etiquetadas)
            # imagenes = imagenes_etiquetadas 
            menu_seleccion.indice = 0
            menu_seleccion.cargar_imagen()
            menu_seleccion.eventos(
                click=click_imagen_seleccion,
                funcion_botones = lambda _ : click_botones_seleccion(_)
                )
            # actualizacion del etiquetador --> habilita los controles y etiquetas
            etiquetador_botones.setear_salida(imagenes_etiquetadas[0])
            etiquetador_botones.update()

            # actualizacion del selector de imagenes --> habilita los controles
            menu_seleccion.alto  = altura_tab_etiquetado
            menu_seleccion.ancho = 600
            menu_seleccion.expand = True
            menu_seleccion.habilitado = True
            menu_seleccion.update()

            # reporte por consola
            print("[bold red]Carga imagenes")
            print("[bold red]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
            print("[bold red]Nº imagenes galeria     : ", len(imagenes_galeria))
        else:
            return


    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        if e.files:

            ruta = e.files[0]                   # SOLO UN ARCHIVO DE LISTA ( FIX )
            archivo_dataset = ruta.path

            # Objeto etiquetador
            dataset = Etiquetas(archivo_dataset) 
            etiquetador_botones.leer_dataset( dataset )

            # se asegura que los botones esten deshabilitados hasta abrir galeria
            etiquetador_botones.habilitado = True if menu_seleccion.habilitado else False
            etiquetador_botones.update() 

            etiquetador_botones.alto  = altura_tab_etiquetado
            etiquetador_botones.ancho = 500
            etiquetador_botones.expand = True
            etiquetador_botones.update()

            print("[bold cyan]Carga dataset")
            print("[bold cyan]Nombre archivo: ", archivo_dataset)

        else:
            return

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   = ft.FilePicker(on_result = resultado_directorio )
    dialogo_dataset      = ft.FilePicker(on_result = resultado_dataset)

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, dialogo_dataset
        ])


    def scroll_to_key(n):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su numero ('key')."""
        galeria.scroll_to(key=str(n), duration=1000)


    def clave_imagen(key, x: Contenedor_Etiquetado):
        return True if key == x.content.key else False


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Esta imagen permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        clave = contenedor.content.key
        # i = int(key) 
        global imagenes_etiquetadas
        global imagenes_galeria
        # actualizacion de imagen seleccionada y etiquetado
        print("[bold yellow]Click imagen galeria")
        print("[bold yellow]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
        print("[bold yellow]Nº imagenes galeria     : ", len(imagenes_galeria))
        print("[bold yellow]Clave imagen: " , clave)

        key_imagen = lambda x: clave_imagen(clave, x)
        objeto_filtrado = filter(key_imagen ,imagenes_etiquetadas)
        imagen_seleccionada = list(objeto_filtrado)[0]

        # etiquetador_botones.setear_salida(imagenes_etiquetadas[i])
        etiquetador_botones.setear_salida(imagen_seleccionada)
        patron = r"[0-9]+" 
        retorno = re.search(patron, clave)
        indice = retorno.group()
        print(clave, retorno)
        menu_seleccion.indice = int(indice)
        #cambio de pestaña
        pestanias.selected_index = 1
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        #regreso a la galeria
        contenedor_imagen = e.control
        key = contenedor_imagen.content.key
        global imagenes_etiquetadas
        global imagenes_galeria
        print("[bold green]Click imagen seleccion")
        print("[bold green]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
        print("[bold green]Nº imagenes galeria     : ", len(imagenes_galeria))
        print("[bold green]Indice : " , key)
        scroll_to_key( key)      
        #cambio de pestaña
        pestanias.selected_index=0
        # galeria.update()
        pagina.update()


    def click_botones_seleccion( indice: int ):
        """ Esta funcion controla el cambio de imagen en el selector"""
        # (el cambio de imagen está integrado al componente)
        # actualizacion etiquetas
        # global imagenes_etiquetadas
        global imagenes_etiquetadas
        global imagenes_galeria
        print("[bold magenta]Botones seleccion")
        print("[bold magenta]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
        print("[bold magenta]Nº imagenes galeria     : ", len(imagenes_galeria))
        print("[bold magenta]Imagen boton seleccion:" , indice)
        etiquetador_botones.setear_salida(imagenes_etiquetadas[indice])
        # actualizacion pagina
        tab_etiquetado.update()


    # manejador del teclado
    def on_keyboard(e: ft.KeyboardEvent):
        tecla = e.key   
        # Avance y retroseso de imagenes en seleccion y galeria
        incremento = 0
        if tecla == "Arrow Left" or tecla == "A":
            incremento = - 1     # retroceso
        elif tecla == "Arrow Right" or tecla == "D":
            incremento = 1      # avance
        # cambio de imagen seleccion
        menu_seleccion.cambiar_indice(incremento, 1 )


    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = on_keyboard

    def cambio_pestanias(e):
        indice = menu_seleccion.indice
        if pestanias.selected_index == 0:
            scroll_to_key(indice)

    pestanias.on_change = cambio_pestanias


    ############## CONFIGURACIONES ################     
     
    galeria.ancho = 1200

    menu_seleccion.alto  = altura_tab_etiquetado
    # menu_seleccion.ancho = 600
    menu_seleccion.expand = True
    menu_seleccion.habilitado = False

    etiquetador_botones.alto  = altura_tab_etiquetado
    etiquetador_botones.ancho = 500
    etiquetador_botones.expand = True
    etiquetador_botones.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = 1500
    pagina.window_height = 900
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)