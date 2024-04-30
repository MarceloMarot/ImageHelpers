

from rich import print as print
import flet as ft

from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor, imagen_clave,indice_clave, ContImag
from componentes.etiquetador_botones import EtiquetadorBotones , BotonBiestable
from componentes.estilos_contenedores import estilos_seleccion, estilos_galeria
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from sistema_archivos.buscar_extension import buscar_imagenes

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen


def nada( e ):
    pass


class Contenedor_Etiquetado( Etiquetas, Contenedor_Imagen):
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, Estilo_Contenedor] = estilos_galeria
        ):
        Etiquetas.__init__(self, ruta)
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        self.__etiquetada = False
        self.__guardada = False
        self.__defectuosa = False
        self.__dimensiones: tuple[int, ...]|None
        self.leer_dimensiones()
        self.verificar_imagen()   
        self.verificar_etiquetado()
        self.verificar_guardado()
        self.estilos = estilos


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


    def verificar_etiquetado(self)->bool:
        """Verifica si hay etiquetas en la imagen, ya sea guardadas o sin guardar """
        self.__etiquetada = True if len(self.tags) > 0 else False
        return self.__etiquetada


    @property
    def etiquetada(self)->bool:
        return self.__etiquetada 


    def verificar_guardado(self , tags: list[str] | None = None)->bool:
        """Comprueba si las etiquetas actuales son las mismas que las guardas en archivo de texto"""
        archivado = Etiquetas(self.ruta)
        if tags == None:
            guardado = True if set(self.tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        else:    
            guardado = True if set(tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        # se lee cuantas etiquetas hay en archivo
        etiquetado = True if len(archivado.tags) > 0 else False
        self.__guardada = guardado  and etiquetado     # se descartan no etiquetados
        return self.__guardada


    @property
    def guardada(self)->bool:
        return self.__guardada 


    def guardar_archivo(self)->bool:
        """
        Escribe/rescribe el archivo de etiquetas si éstas no coinciden con las indicadas. 
        Si 'tags' es 'None' se usan las etiquetas almacenadas en el objeto imagen.
        """
        guardado_exitoso = False

        self.verificar_guardado()
        self.verificar_etiquetado()
        
        if (self.guardada == False) and self.etiquetada:
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
        elif contenedor.guardada :
            estilo = estilos["guardado"]
        elif contenedor.etiquetada :
            estilo = estilos["modificado"]
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
    """
    Devuelve solamente los contenedores de imagen con el ancho y altura correctos. 
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
    etiquetas: list[str] | None = [],
    )->list[Contenedor_Etiquetado]:
    imagenes_filtradas = []
    """
    Devuelve las imagenes que tengan al menos una etiqueta de entrada. 
    Si la entrada es 'None' devuelve toda la lista de entrada.
    """
    if etiquetas == None or etiquetas == []:
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
    """
    Devuelve solamente los contenedores con el estado de etiquetado pedido. 
    """
    imagen : Contenedor_Etiquetado
    imagenes_filtradas = []
    if estado == "guardadas":
        for imagen in lista_imagenes: 
            if imagen.guardada:    
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    elif estado == "modificadas":
        for imagen in lista_imagenes: 
            if imagen.etiquetada and not imagen.guardada:   # etiquetadas pero no guardadas  
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    elif estado == "no etiquetadas":
        for imagen in lista_imagenes: 
            if not imagen.etiquetada:    
                imagenes_filtradas.append(imagen)
        return imagenes_filtradas
    else:
        # no filtrado
        return lista_imagenes


dimensiones_elegidas = None
imagenes_galeria = []
imagenes_galeria_backup = []
imagenes_galeria_filtradas_backup = []

botones_tags = []

tupla_estados = (
    "todas",
    "guardadas",
    "modificadas",
    "no etiquetadas"
)


ruta_dataset = "imag_0"


def main(pagina: ft.Page):


    ############# COMPONENTES GRAFICOS ######################## 

    # Botones apertura de ventana emergente
    boton_carpeta = ft.ElevatedButton(
        text = "Abrir carpeta",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.RED,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_directorio.get_directory_path(
            dialog_title="Elegir carpeta con todas las imágenes"
        ),
        tooltip="Abre la carpeta con todas las imágenes a etiquetar",
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
        tooltip="Elige el archivo TXT con todas las etiquetas\n(cada renglon de archivo representa un 'grupo')"
    )

    boton_filtrar_dimensiones = BotonBiestable("Filtrar por tamaño", ft.colors.BROWN_100, ft.colors.BROWN_800)
    boton_filtrar_dimensiones.color = ft.colors.WHITE

    boton_filtrar_etiquetas = BotonBiestable("Filtrar por etiquetas", ft.colors.PURPLE_100, ft.colors.PURPLE_800)
    boton_filtrar_etiquetas.color = ft.colors.WHITE

    boton_guardar = ft.FloatingActionButton(
        icon=ft.icons.ADD, bgcolor=ft.colors.YELLOW_600, tooltip="Guardar todas las etiquetas cambiadas"
    )

    # listas desplegable para elegir opciones de imagen 
    lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones, ancho=120)
    lista_estados_desplegable= crear_lista_desplegable(tupla_estados, ancho=120)

    # Componentes especiales
    etiquetador_imagen = EtiquetadorBotones()
    etiquetador_imagen.altura = pagina.height - 100

    galeria = GaleriaEtiquetado( estilos_galeria )

    # textos
    texto_dimensiones = ft.Text("Dimensiones\nimagen:")
    texto_estados = ft.Text("Estado\netiquetado:")
    texto_imagen= ft.Text("(Titulo)")
    texto_datos = ft.Text("(nada)")

    # contenedor_seleccion = Contenedor(512, 512)
    # contenedor_seleccion = Contenedor_Etiquetado("",512, 512)
    contenedor_seleccion = Contenedor_Imagen("",512,512)
    contenedor_seleccion.estilo(estilos_seleccion["predefinido"])
    contenedor_seleccion.bgcolor = ft.colors.LIGHT_BLUE

    #############  MAQUETADO ############################

    # componentes repartidos en segmentos horizontales
    fila_controles_apertura =ft.Row(
        [boton_carpeta, boton_dataset],
        width = 350,
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap = True
        )
    fila_controles_dimensiones =ft.Row(
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

    galeria.expand=1

    columna_etiquetas = ft.Column(
        controls=[],
        visible=False,
        expand=1,
        scroll=ft.ScrollMode.AUTO,
        )


    fila_galeria_etiquetas = ft.Row(
        [galeria, ft.VerticalDivider(), columna_etiquetas],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.START,
        wrap = False,
        expand=True,
        )

    # Fila de botones para abrir carpetas y leer archivos
    pagina.add(
        ft.Row([
            fila_controles_apertura,
            fila_controles_dimensiones,
            # fila_controles_estados,
            fila_controles_etiquetas
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.END,
            )
        )

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=fila_galeria_etiquetas,
        visible=True,
        )


    columna_seleccion = ft.Column(
        [texto_imagen, contenedor_seleccion, texto_datos],
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
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=0,
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
            imagen_seleccionada: Contenedor_Etiquetado|None
            imagen_seleccionada = imagen_clave(clave, imagenes_galeria) 

            # Se transfieren los tags de la botonera a las imagenes 
            etiquetas_botones = etiquetador_imagen.leer_botones()
            imagen_seleccionada.agregar_tags(etiquetas_botones, sobreescribir=True)

            # actualizacion bordes galeria
            imagen_seleccionada.verificar_etiquetado()
            imagen_seleccionada.verificar_imagen(dimensiones_elegidas)
            imagen_seleccionada.verificar_guardado()
            imagen_seleccionada.actualizar_estilo_estado()
            imagen_seleccionada.verificar_guardado(etiquetas_botones)
            imagen_seleccionada.update()

            galeria.cargar_imagenes( imagenes_galeria )
            galeria.update()

            # actualizacion bordes selector
            imagen_seleccion(imagen_seleccionada)

        # renovar lista de etiquetas
        estadisticas()
   

    def actualizar_lista_dimensiones():
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


    def crear_botones_etiquetador(ruta_dataset: str = ""):

        # lectura del archivo de dataset (si no existe el dataset queda vacio)
        dataset = Etiquetas(ruta_dataset) 

        # busqueda de todas las etiquetas encontradas en las imagenes
        conteo_etiquetas = estadisticas()
        tags_encontradas = list(conteo_etiquetas.keys())

        # se agregan al etiquetador las etiquetas faltantes encontradas
        tags_archivo = dataset.tags
        tags_faltantes = set(tags_encontradas).difference(tags_archivo)
        tags_faltantes = list(tags_faltantes)
        dataset.agregar_tags(tags_faltantes, sobreescribir=False)

        #carga al elemento grafico
        etiquetador_imagen.leer_dataset(dataset)

        # Eventos de los botones
        etiquetador_imagen.evento_click(
            # funcion_etiquetas   = click_botones_etiquetador,
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

            # busqueda 
            directorio = e.path
            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            imagenes_galeria = cargar_imagenes(rutas_imagen) 

            # copias de respaldo para los filtros de imagenes
            global imagenes_galeria_backup
            imagenes_galeria_backup = imagenes_galeria

            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones()  
            # actualizacion de la app
            cargar_galeria_componentes()

            # reporte por snackbar
            ventana_emergente(pagina, f"Directorio de imagenes abierto\nRuta: {directorio} \nNº imágenes: {len(imagenes_galeria)}")
 

    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        """Carga el archivo de texto con las etiquetas del proyecto."""
        if e.files:
            archivo = e.files[0]                   
            global ruta_dataset
            ruta_dataset = archivo.path
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
        crear_botones_etiquetador(ruta_dataset)

        if len(imagenes_galeria) > 0:
            # Objeto galeria
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_imagen_galeria)
            # estilos bordes
            actualizar_estilo_estado( imagenes_galeria, estilos_galeria )
            galeria.update()
            # asigna la primera imagen a la pestaña de etiquetado
            clave = imagenes_galeria[0].clave
            asignar_imagen_edicion(clave)
            columna_seleccion.visible = True
            columna_seleccion.update()
            etiquetador_imagen.habilitado = True
            etiquetador_imagen.update()

        else:
            ventana_emergente(pagina, f"Directorio de imagenes vacío.")
            columna_seleccion.visible = False
            columna_seleccion.update()
            etiquetador_imagen.habilitado = False
            etiquetador_imagen.update()


    def asignar_imagen_edicion(clave:str):
        """Asigna imagen a la pestaña de etiquetado. Se presupone que la clave indicada existe"""
        global imagenes_galeria
        # actualizacion de imagen seleccionada y etiquetado
        imagen_seleccionada = imagen_clave(clave, imagenes_galeria)
        # actualizacion de controles
        etiquetador_imagen.setear_salida(imagen_seleccionada) 
        etiquetador_imagen.update()
        # actualizacion de imagen
        imagen_seleccion(imagen_seleccionada)

    
    def imagen_seleccion(imagen: Contenedor_Etiquetado):
        """Actuliza imagen y estilo de bordes del selector de imagen"""
        contenedor_seleccion.ruta_imagen = imagen.ruta
        # actualizacion de estilo de bordes
        if imagen.defectuosa :
            estilo = "erroneo"    
        elif imagen.guardada :
            estilo = "guardado"
        elif imagen.etiquetada :
            estilo = "modificado"
        else: 
            estilo = "predefinido"
        contenedor_seleccion.estilo(estilos_seleccion[estilo]) 
        contenedor_seleccion.update()


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Este handler permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        global clave
        clave = contenedor.clave
        # asigna imagen y estilo de bordes a la pestaña de etiquetado
        asignar_imagen_edicion(clave)
        #cambio de pestaña
        pestanias.selected_index = 1
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        global clave
        apuntar_galeria( clave)   
        #cambio de pestaña
        pestanias.selected_index=0
        pagina.update()


    def filtrar_dimensiones_estados( e: ft.ControlEvent | None = None):
        """Selecciona solamente aquellas imagenes que cumplan con el tamaño y estado especificados."""
        global imagenes_galeria
        global imagenes_galeria_backup
        # restauracion temporal de las imagenes 
        imagenes_galeria = imagenes_galeria_backup
        # prevencion de problemas por galeria vacia 
        if len(imagenes_galeria) == 0 : 
            ventana_emergente(pagina, "Galeria vacía")
            return

        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        global dimensiones_elegidas 
        opcion = lista_dimensiones_desplegable.value
        dimensiones_elegidas = convertir_dimensiones_opencv(str(opcion))

        # Filtrado en base a las dimensiones de imagen
        dimensiones = dimensiones_elegidas if boton_filtrar_dimensiones.estado else None
        imagenes_galeria = filtrar_dimensiones(imagenes_galeria, dimensiones)
        # Filtrado en base a los estados de las imagenes
        estado = lista_estados_desplegable.value
        imagenes_galeria = filtrar_estados(imagenes_galeria, estado)

        # marcado de bordes según las dimensiones requeridas 
        for imagen in imagenes_galeria:
            imagen.verificar_imagen(dimensiones_elegidas)

        # busqueda de etiquetas presentes en imagenes
        global botones_tags 
        tags = []
        if boton_filtrar_etiquetas.estado == True:
            for boton in botones_tags:
                if boton.estado: 
                    tags.append(boton.text)

        # reporte por snackbar
        ventana_emergente(pagina, f"Filtrado por dimensiones y estado - {len(imagenes_galeria)} imagenes seleccionadas.")
        # actualizacion de las etiquetas encontradas
        estadisticas()

        # respaldo para que funcione el filtro de etiquetas
        global imagenes_galeria_filtradas_backup
        imagenes_galeria_filtradas_backup = imagenes_galeria

        # asignacion de la primera imagen de la galeria filtrada
        global clave
        clave = imagenes_galeria[0].clave
        actualizar_componentes(e)    


    def guardar_cambios(e):
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
            imagen.verificar_guardado()
        # reporte por snackbar
        if i == 0:
            ventana_emergente(pagina,f"Etiquetas sin cambios")
        else:
            ventana_emergente(pagina,f"¡Etiquetas guardadas! - {i} archivos modificados")
        # actualizacion grafica
        actualizar_componentes(e)    


    def ventana_emergente(pagina:ft.Page, texto: str):
        pagina.show_snack_bar(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )


    def actualizar_componentes( e: ft.ControlEvent | None):
        global imagenes_galeria
        global clave
        if len(imagenes_galeria):
            # Objeto galeria
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.update()
            # busqueda imagen
            imagen_elegida = imagen_clave(clave, imagenes_galeria)
            # si la clave no se encuentra se toma la primera de la lista
            if imagen_elegida == None:
                imagen_elegida = imagenes_galeria[0] 
                clave = imagen_elegida.clave 
            # seleccion imagen
            etiquetador_imagen.setear_salida(imagen_elegida)
            etiquetador_imagen.update()
            imagen_seleccion(imagen_elegida)


    def filtrar_todas_etiquetas( e: ft.ControlEvent | None ):
        """Selecciona las imagenes con al menos una de las etiquetas activadas en la pestaña de estadisticas."""
    
        global imagenes_galeria
        global imagenes_galeria_filtradas_backup
        global botones_tags 

        set_etiquetas = set()
        for boton in botones_tags:
            if boton.estado == True:
                # extraccion del numero de repeticiones
                texto = boton.text.split("(")[0]
                texto = texto.strip()
                set_etiquetas.add(texto)

        imagenes_galeria = imagenes_galeria_filtradas_backup

        # prevencion de problemas por galeria vacia 
        if len(imagenes_galeria) == 0 : 
            ventana_emergente(pagina, "Galeria vacía")
            boton_filtrar_dimensiones.estado = False
            boton_filtrar_dimensiones.update()
            return

        if boton_filtrar_etiquetas.estado == True:
            imagenes_galeria = filtrar_etiquetas(imagenes_galeria, list(set_etiquetas))

        # reporte por snackbar
        if boton_filtrar_etiquetas.estado:
            renglon1 = f"Filtrado por etiquetas habilitado"
            renglon2 = f" - {len(set_etiquetas)} de {len(botones_tags)} etiquetas seleccionadas;"
            renglon3 = f" - {len(imagenes_galeria)}  de {len(imagenes_galeria_filtradas_backup)} imagenes seleccionadas."
            ventana_emergente(pagina, 
                f"{renglon1}\n{renglon2}\n{renglon3}")
            columna_etiquetas.visible = True
            columna_etiquetas.update()
        else:
            ventana_emergente(pagina, 
                f"Filtrado por etiquetas deshabilitado.")
            columna_etiquetas.visible = False
            columna_etiquetas.update()

        # prevencion de errores por clave inexistente
        global clave
        indice = indice_clave(clave, imagenes_galeria)
        if indice == None:
            clave = imagenes_galeria[0].clave
        # actualizacion grafica
        actualizar_componentes(e)


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
            if tecla == "A" or tecla =="Page Up" or tecla == "Arrow Left":
                indice -= 1 
                indice = indice if indice>0 else 0
                cambiar_imagen = True
            # retroceder
            elif tecla == "D" or tecla=="Page Down" or tecla == "Arrow Right":
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
            
            if cambiar_imagen:
                imagen: Contenedor_Etiquetado
                # actualizacion de parametros
                imagen = imagenes_galeria[indice]
                clave = imagen.clave 
                # carga de imagen
                asignar_imagen_edicion(clave)
                apuntar_galeria(clave)


    def cambio_pestanias(e):
        global imagenes_galeria
        global clave
        if len(imagenes_galeria)>0:
            if pestanias.selected_index == 0:
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
        galeria.scroll_to(key=clave, duration=1000)


    def reset_tags_filtros(e):
        """Restaura todos los botones de filtrado."""
        global botones_tags 
        if len(botones_tags)>0:
            for boton in botones_tags:
                boton.estado = False
            filtrar_todas_etiquetas(e)


    def estadisticas()->dict:
        """Detecta todas las etiquetas usadas en las imagenes y cuenta cuantas repeticiones tiene cada una."""

        global imagenes_galeria
        global imagenes_galeria_resolucion_backup

        # backup de la lista de imagenes con dimensiones correctas
        imagenes_galeria_resolucion_backup = imagenes_galeria 
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

        boton_reset_tags = ft.ElevatedButton(
            text = f"Deseleccionar todos  ({nro_tags} tags)",
            bgcolor = ft.colors.BLUE_800,
            color = ft.colors.WHITE,
            # width = 200,
            on_click = reset_tags_filtros,
            )
        
        filas_conteo = [                
            ft.Row(
                [ boton_reset_tags],
                alignment=ft.MainAxisAlignment.CENTER,
                ),  
            ft.Divider(height=7, thickness=1) , 
            ]
        global botones_tags 
        botones_tags = []

        for tag in conteo_etiquetas.keys():
            boton = BotonBiestable(f"{tag}  ({conteo_etiquetas[tag]})",color_true=ft.colors.BLUE_800) 
            boton.click_boton = filtrar_todas_etiquetas
            botones_tags.append(boton)

        # coloreo de botones en base a percentiles
        
        for i in range(0, int(nro_tags * 0.25)):
            botones_tags[i].color_true  = ft.colors.GREEN_800
            botones_tags[i].color_false = ft.colors.GREEN_200
            botones_tags[i].bgcolor = ft.colors.GREEN_200

        for i in range(int(nro_tags * 0.25), int(nro_tags * 0.5)):
            botones_tags[i].color_true  = ft.colors.YELLOW_800
            botones_tags[i].color_false = ft.colors.YELLOW_200
            botones_tags[i].bgcolor = ft.colors.YELLOW_200

        for i in range(int(nro_tags * 0.5), int(nro_tags * 0.75)):
            botones_tags[i].color_true  = ft.colors.ORANGE_800
            botones_tags[i].color_false = ft.colors.ORANGE_200
            botones_tags[i].bgcolor = ft.colors.ORANGE_200

        for i in range(int(nro_tags * 0.75), int(nro_tags * 1)):
            botones_tags[i].color_true  = ft.colors.RED_800
            botones_tags[i].color_false = ft.colors.RED_200
            botones_tags[i].bgcolor = ft.colors.RED_200

        filas_etiquetas = ft.Row(
            controls = botones_tags,
            wrap = True,
            )
        filas_conteo.append(filas_etiquetas)

        filas_conteo.append(ft.Divider(height=7, thickness=1))
        filas_conteo.append(ft.Divider(height=7, thickness=1))

        columna_etiquetas.controls = filas_conteo
        columna_etiquetas.update()

        return conteo_etiquetas


    def redimensionar_botonera(e):

        # redimensionado etiquetador:
        etiquetador_imagen.base   = int(pagina.width/2)
        etiquetador_imagen.altura = pagina.height - 100
        etiquetador_imagen.update()


    ###########  ASIGNACION HANDLERS #################

    pagina.on_resize = redimensionar_botonera

    # eventos deshabilitados mientras no haya imagenes cargadas
    lista_dimensiones_desplegable.on_change = cargar_galeria_componentes    
    lista_estados_desplegable.on_change = cargar_galeria_componentes
    boton_filtrar_dimensiones.click_boton = cargar_galeria_componentes
    boton_filtrar_etiquetas.click_boton = filtrar_todas_etiquetas
    # inicializacion opciones
    boton_filtrar_dimensiones.estado = False
    boton_filtrar_etiquetas.estado = False

    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = desplazamiento_teclado
    
    pestanias.on_change = cambio_pestanias

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   = ft.FilePicker(on_result = resultado_directorio )
    dialogo_dataset      = ft.FilePicker(on_result = resultado_dataset)

    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, dialogo_dataset
        ])


    boton_guardar.on_click = guardar_cambios

    contenedor_seleccion.on_click = click_imagen_seleccion

    ############## CONFIGURACIONES GRAFICAS ################     
     
    galeria.ancho = 1200

    etiquetador_imagen.altura = altura_tab_etiquetado
    etiquetador_imagen.base = 500
    etiquetador_imagen.expand = True
    etiquetador_imagen.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    # pagina.window_width  = 1500
    pagina.window_width  = 1300
    # pagina.window_min_width = 1300
    pagina.window_height = 900
    # pagina.theme_mode = ft.ThemeMode.DARK
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)