
# import i18n 
import flet as ft
import time
import cv2
import os 
import pathlib

from sistema_archivos.clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara
# from sistema_archivos.mover_archivos import Mover_Archivo
from sistema_archivos.listar_extensiones import listar_extensiones
from sistema_archivos.buscar_extension import buscar_extension, buscar_imagenes

from componentes.anillo_reporte import AnilloReporte



def convertir_imagen(ruta_origen: str, ruta_destino: str):
    guardado_exitoso = False

    if not cv2.haveImageReader(ruta_origen):
        return guardado_exitoso 

    if not cv2.haveImageWriter(ruta_destino):
        return guardado_exitoso

    img = cv2.imread(ruta_origen)

    #prevencion de sobreescritura
    if os.path.exists(ruta_destino):
        return False

    # if img != None:
    guardado_exitoso = cv2.imwrite(ruta_destino, img)
    del img
    return guardado_exitoso



# lista de extensiones habituales
extensiones_predeterminadas = [
    ".jpg",
    ".jpeg",
    ".webp",
    ".png",
    ".bmp",
    # ".gif",
]


def main(page: ft.Page):


    ############### DIMENSIONES DISEÑO ####################

    # dimensiones de referencia para el diseño de la app
    ancho_filas = 500
    altura_columnas =  800


    ################# FUNCIONES ############################

    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):

        ruta_directorio_origen.value = e.path 
        ruta_directorio_origen.update()

        anillo_reporte.valor_anillo = None
        anillo_reporte.color_anillo = ft.colors.AMBER_800
        anillo_reporte.texto_reporte(renglon3="Buscando extensiones...")
        anillo_reporte.update()

        inicio = time.time()

        extensiones_disponibles = listar_extensiones(e.path)
        extensiones_filtradas = []
        for extensiones in  extensiones_predeterminadas:
            if extensiones in extensiones_disponibles:
                extensiones_filtradas.append( extensiones )

        extensiones_entrada.options = agregar_opciones(extensiones_filtradas )
        extensiones_entrada.update()

        fin = time.time()

        numero_extensiones = len(extensiones_filtradas)

        anillo_reporte.valor_anillo = 1
        anillo_reporte.texto_reporte(
            f"Extensiones encontradas : {numero_extensiones}","",
            "Lista extensiones actualizada","",
            f"Tiempo busqueda : {fin-inicio:.5} segundos"
            )
        anillo_reporte.update()

        habilitar_controles()






    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        ruta_directorio_destino.value = e.path
        ruta_directorio_destino.update()

        habilitar_controles()

        anillo_reporte.valor_anillo = 1
        anillo_reporte.color_anillo = ft.colors.AMBER_800
        anillo_reporte.texto_reporte(renglon3="Directorio de destino elegido")
        anillo_reporte.update()


    def agregar_opciones(lista_opciones: list ):
        opciones = []
        for opcion in lista_opciones:
            opciones.append(ft.dropdown.Option(opcion))
        return opciones


    def convertir_imagenes(e):


        directorio_origen = str(ruta_directorio_origen.value)
        directorio_destino = str(ruta_directorio_destino.value)
        # extension entrada
        extension = str(extensiones_entrada.value)

        # Paso 1: busqueda de archivos
        anillo_reporte.valor_anillo = None
        anillo_reporte.color_anillo = ft.colors.AMBER_800
        anillo_reporte.texto_reporte(renglon3="Buscando imágenes...")
        anillo_reporte.update()

        inicio = time.time()
        lista_imagenes = buscar_extension(directorio_origen, "*"+extension)

        # Paso 2: conversion uno a uno de las imagenes
        anillo_reporte.valor_anillo = 0
        anillo_reporte.color_anillo = ft.colors.RED_800
        anillo_reporte.texto_reporte(
            renglon2= f"Convirtiendo imágenes..."
            )
        anillo_reporte.update()

        extension = str(extensiones_salida.value)
        total = len(lista_imagenes)
        convertidos = 0
        repetidos = 0

        i = 0
        for ruta_imagen in lista_imagenes:

            ruta_relativa = pathlib.Path(ruta_imagen).relative_to(directorio_origen)
            ruta_relativa = str(ruta_relativa) 
            ruta_destino = pathlib.Path(directorio_destino , ruta_relativa)
            subdirectorio = ruta_destino.parent
            ruta_destino = str(ruta_destino.with_suffix(extension))

            # se crea el subdirectorio si no existe
            subdirectorio.mkdir(parents=True,exist_ok=True)

            guardado = convertir_imagen(ruta_imagen, ruta_destino)
            if guardado==True:
                convertidos += 1
            else:
                repetidos += 1

            i += 1
            anillo_reporte.valor_anillo = i/total

            anillo_reporte.texto_reporte(
                renglon2 = f"Convirtiendo imágenes...",
                renglon4 = f"Imagen {i+1} de {total}"
                )
            anillo_reporte.update()


        fin = time.time()

        # indicador busqueda completada 
        anillo_reporte.valor_anillo = 1
        anillo_reporte.update()
        exti = str(extensiones_entrada.value)
        extf = str(extensiones_entrada.value)
        anillo_reporte.texto_reporte(
            f"Imagenes {exti} convertidas a {extf}",
            f"Imagenes totales: {total}",
            f"Convertidas: {convertidos}",
            f"Repetidas: {repetidos}",
            f"Tiempo : {fin-inicio:.5} segundos",
            )


    def cambio_opcion(e: ft.ControlEvent):

        habilitar_controles()

        extension = e.control.value

        anillo_reporte.valor_anillo = 1
        anillo_reporte.color_anillo = ft.colors.GREEN_800
        anillo_reporte.texto_reporte(renglon3=f"Extension {extension} elegida")
        anillo_reporte.update()


    def habilitar_controles():

        if extensiones_entrada.value == None or extensiones_salida.value == None :
            return
        if ruta_directorio_origen.value==None or  ruta_directorio_destino.value==None:
            return

        boton_convertir_archivos.disabled = False
        boton_convertir_archivos.update()


    ####################### COMPONENTES  GRAFICOS ##############################3

    # Clase para manejar dialogos de archivo
    dialogo_directorio_origen  = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino = ft.FilePicker(on_result = resultado_directorio_destino )

    # Lista desplegable ('dropdown')
    extensiones_entrada = ft.Dropdown(
        height = 60,
        width = 150,
        options = agregar_opciones(extensiones_predeterminadas),
        on_change = cambio_opcion
    )

    extensiones_salida = ft.Dropdown(
        height = 60,
        width = 150,
        options = agregar_opciones(extensiones_predeterminadas),
        on_change = cambio_opcion
    )

    # Botones
    ancho_botones = 200
    altura_botones = 40

    boton_carpeta_origen = ft.ElevatedButton(
        text="Carpeta Origen",
        # text = i18n.t('filemover.source_dir_button') ,
        icon=ft.icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_origen.get_directory_path(
            dialog_title="Elegir carpeta origen",
            # initial_directory=str(pathlib.Path.cwd())
            ),
        disabled=page.web,       # deshabiliado en modo pagina web
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.BLUE_900,
        color = ft.colors.WHITE,
    )

    boton_carpeta_destino = ft.ElevatedButton(
        text="Carpeta Destino",
        # text = "i18n.t('filemover.target_dir_button')",
        icon=ft.icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_destino.get_directory_path(
            dialog_title="Elegir carpeta destino",
            # initial_directory=str(pathlib.Path.cwd())            
            ),
        disabled=page.web,       # deshabiliado en modo pagina web
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.ORANGE_900,
        color = ft.colors.WHITE,
    )


    boton_convertir_archivos = ft.ElevatedButton(
        text="Convertir Imagenes",
        # text=i18n.t('filemover.file_move_button'),
        icon=ft.icons.SAVE ,
        on_click = convertir_imagenes ,
        disabled = True, # deshabilitado (hasta completar campos requeridos)     
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.RED_800,
        color = ft.colors.WHITE,
    )

    # Cajas de texto
    ruta_directorio_origen  = ft.Text(
        value=None, 
        weight=ft.FontWeight.BOLD
        )

    ruta_directorio_destino = ft.Text(
        value=None, 
        weight=ft.FontWeight.BOLD
        ) 
    # anillo y texto reporte
    anillo_reporte = AnilloReporte()
    # Añadido de diálogos a la página
    page.overlay.extend([
        dialogo_directorio_origen, dialogo_directorio_destino
        ])

    #################### MAQUETADO ######################3

    # filas y columnas
    lista_filas_apertura = [
        ft.Divider(),
        ft.Row(
            controls = [extensiones_entrada , boton_carpeta_origen, ruta_directorio_origen],
            expand = False,
            width = ancho_filas, 
            height = 60,
            alignment= ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row( 
            controls = [ extensiones_salida, boton_carpeta_destino, ruta_directorio_destino  ],       
            expand=False,
            width = ancho_filas,
            height=60,
            alignment= ft.MainAxisAlignment.START, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            controls = [boton_convertir_archivos],
            expand = False,
            width = ancho_filas, 
            height=60,
            alignment= ft.MainAxisAlignment.CENTER,  
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            controls = [ anillo_reporte],
            expand = False,
            width = ancho_filas, 
            height= anillo_reporte.height,
            alignment= ft.MainAxisAlignment.CENTER, 
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
    ]


    columna_apertura= ft.Column(
        controls = lista_filas_apertura,

        # expand = True,
        expand = False, 
        # run_spacing=1,     # espaciado vertical entre filas
        # wrap=False,
        spacing=30, 
        height = altura_columnas,
        width  = ancho_filas + 100,
        scroll=ft.ScrollMode.AUTO,
    )

    fila_final = ft.Row(
        controls = [columna_apertura],
        width = 1200,
        height = altura_columnas
        )

    # page.add(texto_titulo)
    page.add(fila_final)


    ################# DIMENSIONES DE VENTANA ###########################
    ancho_pagina = 700
    # texto_titulo.width = ancho_pagina
    # tema_pagina(page)
    # Propiedades pagina 
    page.title = "Conversor Imagenes"
    page.window_width       = ancho_pagina
    # page.window_max_width   = ancho_pagina
    page.window_min_width   = ancho_pagina
    page.window_height = altura_columnas + 100
    page.window_maximizable=False
    page.window_minimizable=False
    page.window_maximized=False
    page.scroll = ft.ScrollMode.AUTO
    page.update()


################## EJECUCION ###################

ft.app(target=main)