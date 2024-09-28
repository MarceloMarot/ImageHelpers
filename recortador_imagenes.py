import flet as ft
from typing import TypeVar
import pathlib
import  time

# from manejo_imagenes.verificar_dimensiones import dimensiones_imagen
from componentes.galeria_imagenes import ContImag, Galeria, imagen_clave, imagen_nombre, indice_clave
from componentes.dialogo_alerta import DialogoAlerta
from sistema_archivos.buscar_extension import buscar_imagenes
from estilos.estilos_contenedores import estilos_galeria, estilos_seleccion
# from componentes.selector_recortes import SelectorRecorte, DataRecorte
from componentes.selector_recortes import DataRecorte
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones
from sistema_archivos.imagen_editable import ImagenEditable, crear_directorio_RAM

from componentes.contenedor_estados import ContenedorEstados
from componentes.galeria_estados import GaleriaEstados, actualizar_estilo_estado

from vistas.recortador.menu_recortador import ayuda_emergente
from vistas.recortador.dialogos import dialogo_directorio_origen, dialogo_directorio_destino
from vistas.recortador.menu_recortador import boton_carpeta_origen, boton_carpeta_destino, fila_controles, lista_dimensiones_desplegable
from vistas.recortador.columna_selector import columna_selector
from vistas.recortador.columna_selector import texto_imagen, texto_zoom
from vistas.recortador.columna_selector import selector_recorte, barra_escala

from constantes.rutas import DIRECTORIO_RECORTES, PREFIJO_DIRECTORIO_MINIATURAS
from componentes.contenedores import ContenedorImagen


def nada( e ):
    pass


directorio_recortes = DIRECTORIO_RECORTES
directorio_miniaturas = crear_directorio_RAM(PREFIJO_DIRECTORIO_MINIATURAS)

clave_actual = None

imagenes_galeria = []

class ContenedorRecortes( ContenedorImagen):
    def __init__(self, ruta, clave: str, ancho=768, alto=768, redondeo=0,):
        ContenedorImagen.__init__(self,ruta, ancho, alto, redondeo)
        # flags para el coloreo de bordes
        self.modificada = False
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
        if self.modificada:
            archivo_origen = pathlib.Path(self.recorte_temporal.ruta )
            data_binaria = archivo_origen.read_bytes()

            archivo_destino = pathlib.Path(self.ruta_destino)
            nro_bytes = archivo_destino.write_bytes(data_binaria)

        # actualizacion de flags si la escritura fue exitosa
        if nro_bytes > 0:
            self.modificada = False
            self.guardada = True

        return nro_bytes





#  RESCATADA DE VIEJA IMPLEMENTACION
class GaleriaEtiquetado( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos


    def cargar_imagenes(self, 
        imagenes: list[ContImag ], 
        cuadricula=True):
        """Lee objetos de imagen Flet del tipo Contenedor_Imagen previamente creados."""
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        self.actualizar_estilos( )  


    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    





class GaleriaRecortes( GaleriaEtiquetado):
    def __init__(self, estilos: dict):
        super().__init__(estilos)


    def ruta_recortes(self, ruta_directorio: str):

        for contenedor in self.controls:
            contenedor: ContenedorRecortes
            contenedor.ruta_recorte(ruta_directorio)   


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






def pagina_galeria(pagina: ft.Page):
    """Funcion gráfica para crear la galería de Flet"""

    ancho_pagina = 1500
    altura_pagina = 900

    pagina.window_height = altura_pagina
    pagina.window_width  = ancho_pagina

    ################## COMPONENTES ########################



   galeria = GaleriaRecortes(estilos_galeria)
    
    boton_guardar = ft.FloatingActionButton(
        icon=ft.icons.SAVE, bgcolor=ft.colors.YELLOW_600, tooltip="Guarda todos los recortes marcados"
    )

    # boton para guardar cambios 
    pagina.floating_action_button = boton_guardar

    #################### MAQUETADO ########################


    


    fila_galeria = ft.Row(
        [galeria, 
        ft.VerticalDivider(width=6),
        columna_selector],
        expand = True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        )


    pagina.add( fila_controles )
    pagina.add(fila_galeria)

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
            ventana_emergente(pagina,f"Buscando imágenes...")
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
            ventana_emergente(pagina,f"Directorio de imágenes abierto\nRuta: {directorio} \nNº imágenes: {len(imagenes_galeria)}")


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
            ventana_emergente(pagina,f"Directorio de recortes elegido\nRuta: {directorio} ")


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
        ancho_pagina = int(pagina.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)

        n = len(imagenes_galeria)
        i = imagenes_galeria.index(imagen)
        nombre =  pathlib.Path(imagen.ruta_origen).name

        # habilitacion redimensionamiento del selector de recortes
        pagina.on_resize = redimensionar_selector

        # se acomoda la barra de escala al valor preguardado
        if imagen.guardada:
            escala = imagen.data_guardado.escala
            actualizar_barra_zoom(escala)
        elif imagen.modificada:
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
        imagen.modificada = not guardar # FIX
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

    
    def guardar_cambios(e:ft.ControlEvent | None = None):
        """Guarda los recortes en archivo de todas las imagenes modificadas. También actualiza estados y graficas."""
        
        global imagenes_galeria

        if len(imagenes_galeria) == 0 : 
            ventana_emergente(pagina,f"Galería vacía - sin cambios")
            return
        imagen: ContenedorRecortes
        i = 0
        for imagen in imagenes_galeria:  #
            # busqueda de recortes modificados
            if imagen.modificada :
                i += 1 
                imagen.guardar_recorte_archivo()

        galeria.actualizar_estilos()
        galeria.update()

        # reporte por snackbar
        if i == 0:
            ventana_emergente(pagina,f"Recortes sin cambios")
        else:
            ventana_emergente(pagina,f"¡Recortes guardados! - {i} archivos modificados")
        # actualizacion grafica 
        cerrar_dialogo(e)  


    def abrir_dialogo_guardado(e:ft.ControlEvent | None = None):

        global imagenes_galeria
        # conteo imagenes a guardar
        j = 0
        imagen: ContenedorRecortes
        for imagen in imagenes_galeria:  
            if imagen.modificada:
                j += 1 

        if j == 0:
            # se ignora (nada que hacer)
            ventana_emergente(pagina, "Sin cambios para guardar.")
            return
        else:
            # en caso contrario se lanza la alerta de guardado
            dialogo_guardado_imagenes = DialogoAlerta(
                pagina,
                "¿Guardar cambios?", 
                f"Hay {j} imágenes modificadas."
                )

            dialogo_guardado_imagenes.funcion_confirmacion = guardar_cambios
            dialogo_guardado_imagenes.abrir_alerta() 


    def cerrar_dialogo(e):
        pagina.dialog.open = False
        pagina.update()


    def confirmar_cierre_programa(e:ft.ControlEvent):
        if e.data == "close":
            global imagenes_galeria
            # conteo imagenes con cambios sin guardar
            j = 0
            if len(imagenes_galeria)==0:
                cierre_programa()

            imagen: ContenedorRecortes
            for imagen in imagenes_galeria:  
                if imagen.modificada:
                    j += 1 

            # si no hay modificaciones realizadas se cierra directamente
            if j==0:
                    pagina.window_destroy()
            # en caso contrario se lanza la alerta de cierre
            else:
                dialogo_cierre_programa = DialogoAlerta(
                    pagina,
                    "¿Descartar cambios?", 
                    f"Hay {j} modificaciones sin guardar."
                    )

                dialogo_cierre_programa.funcion_confirmacion = pagina.window_destroy
                dialogo_cierre_programa.abrir_alerta()


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
            pagina.window_destroy()
            time.sleep(0.5)
            selector_recorte.cerrar()
            directorio_miniaturas.cleanup()


    def redimensionar_selector(e):
        # if e.data =="resize":
        ancho_pagina = int(pagina.window_width)
        ancho_selector = int(ancho_pagina/2)
        selector_recorte.dimensiones_graficas(1, ancho_selector, ancho_selector)

        fila_galeria.width = pagina.window_width
        fila_galeria.update()

    ##################### ASIGNACION HANDLERS ##################

    lista_dimensiones_desplegable.on_change = cambio_dimensiones_recorte
    barra_escala.on_change = escalar_imagen

    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = teclado_galeria

    # confirmacion guardado en grupo
    boton_guardar.on_click = abrir_dialogo_guardado

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio_origen .on_result = resultado_directorio_origen 
    dialogo_directorio_destino.on_result = resultado_directorio_destino 




    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio_origen, dialogo_directorio_destino
        ])

    selector_recorte.dimensiones_recorte = [512, 512]
    selector_recorte.funcion_click_izquierdo = click_izquierdo_selector
    selector_recorte.funcion_click_derecho = click_derecho_selector
    selector_recorte.funcion_scroll_mouse = actualizar_barra_zoom

    # rutina para liberar archivos temporales
    pagina.window_prevent_close = True
    # pagina.on_window_event = cierre_programa
    pagina.on_window_event = confirmar_cierre_programa

    pagina.title="Galeria Recorte"
    # pagina.theme_mode = ft.ThemeMode.DARK
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.update()


if __name__=="__main__":

    ft.app(target=pagina_galeria)
