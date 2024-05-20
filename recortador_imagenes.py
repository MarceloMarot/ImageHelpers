


import flet as ft
from typing import TypeVar
import pathlib
import  time

# from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
from componentes.galeria_imagenes import ContImag, Galeria, Contenedor_Imagen, imagen_clave, imagen_nombre, indice_clave
from sistema_archivos.buscar_extension import buscar_imagenes
from componentes.estilos_contenedores import estilos_galeria, estilos_seleccion, Estilo_Contenedor
from componentes.selector_recortes import SelectorRecorte, DataRecorte
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from sistema_archivos.imagen_editable import ImagenEditable, crear_directorio_RAM


def nada( e ):
    pass


directorio_recortes = "recortes/"

prefijo_directorio_temporal = "recortador_imagenes_"
prefijo_directorio_miniaturas = "recortador_miniaturas_"

# carpeta auxiliar para contener las miniaturas de los recortes, de ser posible en RAM
directorio_miniaturas = crear_directorio_RAM(prefijo_directorio_miniaturas)


imagenes_galeria = []

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
        # carpeta destino dentro de la carpeta de ejecutable
        self.directorio_recortes = directorio_recortes

        # resuelve la ruta predefinida para el archivo de recorte
        self.ruta_destino : str
        self.ruta_recorte(self.directorio_recortes)

        # data auxiliar para las coordenadas y escalas de seleccion
        self.data_actual   = DataRecorte()
        self.data_marcado  = DataRecorte()
        self.data_guardado = DataRecorte()

        # archivo temporal (en RAM si es posible) con la imagen recortada
        self.recorte_temporal = ImagenEditable(
            directorio = directorio_miniaturas.name,
            extension = pathlib.Path(ruta).suffix   # respeta formato entrada 
            # extension = ".jpg"
            )
        self.tooltip = "Click izquierdo para seleccionar esta imagen."


    def ruta_recorte(self, ruta_directorio: str):
        """Este metodo asigna una ruta de destino para el recorte dentro del directorio indicado"""
        directorio = pathlib.Path(ruta_directorio)
        # creacion del directorio destino para los recortes
        directorio.mkdir(mode=0o777, exist_ok=True )
        # data de carpeta destino guardada
        self.directorio_recortes = str(directorio)
        # composicion de la ruta de archivo de salida
        nombre_archivo = pathlib.Path(self.ruta_imagen).name
        ruta_archivo = pathlib.Path(directorio, nombre_archivo)
        # asignacion de ruta de salida
        self.ruta_destino = str(ruta_archivo)


    def asignar_miniatura(self, ruta_origen):
        """Copia la imagen de entrada como archivo temporal y la asigna al componente grafico."""
        # copia a carpeta temporal
        self.recorte_temporal.subir(ruta_origen)  
        # asignacion grafica
        self.ruta_imagen = self.recorte_temporal.ruta  


    def guardar_recorte_archivo(self)->int:
        """Copia el archivo del recorte a la ruta preasignada"""
        nro_bytes = 0
        # copia el archivo si hay modificaciones registradas
        if self.marcada:
            archivo_origen = pathlib.Path(self.recorte_temporal.ruta )
            data_binaria = archivo_origen.read_bytes()

            archivo_destino = pathlib.Path(self.ruta_destino)
            nro_bytes = archivo_destino.write_bytes(data_binaria)

        # actualizacion de flags si la escritura fue exitosa
        if nro_bytes > 0:
            self.marcada = False
            self.guardada = True

        return nro_bytes



# nuevos tipados para contenedor y sus subclases
ContRec = TypeVar('ContRec', bound=ContenedorRecortes)


class GaleriaRecortes( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.imagenes: list[ContenedorRecortes]


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


def cargar_imagenes_galeria(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
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


def actualizar_estilo_estado(
    contenedores: list[ContenedorRecortes], estilos : dict ):
    """Actualiza los colores de borde de todas las imagenes en base a los flags internos."""
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



texto_ayuda = """
Bordes de Imagen:
Cada color de borde da informacion sobre el estado del recorte de cada imagen.
Opciones:
- Celeste: no recortado
- Verde: archivo de recorte guardado
- Amarillo: recorte marcado pero sin guardar en disco

Galería de imágenes:
- Click izquierdo sobre cualquier imagen para seleccionarla.
  Se abrirá el selector de recortes a la derecha.

Selector de recortes:
- Click derecho sobre la imagen ampliada para guardar el recorte marcado;
- Click izquierdo para marcado provisional (no se guarda);
- Rueda del mouse: cambio del zoom de imagen.

Barra de zoom:
- Deslizar la barra para ajustar el zoom de imagen.

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
    texto_imagen = ft.Text(
        "(Titulo)",
        size=20,
        # height=30, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        )


    texto_dimensiones = ft.Text("Dimensiones\nrecorte:", tooltip="512x512 por defecto")

    barra_escala = ft.Slider(
        min=30, 
        max=330, 
        divisions=300,
        value=100, 
        label="{value}", 
        width=700,
        round=0,
        )

    texto_zoom = ft.Text(f"Zoom: {int(barra_escala.value) } %", width=300)


    ayuda_emergente = ft.Tooltip(
        message=texto_ayuda,
        content=ft.Text("Ayuda emergente",size=20, width=200),
        padding=20,
        border_radius=10,
        text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
    )

    selector_recorte = SelectorRecorte(prefijo_directorio_temporal)
    selector_recorte.height = 768
    selector_recorte.width  = 768

    galeria = GaleriaRecortes(estilos_galeria)
    
    boton_guardar = ft.FloatingActionButton(
        icon=ft.icons.SAVE, bgcolor=ft.colors.YELLOW_600, tooltip="Guarda todos los recortes marcados"
    )

    # boton para guardar cambios 
    page.floating_action_button = boton_guardar

    #################### MAQUETADO ########################

    fila_zoom = ft.Row(
        [texto_zoom, barra_escala],
        width=768,
        wrap=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    columna_selector = ft.Column(
        [
        texto_imagen,
        selector_recorte,
        fila_zoom
        ],
        width  = 768,
        # height = altura_pagina,
        expand = True ,
        visible= False,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

    ####################### HANDLERS Y FUNCIONES ##################################


    def ventana_emergente(pagina:ft.Page, texto: str):
        pagina.show_snack_bar(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )

    def cambio_dimensiones_recorte(e):
        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        opcion = lista_dimensiones_desplegable.value
        dimensiones = convertir_dimensiones_opencv(str(opcion))
        # asignacion de nuevas dimensiones del recorte 
        dimensiones_recorte = [dimensiones[1], dimensiones[0]]
        selector_recorte.dimensiones_recorte = dimensiones_recorte


    def escalar_imagen(e: ft.ControlEvent | int):
        if type(e)==int:
            valor = e
        else:
            valor = e.control.value
        selector_recorte.escalar(int(valor))
        actualizar_barra_zoom(valor)


    # Funcion de apertura de directorio
    def resultado_directorio_origen(e: ft.FilePickerResultEvent):
        """Elige la carpeta de las imagenes originales."""
        if e.path:
            # acceso a elementos globales
            global imagenes_galeria
            global directorio_recortes
            # ruta de directorio elegido
            directorio = e.path
             # reporte por snackbar
            ventana_emergente(page,f"Buscando imágenes...")
            # busqueda de imagenes
            rutas_imagen = buscar_imagenes(directorio)
            # Creacion y carga de imagenes del directorio
            imagenes_galeria = cargar_imagenes_galeria(rutas_imagen,128,128)
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_galeria)
            galeria.estilo(estilos_galeria["predefinido"])
            galeria.update()
            # desbloquea el boton de recortes
            boton_carpeta_destino.disabled = False 
            boton_carpeta_destino.update()
            # ocultamiento del recortador de imagenes
            columna_selector.visible = False
            columna_selector.update()
            # carga de recortes preexistentes
            buscar_archivos_recortes(directorio_recortes)  
            # reporte por snackbar
            ventana_emergente(page,f"Directorio de imágenes abierto\nRuta: {directorio} \nNº imágenes: {len(imagenes_galeria)}")


    def resultado_directorio_destino(e: ft.FilePickerResultEvent):
        """Cambia la ruta de destino para los recortes de imagen."""
        if e.path:
            directorio = e.path
            # asignacion de rutas de salida
            galeria.ruta_recortes(directorio)
            # carga de recortes preexistentes
            buscar_archivos_recortes(directorio)
            # ocultamiento del recortador de imagenes
            columna_selector.visible = False
            columna_selector.update()
            # reporte por snackbar
            ventana_emergente(page,f"Directorio de recortes elegido\nRuta: {directorio} ")


    def buscar_archivos_recortes(directorio: str):
        """ASigna los recortes ya hechos a la galeria de imagenes"""

        rutas_recortes = buscar_imagenes(directorio)
        nombres_recortes = []
        for recorte in rutas_recortes:
            nombres_recortes.append(str(pathlib.Path(recorte).name))

        global imagenes_galeria

        # lectura de todas las rutas de imagen originales
        nombres_imagen = []
        for imagen in imagenes_galeria:
            ruta_imagen = imagen.ruta_imagen
            nombres_imagen.append(str(pathlib.Path(ruta_imagen).name))

        # asignacion de recortes ya hechos y marcado de estado 'guardado'
        for nombre in nombres_imagen:
            if nombre in nombres_recortes:
                imagen_seleccionada = imagen_nombre(nombre, imagenes_galeria)
                indice = nombres_recortes.index(nombre)
                imagen_seleccionada.guardada = True
                imagen_seleccionada.ruta_imagen = rutas_recortes[indice]
                imagen_seleccionada.update()
            else:
                imagen_seleccionada = imagen_nombre(nombre, imagenes_galeria)
                # indice = nombres_recortes.index(nombre)
                imagen_seleccionada.guardada = False
                imagen_seleccionada.ruta_imagen = imagen_seleccionada.ruta_origen
                imagen_seleccionada.update()
        # actualizar graficas con los recortes 
        galeria.actualizar_estilos()
        galeria.update()


    def cargar_selector(imagen: ContenedorRecortes):
        """Asigna toda la data de la imagen seleccionada al selector de recortes."""
        # se transfieren los datos auxiliares: escalas, coordenadas, etc
        selector_recorte.temporal.data_actual  .leer(imagen.data_actual )
        selector_recorte.temporal.data_marcado .leer(imagen.data_marcado )
        selector_recorte.temporal.data_guardado.leer(imagen.data_guardado )
        selector_recorte.temporal.clave = imagen.clave
 
        selector_recorte.abrir_imagen( imagen.ruta_origen)  

        # redimensionado del selector de recortes
        ancho_pagina = int(page.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)

        n = len(imagenes_galeria)
        i = imagenes_galeria.index(imagen)
        nombre =  pathlib.Path(imagen.ruta_origen).name

        # habilitacion redimensionamiento del selector de recortes
        page.on_resize = redimensionar_selector

        # se acomoda la barra de escala al valor preguardado
        if imagen.guardada:
            escala = imagen.data_guardado.escala
            actualizar_barra_zoom(escala)
        elif imagen.marcada:
            escala = imagen.data_marcado.escala
            actualizar_barra_zoom(escala)
        else:
            escala = imagen.data_actual.escala
            actualizar_barra_zoom(escala)

        # marcado de recorte preliminar
        selector_recorte.coordenadas()
        # 
        galeria.actualizar_estilos()

        # reestablecimiento de bordes para todas las imagenes de galeria
        actualizar_estilo_estado(
            imagenes_galeria, 
            estilos_galeria
            )
        galeria.update()

        # bordes gruesos y cambio color de imagen actual en galeria
        imagen.border = ft.border.all(20, ft.colors.PURPLE_300)
        imagen.height = 148
        imagen.width  = 148
        imagen.margin  = 0
        imagen.update()

        texto_imagen.value = f"{i+1} / {n} - '{nombre}'"
        texto_imagen.visible = True 
        texto_imagen.update()


    def click_galeria(e: ft.ControlEvent):
        """Abre la imagen seleccionada por click en el selector de recortes."""

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

        galeria.scroll_to(key=clave_actual, duration=1000)


    # manejador del teclado
    def teclado_galeria(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   

        global imagenes_galeria
        global clave_actual

        if clave_actual != None:

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
                valor = barra_escala.value
                valor += selector_recorte.incremento_escala
                escalar_imagen(int(valor))
                selector_recorte.escalar(int(valor))
            elif tecla == "S":
                valor = barra_escala.value
                valor -= selector_recorte.incremento_escala
                escalar_imagen(int(valor))
                selector_recorte.escalar(int(valor))


    def marcar_recorte(guardar:bool=False):
        """Marca el rectangulo del recorte actual y actualiza los bordes.
        Guarda el recorte en archivo sólo en caso de requerirse.
        """
        global imagenes_galeria
        global clave_actual
        # busqueda de imagen y guardado de estado
        clave_actual = selector_recorte.temporal.clave  # FIX: forzado
        imagen: ContenedorRecortes
        imagen = imagen_clave(clave_actual, imagenes_galeria)
        imagen.marcada = not guardar # FIX
        imagen.guardada = guardar    # FIX
        # se transfieren los datos auxiliares: escalas, coordenadas, etc
        imagen.data_actual  .leer(selector_recorte.temporal.data_actual  )    
        imagen.data_marcado .leer(selector_recorte.temporal.data_marcado )
        imagen.data_guardado.leer(selector_recorte.temporal.data_guardado)     
        
        # asignacion miniatura
        archivo_recorte = selector_recorte.ruta_recorte
        imagen.asignar_miniatura(archivo_recorte)
        imagen.update()

        if guardar:
            # guardado en disco
            ruta_archivo = imagen.ruta_destino
            selector_recorte.temporal.guardar_recorte_archivo(ruta_archivo) # FIX
            # imagen.guardar_recorte_archivo()
            # asignacion de imagen a la galeria
            imagen.ruta_imagen = imagen.ruta_destino

        galeria.actualizar_estilos()
        galeria.update()


    def click_izquierdo_selector(e):
        """"Click izquierdo para crear recorte provisorio"""
        marcar_recorte(guardar=False)


    def click_derecho_selector(e):
        """Click derecho para crear recorte definitivo."""
        marcar_recorte(guardar=True)


    def actualizar_barra_zoom(e:ft.ControlEvent|int):
        """Actualiza los valores de la barra de zoom y del texto en base a la data del selector de recortes."""
        # actualizacion grafica de la barra deslizante
        if type(e)==int:
            barra_escala.value = e
        else:
            barra_escala.value = selector_recorte.escala_actual
        barra_escala.update()
        # actualiacion de texto
        texto_zoom.value = f"Zoom: {int(barra_escala.value) } %"
        texto_zoom.update()


        # global imagenes_galeria, clave_actual
        # if indice_clave(str(clave_actual), imagenes_galeria)!=None:
        #     g = selector_recorte.temporal.data_guardado.escala
        #     m = selector_recorte.temporal.data_marcado.escala
        # texto_zoom.value = f"Zoom: {int(barra_escala.value)}% {int(m)}% {int(g)}%"
        # texto_zoom.update()
    
    
    def guardar_cambios(e:ft.ControlEvent | None = None):
        """Guarda las etiquetas en archivo de todas las imagenes modificadas. También actualiza estados y graficas."""
        
        global imagenes_galeria



        if len(imagenes_galeria) == 0 : 
            ventana_emergente(page,f"Galería vacía - sin cambios")
            return
        imagen: ContenedorRecortes
        i = 0
        for imagen in imagenes_galeria:  #
            # busqueda de recortes modificados
            # clave = imagen.clave
            # imag = imagen_clave(clave, imagenes_galeria)
            if imagen.marcada :
                i += 1 
                # clave_actual = clave
                # marcar_recorte(guardar=True)
                # ruta_recorte = imagen.ruta_imagen

                imagen.guardar_recorte_archivo()

                # imagen.marcada = False
                # imagen.guardada = True

        galeria.actualizar_estilos()
        galeria.update()

        # reporte por snackbar
        if i == 0:
            ventana_emergente(page,f"Recortes sin cambios")
        else:
            ventana_emergente(page,f"¡Recortes guardados! - {i} archivos modificados")
        # actualizacion grafica 
        cerrar_dialogo(e)  


    def abrir_dialogo_guardado(e:ft.ControlEvent | None = None):

        global imagenes_galeria
        # conteo imagenes a guardar
        j = 0
        imagen: ContenedorRecortes
        for imagen in imagenes_galeria:  
            if imagen.marcada:
                j += 1 

        if j == 0:
            # se ignora (nada que hacer)
            ventana_emergente(page, "Sin cambios para guardar.")
            return
        else:
            # pedido de confirmacion
            page.dialog = ft.AlertDialog(
                # modal=True,
                modal=False,
                title=ft.Text("¿Guardar cambios?"),
                content=ft.Text(f"{j} imágenes modificadas."),
                actions=[
                    ft.ElevatedButton(
                        "Sí", 
                        on_click=guardar_cambios,
                        autofocus=False,
                        ),
                    # ft.OutlinedButton("No", on_click=no_click),
                    ft.OutlinedButton(
                        "No", 
                        on_click=cerrar_dialogo, 
                        autofocus=True ),
                ],
            )
            # mantener dialogo abierto
            page.dialog.open = True
            page.update()



    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()


    def confirmar_cierre_programa(e:ft.ControlEvent):
        if e.data == "close":
            global imagenes_galeria
            # conteo imagenes con cambios sin guardar
            j = 0
            if len(imagenes_galeria)==0:
                print("galeria vacia")
                cierre_programa()

            imagen: ContenedorRecortes
            for imagen in imagenes_galeria:  
                if imagen.marcada:
                    j += 1 
                    # print(j)

            # si no hay modificaciones realizadas se cierra directamente
            # print(j)
            if j==0:
                print("sin cambios registrados")
                cierre_programa()
            else:
                page.dialog = ft.AlertDialog(
                    modal=False,
                    title=ft.Text("¿Descartar cambios y salir?"),
                    content=ft.Text(f"Hay {j} imágenes con modificaciones sin guardar."),
                    actions=[
                        ft.ElevatedButton(
                            "Sí", 
                            on_click=cierre_programa,
                            autofocus=False,
                            ),
                        ft.OutlinedButton(
                            "No", 
                            on_click=cerrar_dialogo,
                            autofocus=True 
                            ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
                page.dialog.open = True
                page.update()


    def cierre_programa(e:ft.ControlEvent|None=None):
        cerrar = False
        if e == None:
            cerrar = True
        else:
            if e.data == "close":
                cerrar = True
            elif e.control.text == "Sí":   # FIX
                cerrar = True

        if cerrar:
            page.window_destroy()
            time.sleep(0.5)
            selector_recorte.cerrar()
            directorio_miniaturas.cleanup()


    def redimensionar_selector(e):
        # if e.data =="resize":
        ancho_pagina = int(page.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)

        fila_galeria.width = page.window_width
        fila_galeria.update()

    ##################### ASIGNACION HANDLERS ##################

    lista_dimensiones_desplegable.on_change = cambio_dimensiones_recorte
    barra_escala.on_change = escalar_imagen

    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = teclado_galeria

    # confirmacion guardado en grupo
    boton_guardar.on_click = abrir_dialogo_guardado

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen   = ft.FilePicker(on_result = resultado_directorio_origen )
    dialogo_directorio_destino  = ft.FilePicker(on_result = resultado_directorio_destino )
   
    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio_origen, dialogo_directorio_destino
        ])

    selector_recorte.dimensiones_recorte = [512, 512]
    selector_recorte.funcion_click_izquierdo = click_izquierdo_selector
    selector_recorte.funcion_click_derecho = click_derecho_selector
    selector_recorte.funcion_scroll_mouse = actualizar_barra_zoom

    # rutina para liberar archivos temporales
    page.window_prevent_close = True
    # page.on_window_event = cierre_programa
    page.on_window_event = confirmar_cierre_programa

    page.title="Galeria Recorte"
    # page.theme_mode = ft.ThemeMode.DARK
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()


if __name__=="__main__":

    ft.app(target=pagina_galeria)
