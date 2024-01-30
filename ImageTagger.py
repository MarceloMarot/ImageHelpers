
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

    # BASURA XD
    # b1=ft.ElevatedButton(text= "nada")
    # b2=ft.ElevatedButton(text= "todo")
    # fila_basura = ft.Row([b1, b2])
    # pagina.add(fila_basura)

    #  LECTURA DATOS (REEESCRIBIR)          FIX

    # Busqueda de las imagenes disponibles
    directorio   = "/home/x/Codigos/cartoons"
    rutas_imagen  = buscar_imagenes(directorio)

    # truncamiento de lista imagenes         FIX
    # rutas_imagen = rutas_imagen[0:10]      # FIX

    # dataset con todos los tags
    archivo_dataset = "demo_etiquetas.txt"

    # Imagenes - objetos ft.Image con etiquetas leidas desde archivo TXT
    imagenes_etiquetadas = leer_imagenes_etiquetadas(
        rutas_imagen,
        ancho=768,
        alto=768, 
        redondeo=30
        )
    # replica de imagenes para la galeria - menor resolucion
    imagenes_galeria = leer_imagenes(
        rutas_imagen,
        ancho=256,
        alto=256, 
        redondeo=10
        )

    ############# COMPONENTES ######################## 

    # etiquetas seleccionables
    # filas_etiquetas     = FilasBotones()
    # etiquetador_botones = EtiquetadorBotones(filas_etiquetas)
    etiquetador_botones = EtiquetadorBotones()
    # componente galeria
    galeria = Galeria()
    # componente seleccion imagen
    menu_seleccion = MenuNavegacion()

    #############  MAQUETADO ############################

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
        )

    # pestaña de etiquetado y navegacion de imagenes
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            menu_seleccion ,
            ft.VerticalDivider(),
            etiquetador_botones
            ], 
        spacing = 10, 
        # width   = 1000, 
        # expand  = True
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
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)


    ############## HANDLERS ##################################

    def scroll_to_key(n):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su numero ('key')."""
        galeria.scroll_to(key=str(n), duration=1000)


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Esta imagen permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        key = contenedor.content.key
        # actualizacion de imagen seleccionada 
        # menu_seleccion.indice = int(key)
        # actualizacion del archivo de etiquetado
        # lectura de nombre archivo
        # ruta = contenedor.content.src
        # filas_etiquetas.leer_etiquetas(ruta)
        # imagen = contenedor.content
        # print(imagen)
        # print(imagen.key)
        i = int(key) 
        etiquetador_botones.leer_etiquetas(imagenes_etiquetadas[i])
        menu_seleccion.indice = i
        #cambio de pestaña
        pestanias.selected_index=1
        # actualizacion grafica
        pagina.update()
        # menu_seleccion.cargar_imagen()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        #regreso a la galeria
        contenedor_imagen = e.control
        key = contenedor_imagen.content.key
        print(key)
        scroll_to_key( key)      
        #cambio de pestaña
        pestanias.selected_index=0
        galeria.update()
        pagina.update()


    def click_botones_seleccion( indice: int ):
        """ Esta funcion controla el cambio de imagen en el selector"""
        # (el cambio de imagen está integrado al componente)
        # actualizacion etiquetas
        # ruta = imagenes_etiquetadas[indice].src
        # filas_etiquetas.leer_etiquetas(ruta)
        etiquetador_botones.leer_etiquetas(imagenes_etiquetadas[indice])
        # actualizacion pagina
        tab_etiquetado.update()


    ############## CONFIGURACIONES ################                                     FIX

    # Objeto seleccion imagen
    # menu_seleccion.estilo_contenedor = menu_estilo_defecto
    menu_seleccion.imagenes( imagenes_etiquetadas )
    menu_seleccion.estilo(menu_estilo_defecto)
    menu_seleccion.cargar_imagen()
    menu_seleccion.eventos(click=click_imagen_seleccion)
    menu_seleccion.funcion_botones = lambda _ : click_botones_seleccion(_)
    # menu_seleccion.funcion_botones = click_botones_seleccion()

    # Objeto galeria
    galeria.cargar_imagenes( imagenes_galeria )
    galeria.estilo(galeria_estilo_defecto)
    galeria.eventos(click = click_imagen_galeria)

    # Objeto etiquetador
    # filas_etiquetas.leer_dataset(archivo_dataset)
    # filas_etiquetas.leer_etiquetas(rutas_imagen[0])
    dataset = Etiquetas(archivo_dataset) 
    etiquetador_botones.leer_dataset( dataset )
    etiquetador_botones.leer_etiquetas(imagenes_etiquetadas[0])
    etiquetador_botones.update() 


    # galeria.ancho =1200

    menu_seleccion.alto  = 800
    menu_seleccion.ancho = 600

    etiquetador_botones.alto  = 800
    etiquetador_botones.ancho = 500

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = 1200
    pagina.window_height = 1000
    pagina.window_maximizable=True
    pagina.window_minimizable=True
    pagina.window_maximized=False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)