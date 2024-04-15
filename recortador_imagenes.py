

from rich import print as print
import flet as ft
from typing import TypeVar
import pathlib

# from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
from componentes.galeria_imagenes import ContImag, Galeria, Contenedor_Imagen, imagen_clave, imagen_nombre
from sistema_archivos.buscar_extension import buscar_imagenes
from componentes.estilos_contenedores import estilos_galeria, estilos_seleccion
from componentes.selector_recortes import ImagenTemporal, SelectorRecorte, DataRecorte
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones


def nada( e ):
    pass


class ContenedorRecortes( Contenedor_Imagen):
    def __init__(self, ruta, clave: str, ancho=768, alto=768, redondeo=0,):
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        # flags para el coloreo de bordes
        self.marcada = False
        self.guardada = False
        self.defectuosa = False
        # datos de la ventana emergente
        self.clave = clave 
        self.ruta_origen = ruta
        self.ruta_destino = "recorte.jpg"
        self.data_actual   = DataRecorte()
        self.data_marcado  = DataRecorte()
        self.data_guardado = DataRecorte()
        # archivo temporal con la imagen recortada
        self.recorte_imagen = None
        self.tooltip = "Click izquierdo para seleccionar esta imagen."


    def ruta_recorte(self, ruta_directorio: str):
        """Este metodo asigna una ruta de destino para el recorte dentro del directorio indicado"""
        directorio = pathlib.Path(ruta_directorio)
        nombre_archivo = pathlib.Path(self.ruta_imagen).name
        # composicion del archivo de salida
        ruta_recorte = pathlib.Path(directorio, nombre_archivo)
        # asignacion de ruta de salida
        self.ruta_destino = str(ruta_recorte)


# nuevos tipados para contenedor y sus subclases
ContRec = TypeVar('ContRec', bound=ContenedorRecortes)


class GaleriaRecortes( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.imagenes: list[ContenedorRecortes]


    # def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
    #     self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        
    #     contenedores = leer_imagenes_etiquetadas(rutas_imagen, ancho, alto, redondeo)
    #     self.numero = len(contenedores)
    #     self.controls = contenedores

    #     actualizar_estilo_estado( contenedores, self.estilos)


    def cargar_imagenes(self, 
        imagenes: list[ContRec ], 
        cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes

        self.actualizar_estilos( )  


    def ruta_recortes(self, ruta_directorio: str):

        for contenedor in self.controls:
            contenedor: ContenedorRecortes
            contenedor.ruta_recorte(ruta_directorio)    


    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    


def leer_imagenes_recortes(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        clave = f"imag_{i}"
        contenedor = ContenedorRecortes(rutas_imagen[i], clave, ancho, alto, redondeo)
        contenedor.clave = clave
        contenedores.append(contenedor)

    return contenedores


def cargar_imagenes_recortes(rutas: list[str]):
    # replica de imagenes para la galeria - menor resolucion
    galeria = []
    galeria = leer_imagenes_recortes(
        rutas,
        ancho=128,
        alto=128, 
        redondeo=10
        )
    return galeria


def actualizar_estilo_estado(
    contenedores: list[ContenedorRecortes], estilos : dict ):
    for contenedor in contenedores:
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.marcada :
            estilo = estilos["modificado"]
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        else: 
            estilo = estilos["predefinido"]

        contenedor.estilo( estilo )


# reasignacion de dimensiones para las imagenes de galeria
estilos_galeria["predefinido"]. width   = 128
estilos_galeria["predefinido"]. height  = 128
estilos_galeria["guardado"].    width   = 128
estilos_galeria["guardado"].    height  = 128
estilos_galeria["modificado"].  width   = 128
estilos_galeria["modificado"].  height  = 128
estilos_galeria["erroneo"].     width   = 128
estilos_galeria["erroneo"].     height  = 128


texto_ayuda = """Selector de recortes:
- Click derecho sobre la imagen ampliada para guardar el recorte marcado;
- Click izquierdo para marcado provisional (no se guarda);
- Deslizar la barra para ajustar el zoom.
Teclas rápidas:
- Home:  primera imagen;
- RePag | A: imagen anterior;
- AvPag | D: imagen siguiente;
- End:   última imagen;
- Flechas: cambia zoom
"""


clave_actual = None


def pagina_galeria(page: ft.Page):
    """Funcion gráfica para crear la galería de Flet"""

    ancho_pagina = 1500
    altura_pagina = 900

    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    ################## COMPONENTES ########################

    ancho_botones = 200
    altura_botones = 40

    # Botones apertura de ventana emergente
    boton_carpeta_origen = ft.ElevatedButton(
        text = "Carpeta capturas",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.BLUE_900,
        color= ft.colors.WHITE,
        height = altura_botones,
        width  = ancho_botones,
        ## manejador
        on_click=lambda _: dialogo_directorio_origen.get_directory_path(
            dialog_title="Elegir carpeta con las capturas de imagen"
        ),
        tooltip="Elegir carpeta con las capturas de imagen",
    )

    boton_carpeta_destino = ft.ElevatedButton(
        text = "Carpeta recortes",
        icon=ft.icons.FOLDER_OPEN,
        ## manejador: leer sólo directorios
        on_click=lambda _: dialogo_directorio_destino.get_directory_path(
            dialog_title="Elegir carpeta para los recortes creados",
            ),
        tooltip = "Elegir carpeta para los recortes creados",
        disabled = True,       
        height = altura_botones,
        width  = ancho_botones,
        bgcolor = ft.colors.RED_900,
        color = ft.colors.WHITE,
    )

    # lista desplegable para elegir opciones de imagen 
    lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones[1:], ancho=120)
    
    # textos
    texto_dimensiones = ft.Text("Dimensiones\nrecorte:", tooltip="512x512 por defecto")

    # texto_ayuda = ft.Text("Click derecho para guardar el recorte\nClick izquierdo para marcado provisional.")
    # texto_titulo = ft.Text("", expand=True, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, size =20)
    texto_zoom = ft.Text("Zoom:")


    ayuda_emergente = ft.Tooltip(
        message=texto_ayuda,
        content=ft.Text("Ayuda emergente",size=20, width=200),
        padding=20,
        border_radius=10,
        text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
    )

    barra_escala = ft.Slider(
        min=30, 
        max=330, 
        divisions=300,
        value=100, 
        label="{value}", 
        width=700,
        round=0,
        )

    selector_recorte = SelectorRecorte()
    selector_recorte.height = 768
    selector_recorte.width  = 768
    # selector_recorte.tooltip = "Click derecho para guardar el recorte\nClick izquierdo para marcado provisional."

    galeria = GaleriaRecortes(estilos_galeria)
    

    #################### MAQUETADO ########################

    columna_selector = ft.Column(
        [
        # ft.Row([texto_titulo], height=30,expand=True, alignment=ft.MainAxisAlignment.CENTER  ),
        selector_recorte,
        # ft.Row([texto_zoom, barra_escala]),
        texto_zoom,
        barra_escala,
        # ayuda_emergente,
        ],
        width  = 768,
        # height = altura_pagina,
        expand = True ,
        visible= False,
        # alignment=ft.MainAxisAlignment.START,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

    # componentes repartidos en segmentos horizontales
    fila_controles_apertura = ft.Row(
        [boton_carpeta_origen, boton_carpeta_destino],
        width = 500,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = True
        )

    fila_controles_dimensiones = ft.Row(
        [texto_dimensiones, lista_dimensiones_desplegable],
        width = 400,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = False
        )

    fila_controles = ft.Row([
        # boton_carpeta_origen, boton_carpeta_destino, 
        fila_controles_apertura,
        fila_controles_dimensiones,
        ayuda_emergente
        ],
        wrap = True,
        # alignment=ft.MainAxisAlignment.END,
        )

    fila_galeria = ft.Row(
        [galeria, 
        ft.VerticalDivider(width=6),
        columna_selector],
        expand = True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        )


    page.add( fila_controles )
    page.add(fila_galeria)

    ####################### HANDLERS ##################################


    def ventana_emergente(pagina:ft.Page, texto: str):
        page.show_snack_bar(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )

    def cambio_dimensiones_recorte(e):
        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        # global dimensiones_recorte 
        opcion = lista_dimensiones_desplegable.value
        dimensiones = convertir_dimensiones_opencv(str(opcion))
        # asignacion de nuevas dimensiones del recorte 
        dimensiones_recorte = [dimensiones[1], dimensiones[0]]
        selector_recorte.dimensiones_recorte = dimensiones_recorte

    lista_dimensiones_desplegable.on_change = cambio_dimensiones_recorte

    def escalar_imagen(e):
        valor = e.control.value
        imagen_temporal.ampliar(int(valor))
        # print("cambio escala disparado")

    barra_escala.on_change = escalar_imagen


    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):
        if e.path:
            # acceso a elementos globales
            global imagenes_galeria
            # ruta de directorio elegido
            directorio = e.path
             # reporte por snackbar
            ventana_emergente(page,f"Buscando imágenes...")
            # busqueda de imagenes
            rutas_imagen = buscar_imagenes(directorio)
            # Creacion y carga de imagenes del directorio
            imagenes_galeria = cargar_imagenes_recortes(rutas_imagen)
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_galeria)
            galeria.estilo(estilos_galeria["predefinido"])
            galeria.update()
            # desbloquea el boton de recortes
            boton_carpeta_destino.disabled=False
            boton_carpeta_destino.update()

            # ocultamiento del recortador de imagenes
            columna_selector.visible = False
            columna_selector.update()

            # reporte por snackbar
            ventana_emergente(page,f"Directorio de imágenes abierto\nRuta: {directorio} \nNº imágenes: {len(imagenes_galeria)}")


    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        if e.path:
            directorio = e.path
            # asignacion de rutas de salida
            galeria.ruta_recortes(directorio)
            # busqueda de recortes preexistentes
            rutas_recortes = buscar_imagenes(directorio)
            nombres_recortes = []
            for recorte in rutas_recortes:
                nombres_recortes.append(str(pathlib.Path(recorte).name))
            global imagenes_galeria
            nombres_imagen = []
            for imagen in imagenes_galeria:
                ruta_imagen = imagen.ruta_imagen
                nombres_imagen.append(str(pathlib.Path(ruta_imagen).name))
            for nombre in nombres_imagen:
                if nombre in nombres_recortes:
                    imagen_seleccionada = imagen_nombre(nombre, imagenes_galeria)
                    indice = nombres_recortes.index(nombre)
                    imagen_seleccionada.guardada = True
                    imagen_seleccionada.ruta_imagen = rutas_recortes[indice]
                    imagen_seleccionada.update()

            # actualizar graficas con los recortes 
            galeria.actualizar_estilos()
            galeria.update()

            # ocultamiento del recortador de imagenes
            columna_selector.visible = False
            columna_selector.update()

            # reporte por snackbar
            ventana_emergente(page,f"Directorio de recortes elegido\nRuta: {directorio} ")




    def cargar_selector(imagen: ContenedorRecortes):
        """Asigna toda la data de la imagen seleccionada al selector de recortes."""
        # se transfieren los datos auxiliares: escalas, coordenadas, etc
        global imagen_temporal
        imagen_temporal.data_actual   = imagen.data_actual 
        imagen_temporal.data_marcado  = imagen.data_marcado 
        imagen_temporal.data_guardado = imagen.data_guardado 
        imagen_temporal.clave = imagen.clave
        # imagen_temporal.clave = clave_actual

        imagen_temporal.abrir_imagen( imagen.ruta_origen)  

        selector_recorte.asignar( imagen_temporal)
        
        # redimensionado del selector de recortes
        ancho_pagina = int(page.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)


        n = len(imagenes_galeria)
        i = imagenes_galeria.index(imagen)
        nombre =  pathlib.Path(imagen.ruta_origen).name

        # reporte por snackbar
        ventana_emergente(page,f"Imagen {i+1} de {n}\nNombre archivo: {nombre}")

        # habilitacion redimensionamiento del selector de recortes
        page.on_resize = redimensionar_selector

        # se acomoda la barra de escala al valor preguardado
        if imagen.guardada:
            escala = imagen.data_guardado.escala
            barra_escala.value = escala
            barra_escala.update()
        elif imagen.marcada:
            escala = imagen.data_marcado.escala
            barra_escala.value = escala
            barra_escala.update()
        else:
            escala = imagen.data_actual.escala
            barra_escala.value = escala
            barra_escala.update()


        galeria.actualizar_estilos()
        # imagen.bgcolor = ft.colors.INDIGO_400
        imagen.bgcolor = ft.colors.PURPLE_200
        imagen.border=ft.border.all(10, ft.colors.LIGHT_BLUE_ACCENT_200)
        imagen.update()
        galeria.update()



    def click_galeria(e: ft.ControlEvent):

        # visibilizacion del recortador de imagenes
        columna_selector.visible = True
        columna_selector.update()

        global imagenes_galeria
        global clave_actual

        # lectura de datos de la imagen elegida
        contenedor = e.control     # es ft.Container
        clave_actual = contenedor.clave

        imagen: ContenedorRecortes
        imagen = imagen_clave(clave_actual, imagenes_galeria)

        cargar_selector(imagen)

        

    # manejador del teclado
    def teclado_galeria(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")

        global imagenes_galeria
        global clave_actual


        # print(clave_actual)
        if clave_actual != None:

            # lectura de datos de la imagen elegida
            # contenedor = e.control     # es ft.Container
            # clave_actual = contenedor.clave
            numero_imagenes = len(imagenes_galeria)

            imagen: ContenedorRecortes
            imagen = imagen_clave(clave_actual, imagenes_galeria)

            indice = imagenes_galeria.index(imagen)
            # cambio de imagen seleccionada
            cambiar_imagen = False
            if tecla == "A" or tecla =="Page Up":
                indice -= 1 
                indice = indice if indice>0 else 0
                cambiar_imagen = True
            elif tecla == "D" or tecla=="Page Down":
                indice += 1 
                indice = indice if indice<numero_imagenes else numero_imagenes-1
                cambiar_imagen = True
            elif tecla == "Home":
                indice = 0
                cambiar_imagen = True
            elif tecla == "End":
                indice = numero_imagenes - 1
                cambiar_imagen = True
            
            # if tecla=="A" or tecla =="D":
            if cambiar_imagen:
                imagen: ContenedorRecortes
                # actualizacion de parametros
                imagen = imagenes_galeria[indice]
                clave_actual = imagen.clave 
                galeria.scroll_to(key=clave_actual, duration=1000)
                cargar_selector(imagen)

            # cambio de zoom
            if tecla == "W":
                barra_escala.value +=1
                barra_escala.update()
                valor = barra_escala.value
                imagen_temporal.ampliar(int(valor))
            elif tecla == "S":
                barra_escala.value -=1
                barra_escala.update()
                valor = barra_escala.value
                imagen_temporal.ampliar(int(valor))

            



  
    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = teclado_galeria


    def click_izquierdo_selector(e):
        global imagenes_galeria
        global clave_actual
        # busqueda de imagen y guardado de estado
        clave_actual = imagen_temporal.clave
        imagen: ContenedorRecortes
        imagen = imagen_clave(clave_actual, imagenes_galeria)
        imagen.marcada = True
        imagen.guardada = False
        # se transfieren los datos auxiliares: escalas, coordenadas, etc
        imagen.data_actual   = imagen_temporal.data_actual 
        imagen.data_marcado  = imagen_temporal.data_marcado
        imagen.data_guardado = imagen_temporal.data_guardado  

        galeria.actualizar_estilos()
        galeria.update()
        # print(f"dimensiones marcado: {imagen_temporal.dimensiones_recorte}")
        
        # reporte por snackbar
        ventana_emergente(page,f"Marca provisoria creada.")



    def click_derecho_selector(e):
        global imagenes_galeria
        global clave_actual
        # busqueda de imagen y guardado de estado
        clave_actual = imagen_temporal.clave
        imagen: ContenedorRecortes
        imagen = imagen_clave(clave_actual, imagenes_galeria)
        imagen.marcada = False
        imagen.guardada = True
        # se transfieren los datos auxiliares: escalas, coordenadas, etc
        imagen.data_actual   = imagen_temporal.data_actual 
        imagen.data_marcado  = imagen_temporal.data_marcado
        imagen.data_guardado = imagen_temporal.data_guardado  
        # guardado en disco
        ruta_archivo = imagen.ruta_destino
        print("ruta archivo: ", ruta_archivo)
        imagen_temporal.guardar_recorte_archivo(ruta_archivo)
        # asignacion de imagen a la galeria
        imagen.ruta_imagen = imagen.ruta_destino

        galeria.actualizar_estilos()
        galeria.update()

        # reporte por snackbar
        ventana_emergente(page,f"Recorte de archivo creado!")



 
    selector_recorte.dimensiones_recorte = [512, 512]
    selector_recorte.funcion_click_izquierdo = click_izquierdo_selector
    selector_recorte.funcion_click_derecho = click_derecho_selector

    global imagen_temporal
    imagen_temporal = ImagenTemporal("recortador_imagenes_")

    def redimensionar_selector(e):
        # if e.data =="resize":
        ancho_pagina = int(page.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)
        # print(f"Redimensionado. Ancho:{ancho_pagina}")
        fila_galeria.width = page.window_width
        fila_galeria.update()

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen   = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino  = ft.FilePicker(on_result = resultado_directorio_destino )
   
    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio_origen, dialogo_directorio_destino
        ])

    # page.on_resize = redimensionar_selector

    page.title="Galeria Recorte"
    # page.theme_mode = ft.ThemeMode.DARK
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()


if __name__=="__main__":

    ft.app(target=pagina_galeria)

    # elimina la carpeta temporal y sus archivos internos al salir
    global imagen_temporal
    imagen_temporal.cerrar()