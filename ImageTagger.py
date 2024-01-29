
import flet as ft

# from componentes.contenedor import Contenedor ,Contenedor_Imagen, Estilo_Contenedor
# from componentes.etiquetado import Columna_Etiquetas
from componentes.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Imagen, Contenedor_Imagen, Estilo_Contenedor
from componentes.menu_navegacion import  MenuNavegacion

from sistema_archivos.buscar_extension import buscar_imagenes

from componentes.etiquetador_botones import FilasBotones, EtiquetadorBotones


# class Imagen_Etiquetada( Etiquetas, ft.Image):
class Imagen_Etiquetada( Etiquetas, Imagen):
    def __init__(self, ruta, ancho=768, alto=768, redondeo=0):
        Etiquetas.__init__(self, ruta)
        Imagen.__init__(self,ruta, ancho, alto, redondeo)
        # ft.Image.__init__(
        #     self,
        #     src   = ruta,
        #     width = 768,
        #     height = 768,
        #     fit=ft.ImageFit.CONTAIN,
        #     repeat=ft.ImageRepeat.NO_REPEAT,
        # )

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



    # Busqueda de las imagenes disponibles
    directorio   = "/home/x/Codigos/cartoons"
    rutas_imagen  = buscar_imagenes(directorio)

    # truncamiento de lista imagenes         FIX
    rutas_imagen = rutas_imagen[0:10]      # FIX

    # dataset con todos los tags
    archivo_dataset = "demo_etiquetas.txt"




    # objetos ft.Image con etiquetas leidas desde archivo TXT
    imagenes_etiquetadas = leer_imagenes_etiquetadas(
        rutas_imagen,
        ancho=768,
        alto=768, 
        redondeo=30
        )

    # por defecto: menu etiquetado de primera imagen
    # etiquetas_seleccion = etiquetas_imagen[0]
    ## Aglutinado columnas
    # columna_etiquetado = Columna_Etiquetas( )
    filas_etiquetas     = FilasBotones()
    etiquetador_botones = EtiquetadorBotones(filas_etiquetas)


    # componente galeria
    galeria = Galeria()

    galeria.cargar_imagenes(imagenes_etiquetadas)
    # galeria.crear_contenedores(numero_imagenes)
    galeria.estilo(galeria_estilo_defecto)
    # galeria.imagenes(rutas_imagen, redondeo=60)





    menu_seleccion = MenuNavegacion()

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
    )

    # pestaña de etiquetado y navegacion de imagenes
    etiquetado_navegacion=ft.Row(
        controls = [ 
            menu_seleccion ,
            ft.VerticalDivider(),
            etiquetador_botones
            ], 
        spacing = 100, 
        width   = 1000, 
        expand  = True
        ) 

    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=etiquetado_navegacion,
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

    menu_seleccion.estilo_contenedor = menu_estilo_defecto
    menu_seleccion.imagenes( imagenes_etiquetadas )
    menu_seleccion.estilo()
    menu_seleccion.cargar_imagen()

    def scroll_to_key(n):
        galeria.scroll_to(key=str(n), duration=1000)


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        #cambio de pestaña
        # print(e.control)
        # print(e.control.content)
        # print(e.control.content.key)
        contenedor = e.control
        key = contenedor.content.key
        # actualizacion de imagen seleccionada 
        menu_seleccion.indice = int(key)
        # menu_seleccion.cargar_imagen()
        # actualizacion del archivo de etiquetado
        # columna_etiquetado.setEtiquetas(etiquetas_imagen[id])
        # columna_etiquetado.actualizar()
        # print(key)

        # lectura de nombre archivo
        ruta = contenedor.content.src
        filas_etiquetas.leer_etiquetas(ruta)
        # actualizacion grafica
        pestanias.selected_index=1
        menu_seleccion.cargar_imagen()
        # menu_seleccion.update()
        pagina.update()

    galeria.eventos(click = click_imagen_galeria)


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        #regreso a la galeria
        # id = menu_seleccion.indice
        # key = menu_seleccion.indice
        contenedor_imagen = e.control
        key = contenedor_imagen.content.key
        # print(key)
        scroll_to_key( key)      
        #cambio de pestaña
        pestanias.selected_index=0
        galeria.update()
        pagina.update()


    menu_seleccion.eventos(click=click_imagen_seleccion)

    def click_botones_seleccion( indice: int ):
        """ Esta funcion controla el cambio de imagen en el selector"""
        # (el cambio de imagen está integrado al componente)
        # actualizacion etiquetas
        ruta = imagenes_etiquetadas[indice].src
        filas_etiquetas.leer_etiquetas(ruta)
        # actualizacion pagina
        tab_etiquetado.update()




    menu_seleccion.funcion_botones = lambda _ : click_botones_seleccion(_)



    # Etiquetado
    filas_etiquetas.leer_dataset(archivo_dataset)
    filas_etiquetas.leer_etiquetas(rutas_imagen[0])



    menu_seleccion.height  = 700
    menu_seleccion.expand = True
    filas_etiquetas.height = 700



    # filas_etiquetas.update()
    etiquetador_botones.update() 

    # Propiedades pagina 
    pagina.title = "Asistente Etiquetado"
    # pagina.window_width=450
    pagina.window_height = 1000
    pagina.window_maximizable=True
    pagina.window_minimizable=True
    pagina.window_maximized=False
    pagina.update()
    



ft.app(target=main)