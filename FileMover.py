from flet_core import container
# from clasificar_archivos import clasificar_archivos

from clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara
from mover_archivos import Mover_Archivo

from listar_extensiones import listar_extensiones

import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    alignment,
    border,
    icons,
    TextField
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




    def estadisticas_extension():

        inicio  = time.time()
        # global archivos_origen

        archivos_origen , ilegibles = clasificar_archivos( ruta_directorio_origen.value, str(extensiones.value) ,patron)
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
        \nDirectorio:           {ruta_directorio_origen.value} 
        \nExtension :           {extensiones.value} 
        \nFiltrado de archivos terminado
        \nTiempo de rutina:         {(fin-inicio):.3} segundos
        \nNumero de archivos:       {numero_archivos_origen }
        \nPeso total de archivos:   {espacio_archivos_origen } MB
        \nArchivos ilegibles:       {archivos_origen_ilegibles}
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

        # else:
        #     return



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
        # directory_path.value = e.path if e.path else "Cancelled!"
        # if e.path:
        # ruta_directorio_destino.value = e.path
        # ruta_directorio_destino.update()

        inicio  = time.time()

        # archivos_origen = clasificar_archivos(ruta_origen, extension)
        # archivos_origen, _ = clasificar_archivos(ruta_origen, extension,patron)
                
        # archivos_origen
        fechar_anio = bool(checkbox_anio.value)
        fechar_mes  = bool(checkbox_mes.value)

        movidos = 0
        repetidos = 0

        ruta    = str(ruta_directorio_origen.value) 
        ext     = "*" + str(extensiones.value) 

        # global archivos_origen
        # archivos_origen , ilegibles = clasificar_archivos( "/home/x/imag", "webp" ,patron)
        archivos_origen , ilegibles = clasificar_archivos(ruta , ext, patron)
        # print(archivos_origen)

        total = len(archivos_origen)
   
        for archivo in archivos_origen:
            retorno = Mover_Archivo(archivo, str(ruta_directorio_destino.value), fechar_anio, fechar_mes)
            if retorno:
                movidos += 1
            else:
                repetidos += 1

        fin   = time.time()
        texto = f'''
        \nDirectorio origen :   {ruta_directorio_origen.value } 
        \nDirectorio destino:   {ruta_directorio_destino.value} 
        \nExtension :           {extensiones.value} 
        \nOrdenado de archivos terminado
        \nTiempo de rutina:         {(fin-inicio):.3} segundos
        \nArchivos movidos   : {movidos} de {total}
        \nArchivos repetidos : {repetidos} de {total}
        '''
        reporte_destino.value = texto
        reporte_destino.update()

        # boton_carpeta_destino.disabled = True
        # boton_carpeta_destino.update()

        # else: 
        #     return

    def buscar_extensiones_directorio(e):
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

        extensiones.update()


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

        # extensiones.options = agregar_opciones(extensiones_predeterminadas),
        extensiones.update()



    def habilitar_controles():


        if ruta_directorio_origen.value != "":
            boton_busqueda_extensiones.disabled = False
        else: 
            boton_busqueda_extensiones.disabled = True

        if ((ruta_directorio_origen.value != "") and (ruta_directorio_destino.value != "")) and (extensiones.value != None ):
            boton_mover_archivos.disabled = False
        else:
            boton_mover_archivos.disabled = True

        boton_busqueda_extensiones.update()
        boton_mover_archivos.update()


    def cambio_opcion(e):
        habilitar_controles()
        extensiones.update()






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
        height=300, 
        width=600, 
        # bgcolor=ft.colors.AMBER_100, 
        weight=ft.FontWeight.BOLD,
        # weight=ft.FontWeight.W_200,
        )

    reporte_destino = Text(
        value="", 
        height=300, 
        width=600, 
        # bgcolor=ft.colors.AMBER_100, 
        weight=ft.FontWeight.BOLD,
        # weight=ft.FontWeight.W_200,
        )



        








    # Lista desplegable ('dropdown')

    extensiones = ft.Dropdown(
        width = 200,
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
        text="Buscar Extensiones",
        icon=icons.SEARCH  ,
        ## manejador: leer sólo directorios
        on_click= buscar_extensiones_directorio,
        disabled=True, # deshabilitado (hasta definir directorio origen)     
        height = 50,
        width  = 200,
        bgcolor = ft.colors.AMBER_800,
        color = ft.colors.WHITE,
    )

    boton_restablecer_extensiones = ft.ElevatedButton(
        text="Restablecer Extensiones",
        icon=icons.RESTORE ,
        on_click=restablecer_opciones,
        disabled=False,       
        height = 50,
        width  = 200,
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



    # campo_extension = TextField(
    #     value="jpg",
    #     width=100,
    #     height=40, 
    #     # text_align=ft.TextAlign.LEFT,
    #     autofocus=True ,
    #     border_color=ft.colors.GREY_400
    #     )



    contenedor_apertura = ft.Container(
                margin=10,
                padding=10,
                width   = 576,
                height  = 500,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREEN_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                col={"md": 6}
            )

    contenedor_destino = ft.Container(
                margin=10,
                padding=10,
                width   = 576,
                height  = 500,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                col={"md": 6}
            )


    checkbox_anio = ft.Checkbox(label="Ordenar por año", value=True  )
    checkbox_mes  = ft.Checkbox(label="Ordenar por mes", value=False )


    columna_apertura = ft.Column([
        Row(
            [   
                boton_carpeta_origen,
                ruta_directorio_origen,
            ]
        ),
        Row(
            [   
                Text("Extensión"),
                # campo_extension
                extensiones,
                # boton_restablecer_extensiones,
                # boton_busqueda_extensiones
            ]
        ),
        Row(
            [   
                boton_restablecer_extensiones,
                boton_busqueda_extensiones
            ]
        ),
        Row(
            [
                reporte_origen
            ]
        )
    ])

    contenedor_apertura.content=columna_apertura

    columna_destino= ft.Column([
        Row(
            [   
                boton_carpeta_destino,
                ruta_directorio_destino,
            ],
            # expand=True
        ),
        Row(
            [   
                checkbox_anio,
                checkbox_mes
            ]
        ),
        Row(
            [
                reporte_destino
            ]
        )
    ])

    contenedor_destino.content = columna_destino

    fila_completa=ft.ResponsiveRow(
        
        controls= [contenedor_apertura, contenedor_destino],
        run_spacing={"xs": 10},
    )







    # Añadido de diálogos a la página
    page.overlay.extend([
        dialogo_directorio_origen,
        dialogo_directorio_destino
        ])


    page.add(
        fila_completa
    )
    # page.add(boton_busqueda_extensiones)
    # page.add(boton_restablecer_extensiones)
    page.add(boton_mover_archivos)
    # print(extensiones.value)



ft.app(target=main)



