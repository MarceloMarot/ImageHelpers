from flet_core import container
# from clasificar_archivos import clasificar_archivos

from clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara
from mover_archivos import Mover_Archivo

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






def main(page: Page):

    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: FilePickerResultEvent):
        # directory_path.value = e.path if e.path else "Cancelled!"
        if e.path:
            ruta_directorio_origen.value = e.path 
            ruta_directorio_origen.update()
            # ruta_directorio = e.path 

            inicio  = time.time()

            global archivos_origen
 
            archivos_origen , ilegibles = clasificar_archivos( e.path, "*."+ str(extensiones.value) ,patron)
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
            \nDirectorio:           {e.path} 
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

        else:
            return



    def resultado_directorio_destino(e: FilePickerResultEvent):
        # directory_path.value = e.path if e.path else "Cancelled!"
        if e.path:
            ruta_directorio_destino.value = e.path
            ruta_directorio_destino.update()


            inicio  = time.time()

            # archivos_origen = clasificar_archivos(ruta_origen, extension)
            # archivos_origen, _ = clasificar_archivos(ruta_origen, extension,patron)
                    
            # archivos_origen
            fechar_anio = bool(checkbox_anio.value)
            fechar_mes  = bool(checkbox_mes.value)

            movidos = 0
            repetidos = 0


            global archivos_origen
            
            total = len(archivos_origen)
            # if total == 0:
            #     boton_carpeta_destino.disabled = 

            for archivo in archivos_origen:
                retorno = Mover_Archivo(archivo, e.path, fechar_anio, fechar_mes)
                if retorno:
                    movidos += 1
                else:
                    repetidos += 1

            fin   = time.time()
            texto = f'''
            \nDirectorio:           {e.path} 
            \nExtension :           {extensiones.value} 
            \nOrdenado de archivos terminado
            \nTiempo de rutina:         {(fin-inicio):.3} segundos
            \nArchivos movidos   : {movidos} de {total}
            \nArchivos repetidos : {repetidos} de {total}
            '''
            reporte_destino.value = texto
            reporte_destino.update()

            boton_carpeta_destino.disabled = True
            boton_carpeta_destino.update()

        else: 
            return



    # archivos_origen = []

    #patron REGEX para filtrar archivos
    patron = None

    # Clase para manejar dialogos de archivo
    dialogo_directorio_origen   = FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino  = FilePicker(on_result = resultado_directorio_destino )
    # Caja de texto
    ruta_directorio_origen = Text()
    ruta_directorio_destino = Text() 
    # Añadido de diálogos a la página
    page.overlay.extend([
        dialogo_directorio_origen,
        dialogo_directorio_destino
        ])


    extensiones = ft.Dropdown(
        width = 200,
        options=[
            ft.dropdown.Option("jpg"),
            ft.dropdown.Option("jpeg"),
            ft.dropdown.Option("webp"),
            ft.dropdown.Option("png"),
            ft.dropdown.Option("gif"),
        ],
    )




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
        bgcolor = ft.colors.RED_900,
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


    contenedor_apertura = ft.Container(
                margin=10,
                padding=10,
                width   = 576,
                height  = 400,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREEN_100,
                border_radius=ft.border_radius.all(10) ,          # redondeo
                col={"md": 6}
            )

    contenedor_destino = ft.Container(
                margin=10,
                padding=10,
                width   = 576,
                height  = 400,
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
                extensiones
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
            ]
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



    page.add(
        fila_completa
    )

    # prevencion de envios erroneos
    boton_carpeta_destino.disabled = True
    boton_carpeta_destino.update()

    



ft.app(target=main)



