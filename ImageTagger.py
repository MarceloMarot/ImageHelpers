from rich import print as print
import flet as ft

from componentes.procesar_etiquetas import Etiquetas 
from componentes.galeria_imagenes import Galeria, Imagen, Contenedor_Imagen, Estilo_Contenedor, leer_imagenes
from componentes.menu_navegacion import  MenuNavegacion
from componentes.etiquetador_botones import FilasBotones, EtiquetadorBotones

from sistema_archivos.buscar_extension import buscar_imagenes


class Imagen_Etiquetada( Etiquetas, Imagen):
    def __init__(self, ruta, ancho=768, alto=768, redondeo=0):
        Etiquetas.__init__(self, ruta)
        Imagen.__init__(self,ruta, ancho, alto, redondeo)


def leer_imagenes_etiquetadas(rutas: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    imagenes = []
    i = 0 
    for ruta in rutas:
        imagen = Imagen_Etiquetada(ruta, ancho, alto, redondeo)
        imagen.key = str(i) # asignacion de indice como clave
        imagenes.append(imagen)
        i += 1
    return imagenes


# estilos para contenedores 
galeria_estilo_defecto = Estilo_Contenedor(
    width = 256,
    height = 256,
    border_radius = 50, 
    # bgcolor = ft.colors.BLUE_400,
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )


# estilos para el contenedor 
menu_estilo_defecto = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 50, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )


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
        galeria = leer_imagenes(
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
        # disabled = True,    # comienza deshabilitado
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
    # componente galeria
    galeria = Galeria()
    # componente seleccion imagen
    menu_seleccion = MenuNavegacion()

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
            galeria.estilo(galeria_estilo_defecto)
            galeria.eventos(click = click_imagen_galeria)
            galeria.update()

            # Objeto seleccion imagen
            menu_seleccion.imagenes( imagenes_etiquetadas )
            menu_seleccion.estilo(menu_estilo_defecto)
            menu_seleccion.indice = 0
            menu_seleccion.cargar_imagen()
            menu_seleccion.eventos(
                click=click_imagen_seleccion,
                funcion_botones = lambda _ : click_botones_seleccion(_)
                )
            # actualizacion del etiquetador --> habilita los controles y etiquetas
            # if etiquetador_botones.salida_seteada and etiquetador_botones.dataset_seteado:
            #     etiquetador_botones.habilitado =
            # if etiquetador_botones.habilitado: 
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
            # se habilita la lectura de archivos
            # boton_carpeta.disabled = False
            # boton_carpeta.update()

            etiquetador_botones.alto  = altura_tab_etiquetado
            etiquetador_botones.ancho = 500
            etiquetador_botones.expand = True
            etiquetador_botones.update()

            print("[bold cyan]Carga dataset")
            print("[bold cyan]nombre archivo: ", archivo_dataset)

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


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Esta imagen permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        key = contenedor.content.key
        i = int(key) 
        global imagenes_etiquetadas
        global imagenes_galeria
        # actualizacion de imagen seleccionada y etiquetado
        print("[bold yellow]Click imagen galeria")
        print("[bold yellow]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
        print("[bold yellow]Nº imagenes galeria     : ", len(imagenes_galeria))
        print("[bold yellow]Indice : " , i)
        etiquetador_botones.setear_salida(imagenes_etiquetadas[i])
        menu_seleccion.indice = i
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
        # print(key)
        scroll_to_key( key)      
        #cambio de pestaña
        pestanias.selected_index=0
        galeria.update()
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
        print("[bold magenta]imagen boton seleccion:" , indice)
        etiquetador_botones.setear_salida(imagenes_etiquetadas[indice])
        # actualizacion pagina
        tab_etiquetado.update()



    # manejador del teclado
    def on_keyboard(e: ft.KeyboardEvent):
        tecla = e.key   
        # Avance y retroseso de imagenes en seleccion y galeria
        incremento = 0
        if tecla == "Arrow Left" or tecla == "A":
            incremento = -1     # retroceso
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
    menu_seleccion.ancho = 600
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
    pagina.window_maximizable=True
    pagina.window_minimizable=True
    pagina.window_maximized=False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)