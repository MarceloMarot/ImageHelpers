
import flet as ft
from functools import partial

# from componentes.contenedor import Contenedor ,crear_imagen
# from componentes.etiquetado import Columna_Etiquetas
# from componentes.procesar_etiquetas import Etiquetas 

from contenedor import Contenedor ,crear_imagen
from etiquetado import Columna_Etiquetas
from procesar_etiquetas import Etiquetas 
from buscar import buscar_imagenes
from galeria_imagenes import crear_galeria, estilo_galeria, imagenes_galeria, eventos_galeria



from copy import copy, deepcopy










def main(pagina: ft.Page):

    # GALERIA

    # Maquetado galería
    numero_imagenes = 16
    
    # componente galeria
    galeria = crear_galeria(numero_imagenes, True)
    # page.add(galeria)

    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
    )

    # ETIQUETADO

    

    # Procesado de archivos

    # Bsuqueda de las imagenes disponibles
    ruta_imagenes   = "D:\Proyectos_Programacion\cartoons"
    rutas_imagenes = []
    rutas_imagenes  = buscar_imagenes(ruta_imagenes)
    numero_imagenes = len(rutas_imagenes)

    archivo_dataset = "../demo_etiquetas.txt"

    # dataset con todos los tags
    etiquetas_dataset = Etiquetas(archivo_dataset)
    # Lista de etiquetas para las imagenes
    etiquetas_imagen = []
    for ruta in  rutas_imagenes:
        etiquetas_imagen.append(Etiquetas(ruta))

    # por defecto: menu etiquetado de primera imagen
    # etiquetas_seleccion = etiquetas_imagen[0]      

    # etiquetas_seleccion = Etiquetas("")
    etiquetas_seleccion = deepcopy( etiquetas_imagen[0] )

    ## Aglutinado columnas
    columna_etiquetado = Columna_Etiquetas( etiquetas_dataset = etiquetas_dataset,  etiquetas_imagen = etiquetas_seleccion)




    # componente galeria
    # cuadro_seleccion = crear_galeria(1, False)
    cuadro_seleccion = Contenedor()   
    # page.add(galeria)


    # pestaña de etiquetado y navegacion de imagenes
    etiquetado_navegacion=ft.Row(
        controls = [columna_etiquetado, cuadro_seleccion]
        ) 

    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=etiquetado_navegacion,
    )


    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            tab_galeria   ,
            tab_etiquetado,
        ],
        expand=1,
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)


    # Eventos galeria
    def click_imagen_galeria(cont):
        #cambio de pestaña
        pestanias.selected_index=1
        id = cont.getID()
        # actualizacion de imagen seleccionada 
        imagen_seleccion = crear_imagen(rutas_imagenes[id], base_seleccion, altura_seleccion)
        cuadro_seleccion.setContenido(imagen_seleccion)
        # actualizacion etiquetas seleccionadas
        etiquetas_seleccion = etiquetas_imagen[id]
        etiquetas_seleccion.leer()
        # columna_etiquetado.update()
        print("orden:" , id)
        print(etiquetas_seleccion.ruta)
        print(etiquetas_seleccion.tags)

        pagina.update()


    color_defecto  = ft.colors.AMBER
    base_defecto   = 256
    altura_defecto = 256


    estilo_galeria(galeria,color=ft.colors.AMBER,base=base_defecto, altura=altura_defecto)
    imagenes_galeria(galeria, rutas_imagenes, base=base_defecto, altura=altura_defecto)
    eventos_galeria(galeria, funcclick=click_imagen_galeria)


    def click_imagen_seleccion():
        pestanias.selected_index=0
        pagina.update()


    base_seleccion   = 512
    altura_seleccion = 512

    # imagen_seleccion = galeria.controls[0].getContenido
    imagen_seleccion = crear_imagen(rutas_imagenes[0],base_seleccion,altura_seleccion)
    cuadro_seleccion.setContenido(imagen_seleccion)

    cuadro_seleccion.setBGColor(color_defecto)
    cuadro_seleccion.setDimensiones(base_seleccion, altura_seleccion)
    cuadro_seleccion.setClick(click_imagen_seleccion)
        

    # Propiedades pagina 
    pagina.title = "Asistente Etiquetado"
    # pagina.window_width=450
    pagina.window_height = 1000
    pagina.window_maximizable=True
    pagina.window_minimizable=True
    pagina.window_maximized=False
    pagina.update()
    



ft.app(target=main)