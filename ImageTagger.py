
import flet as ft

from componentes.contenedor import Contenedor ,Contenedor_Imagen, Estilo_Contenedor
from componentes.etiquetado import Columna_Etiquetas
from componentes.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria
from componentes.menu_navegacion import  MenuNavegacion

from sistema_archivos.buscar_extension import buscar_imagenes


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
    width = 768,
    height = 768,
    border_radius = 50, 
    # bgcolor = ft.colors.BLUE_400,
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )



def main(pagina: ft.Page):


    # Busqueda de las imagenes disponibles
    directorio   = "/home/x/Codigos/cartoons"
    rutas_imagen  = buscar_imagenes(directorio)
    numero_imagenes = len(rutas_imagen)

    archivo_dataset = "demo_etiquetas.txt"

    # dataset con todos los tags
    etiquetas_dataset = Etiquetas(archivo_dataset)
    # Lista de etiquetas para las imagenes
    etiquetas_imagen = []
    for ruta in  rutas_imagen:
        etiquetas_imagen.append(Etiquetas(ruta))


    # por defecto: menu etiquetado de primera imagen
    etiquetas_seleccion = etiquetas_imagen[0]
    ## Aglutinado columnas
    columna_etiquetado = Columna_Etiquetas( )


    # componente galeria
    galeria = Galeria()

    galeria.crear(numero_imagenes)
    galeria.estilo(galeria_estilo_defecto)
    galeria.imagenes(rutas_imagen, redondeo=60)

    menu_seleccion = MenuNavegacion()

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
    )

    # pestaña de etiquetado y navegacion de imagenes
    etiquetado_navegacion=ft.Row(
        controls = [columna_etiquetado, menu_seleccion ]
        # controls = [columna_etiquetado]
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
            tab_etiquetado,
        ],
        expand=1,
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)



    menu_seleccion.estilo_contenedor = menu_estilo_defecto
    menu_seleccion.imagenes( rutas_imagen )
    menu_seleccion.estilo()
    menu_seleccion.cargar_imagen()

    def scroll_to_key(n):
        galeria.scroll_to(key=str(n), duration=1000)


    # Eventos galeria
    def click_imagen_galeria(cont: Contenedor_Imagen, e):
        #cambio de pestaña
        pestanias.selected_index=1
        id = int(cont.content.key)
        # actualizacion de imagen seleccionada 
        menu_seleccion.indice = id
        menu_seleccion.cargar_imagen()
        # actualizacion del archivo de etiquetado
        columna_etiquetado.setEtiquetas(etiquetas_imagen[id])
        columna_etiquetado.actualizar()
        # actualizacion
        pagina.update()

    galeria.eventos(click = click_imagen_galeria)


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( _ , e):
        #regreso a la galeria
        id = menu_seleccion.indice
        scroll_to_key(id)      
        #cambio de pestaña
        pestanias.selected_index=0
        pagina.update()

    menu_seleccion.eventos(click=click_imagen_seleccion)

    # Funcion para el cambio de imagen seleccionada 
    def click_botones_seleccion( indice: int ):
        columna_etiquetado.setEtiquetas(etiquetas_imagen[indice])
        columna_etiquetado.actualizar()
        pagina.update()

    menu_seleccion.funcion_botones = lambda _ : click_botones_seleccion(_)



    # Etiquetado
    columna_etiquetado.setEtiquetas(etiquetas_seleccion,etiquetas_dataset)
    columna_etiquetado.update()



    # Propiedades pagina 
    pagina.title = "Asistente Etiquetado"
    # pagina.window_width=450
    pagina.window_height = 1000
    pagina.window_maximizable=True
    pagina.window_minimizable=True
    pagina.window_maximized=False
    pagina.update()
    



ft.app(target=main)