

from rich import print as print
import flet as ft

from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor, imagen_clave
from componentes.menu_navegacion import  MenuNavegacion
from componentes.etiquetador_botones import EtiquetadorBotones , BotonBiestable
from componentes.estilos_contenedores import estilos_seleccion, estilos_galeria
from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from sistema_archivos.buscar_extension import buscar_imagenes

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen


# reasignacion de dimensiones para las imagenes de galeria
estilos_galeria["predefinido"]. width   = 128
estilos_galeria["predefinido"]. height  = 128
estilos_galeria["guardado"].    width   = 128
estilos_galeria["guardado"].    height  = 128
estilos_galeria["modificado"].  width   = 128
estilos_galeria["modificado"].  height  = 128
estilos_galeria["erroneo"].     width   = 128
estilos_galeria["erroneo"].     height  = 128



def nada( e ):
    pass


class Contenedor_Etiquetado( Etiquetas, Contenedor_Imagen):
    def __init__(self, ruta, ancho=768, alto=768, redondeo=0):
        Etiquetas.__init__(self, ruta)
        Contenedor_Imagen.__init__(self,ruta, ancho, alto, redondeo)
        self.__etiquetada = False
        self.__guardada = False
        self.__defectuosa = False
        self.__dimensiones: tuple[int, int, int] | None
        self.leer_dimensiones()
        self.verificar_imagen( None)   # Modificar
        self.verificar_etiquetado()
        self.verificar_guardado(None)


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


    def verificar_imagen(self, dimensiones: tuple[int, int, int] | None):
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
    def defectuosa(self):
        return self.__defectuosa


    def verificar_etiquetado(self):
        """Verifica si hay etiquetas en la imagen, ya sea guardadas o sin guardar """
        self.__etiquetada = True if len(self.tags) > 0 else False


    @property
    def etiquetada(self):
        return self.__etiquetada 


    def verificar_guardado(self , tags: list[str] | None):
        """Comprueba si las etiquetas actuales son las mismas que las guardas en archivo de texto"""
        archivado = Etiquetas(self.ruta)
        if tags == None:
            guardado = True if set(self.tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        else:    
            guardado = True if set(tags) == set(archivado.tags) else False   # si los tags son iguales da True; en caso contrario da False
        # se lee cuantas etiquetas hay en archivo
        etiquetado = True if len(archivado.tags) > 0 else False
        self.__guardada = guardado  and etiquetado     # se descartan no etiquetados


    @property
    def guardada(self):
        return self.__guardada 

    @guardada.setter
    def guardada(self, valor: bool):
        self.__guardada = valor


class MenuEtiquetado( MenuNavegacion):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.alto  = 800
        self.ancho = 600
        

    def cargar_imagen(self):
        """"Este metodo carga la imagen y cambia el estilo del contenedor segun el estado del etiquetado"""
        super().cargar_imagen()
        indice = self.indice
        contenedor_imagen = self.imagenes[indice]
        # seleccion de estilo segun jerarquia
        actualizar_estilo_estado( [contenedor_imagen], self.estilos)


    def cargar_imagenes(self, imagenes: list[Contenedor]):
        super().cargar_imagenes(imagenes)
        # self.__contenedores_imagen 
        # actualizar_estilo_estado( self.__contenedores_imagen , self.estilos)
        actualizar_estilo_estado( imagenes, self.estilos)


class GaleriaEtiquetado( Galeria):
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos
        self.imagenes: list[Contenedor_Etiquetado ]

    # def leer_imagenes(self, rutas_imagen: list[str], ancho=256, alto=256, redondeo=0,  cuadricula=True):
    #     self.wrap = cuadricula # version galería (si es 'False' las imagenes van en linea)
        
    #     contenedores = leer_imagenes_etiquetadas(rutas_imagen, ancho, alto, redondeo)
    #     self.numero = len(contenedores)
    #     self.controls = contenedores

    #     actualizar_estilo_estado( contenedores, self.estilos)


    def cargar_imagenes(self, 
        imagenes: list[Contenedor_Etiquetado ], 
        cuadricula=True):
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        self.actualizar_estilos( )  


    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    


def actualizar_estilo_estado(
    contenedores: list[Contenedor_Etiquetado], estilos : dict ):
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
        # contenedor.content.key = str(i)
        contenedor.content.key = f"imag_{i}"
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
    # estado = lista_estados.value
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
imagenes_etiquetadas = []
imagenes_etiquetadas_backup = []
imagenes_galeria_backup = []
imagenes_etiquetadas_filtradas_backup = []
imagenes_galeria_filtradas_backup = []

botones_tags = []


tupla_estados = (
    "todas",
    "guardadas",
    "modificadas",
    "no etiquetadas"
)



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
    )

    boton_dataset = ft.ElevatedButton(
        text = "Abrir dataset",
        icon=ft.icons.FILE_OPEN,
        bgcolor=ft.colors.BLUE,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_dataset.pick_files(
            dialog_title= "Elegir archivo TXT con todas las etiquetas",
            allowed_extensions=["txt"],
            allow_multiple=False,
        )
    )

    boton_filtrar_dimensiones = BotonBiestable("Filtrar por tamaño", ft.colors.BROWN_100, ft.colors.BROWN_800)
    boton_filtrar_dimensiones.color = ft.colors.WHITE

    boton_filtrar_etiquetas = BotonBiestable("Filtrar por etiquetas", ft.colors.PURPLE_100, ft.colors.PURPLE_800)
    boton_filtrar_etiquetas.color = ft.colors.WHITE

    # lista desplegable para elegir las dimensiones de imagen correctas
    lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones, ancho=120)

    lista_estados = crear_lista_desplegable(tupla_estados, ancho=120)

    # Componentes gráficos
    etiquetador_imagen = EtiquetadorBotones()
    galeria = GaleriaEtiquetado( estilos_galeria )
    menu_seleccion = MenuEtiquetado( estilos_seleccion)

    # textos
    texto_dimensiones = ft.Text("Dimensiones\nimagen:")
    texto_estados = ft.Text("Estado\netiquetado:")

    #############  MAQUETADO ############################

    # Fila de botones para abrir carpetas y leer archivos
    pagina.add(ft.Row([
        boton_carpeta,
        boton_dataset,
        ft.VerticalDivider(visible=True, width=20),
        texto_dimensiones,
        lista_dimensiones_desplegable,
        boton_filtrar_dimensiones,
        ft.VerticalDivider(visible=True, width=20),
        texto_estados,
        lista_estados,
        # ft.VerticalDivider(visible=True, width=20),
        boton_filtrar_etiquetas,
        ]))

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=galeria,
        )

    # pestaña de etiquetado y navegacion de imagenes
    altura_tab_etiquetado = 800
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            menu_seleccion ,
            ft.VerticalDivider(),
            etiquetador_imagen
            ], 
        spacing = 10, 
        height = altura_tab_etiquetado
    ) 
    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=fila_etiquetado_navegacion,
    )
    tab_estadisticas = ft.Tab(
        text="Estadisticas",
        content= ft.Column(
            controls = [],
            spacing = 10, 
            height = altura_tab_etiquetado,
            width = 800,
            scroll=ft.ScrollMode.AUTO,
        )
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            tab_galeria   ,
            tab_etiquetado,
            tab_estadisticas,
        ],
        expand=1,
        # disabled=True,        # deshabilita controles internos, no las pestañas en si
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)

    ############## HANDLERS ##################################

    def etiquetas_a_imagen(indice: int):
        global imagenes_etiquetadas
        global imagenes_galeria
        # Se transfieren los botones de la botonera a las imagenes 

        etiquetas_botones = etiquetador_imagen.leer_botones()
        imagenes_galeria[indice].tags = etiquetas_botones
        imagenes_etiquetadas[indice].tags = etiquetas_botones
        # etiquetador_imagen.update()
        return etiquetas_botones


    def etiquetas_a_botones(indice: int):
        global imagenes_etiquetadas
        # Se transfieren los botones de la imagen  a la botonera 
        etiquetas_imagen = imagenes_etiquetadas[indice].tags 

        # actualizacion grafica
        etiquetador_imagen.asignar_etiquetas(etiquetas_imagen)
        return etiquetas_imagen


    def actualizar_bordes( e: ft.ControlEvent ):

        # acceso a elementos globales
        global imagenes_etiquetadas
        global imagenes_galeria
        global dimensiones_elegidas 

        indice = menu_seleccion.indice
        # Se transfieren los botones de la botonera a las imagenes 
        etiquetas_botones = etiquetas_a_imagen(indice)

        # actualizacion bordes galeria
        imagenes_galeria[indice].verificar_etiquetado()
        imagenes_galeria[indice].verificar_imagen(dimensiones_elegidas)
        imagenes_galeria[indice].verificar_guardado(etiquetas_botones)
        imagenes_galeria[indice].update()

        # actualizacion bordes selector
        imagenes_etiquetadas[indice].verificar_etiquetado()
        imagenes_etiquetadas[indice].verificar_imagen(dimensiones_elegidas)
        imagenes_etiquetadas[indice].verificar_guardado(etiquetas_botones) 
        imagenes_etiquetadas[indice].update()

        menu_seleccion.cargar_imagen()
        menu_seleccion.update()

        galeria.cargar_imagenes( imagenes_galeria )
        galeria.update()

        # renovar lista de etiquetas
        estadisticas()
   

    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        if e.path:

            # acceso a elementos globales
            global imagenes_etiquetadas
            global imagenes_galeria

            # busqueda 
            directorio = e.path
            rutas_imagen = buscar_imagenes(directorio)
            # Carga de imagenes del directorio
            imagenes_etiquetadas, imagenes_galeria = cargar_imagenes(rutas_imagen)

            # copias de respaldo para los filtros de imagenes
            global imagenes_etiquetadas_backup
            global imagenes_galeria_backup
            imagenes_etiquetadas_backup = imagenes_etiquetadas
            imagenes_galeria_backup = imagenes_galeria

            # actualizar lista dimensiones
            lista_resoluciones = [tupla_resoluciones[0]] # opcion "No filtrar" agregada
            set_dimensiones = set()

            for imagen in imagenes_etiquetadas:
                dimensiones = imagen.dimensiones
                set_dimensiones.add(dimensiones)

            for resolucion in tupla_resoluciones:
                resolucion_conv = convertir_dimensiones_opencv(str(resolucion))
                if resolucion_conv in set_dimensiones:
                    lista_resoluciones.append(resolucion)

            opciones_lista_desplegable(lista_dimensiones_desplegable, tuple(lista_resoluciones))
            lista_dimensiones_desplegable.update()

            # iniciar pestaña estadisticas - todas las etiquetas
            estadisticas()

            # Objeto galeria
            galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_imagen_galeria)
            galeria.update()

            # Objeto seleccion imagen
            menu_seleccion.cargar_imagenes(imagenes_etiquetadas)
            menu_seleccion.indice = 0
            menu_seleccion.cargar_imagen()
            menu_seleccion.eventos(
                click=click_imagen_seleccion,
                funcion_botones = lambda _ : click_botones_seleccion(_)
                )
            # actualizacion del etiquetador --> habilita los controles y etiquetas
            etiquetador_imagen.setear_salida(imagenes_etiquetadas[0])
            etiquetador_imagen.update()

            # actualizacion del selector de imagenes --> habilita los controles
            menu_seleccion.alto  = altura_tab_etiquetado
            menu_seleccion.ancho = 600
            menu_seleccion.expand = True
            menu_seleccion.habilitado = True
            menu_seleccion.update()

            # reporte por consola
            print("[bold red]Carga imagenes")
            print("[bold red]Nº imagenes etiquetadas : ", len(imagenes_etiquetadas))
            print("[bold red]Nº imagenes galeria     : ", len(imagenes_galeria))

            # verificacion de dimensiones al abrir
            filtrar_dimensiones_estados("")     # FIX


    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        if e.files:
            ruta = e.files[0]                   
            archivo_dataset = ruta.path

            global dataset

            # Objeto etiquetador
            dataset = Etiquetas(archivo_dataset) 
            etiquetador_imagen.leer_dataset( dataset )

            # se asegura que los botones esten deshabilitados hasta abrir galeria
            etiquetador_imagen.habilitado = True if menu_seleccion.habilitado else False
            etiquetador_imagen.update() 

            etiquetador_imagen.alto  = altura_tab_etiquetado
            etiquetador_imagen.ancho = 500
            etiquetador_imagen.expand = True
            etiquetador_imagen.update()

            # Eventos de los botones
            etiquetador_imagen.evento_click(
                actualizar_bordes,
                actualizar_bordes,
                actualizar_bordes
                )
            print("[bold cyan]Carga dataset")
            print("[bold cyan]Nombre archivo: ", archivo_dataset)


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Esta imagen permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        contenedor = e.control
        clave = contenedor.content.key
        global imagenes_etiquetadas
        global imagenes_galeria
        # actualizacion de imagen seleccionada y etiquetado
        imagen_seleccionada = imagen_clave(clave, imagenes_etiquetadas)
        # actualizacion del indice
        indice = imagenes_etiquetadas.index(imagen_seleccionada)
        # actaualizacion de controles
        etiquetador_imagen.setear_salida(imagen_seleccionada)
        menu_seleccion.indice = indice
        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)
        #cambio de pestaña
        pestanias.selected_index = 1
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        global imagenes_etiquetadas
        #regreso a la galeria
        indice = menu_seleccion.indice
        clave = imagenes_etiquetadas[indice].content.key
        apuntar_galeria( clave)   
        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)
        #cambio de pestaña
        pestanias.selected_index=0
        pagina.update()


    def filtrar_dimensiones_estados( _ ):
        global imagenes_etiquetadas
        global imagenes_galeria
        global imagenes_etiquetadas_backup
        global imagenes_galeria_backup

        # restauracion temporal de las imagenes 
        imagenes_galeria = imagenes_galeria_backup
        imagenes_etiquetadas = imagenes_etiquetadas_backup

        if len(imagenes_etiquetadas) == 0 or len(imagenes_galeria) == 0 :
            print("[bold cyan]Galeria vacía")
            return

        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        global dimensiones_elegidas 
        opcion = lista_dimensiones_desplegable.value
        dimensiones_elegidas = convertir_dimensiones_opencv(str(opcion))
        print(f"[bold magenta]Dimensiones imagen requeridas: [bold yellow]{dimensiones_elegidas}")

        # Filtrado en base a las dimensiones de imagen
        dimensiones = dimensiones_elegidas if boton_filtrar_dimensiones.estado else None
        imagenes_etiquetadas = filtrar_dimensiones(imagenes_etiquetadas, dimensiones)
        imagenes_galeria = filtrar_dimensiones(imagenes_galeria, dimensiones)
        # Filtrado en base a los estados de las imagenes
        estado = lista_estados.value
        imagenes_etiquetadas = filtrar_estados(imagenes_etiquetadas, estado)
        imagenes_galeria = filtrar_estados(imagenes_galeria, estado)

        # marcado de bordes según las dimensiones requeridas 
        for imagen in imagenes_etiquetadas:
            imagen.verificar_imagen(dimensiones_elegidas)
        for imagen in imagenes_galeria:
            imagen.verificar_imagen(dimensiones_elegidas)

        # Filtrado en base a las etiquetas seleccionadas
        global botones_tags 
        tags = []
        if boton_filtrar_etiquetas.estado == True:
            for boton in botones_tags:
                if boton.estado: 
                    tags.append(boton.text)

        imagenes_etiquetadas = filtrar_etiquetas(imagenes_etiquetadas, tags)
        imagenes_galeria = filtrar_etiquetas(imagenes_galeria, tags)
        # iniciar pestaña estadisticas - sólo etiquetas de imagenes filtradas
        # actualizacion de las etiquetas encontradas
        # estadisticas() # FIX
        # Actualizacion componentes graficos
        # Objeto galeria
        # galeria.cargar_imagenes( imagenes_galeria )
        # galeria.update()
        # # Objeto seleccion imagen
        # menu_seleccion.indice = 0
        # menu_seleccion.cargar_imagenes(imagenes_etiquetadas)
        # menu_seleccion.cargar_imagen()
        # menu_seleccion.update()
        # # actualizacion del etiquetador --> habilita los controles y etiquetas
        # etiquetador_imagen.setear_salida(imagenes_etiquetadas[0])
        # etiquetador_imagen.update()
        # actualizacion de las etiquetas encontradas
        estadisticas()
        actualizar_componentes()    # FIX
        # respaldo para que funcione el filtro de etiquetas
        global imagenes_etiquetadas_filtradas_backup
        global imagenes_galeria_filtradas_backup
        imagenes_etiquetadas_filtradas_backup = imagenes_etiquetadas
        imagenes_galeria_filtradas_backup = imagenes_galeria



    def actualizar_componentes():
        global imagenes_etiquetadas
        global imagenes_galeria
        # Objeto galeria
        galeria.cargar_imagenes( imagenes_galeria )
        galeria.update()
        # Objeto seleccion imagen
        menu_seleccion.indice = 0
        menu_seleccion.cargar_imagenes(imagenes_etiquetadas)
        menu_seleccion.cargar_imagen()
        menu_seleccion.update()
        # actualizacion del etiquetador --> habilita los controles y etiquetas
        etiquetador_imagen.setear_salida(imagenes_etiquetadas[0])
        etiquetador_imagen.update()



    def filtrar_todas_etiquetas(_):
        global imagenes_etiquetadas
        global imagenes_galeria
        global imagenes_etiquetadas_filtradas_backup
        global imagenes_galeria_filtradas_backup

        global botones_tags 

        set_etiquetas = set()
        for boton in botones_tags:
            if boton.estado==True:
                set_etiquetas.add(boton.text)

        print(set_etiquetas)

        imagenes_etiquetadas = imagenes_etiquetadas_filtradas_backup
        imagenes_galeria = imagenes_galeria_filtradas_backup

        if boton_filtrar_etiquetas.estado == True:
            imagenes_etiquetadas = filtrar_etiquetas(imagenes_etiquetadas, list(set_etiquetas))
            imagenes_galeria = filtrar_etiquetas(imagenes_galeria, list(set_etiquetas))

        actualizar_componentes()



    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        # Avance y retroseso de imagenes en seleccion y galeria
        incremento = 0
        if tecla == "Arrow Left" or tecla == "A":
            incremento = - 1     # retroceso
        elif tecla == "Arrow Right" or tecla == "D":
            incremento = 1      # avance
        # cambio de imagen seleccion
        menu_seleccion.cambiar_indice(incremento, 1 )


    def cambio_pestanias(e):
        indice = menu_seleccion.indice
        if menu_seleccion.maximo > 0:
            clave = imagenes_etiquetadas[indice].content.key
            if pestanias.selected_index == 0:
                apuntar_galeria(clave)


    ###########  FUNCIONES LOCALES #################

    # Creacion de imagenes con su propio contenedor por duplicado con distintas resoluciones
    # (Compartir una misma imagen en distintos contenedores funciona mal)
    def cargar_imagenes(rutas: list[str]):
        # Imagenes - objetos ft.Image con etiquetas leidas desde archivo TXT
        etiquetadas = []
        etiquetadas = leer_imagenes_etiquetadas(
            rutas,
            ancho=768,
            alto=768, 
            redondeo=30
            )
        # replica de imagenes para la galeria - menor resolucion
        galeria = []
        galeria = leer_imagenes_etiquetadas(
            rutas,
            ancho=256,
            alto=256, 
            redondeo=10
            )
        return [etiquetadas, galeria]


    def apuntar_galeria(clave):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su numero ('key')."""
        galeria.scroll_to(key=clave, duration=1000)


    def click_botones_seleccion( indice: int ):
        """ Esta funcion controla el cambio de imagen en el selector"""
        # (el cambio de imagen está integrado al componente)
        # actualizacion etiquetas
        global imagenes_etiquetadas
        global imagenes_galeria

        etiquetador_imagen.setear_salida(imagenes_etiquetadas[indice])
        # carga de etiquetas a los botones
        etiquetas_a_botones(indice)
        # actualizacion pagina
        tab_etiquetado.update()


    def estadisticas():
        global imagenes_etiquetadas
        global imagenes_galeria

        global imagenes_etiquetadas_resolucion_backup
        global imagenes_galeria_resolucion_backup

        # backup de la lista de imagenes con dimensiones correctas
        imagenes_galeria_resolucion_backup = imagenes_galeria 
        imagenes_etiquetadas_resolucion_backup = imagenes_etiquetadas

        conteo_etiquetas = dict()
        # busqueda de etiquetas
        for imagen in imagenes_etiquetadas:
            for tag in imagen.tags:
                conteo_etiquetas[tag] = 0

        # conteo 
        for imagen in imagenes_etiquetadas:
            for tag in imagen.tags:
                conteo_etiquetas[tag] += 1

        filas_conteo = []
        global botones_tags 
        botones_tags = []
        for tag in conteo_etiquetas.keys():
            boton = BotonBiestable(f"{tag}",color_true=ft.colors.BLUE_800)  
            boton.click_boton = filtrar_todas_etiquetas
            botones_tags.append(boton)
            filas_conteo.append(
                # ft.Text(f"'{tag}' : {conteo_etiquetas[tag]} ")
                ft.Row([
                    boton,
                    ft.Text(f"Aparece {conteo_etiquetas[tag]} veces"),
                    ],
                    width=300,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                )
            )
        tab_estadisticas.content = ft.Column(
            controls=filas_conteo,
            height=altura_tab_etiquetado,
            scroll=ft.ScrollMode.AUTO,
            wrap=True,
            # width=1200,
            # expand=True
        ) 
        tab_estadisticas.update()


    ###########  ASIGNACION HANDLERS #################


    # eventos deshabilitados mientras no haya imagenes cargadas
    # lista_dimensiones_desplegable.on_change = nada
    lista_dimensiones_desplegable.on_change = filtrar_dimensiones_estados  
    # lista_dimensiones_desplegable.on_change = verificar_dimensiones_imagenes   
    lista_estados.on_change = filtrar_dimensiones_estados
    # boton_filtrar_dimensiones.click_boton = nada
    boton_filtrar_dimensiones.click_boton = filtrar_dimensiones_estados
    # boton_filtrar_etiquetas.click_boton = nada
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

    ############## CONFIGURACIONES GRAFICAS ################     
     
    galeria.ancho = 1200

    menu_seleccion.alto  = altura_tab_etiquetado
    # menu_seleccion.ancho = 600
    menu_seleccion.expand = True
    menu_seleccion.habilitado = False

    etiquetador_imagen.alto  = altura_tab_etiquetado
    etiquetador_imagen.ancho = 500
    etiquetador_imagen.expand = True
    etiquetador_imagen.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = 1500
    pagina.window_height = 900
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)