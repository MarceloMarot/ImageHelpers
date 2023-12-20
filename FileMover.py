from flet_core import container
# from clasificar_archivos import clasificar_archivos

from sistema_archivos.clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara
from sistema_archivos.mover_archivos import Mover_Archivo
from sistema_archivos.listar_extensiones import listar_extensiones


# from sistema_archivos import clasificar_archivos 
# from sistema_archivos  import mover_archivos 
# from sistema_archivos import listar_extensiones 




import flet as ft
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextAlign,
    alignment,
    border,
    icons,
    TextField,
    padding
)
from flet_core.utils import string


# from rich import print
import time


# lista de extensiones habituales
extensiones_predeterminadas = [
    ".txt",
    ".pdf",
    ".jpg",
    ".jpeg",
    ".webp",
    ".png",
    ".gif",
    ".mp3",
    ".flac",
    ".mp4",
    ".avi",
]




def main(page: Page):

    ############### DIMENSIONES DISEÑO ####################


    # dimensiones de referencia para el diseño de la app
    ancho_filas = 450
    altura_reportes = 400
    altura_columnas = altura_reportes + 250


    ################# FUNCIONES ############################

    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: FilePickerResultEvent):
        # directory_path.value = e.path if e.path else "Cancelled!"
        if e.path:
            ruta_directorio_origen.value = e.path 
            ruta_directorio_origen.update()
            # habilitar otros botones de ser necesario
            habilitar_controles()
        else:
            return


    def estadisticas_extension(e):

        # Mensaje de notificacion inicial
        texto= f'''
        Búsqueda de archivos

        ( En progreso )

        .......
        '''
        reporte_origen.value=texto
        reporte_origen.update()


        inicio  = time.time()
        # global archivos_origen

        ruta    = str(ruta_directorio_origen.value) 
        ext     = "*" + str(extensiones.value) 

        archivos_origen , ilegibles = clasificar_archivos( ruta,  ext ,patron)
        # archivos_origen , ilegibles = clasificar_archivos(ruta_entrada,extension,patron)
        espacio_archivos_origen  = 0
        # Lectura despacio en disco (en MB)
        for archivo in archivos_origen : 
            espacio_archivos_origen  += archivo.peso

        espacio_archivos_origen  = f"{espacio_archivos_origen /(1024**2) :.4}" #peso en MB, 4 digitos
        numero_archivos_origen  = len(archivos_origen )
        archivos_origen_ilegibles = len(ilegibles)

        fin  = time.time()

        texto= f'''
        ¡Búsqueda de archivos terminada! 

        Directorio:             {ruta_directorio_origen.value}  
        Extension :             {extensiones.value}  
        Patrón de nombre:       (ninguno)

        Numero de archivos:             {numero_archivos_origen } 
        Peso total de archivos:         {espacio_archivos_origen } MB 

        Numero de archivos ilegibles:   {archivos_origen_ilegibles} 






        Tiempo de búsqueda:         {(fin-inicio):.3} segundos 
        '''

        # muestra de resultados
        reporte_origen.value=texto
        reporte_origen.update()

        # habilitacion del boton "Mover"
        if len(archivos_origen) > 0 :
            boton_carpeta_destino.disabled = False
            boton_carpeta_destino.update()

        # habilitacion del boton de busqueda de extensiones
        boton_busqueda_extensiones.disabled = False
        boton_busqueda_extensiones.update()
        # page.update()


    def resultado_directorio_destino(e: FilePickerResultEvent):
        # directory_path.value = e.path if e.path else "Cancelled!"
        if e.path:
            ruta_directorio_destino.value = e.path
            ruta_directorio_destino.update()
            # habilitar otros botones de ser necesario
            habilitar_controles()
        else:
            return


    def mover_archivos(e):

        # Mensaje de notificacion inicial
        texto= f'''
        Movimiento de archivos

        ( En progreso )

        .......
        '''
        reporte_destino.value=texto
        reporte_destino.update()


        inicio  = time.time()

                
        fechar_anio = bool(checkbox_anio.value)
        fechar_mes  = bool(checkbox_mes.value)

        movidos = 0
        repetidos = 0

        ruta    = str(ruta_directorio_origen.value) 
        ext     = "*" + str(extensiones.value) 

        # se repite la búsqueda de archivos
        archivos_origen , ilegibles = clasificar_archivos(ruta , ext, patron)

        total = len(archivos_origen)
   
        for archivo in archivos_origen:
            retorno = Mover_Archivo(archivo, str(ruta_directorio_destino.value), fechar_anio, fechar_mes)
            if retorno:
                movidos += 1
            else:
                repetidos += 1

        fin   = time.time()

        texto = f'''
            ¡Ordenado de archivos terminado! 

            Directorio origen :   {ruta_directorio_origen.value } 
            Directorio destino:   {ruta_directorio_destino.value} 

            Extension :           {extensiones.value} 

            Archivos movidos   : {movidos} de {total} 
            Archivos repetidos : {repetidos} de {total} 







            Tiempo de rutina:     {(fin-inicio):.3} segundos 
        '''
        reporte_destino.value = texto
        reporte_destino.update()
        # page.update()

    def buscar_extensiones_directorio(e):

        # Mensaje de notificacion inicial
        texto= f'''
        Búsqueda de extensiones

        ( En progreso )

        .......
        '''
        reporte_origen.value=texto
        reporte_origen.update()

        inicio  = time.time()

        # se buscan todas las extensiones de archivo del directorio
        ruta = ruta_directorio_origen.value
        lista_extensiones = [] 
        lista_extensiones = listar_extensiones(ruta, False)

        # Borra TODAS las extensiones de la lista desplegable
        extensiones.options.clear()

        # añadido a la lista desplegable 
        for extension in lista_extensiones:
            nuevo = ft.dropdown.Option(extension)
            extensiones.options.append(nuevo)

        numero_extensiones = len(lista_extensiones)
        fin = time.time()

        texto= f'''
            ¡Búsqueda  de extensiones terminada!  

            Directorio:           {ruta_directorio_origen.value} 

            Numero de extensiones encontradas:    {numero_extensiones } 






            Tiempo de búsqueda:         {(fin-inicio):.3} segundos 
        '''

        # muestra de resultados
        reporte_origen.value=texto
        reporte_origen.update()

        # actualizacion grafica
        extensiones.update()
        # page.update()


    def agregar_opciones(lista_opciones: list ):
        opciones = []
        for opcion in lista_opciones:
            opciones.append(ft.dropdown.Option(opcion))
        return opciones


    def restablecer_opciones(e):
        # Borra TODAS las extensiones de la lista desplegable
        extensiones.options.clear()

        # añadido a la lista desplegable 
        for extension in extensiones_predeterminadas:
            nuevo = ft.dropdown.Option(extension)
            extensiones.options.append(nuevo)

        texto= f'''
            Lista de extensiones restablecida 
        '''

        # muestra de resultados
        reporte_origen.value=texto
        reporte_origen.update()

        # extensiones.options = agregar_opciones(extensiones_predeterminadas),
        extensiones.update()
        # page.update()


    def habilitar_controles():

        if ruta_directorio_origen.value != "":
            boton_busqueda_extensiones.disabled = False
        else: 
            boton_busqueda_extensiones.disabled = True

        if (ruta_directorio_origen.value != "") and (extensiones.value != None ):
            boton_busqueda_archivos.disabled = False
        else: 
            boton_busqueda_archivos.disabled = True

        if ((ruta_directorio_origen.value != "") and (ruta_directorio_destino.value != "")) and (extensiones.value != None ):
            boton_mover_archivos.disabled = False
        else:
            boton_mover_archivos.disabled = True

        boton_busqueda_extensiones.update()
        boton_busqueda_archivos.update()
        boton_mover_archivos.update()
        page.update()

    def cambio_opcion(e):
        habilitar_controles()
        extensiones.update()
        # page.update()


    ####################### COMPONENTES  GRAFICOS ##############################3

    #patron REGEX para filtrar archivos
    patron = None

    # Clase para manejar dialogos de archivo
    dialogo_directorio_origen   = FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino  = FilePicker(on_result = resultado_directorio_destino )

    # Cajas de texto
    ruta_directorio_origen  = Text(
        value="", 
        weight=ft.FontWeight.BOLD
        )

    ruta_directorio_destino = Text(
        value="", 
        weight=ft.FontWeight.BOLD
        ) 

    reporte_origen = Text(
        value="", 
        height=altura_reportes, 
        width=ancho_filas, 
        weight=ft.FontWeight.BOLD,
        text_align=TextAlign.START,
        )

    reporte_destino = Text(
        value="", 
        height=altura_reportes, 
        width=ancho_filas, 
        weight=ft.FontWeight.BOLD,
        text_align=TextAlign.START,
        )

    # Lista desplegable ('dropdown')

    extensiones = ft.Dropdown(
        height = 50,
        width = 100,
        options = agregar_opciones(extensiones_predeterminadas),
        on_change = cambio_opcion
    )

    # Botones

    boton_carpeta_origen = ft.ElevatedButton(
        text="Carpeta Origen",
        icon=icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_origen.get_directory_path(),
        disabled=page.web,       # deshabiliado en modo pagina web
        height = 50,
        width  = 200,
        bgcolor = ft.colors.BLUE_900,
        color = ft.colors.WHITE,

        # icon_color=ft.colors.GREEN_800
    )

    boton_carpeta_destino = ft.ElevatedButton(
        text="Carpeta Destino",
        icon=icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_destino.get_directory_path(),
        disabled=page.web,       # deshabiliado en modo pagina web
        height = 50,
        width  = 200,
        bgcolor = ft.colors.GREEN_900,
        color = ft.colors.WHITE,
    )

    boton_busqueda_extensiones = ft.ElevatedButton(
    # boton_busqueda_extensiones = ft.IconButton(
        text="Buscar Extensiones",
        icon=icons.SEARCH  ,
        ## manejador: leer sólo directorios
        on_click= buscar_extensiones_directorio,
        disabled=True, # deshabilitado (hasta definir directorio origen)     
        height = 50,
        width  = 150,
        bgcolor = ft.colors.AMBER_800,
        color = ft.colors.WHITE,
    )

    boton_busqueda_archivos = ft.ElevatedButton(
        text="Buscar Archivos",
        icon=icons.SEARCH  ,
        ## manejador: leer sólo directorios
        on_click= estadisticas_extension,
        disabled=True, # deshabilitado (hasta definir directorio origen)     
        height = 50,
        width  = 200,
        bgcolor = ft.colors.GREEN_800,
        color = ft.colors.WHITE,
    )


    boton_restablecer_extensiones = ft.ElevatedButton(
    # boton_restablecer_extensiones = ft.IconButton(
        text="Restablecer Extensiones",
        icon=icons.RESTORE ,
        on_click=restablecer_opciones,
        disabled=False,       
        height = 50,
        width  = 150,
        bgcolor = ft.colors.AMBER_800,
        color = ft.colors.WHITE,
    )

    boton_mover_archivos= ft.ElevatedButton(
        text="Mover Archivos",
        icon=icons.SAVE ,
        on_click = mover_archivos ,
        disabled = True, # deshabilitado (hasta completar campos requeridos)     
        height = 50,
        width  = 200,
        bgcolor = ft.colors.RED_800,
        color = ft.colors.WHITE,
    )


    # contenedores

    contenedor_apertura = ft.Container(
                margin=10,
                padding=10,
                width   = ancho_filas,
                height  = altura_columnas,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREEN_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                border = ft.border.all(5, ft.colors.INDIGO_200),

            )

    contenedor_destino = ft.Container(
                margin=10,
                padding=10,
                width   = ancho_filas,
                height  = altura_columnas,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                border = ft.border.all(5, ft.colors.INDIGO_200),

            )


    contenedor_reporte_origen = ft.Container(
                content= reporte_origen,
                # margin=10,
                # padding=10,
                width   = ancho_filas - 30,
                height  = altura_reportes - 30,
                alignment=ft.alignment.center,
                # bgcolor=ft.colors.AMBER_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                border = ft.border.all(5, ft.colors.INDIGO_200),
            )

    contenedor_reporte_destino = ft.Container(
                content= reporte_destino,
                # margin=10,
                # padding=10,
                width   = ancho_filas - 30,
                height  = altura_reportes - 30,
                alignment=ft.alignment.center,
                # bgcolor=ft.colors.AMBER_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                # border = ft.border.all(10, ft.colors.PURPLE_200),
                border = ft.border.all(5, ft.colors.INDIGO_200),
            )


    # checkboxes 

    checkbox_anio = ft.Checkbox(label="Ordenar por año", value=True  )
    checkbox_mes  = ft.Checkbox(label="Ordenar por mes", value=False )


    # filas y columnas

    lista_filas_apertura = [
        Row(
            controls = [ boton_carpeta_origen, ruta_directorio_origen ],
            expand = False,
            width = ancho_filas, 
            height = boton_carpeta_origen.height,
            alignment= ft.MainAxisAlignment.CENTER
            ),
        Row(
            controls = [boton_busqueda_extensiones,  extensiones ,boton_restablecer_extensiones],
            expand = False,
            width = ancho_filas, 
            height= extensiones.height,
            alignment= ft.MainAxisAlignment.CENTER,  
            ),
        Row(
            controls = [ boton_busqueda_archivos],
            expand = False,
            width = ancho_filas, 
            height= boton_busqueda_archivos.height,
            alignment= ft.MainAxisAlignment.CENTER, 
            ),
        Row(
            [ contenedor_reporte_origen ],
            expand = False,
            width = ancho_filas, 
            height = reporte_origen.height,
            alignment= ft.MainAxisAlignment.CENTER, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
    ]

    lista_filas_destino = [
        Row( 
            controls = [ boton_carpeta_destino, ruta_directorio_destino ],       
            expand=True,
            width = ancho_filas,
            alignment= ft.MainAxisAlignment.CENTER, 
            ),
        Row(
            controls = [ checkbox_anio, checkbox_mes ],
            expand=True,
            width = ancho_filas,
            alignment= ft.MainAxisAlignment.CENTER, 
            ),

        Row(
            controls = [ boton_mover_archivos ],
            expand=True,
            width = ancho_filas,
            alignment= ft.MainAxisAlignment.CENTER, 
            ),
        Row(
            [ contenedor_reporte_destino ],
            expand = False,
            width = ancho_filas, 
            height = reporte_destino.height,
            alignment= ft.MainAxisAlignment.CENTER, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]


    columna_apertura= ft.Column(
        controls = lista_filas_apertura,

        expand = True,
        # expand = False, 
        # run_spacing=1,     # espaciado vertical entre filas
        # wrap=False,
        spacing=30, 
        height = altura_columnas,
        width  = ancho_filas,
        # scroll=ft.ScrollMode.AUTO,
    )

    columna_destino = ft.Column(
  
        controls = lista_filas_destino,
        expand = True,
        # expand = False, 
        # run_spacing=1,     # espaciado vertical entre filas
        # wrap=False,
        spacing=30,       
        height = altura_columnas,
        width  = ancho_filas,
        # scroll=ft.ScrollMode.AUTO,
    )

    fila_final = ft.Row(
        controls = [contenedor_apertura, contenedor_destino],
        )



    # Añadido de diálogos a la página
    page.overlay.extend([
        dialogo_directorio_origen,
        dialogo_directorio_destino
        ])


    # agrupado y añadido  de los componentes a la página de la app
    contenedor_apertura.content = columna_apertura
    contenedor_destino.content = columna_destino

    page.add(fila_final)


    ##################### MENSAJES DE INICIO ###########################

    texto= f'''
                            Búsqueda de Archivos  

        Instrucciones:

        Seleccionar archivos:
         - Elige una carpeta para explorar;
         - Selecciona de la lista desplegable la extensión deseada;
         - Pulsa en el botón "Buscar Archivos".

        Buscar extensiones de archivo: 
         - Elige una carpeta para explorar;
         - Pulsa en el botón "Buscar Extensiones".

        Reestablecer extensiones:
         - Pulsa en el botón "Reestablecer Extensiones".
    '''

    # muestra de resultados
    reporte_origen.value=texto
    reporte_origen.update()


    texto= f'''
                        Movimiento y Ordenado de Archivos  

        Instrucciones:

         - Elige una carpeta de origen para explorar;
         - Selecciona una extensión de la lista desplegable;
         - (Opcional) elecciona un patrón de la lista desplegable;
                        (NO DISPONIBLE AUN)
        - Elige una carpeta de destino para guardar los archivos;
        - (Opcional) marca / desmarca las opciones de ordenado por año y mes del archivo;
        - Pulsa en el botón "Mover Archivos"
    '''

    # muestra de resultados
    reporte_destino.value=texto
    reporte_destino.update()


    ################# DIMENSIONES DE VENTANA ###########################
    ancho_pagina = 980
    # tema_pagina(page)
    # Propiedades pagina 
    page.title = "Ventana Etiquetado Imágenes"
    page.window_width       = ancho_pagina
    page.window_max_width   = ancho_pagina
    page.window_min_width   = ancho_pagina
    page.window_height = altura_columnas + 50
    page.window_maximizable=False
    page.window_minimizable=False
    page.window_maximized=False
    page.scroll = ft.ScrollMode.AUTO
    page.update()


################## EJECUCION ###################

ft.app(target=main)



