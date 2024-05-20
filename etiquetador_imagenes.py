

from re import I
from rich import print as print
import flet as ft
import pathlib

from manejo_texto.procesar_etiquetas import Etiquetas, guardar_archivo, etiquetas2texto

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor, imagen_clave,indice_clave, ContImag
from componentes.etiquetador_botones import EtiquetadorBotones , BotonBiestable, FilasBotonesEtiquetas
from componentes.estilos_contenedores import estilos_seleccion, estilos_galeria
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from sistema_archivos.buscar_extension import buscar_imagenes

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from enum import Enum

class Tab(Enum):
    TAB_GALERIA = 0
    TAB_SELECCION = 1

class Percentil(Enum):
    UMBRAL_1 = 0.2
    UMBRAL_2 = 0.4
    UMBRAL_3 = 0.6
    UMBRAL_4 = 0.8
    UMBRAL_5 = 1

class Estados(Enum):
    TODOS = "todas"
    GUARDADOS = "guardadas"
    MODIFICADOS = "modificadas"
    NO_TAGGEADOS = "no etiquetadas" 

tupla_estados = (
    Estados.TODOS.value,
    Estados.GUARDADOS.value,
    Estados.MODIFICADOS.value,
    Estados.NO_TAGGEADOS.value,
)


texto_ayuda = """
Bordes de imagen:
  Cada color de borde da informacion sobre el estado del etiquetado o de las dimensiones de cada imagen.
  Opciones:
  - Celeste: no etiquetado
  - Verde: tags guardados
  - Amarillo: tags agregados o modificados
  - Rojo: dimensiones incorrectas

Teclado: 
Permite cambiar rápidamente la imagen seleccionada. 
Teclas rápidas:
- Home:  primera imagen;
- RePag | A : imagen anterior;
- AvPag | D : imagen siguiente;
- End:   última imagen.
- Space : restaurar etiquetas (imagen actual)
-  W    : guardar etiquetas   (imagen actual)
- Flechas : navegar por el menú
- ENTER   : abrir ventanas y listas 
- Escape  : salir de ventanas emergentes, deseleccionar opciones
"""



def nada( e ):
    pass


class Contenedor_Etiquetado( Etiquetas, Contenedor_Imagen):
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, Estilo_Contenedor] = estilos_galeria,
        ):
        Etiquetas.__init__(self, ruta)
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        self.__modificada = False
        self.__guardada = False
        self.__defectuosa = False
        self.__dimensiones: tuple[int, ...]|None
        self.leer_dimensiones()
        self.verificar_imagen()   
        self.verificar_guardado_tags()
        self.estilos = estilos
        self.tooltip = ruta


    def buscar_etiqueta(self, etiqueta: str):
        """Este método busca la etiqueta en la imagen y si la encuentra devuelve 'True'."""
        return True if etiqueta in self.tags else False
            

    def leer_dimensiones(self):
        """Este método lee altura, base y numero de canales de la imagen"""
        dim = dimensiones_imagen(self.ruta)  
        self.__dimensiones = dim if dim!=None else None 


    @property
    def dimensiones(self):
        return self.__dimensiones


    def verificar_imagen(self, dimensiones: tuple[int, int, int] | None=None)->bool|None:
        """Este método verifica dimensiones de archivo.
        Devuelve 'True' si las dimensiones coinciden.
        """
        if dimensiones == None:
            self.__defectuosa = False
            return None
        if self.__dimensiones != dimensiones:
            self.__defectuosa = True
            return False
        else:
            self.__defectuosa = False
            return True

    @property
    def defectuosa(self)->bool:
        return self.__defectuosa

    # def verificar_guardado_tags(self , tags: list[str] | None = None):
    def verificar_guardado_tags(self ):
        """Comprueba si las etiquetas actuales son las mismas que las guardadas en archivo de texto"""
        # verificacion guardado
        tags_archivo  = self.tags_archivo 
        self.__guardada = False if len(tags_archivo)==0 else True
        # verificacion modificaciones de etiquetado
        tags_imagen =  self.tags
        self.__modificada = True if set(tags_imagen) != set(tags_archivo) else False 

    @property
    def modificada(self)->bool:
        return self.__modificada 

    @property
    def guardada(self)->bool:
        return self.__guardada 


    def guardar_archivo(self)->bool:
        """
        Escribe/rescribe el archivo de etiquetas si éstas no coinciden con las guardadas en la estructura. 
        Si 'tags' es 'None' se usan las etiquetas almacenadas en el objeto imagen.
        """
        guardado_exitoso = False
        self.verificar_guardado_tags()
        if self.modificada:
            guardado_exitoso = self.guardar(self.tags)
            self.__guardada = guardado_exitoso
        return guardado_exitoso


    def actualizar_estilo_estado(self):
        actualizar_estilo_estado([self], self.estilos)
        

class GaleriaEtiquetado( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos


    def cargar_imagenes(self, 
        imagenes: list[ContImag ], 
        cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        self.actualizar_estilos( )  


    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    


def actualizar_estilo_estado( contenedores: list[Contenedor_Etiquetado], estilos : dict ):
    for contenedor in contenedores:
        if contenedor.defectuosa :
            estilo = estilos["erroneo"]     
        elif contenedor.modificada :
            estilo = estilos["modificado"]
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        else: 
            estilo = estilos["predefinido"]
        contenedor.estilo( estilo )


def leer_imagenes_etiquetadas(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 
    for i in range( len(rutas_imagen)):
        contenedor = Contenedor_Etiquetado(rutas_imagen[i], ancho, alto, redondeo)
        contenedor.clave = f"imag_{i}"
        contenedores.append(contenedor)
    return contenedores


def filtrar_dimensiones(
    lista_imagenes: list[Contenedor_Etiquetado], 
    dimensiones: tuple[int, int, int] | None = None
    )->list[Contenedor_Etiquetado]:
    """Devuelve solamente los contenedores de imagen con el ancho y altura correctos.
    Si las dimensiones de entrada son 'None' devuelve todos los conteedores de entrada. 
    """
    imagenes_filtradas = []
    for imagen in lista_imagenes: 
        if dimensiones == imagen.dimensiones:    
            imagenes_filtradas.append(imagen)

    if dimensiones != None:
        # imagenes con dimensiones correctas
        return imagenes_filtradas
    else:
        # caso sin dimensiones especificas
        return lista_imagenes


def filtrar_etiquetas(
    lista_imagenes: list[Contenedor_Etiquetado], 
    etiquetas: list[str]  = [],
    )->list[Contenedor_Etiquetado]:
    imagenes_filtradas = []
    """
    Devuelve las imagenes que tengan al menos una etiqueta de entrada. 
    Si no hay etiquetas de entrada se devuelve toda la lista de entrada.
    """
    if etiquetas == []:
        # imagenes con dimensiones correctas
        return lista_imagenes
    else:
        for etiqueta in etiquetas:
            for imagen in lista_imagenes:
                # se previene repetir imagenes
                if imagen not in imagenes_filtradas:
                    if etiqueta in imagen.tags:
                        imagenes_filtradas.append(imagen)
        return imagenes_filtradas

    
def filtrar_estados(
    lista_imagenes: list[Contenedor_Etiquetado], 
    estado: str | None ,
    )->list[Contenedor_Etiquetado]:
    """Devuelve solamente los contenedores con el estado de etiquetado pedido."""
    imagen : Contenedor_Etiquetado
    imagenes_filtradas = []
    # imagenes guardadas (sin cambios)
    if estado == Estados.GUARDADOS.value:
        for imagen in lista_imagenes: 
            if imagen.guardada and not imagen.modificada:    
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    # imagenes tags modificados (todas)
    elif estado == Estados.MODIFICADOS.value:
        for imagen in lista_imagenes:   
            if imagen.modificada:    
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    # no etiquetadas ni guardadas
    elif estado == Estados.NO_TAGGEADOS.value:
        for imagen in lista_imagenes: 
            if not imagen.modificada and not imagen.guardada: 
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    else:
        # no filtrado
        return lista_imagenes


dimensiones_elegidas = None
imagenes_galeria = []
imagenes_seleccion = []
imagenes_tags = []
todas_imagenes = []



ruta_dataset = ""


def main(pagina: ft.Page):

    # estructura con data global
    dataset = Etiquetas(ruta_dataset) 


    ############# COMPONENTES GRAFICOS ######################## 
    
    # caja de ayuda
    ayuda_emergente = ft.Tooltip(
        message=texto_ayuda,
        content=ft.Text("Ayuda extra",size=18, width=100),
        padding=20,
        border_radius=10,
        text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
    )

    # Botones apertura de ventana emergente
    boton_carpeta = ft.ElevatedButton(
        text = "Abrir imágenes",
        # icon=ft.icons.FOLDER_OPEN,
        icon=ft.icons.FOLDER,
        bgcolor=ft.colors.RED,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_directorio.get_directory_path(
            dialog_title="Elegir carpeta con todas las imágenes"
        ),
        tooltip="Abre la carpeta con todas las imágenes a etiquetar.",
    )

    boton_dataset = ft.ElevatedButton(
        text = "Abrir dataset",
        icon=ft.icons.FILE_OPEN,
        bgcolor=ft.colors.BLUE,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_dataset.pick_files(
            dialog_title= "Elegir archivo de dataset (formato .txt)",
            allowed_extensions=["txt"],
            allow_multiple=False,
        ),
        tooltip="Elige el archivo TXT con las etiquetas a agregar.\nCada renglón se interpreta como un 'grupo' de tags."
    )
    
    boton_guardar_dataset = ft.ElevatedButton(
        text = f"Guardar como dataset",
        bgcolor = ft.colors.AMBER_800,
        icon=ft.icons.SAVE,
        color = ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_guardado_tags.save_file(
            dialog_title = "Guardar archivo de dataset (formato .txt)",
            allowed_extensions=["txt"],
            ),
        tooltip="Guarda en archivo de texto las etiquetas encontradas. Si el archivo ya existe lo sobreescribe.",
        )

    boton_reset_tags = ft.ElevatedButton(
        text = f"Deseleccionar etiquetas...",
        bgcolor = ft.colors.BLUE_800,
        color = ft.colors.WHITE,
        tooltip="Reinicia la selección de etiquetas encontradas."
        )

    boton_filtrar_dimensiones = BotonBiestable("Filtrar", ft.colors.BROWN_100, ft.colors.BROWN_800)
    boton_filtrar_dimensiones.color = ft.colors.WHITE
    boton_filtrar_dimensiones.tooltip = "Selecciona las imágenes que cumplan con las dimensiones indicadas."

    boton_filtrar_etiquetas = BotonBiestable("Panel filtrado", ft.colors.PURPLE_100, ft.colors.PURPLE_800)
    boton_filtrar_etiquetas.color = ft.colors.WHITE
    boton_filtrar_etiquetas.tooltip = "Abre el panel de filtrado con todas las etiquetas detectadas.\nRequiere que haya al menos una imagen cargada."

    boton_guardar = ft.FloatingActionButton(
        icon=ft.icons.SAVE, bgcolor=ft.colors.YELLOW_600, tooltip="Guardar todas las etiquetas cambiadas."
    )

    # listas desplegable para elegir opciones de imagen 
    lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones, ancho=120)
    lista_estados_desplegable = crear_lista_desplegable(tupla_estados, ancho=120)

    # Componentes especiales
    etiquetador_imagen = EtiquetadorBotones()

    galeria = GaleriaEtiquetado( estilos_galeria )

    filas_filtrado = FilasBotonesEtiquetas()
    filas_filtrado.altura = pagina.height - 200

    filas_filtrado.lista_colores_activo=[
        ft.colors.BLUE_800,
        ft.colors.GREEN_800,
        ft.colors.YELLOW_800,
        ft.colors.ORANGE_800,
        ft.colors.RED_800,
        ]
    filas_filtrado.lista_colores_pasivo=[
        ft.colors.BLUE_100,
        ft.colors.GREEN_100,
        ft.colors.YELLOW_100,
        ft.colors.ORANGE_100,
        ft.colors.RED_100,
        ]

    # textos
    texto_dimensiones = ft.Text("Dimensiones\nimagen:")
    texto_estados = ft.Text("Estado\netiquetado:")
    texto_imagen= ft.Text(
        "(Titulo)",
        size=20,
        # height=30, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        )
    texto_ruta_titulo = ft.Text(
        "(ruta))",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        )
    texto_ruta_data = ft.Text(
        "(ruta_completa))",
        weight=ft.FontWeight.NORMAL,
        text_align=ft.TextAlign.CENTER,
        )
    texto_tags_titulo = ft.Text(
        "(nro tags)",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        )
    texto_tags_data = ft.Text(
        "(tags)",
        weight=ft.FontWeight.NORMAL,
        text_align=ft.TextAlign.CENTER,
        )
    
    texto_contador_tags= ft.Text(
        "Tags encontados:",
        size=15,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.START,
        )
    
    # contenedor visualizador de la imagen actual
    contenedor_seleccion = Contenedor_Imagen("",512,512)
    contenedor_seleccion.estilo(estilos_seleccion["predefinido"])
    contenedor_seleccion.bgcolor = ft.colors.LIGHT_BLUE

    #############  MAQUETADO ############################

    # componentes repartidos en segmentos horizontales
    fila_controles_apertura = ft.Row(
        [boton_carpeta, boton_dataset],
        width = 350,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = True
        )
    fila_controles_dimensiones = ft.Row(
        [texto_dimensiones, lista_dimensiones_desplegable, boton_filtrar_dimensiones],
        width = 400,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = False
        )

    fila_controles_etiquetas = ft.Row(
        [texto_estados, lista_estados_desplegable, boton_filtrar_etiquetas],
        width = 400,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = False
        )

    galeria.expand = 1

    columna_etiquetas = ft.Column(
        controls=[    
            ft.Row(
                [ texto_contador_tags, 
                boton_reset_tags, 
                boton_guardar_dataset],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),  
            ft.Divider(height=7, thickness=1) ,
            filas_filtrado,
        ],
        visible=False,
        expand=1,
        scroll=ft.ScrollMode.HIDDEN, 
        )


    fila_galeria_etiquetas = ft.Row(
        [galeria, ft.VerticalDivider(), columna_etiquetas],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.START,
        wrap = False,
        expand=True,
        )

    # Fila de botones para abrir carpetas y leer archivos
    fila_controles = ft.Row([
        fila_controles_apertura,
        fila_controles_dimensiones,
        fila_controles_etiquetas,
        ayuda_emergente,
        ],
        wrap=True,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

    pagina.add(fila_controles)
    pagina.add(ft.Divider(height=7, thickness=1))

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=fila_galeria_etiquetas,
        visible=True,
        icon=ft.icons.GRID_VIEW_ROUNDED,
        )


    columna_seleccion = ft.Column(
        [
            texto_imagen, 
            contenedor_seleccion, 
            texto_ruta_titulo, 
            texto_ruta_data, 
            texto_tags_titulo,
            texto_tags_data,
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        visible=False,
    )


    # pestaña de etiquetado y navegacion de imagenes
    altura_tab_etiquetado = 800
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            columna_seleccion,  
            ft.VerticalDivider(),
            etiquetador_imagen
            ], 
        spacing = 10, 
        height = altura_tab_etiquetado
    ) 
    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=fila_etiquetado_navegacion,
        visible=True,    
        icon = ft.icons.TAG_OUTLINED,
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=Tab.TAB_GALERIA.value,
        animation_duration=500,
        tabs=[
            tab_galeria   ,
            tab_etiquetado,
        ],
        expand=1,
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)
    # boton para guardar cambios 
    pagina.floating_action_button = boton_guardar

    ############## HANDLERS ##################################


    def click_botones_tags(e: ft.ControlEvent ):
        """Habilita el accionamiento solidario de los botones de etiquetas repetidas. Tambien llama al handler de actualizaciones."""
        tag = e.control.text
        estado = e.control.estado

        # Se transfieren los tags de la botonera a las imagenes 
        etiquetas_botones = etiquetador_imagen.leer_botones()

        # caso de deseleccion de etiquetas -> botones repetidos actualizados
        if estado==False:
            # extraccion de etiqueta actual
            set_actual = set(etiquetas_botones)
            set_resta = set([tag])
            set_tags = set_actual.difference(set_resta)
            etiquetas_botones = list(set_tags)
  
        etiquetador_imagen.agregar_tags(etiquetas_botones, sobreescribir=True)
        # transferencias y actualizaciones graficas de imagenes
        click_botones_etiquetador(None)



    def click_botones_etiquetador( e: ft.ControlEvent | None ):
        """Actualiza etiquetas, estado, estadisticas y estilo de bordes de las imagenes en base al boton del etiquetador accionado."""
        # acceso a elementos globales
        global imagenes_galeria
        global dimensiones_elegidas 
        global clave

        if len(imagenes_galeria)>0:
            # prevencion de errores por posible clave inexistente
            # (suele pasar al cambiar las condiciones de filtrado de imagenes)
            try:
                imagen_seleccionada = imagen_clave(clave, imagenes_galeria) 

                # Se transfieren los tags de la botonera a las imagenes 
                etiquetas_botones = etiquetador_imagen.leer_botones()
                imagen_seleccionada.agregar_tags(etiquetas_botones, sobreescribir=True)

                # actualizacion bordes galeria
                imagen_seleccionada.verificar_imagen(dimensiones_elegidas)
                imagen_seleccionada.verificar_guardado_tags()
                imagen_seleccionada.actualizar_estilo_estado()
            except:
                print(f"[bold red]Imagen '{clave}' no disponible en galeria")


        # actualizacion grafica de todos los componentes
        actualizar_componentes() 
            
        # renovar lista de etiquetas
        estadisticas()
   

    def actualizar_lista_dimensiones():
        """Reduce la lista de dimensiones seleccionables en base al tamaño detectado de las imagenes de galeria."""
        # acceso a elementos globales
        global imagenes_galeria
        lista_resoluciones = [tupla_resoluciones[0]] # opcion "No filtrar" agregada
        set_dimensiones = set()

        for imagen in imagenes_galeria:
            dimensiones = imagen.dimensiones
            set_dimensiones.add(dimensiones)

        for resolucion in tupla_resoluciones:
            resolucion_conv = convertir_dimensiones_opencv(str(resolucion))
            if resolucion_conv in set_dimensiones:
                lista_resoluciones.append(resolucion)

        opciones_lista_desplegable(lista_dimensiones_desplegable, tuple(lista_resoluciones))
        lista_dimensiones_desplegable.update()


    def crear_botones_etiquetador():
        """Crea los botones del etiquetador en base al archivo de texto indicado y a los tags ya presentes en las imagenes actuales"""

        # reestablecimiento de la estructura de dataset (solo deja tags procedentes de archivo)
        dataset.datos = dataset.datos_archivo 

        # lectura de todas las etiquetas encontradas en las imagenes
        tags_grupos = filas_filtrado.dataset.tags_grupos
        # borrado de numeros estadisticos
        for lista in tags_grupos:
            for tag in lista:
                i = tags_grupos.index(lista)
                j = lista.index(tag)
                tag = tag.split("(")[0].strip()
                tags_grupos[i][j] = tag

        # descarte de etiquetas ya incluidas desde archivo     
        tags_archivo = dataset.tags_archivo
        for tags_lista  in tags_grupos:
            i = tags_grupos.index(tags_lista )
            tags_faltantes = set(tags_lista).difference(tags_archivo)
            tags_faltantes = list(tags_faltantes)
            tags_grupos[i] = tags_faltantes

        # agregado de las etiquetas, un grupo por vez
        for lista in tags_grupos:
            dataset.agregar_tags(lista, sobreescribir=False)

        # crea la botonera de edicion
        etiquetador_imagen.leer_dataset(dataset)

        # Eventos de los botones
        etiquetador_imagen.evento_click(
            funcion_etiquetas   = click_botones_tags,
            funcion_grupo       = click_botones_etiquetador,
            funcion_comando     = click_botones_etiquetador
            )


    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        """Carga las imagenes del proyecto."""
        if e.path:
            # acceso a elementos globales
            global imagenes_galeria
            global imagenes_seleccion, imagenes_tags
            global directorio
            global todas_imagenes
            # busqueda 
            directorio = e.path
            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            todas_imagenes = cargar_imagenes(rutas_imagen) 

            # reinicio de las listas de imagenes
            imagenes_seleccion = todas_imagenes
            imagenes_tags = todas_imagenes
            imagenes_galeria = todas_imagenes

            # asignacion de la primera imagen de la galeria 
            global clave
            if len(imagenes_galeria)>0:         
                clave = imagenes_galeria[0].clave
                etiquetador_imagen.setear_salida(imagenes_galeria[0]) # Previene falsas modificaciones al cambiar de carpeta
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes abierto.\nRuta: {directorio} \nNº imágenes: {len(imagenes_galeria)}")
 
            else:
                clave = ""
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes vacío.\nRuta: {directorio} ")

            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones() 
            # relectura del archivo dataset (puede no existir)
            global ruta_dataset
            dataset.ruta = ruta_dataset
            dataset.leer_archivo()
            # actualizacion de la app
            cargar_galeria_componentes()


    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        """Carga el archivo de texto con las etiquetas del proyecto."""
        if e.files:
            archivo = e.files[0]    
            # lectura del archivo de dataset               
            global ruta_dataset
            ruta_dataset = archivo.path
            dataset.ruta = ruta_dataset
            dataset.leer_archivo()
            cargar_galeria_componentes()
            # reporte por snackbar
            ventana_emergente(pagina, f"Archivo de  dataset abierto\nNombre archivo: {ruta_dataset}")


    def cargar_galeria_componentes(  e: ft.ControlEvent | None = None ):
        """Muestra las imagenes encontradas y las asigna a los componentes de seleccion y etiquetado. Si no hay imágenes que mostra oculta y/o inhabilita componentes."""
        # acceso a elementos globales
        global imagenes_galeria
        global ruta_dataset
        global clave

        # si se encuentran imagenes se visibilizan y configuran los controles
        filtrar_dimensiones_estados()   
        # agregado de todas las etiquetas al editor
        crear_botones_etiquetador()  
        # actualizar galeria
        actualizar_estilo_estado( imagenes_galeria, estilos_galeria )
        # actualizacion grafica
        actualizar_componentes()

    
    def imagen_seleccion(imagen: Contenedor_Etiquetado):
        """Actualiza imagen y estilo de bordes del selector de imagen"""
        contenedor_seleccion.ruta_imagen = imagen.ruta
 
        if imagen.defectuosa :
            estilo = "erroneo"      
        elif imagen.modificada :
            estilo = "modificado"
        elif imagen.guardada :
            estilo = "guardado"  
        else: 
            estilo = "predefinido"  

        contenedor_seleccion.estilo(estilos_seleccion[estilo]) 
        contenedor_seleccion.update()

        #textos informativos
        ruta = pathlib.Path(imagen.ruta)
        nombre = ruta.name
        indice = imagenes_galeria.index(imagen)
        tags = imagen.tags
        n = len(imagenes_galeria)
        texto_imagen.value = f"{indice+1}/{n} - '{nombre}'"
        texto_imagen.visible = True 
        texto_imagen.update()
        texto_ruta_titulo.value = f"Ruta archivo:"
        texto_ruta_titulo.visible = True
        texto_ruta_titulo.update()
        texto_ruta_data.value = f"{ruta}"
        texto_ruta_data.visible = True
        texto_ruta_data.update()
        texto_tags_titulo.value = f"Tags imagen ({len(tags)}):"
        texto_tags_titulo.visible = True
        texto_tags_titulo.update()
        texto_tags_data.value = f"{etiquetas2texto(tags)}"
        texto_tags_data.visible = True
        texto_tags_data.update()


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Este handler permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        global clave
        clave = contenedor.clave
        # asigna imagen y estilo de bordes a la pestaña de etiquetado
        actualizar_componentes()
        #cambio de pestaña
        pestanias.selected_index = Tab.TAB_SELECCION.value
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        global clave
        apuntar_galeria( clave)   
        #cambio de pestaña
        pestanias.selected_index = Tab.TAB_GALERIA.value
        pagina.update()


    def filtrar_dimensiones_estados( e: ft.ControlEvent | None = None):
        """Selecciona solamente aquellas imagenes que cumplan con el tamaño y estado especificados."""
        global imagenes_galeria
        # global imagenes_seleccion
        global todas_imagenes

        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        global dimensiones_elegidas 
        opcion = lista_dimensiones_desplegable.value
        dimensiones_elegidas = convertir_dimensiones_opencv(str(opcion))

        # Filtrado en base a las dimensiones de imagen
        dimensiones = dimensiones_elegidas if boton_filtrar_dimensiones.estado else None
        imagenes_galeria = filtrar_dimensiones(todas_imagenes, dimensiones)

        # Filtrado en base a los estados de las imagenes
        estado = lista_estados_desplegable.value
        imagenes_galeria = filtrar_estados(imagenes_galeria, estado)

        # marcado de bordes según las dimensiones requeridas 
        for imagen in imagenes_galeria:
            imagen.verificar_imagen(dimensiones_elegidas)

        # reporte por snackbar 
        if len(todas_imagenes) > 0 and estado != None:
            ventana_emergente(pagina, f"Filtrado por dimensiones y estado - {len(imagenes_galeria)} imagenes seleccionadas.")
        # actualizacion de las etiquetas encontradas
        estadisticas()

        # respaldo para que funcione el filtro de etiquetas
        global imagenes_tags
        imagenes_tags = imagenes_galeria


    def guardar_cambios(e:ft.ControlEvent | None = None):
        """Guarda las etiquetas en archivo de todas las imagenes modificadas. También actualiza estados y graficas."""
        
        global imagenes_galeria
        if len(imagenes_galeria) == 0 : 
            ventana_emergente(pagina,f"Galería vacía - sin cambios")
            return
        imagen: Contenedor_Etiquetado
        i = 0
        for imagen in imagenes_galeria:  #
            guardado = imagen.guardar_archivo()
            if guardado :
                i += 1 
        for imagen in imagenes_galeria:
            imagen.verificar_guardado_tags()
        # reporte por snackbar
        if i == 0:
            ventana_emergente(pagina,f"Etiquetas sin cambios")
        else:
            ventana_emergente(pagina,f"¡Etiquetas guardadas! - {i} archivos modificados")
        # actualizacion grafica
        actualizar_componentes(e)    
        cerrar_dialogo(e)  


    # confirmar_cambios
    def abrir_dialogo_guardado(e:ft.ControlEvent | None = None):

        global imagenes_galeria
        # conteo imagenes a guardar
        j = 0
        for imagen in imagenes_galeria:  
            if imagen.modificada:
                j += 1 

        if j == 0:
            # se ignora (nada que hacer)
            ventana_emergente(pagina, "Sin cambios para guardar.")
            return
        else:
            # pedido de confirmacion
            pagina.dialog = ft.AlertDialog(
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
            pagina.dialog.open = True
            pagina.update()

    def cerrar_dialogo(e):
        pagina.dialog.open = False
        pagina.update()


    def confirmar_cierre_programa(e:ft.ControlEvent):
        if e.data == "close":
            global imagenes_galeria
            # conteo imagenes con cambios sin guardar
            j = 0
            for imagen in imagenes_galeria:  
                if imagen.modificada:
                    j += 1 

            # si no hay modificaciones realizadas se cierra directamente
            if j==0:
                cerrar_programa()
            else:
                pagina.dialog = ft.AlertDialog(
                    modal=False,
                    title=ft.Text("¿Descartar cambios y salir?"),
                    content=ft.Text(f"Hay {j} imágenes con modificaciones sin guardar."),
                    actions=[
                        ft.ElevatedButton(
                            "Sí", 
                            on_click=cerrar_programa,
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
                pagina.dialog.open = True
                pagina.update()


    def cerrar_programa(e:ft.ControlEvent | None = None):
        pagina.window_destroy()


    # prevencion decierre directo de aplicacion
    pagina.window_prevent_close = True
    pagina.on_window_event = confirmar_cierre_programa

    def ventana_emergente(pagina:ft.Page, texto: str):
        pagina.show_snack_bar(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )


    def actualizar_componentes( e: ft.ControlEvent | None = None):
        """Asigna la imagen actual a los componentes de seleccion y etiquetado en base a la 'clave' global.
        Si ésta no se encuentra en la galeria actual busca la primera imagen disponible y actualiza la clave.
        Tambien carga las imagenes disponibles a la galeria gráfica.
        Si la galeria queda vacia se ocultan los componentes graficos
        """
        global imagenes_galeria 
        global clave

        # actualizar galeria
        galeria.cargar_imagenes( imagenes_galeria )
        galeria.eventos(click = click_imagen_galeria)
        galeria.update()

        if len(imagenes_galeria)>0:
            # busqueda imagen
            indice = indice_clave(clave, imagenes_galeria)
            # si la clave actual no se encuentra se toma la primera imagen disponible
            if indice == None:
                ci = clave
                imagen_elegida = imagenes_galeria[0] 
                clave = imagen_elegida.clave 
                cf = clave
                print(f"[bold yellow]cambio imagen: de '{ci}' a '{cf}'")

            # seleccion imagen
            imagen_elegida = imagen_clave(clave, imagenes_galeria)
            etiquetador_imagen.setear_salida(imagen_elegida)
            imagen_seleccion(imagen_elegida)

            columna_seleccion.visible = True
            columna_seleccion.update()
            etiquetador_imagen.habilitado = True
            etiquetador_imagen.update()

        else:
            # ocultamiento de componentes graficos
            columna_etiquetas.visible = False
            columna_etiquetas.update()
            columna_seleccion.visible = False
            columna_seleccion.update()
            etiquetador_imagen.habilitado = False
            etiquetador_imagen.update()


    def filtrar_todas_etiquetas( e: ft.ControlEvent ):
        """Selecciona las imagenes con al menos una de las etiquetas activadas en la pestaña de estadisticas."""
    
        global imagenes_galeria
        global imagenes_tags

        if boton_filtrar_etiquetas.estado:
            # lectura de tags seleccionados
            set_etiquetas = set()
            tags_conteo = filas_filtrado.leer_botones()
            for tag in tags_conteo:
                # extraccion del numero de repeticiones
                texto = tag.split("(")[0].strip()
                set_etiquetas.add(texto)

            # inicializacion previa al filtrado
            imagenes_galeria = imagenes_tags

            # filtrado - si no hay etiquetas de entrada devuelve todo
            imagenes_galeria = filtrar_etiquetas(imagenes_galeria, list(set_etiquetas))
            # foco en la galeria
            pestanias.selected_index = Tab.TAB_GALERIA.value
            pestanias.update()

            # reporte por snackbar
            renglon1 = f"Filtrado por etiquetas habilitado"
            renglon2 = f" - {len(set_etiquetas)} de {len(tags_conteo)} etiquetas seleccionadas;"
            renglon3 = f" - {len(imagenes_galeria)}  de {len(imagenes_tags)} imagenes seleccionadas."
            ventana_emergente(pagina, 
                f"{renglon1}\n{renglon2}\n{renglon3}")
            columna_etiquetas.visible = True
            columna_etiquetas.update()
        else:
            ventana_emergente(pagina, f"Filtrado por etiquetas deshabilitado.")
            columna_etiquetas.visible = False
            columna_etiquetas.update()

        # actualizacion grafica
        actualizar_componentes() # incluye prevencion de errores por clave inexistente



    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        global imagenes_galeria
        global clave

        numero_imagenes = len(imagenes_galeria)
        if numero_imagenes > 0:
            # prevencion de errores por posible clave inexistente
            indice = indice_clave(clave, imagenes_galeria)
            if indice == None:
                clave = imagenes_galeria[0].clave

            imagen = imagen_clave(clave, imagenes_galeria)
            indice = imagenes_galeria.index(imagen)
            # cambio de imagen seleccionada
            cambiar_imagen = False
            # avanzar
            if tecla == "A" or tecla =="Page Up":
                indice -= 1 
                indice = indice if indice>0 else 0
                cambiar_imagen = True
            # retroceder
            elif tecla == "D" or tecla=="Page Down":
                indice += 1 
                indice = indice if indice<numero_imagenes else numero_imagenes-1
                cambiar_imagen = True
            # ir al inicio
            elif tecla == "Home":
                indice = 0
                cambiar_imagen = True
            # ir al final
            elif tecla == "End":
                indice = numero_imagenes - 1
                cambiar_imagen = True
            # restaurar imagen actual
            elif tecla == " ":  #  barra espaciadora
                etiquetador_imagen.restablecer_etiquetas("")
            # guardar imagen actual
            elif tecla == "W": 
                etiquetador_imagen.guardar_etiquetas("")
            
            if cambiar_imagen:
                imagen: Contenedor_Etiquetado
                # actualizacion de parametros
                imagen = imagenes_galeria[indice]
                clave = imagen.clave 
                # carga de imagen
                actualizar_componentes()
                apuntar_galeria(clave)


    def cambio_pestanias(e):
        global imagenes_galeria
        global clave
        if len(imagenes_galeria)>0:
            if pestanias.selected_index == Tab.TAB_GALERIA.value:
                apuntar_galeria(clave)


    ###########  FUNCIONES LOCALES #################

    # Creacion de imagenes con su propio contenedor por duplicado con distintas resoluciones
    # (Compartir una misma imagen en distintos contenedores funciona mal)
    def cargar_imagenes(rutas: list[str]):
        # Imagenes - objetos ft.Image con etiquetas leidas desde archivo TXT- baja resolucion
        galeria = []
        galeria = leer_imagenes_etiquetadas(
            rutas,
            ancho=128,
            alto=128, 
            redondeo=10
            )
        return galeria


    def apuntar_galeria(clave):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su numero ('key')."""
        galeria.scroll_to(key=clave, duration=500)


    def reset_tags_filtros(e: ft.ControlEvent):
        """Restaura todos los botones de filtrado."""
        filas_filtrado.agregar_tags([], True)
        filtrar_todas_etiquetas(e)

    def guardar_tags_archivo(e: ft.FilePickerResultEvent):
        if e.path :
            ruta = e.path
            texto=f"Guardado de etiquetas en archivo\nRuta: {ruta}"

            # creación / borrado de archivo
            guardar_archivo(ruta,"",modo="w" )
            # escritura de archivo,un renglon por grupo
            tags_grupos = dataset.tags_grupos
            for lista in tags_grupos:
                texto = etiquetas2texto(lista) + "\n"
                guardar_archivo(ruta,texto,modo="a" )

        else :
            texto=f"Guardado cancelado"
        # etiquetador_imagen.guardar_dataset(INCOMPLETO)
        ventana_emergente(pagina, texto)


    def estadisticas()->dict:
        """Detecta todas las etiquetas usadas en las imagenes y cuenta cuantas repeticiones tiene cada una.
        Crea tambien los botones de filtrado correspondientes a cada una."""

        global imagenes_galeria
        conteo_etiquetas = dict()

        # busqueda de etiquetas
        for imagen in imagenes_galeria:  
            for tag in imagen.tags:
                conteo_etiquetas[tag] = 0

        # conteo de repeticiones para cada etiqueta
        for imagen in imagenes_galeria:
            for tag in imagen.tags:
                conteo_etiquetas[tag] += 1

        # etiquetas ordenadas de más repetidas a menos usadas
        conteo_etiquetas = dict(sorted(conteo_etiquetas.items(), key=lambda item:item[1], reverse=True))

        nro_tags = len(conteo_etiquetas.keys()) 
        lista_tags = list(conteo_etiquetas.keys()) 

        texto_contador_tags.value = f"Etiquetas encontadas: {nro_tags}"

        boton_reset_tags.text = f"Deseleccionar tags"
        # boton_reset_tags.text = f"Deseleccionar etiquetas ({nro_tags} en total)"

        tags_contadas = []
        for tag in lista_tags:
            tags_contadas.append(f"{tag}  ({conteo_etiquetas[tag]})")

        # objeto auxiliar vacio para almacenar etiquetass    
        etiquetas_marcadas = Etiquetas()

        tags_grupo = []

        # reparto en grupos y coloreo de botones en base a percentiles del 20%
        umbral_1 = int(nro_tags * Percentil.UMBRAL_1.value)
        umbral_2 = int(nro_tags * Percentil.UMBRAL_2.value)
        umbral_3 = int(nro_tags * Percentil.UMBRAL_3.value)
        umbral_4 = int(nro_tags * Percentil.UMBRAL_4.value)
        umbral_5 = int(nro_tags * Percentil.UMBRAL_5.value)

        for i in range(0, umbral_1):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_1, umbral_2):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_2, umbral_3):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_3, umbral_4):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_4, umbral_5):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        filas_filtrado.leer_dataset(etiquetas_marcadas, False)
        filas_filtrado.agregar_tags([], True)
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
  
        columna_etiquetas.update()

        return conteo_etiquetas


    def redimensionar_controles(e: ft.ControlEvent | None):

        # redimensionado etiquetador:
        etiquetador_imagen.base   = int(pagina.width/2)
        etiquetador_imagen.altura = pagina.height - 180
        filas_filtrado.altura = pagina.height - 240
        columna_etiquetas.height = pagina.height - 180
        columna_etiquetas.update()
        etiquetador_imagen.update()
        fila_controles.width = pagina.width 
        fila_controles.update() 


    ###########  ASIGNACION HANDLERS #################

    pagina.on_resize = redimensionar_controles
    
    # 
    lista_dimensiones_desplegable.on_change = cargar_galeria_componentes    
    lista_estados_desplegable.on_change = cargar_galeria_componentes     
    boton_filtrar_dimensiones.click_boton = cargar_galeria_componentes   
    boton_filtrar_etiquetas.click_boton = filtrar_todas_etiquetas
    boton_reset_tags.on_click = reset_tags_filtros
    # inicializacion opciones
    boton_filtrar_dimensiones.estado = False
    boton_filtrar_etiquetas.estado = False

    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = desplazamiento_teclado
    
    pestanias.on_change = cambio_pestanias

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio      = ft.FilePicker(on_result = resultado_directorio )
    dialogo_dataset         = ft.FilePicker(on_result = resultado_dataset)
    dialogo_guardado_tags   = ft.FilePicker(on_result = guardar_tags_archivo)

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, dialogo_dataset, dialogo_guardado_tags
        ])

    boton_guardar.on_click = abrir_dialogo_guardado

    contenedor_seleccion.on_click = click_imagen_seleccion

    ############## CONFIGURACIONES GRAFICAS ################     
     
    ancho_pagina = 1400

    galeria.ancho = ancho_pagina 
    fila_controles.width = ancho_pagina 

    etiquetador_imagen.altura = altura_tab_etiquetado
    etiquetador_imagen.base = 500
    etiquetador_imagen.expand = True
    etiquetador_imagen.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = ancho_pagina
    pagina.window_min_width  = 1024
    pagina.window_height = 900
    # pagina.theme_mode = ft.ThemeMode.DARK
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)