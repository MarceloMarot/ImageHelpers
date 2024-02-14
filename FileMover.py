
from sistema_archivos.clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara
from sistema_archivos.mover_archivos import Mover_Archivo
from sistema_archivos.listar_extensiones import listar_extensiones

import i18n 
import flet as ft
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


def main(page: ft.Page):

    ############## COFIGURACION  TRADUCCIONES ############# 

    # directorio con traducciones
    i18n.load_path.append('local/')
    # opciones de idioma
    i18n.set('locale', 'es')   # eleccion: español
    # i18n.set('locale', 'en')   # eleccion: inglés
    i18n.set('fallback', 'en')  # alternativa: inglés 

    ############### DIMENSIONES DISEÑO ####################


    # dimensiones de referencia para el diseño de la app
    ancho_filas = 500
    altura_columnas =  800


    ################# FUNCIONES ############################

    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):
        # print(e.control)
        print(e.path)
        if e.path:
            ruta_directorio_origen.value = e.path 
            ruta_directorio_origen.update()
            # habilitar otros botones de ser necesario
            habilitar_controles()
        else:
            return


    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        if e.path:
            ruta_directorio_destino.value = e.path
            ruta_directorio_destino.update()
            # habilitar otros botones de ser necesario
            habilitar_controles()
        else:
            return


    def buscar_archivos_extension(e):

        # Mensaje de notificacion inicial
        texto = i18n.t('filemover.search_progress_text')

        ruta    = str(ruta_directorio_origen.value) 
        ext     = "*" + str(extensiones.value) 

        reporte.value = f"Buscando archivos {ext}..."
        reporte.update()

        # indicador busqueda animada
        anillo_progreso.value = None
        anillo_progreso.color = ft.colors.GREEN_800
        anillo_progreso.update()

        inicio  = time.time()

        archivos_origen , ilegibles = clasificar_archivos( ruta,  ext ,patron)
        espacio_archivos_origen  = 0
        # Lectura despacio en disco (en MB)
        for archivo in archivos_origen : 
            espacio_archivos_origen  += archivo.peso

        espacio_archivos_origen  = f"{espacio_archivos_origen /(1024**2) :.4}" #peso en MB, 4 digitos
        numero_archivos_origen  = len(archivos_origen )
        archivos_origen_ilegibles = len(ilegibles)

        fin  = time.time()

        texto = i18n.t('filemover.search_finish_text',
            source_path = ruta_directorio_origen.value,
            extensions = extensiones.value,
            n_files = numero_archivos_origen,
            size = espacio_archivos_origen,
            n_no_readable = archivos_origen_ilegibles, 
            time = f'{(fin-inicio):.3}'
        )

        # habilitacion del boton "Mover"
        # if len(archivos_origen) > 0 :
        #     boton_carpeta_destino.disabled = False
        #     boton_carpeta_destino.update()

        # habilitacion del boton de busqueda de extensiones
        boton_busqueda_extensiones.disabled = False
        boton_busqueda_extensiones.update()
        # page.update()

        # indicador busqueda completada 
        anillo_progreso.value = 1
        anillo_progreso.update()

        # muestra de resultados
        reporte.value = f"""Extension {ext}
        Archivos encontrados : {numero_archivos_origen}
        Espacio en disco : {espacio_archivos_origen:.4} MB
        Archivos ilegibles : {archivos_origen_ilegibles}
        Tiempo busqueda : {fin-inicio:.5} segundos"""
        reporte.update()
 






    def buscar_extensiones_directorio(e):

        # Mensaje de notificacion inicial
        texto = i18n.t('filemover.ext_search_text')
        # reporte.value=texto
        # reporte.update()

        # indicador busqueda animado
        anillo_progreso.value = None
        anillo_progreso.color = ft.colors.AMBER_800
        anillo_progreso.update()
        reporte.value = "Buscando extensiones..."
        reporte.update()

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

        # mensaje resultados
        texto = i18n.t('filemover.ext_finish_text',
            path=ruta_directorio_origen.value,
            n_ext = numero_extensiones,
            time = f'{(fin-inicio):.3}'
            )

        # muestra de resultados
        # reporte.value=texto
        # reporte.update()

        # actualizacion grafica
        extensiones.update()
        # page.update()
        # indicador busqueda completada 
        anillo_progreso.value = 1
        anillo_progreso.update()
        # reporte.value = "Extensiones actualizadas"
        reporte.value = f""" Extensiones encontradas : {numero_extensiones}

        Lista extensiones actualizada

        Tiempo busqueda : {fin-inicio:.5} segundos"""
        reporte.update()



    def mover_archivos(e):

        # Mensaje de notificacion inicial
        texto = i18n.t('filemover.move_progress_text')
        # reporte_destino.value=texto
        # reporte_destino.update()


        # fechar_anio = bool(checkbox_anio.value)
        # fechar_mes  = bool(checkbox_mes.value)

        if grupo_radio.value == "1":
            fechar_anio = True
            fechar_mes  = False
        elif grupo_radio.value == "2":
            fechar_anio = True
            fechar_mes  = True
        else:
            fechar_anio = False
            fechar_mes  = False

        movidos = 0
        repetidos = 0

        ruta    = str(ruta_directorio_origen.value) 
        ext     = "*" + str(extensiones.value) 

        # indicador busqueda completada 
        anillo_progreso.value = None
        anillo_progreso.color = ft.colors.RED_800
        anillo_progreso.update()

        reporte.value = f"Moviendo archivos {ext}..."
        reporte.update()

        inicio  = time.time()

        # se repite la búsqueda de archivos
        archivos_origen , ilegibles = clasificar_archivos(ruta , ext, patron)

        total = len(archivos_origen)
   
        for archivo in archivos_origen:
            retorno = Mover_Archivo(archivo, str(ruta_directorio_destino.value), fechar_anio, fechar_mes)
            if retorno:
                movidos += 1
            else:
                repetidos += 1

        fin = time.time()


        texto = i18n.t('filemover.move_finish_text',
            source_path = ruta_directorio_origen.value ,
            target_path = ruta_directorio_destino.value,
            ext = extensiones.value,
            total = total,
            moved = movidos,
            repeated = repetidos,
            time = f'{(fin-inicio):.3}' 
        )
        # reporte_destino.value = texto
        # reporte_destino.update()
        # page.update()
        # indicador busqueda completada 
        anillo_progreso.value = 1
        anillo_progreso.update()
        # reporte.value = "Extensiones actualizadas"
        reporte.value = f"""Archivos {ext} movidos 
        Archivos totales: {total}
        Movidos: {movidos}
        Repetidos: {repetidos}
        Tiempo : {fin-inicio:.5} segundos"""
        reporte.update()


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

        texto = i18n.t('filemover.ext_reset_text')

        # muestra de resultados
        # indicador busqueda completada 
        anillo_progreso.value = 1
        anillo_progreso.color = ft.colors.GREY_300
        anillo_progreso.update()

        reporte.value = f"Lista extensiones reestablecidas"
        reporte.update()

        extensiones.update()


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
    dialogo_directorio_origen  = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino = ft.FilePicker(on_result = resultado_directorio_destino )

    # Lista desplegable ('dropdown')
    extensiones = ft.Dropdown(
        height = 60,
        width = 150,
        options = agregar_opciones(extensiones_predeterminadas),
        on_change = cambio_opcion
    )

    # Botones
    ancho_botones = 200
    altura_botones = 40

    boton_carpeta_origen = ft.ElevatedButton(
        # text="Carpeta Origen",
        text = i18n.t('filemover.source_dir_button') ,
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

        # icon_color=ft.colors.GREEN_800
    )

    boton_carpeta_destino = ft.ElevatedButton(
        # text="Carpeta Destino",
        text = i18n.t('filemover.target_dir_button'),
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

    boton_busqueda_extensiones = ft.ElevatedButton(
    # boton_busqueda_extensiones = ft.IconButton(
        # text="Buscar Extensiones",
        text = i18n.t('filemover.ext_search_button'), 
        icon=ft.icons.SEARCH  ,
        ## manejador: leer sólo directorios
        on_click= buscar_extensiones_directorio,
        disabled=True, # deshabilitado (hasta definir directorio origen)     
        height = altura_botones,
        width  = 150,
        bgcolor = ft.colors.AMBER_800,
        color = ft.colors.WHITE,
    )

    boton_busqueda_archivos = ft.ElevatedButton(
        # text="Buscar Archivos",
        text = i18n.t('filemover.file_search_button'), 
        icon=ft.icons.SEARCH  ,
        ## manejador: leer sólo directorios
        on_click= buscar_archivos_extension,
        disabled=True, # deshabilitado (hasta definir directorio origen)     
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.GREEN_800,
        color = ft.colors.WHITE,
    )


    boton_restablecer_extensiones = ft.ElevatedButton(
    # boton_restablecer_extensiones = ft.IconButton(
        # text="Restablecer Extensiones",,
        text = i18n.t('filemover.ext_reset_button'),
        icon=ft.icons.RESTORE ,
        on_click=restablecer_opciones,
        disabled=False,       
        height = altura_botones,
        width  = 150,
        bgcolor = ft.colors.AMBER_800,
        color = ft.colors.WHITE,
    )

    boton_mover_archivos = ft.ElevatedButton(
        # text="Mover Archivos",
        text=i18n.t('filemover.file_move_button'),
        icon=ft.icons.SAVE ,
        on_click = mover_archivos ,
        disabled = True, # deshabilitado (hasta completar campos requeridos)     
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.RED_800,
        color = ft.colors.WHITE,
    )

    # checkboxes 
    checkbox_anio = ft.Checkbox(
        label=i18n.t('filemover.check_year'), 
        value=True  
        )
    checkbox_mes  = ft.Checkbox(
        label=i18n.t('filemover.check_month'), 
        value=False 
        )

    grupo_radio = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="0", label="(No ordenar)"),
        ft.Radio(value="1", label=i18n.t('filemover.check_year')),
        ft.Radio(value="2", label=i18n.t('filemover.check_month'))
        ],
        width = ancho_filas
        ))

    # indicadores progreso
    dimensiones_anillo = 100
    anillo_progreso = ft.ProgressRing(
        width = dimensiones_anillo, 
        height = dimensiones_anillo, 
        stroke_width = 10 ,
        color=ft.colors.GREY_300,
        value = 1,          # valor inicial
        # value = None,          # tiempo indefinido
        )

    # Cajas de texto
    ruta_directorio_origen  = ft.Text(
        value="", 
        weight=ft.FontWeight.BOLD
        )

    ruta_directorio_destino = ft.Text(
        value="", 
        weight=ft.FontWeight.BOLD
        ) 

    reporte = ft.Text(
        value="", 
        height=100, 
        width= ancho_filas - dimensiones_anillo*1.5, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.START,
        )


    # texto_titulo = ft.Text(
    #     # value="Movedor de Archivos", 
    #     value = i18n.t('filemover.title_text'),
    #     size=30,
    #     height=50, 
    #     width=ancho_filas*2, 
    #     weight=ft.FontWeight.BOLD,
    #     text_align=ft.TextAlign.CENTER,
    #     )



    #################### MAQUETADO ######################3

    # filas y columnas

    lista_filas_apertura = [
        ft.Row(
            controls = [ boton_carpeta_origen, ruta_directorio_origen ],
            expand = False,
            width = ancho_filas, 
            height = boton_carpeta_origen.height,
            # alignment= ft.MainAxisAlignment.CENTER
            alignment= ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        # ft.Divider(),
        ft.Row( 
            controls = [ boton_carpeta_destino, ruta_directorio_destino ],       
            expand=False,
            width = ancho_filas,
            # alignment= ft.MainAxisAlignment.CENTER, 
            alignment= ft.MainAxisAlignment.START, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            controls = [boton_busqueda_extensiones,  extensiones ,boton_restablecer_extensiones],
            expand = False,
            width = ancho_filas, 
            height= extensiones.height,
            alignment= ft.MainAxisAlignment.CENTER,  
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            # controls = [ checkbox_anio, checkbox_mes ],
            controls = [ grupo_radio ],
            expand=False,
            width = ancho_filas,
            # alignment= ft.MainAxisAlignment.CENTER, 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            controls = [ boton_busqueda_archivos, boton_mover_archivos],
            expand = False,
            width = ancho_filas, 
            height= boton_busqueda_archivos.height,
            # alignment= ft.MainAxisAlignment.CENTER, 
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN, 
            # alignment= ft.MainAxisAlignment.SPACE_AROUND, 
            # alignment= ft.MainAxisAlignment.SPACE_EVENLY, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ft.Divider(),
        ft.Row(
            controls = [ anillo_progreso, reporte],
            expand = False,
            width = ancho_filas, 
            height= anillo_progreso.height,
            alignment= ft.MainAxisAlignment.CENTER, 
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        # ft.Divider(),
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

    # Añadido de diálogos a la página
    page.overlay.extend([
        dialogo_directorio_origen, dialogo_directorio_destino
        ])

    # page.add(texto_titulo)
    page.add(fila_final)


    ##################### MENSAJES DE INICIO ###########################

    texto = i18n.t('filemover.search_tutorial_text',
        search_dir = boton_carpeta_origen.text,
        search_files = boton_busqueda_archivos.text,
        search_ext = boton_busqueda_extensiones.text,
        reset_ext = boton_restablecer_extensiones.text    
    )

    # muestra de resultados
    # reporte.value=texto
    # reporte.update()

    texto = i18n.t('filemover.move_tutorial_text',
        search_dir = boton_carpeta_origen.text, 
        target_dir = boton_carpeta_destino.text,
        move_files = boton_mover_archivos.text    
    )

    # muestra de resultados
    # reporte_destino.value=texto
    # reporte_destino.update()


    ################# DIMENSIONES DE VENTANA ###########################
    ancho_pagina = 700
    # texto_titulo.width = ancho_pagina
    # tema_pagina(page)
    # Propiedades pagina 
    page.title = i18n.t('filemover.window_name')
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



