from manejo_texto.procesar_etiquetas import Etiquetas
from componentes.galeria_imagenes import Galeria, Contenedor_Imagen, Estilo_Contenedor, ContImag
from componentes.estilos_contenedores import  estilos_seleccion, estilos_galeria, Estilos

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from constantes.constantes import Tab, Percentil, Estados

from componentes.galeria_etiquetado import Contenedor_Etiquetado,  actualizar_estilo_estado


def leer_imagenes_etiquetadas(rutas_imagen: list[str], ancho=1024, alto=1024, redondeo=0, nro_inicial=0):
    """Esta funcion crea lee imagenes desde archivo y crea una lista de objetos ft.Image.
    También asigna una clave ('key') a cada una.
    """
    contenedores = [] 

    for i in range(nro_inicial, nro_inicial + len(rutas_imagen)):
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

    if dimensiones != None:
        # imagenes con dimensiones correctas
        objeto_resultado = filter(lambda imagen: imagen.dimensiones == dimensiones, lista_imagenes)
        imagenes_filtradas = list(objeto_resultado)
        return imagenes_filtradas

    else:
        # caso sin dimensiones especificas
        return lista_imagenes


def filtrar_etiquetas(
    lista_imagenes: list[Contenedor_Etiquetado], 
    etiquetas: list[str]  = [],
    )->list[Contenedor_Etiquetado]:
    """
    Devuelve las imagenes que tengan al menos una etiqueta de entrada. 
    Si no hay etiquetas de entrada se devuelve toda la lista de entrada.
    """
    imagenes_filtradas = []
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
        objeto_resultado = filter(lambda imagen: imagen.guardada and not imagen.modificada, lista_imagenes)
        return list(objeto_resultado)

    # imagenes tags modificados (todas)
    elif estado == Estados.MODIFICADOS.value:
        objeto_resultado = filter(lambda imagen: imagen.modificada, lista_imagenes)
        return list(objeto_resultado)

    # no etiquetadas ni guardadas
    elif estado == Estados.NO_ALTERADOS.value:
        objeto_resultado = filter(lambda imagen: not imagen.modificada and not imagen.guardada, lista_imagenes)
        return list(objeto_resultado)

    # defectuosas por uno u otro motivo
    elif estado == Estados.DEFECTUOSOS.value:
        objeto_resultado = filter(lambda imagen: imagen.defectuosa, lista_imagenes)
        return list(objeto_resultado)

    else:
        # no filtrado
        return lista_imagenes


# Clases


class ClasificadorImagenes:
    """Clase pensada para gestionar las listas de imágenes de forma centralizada y ordenada."""
    def __init__(self):
        self.todas          : list = []
        self.seleccion      : list = []
        self.guardadas      : list = []
        self.modificadas    : list = []
        self.no_alteradas   : list = []
        self.defectuosas    : list = []

        # clave de la imagen actualmente seleccionada
        self.clave_actual: str= ""

        self.ruta_directorio : str = ""
        self.ruta_dataset : str = ""
        self.ruta_descarte : str = "descartados"

        self.dimensiones_elegidas :tuple[int, int, int]|None = None


    # def cargar_imagenes(self, 
    def leer_imagenes(self, 
        rutas_imagen: list[str], 
        estilo=estilos_galeria[Estilos.DEFAULT.value],
        agregado=False
        ):

        nro_inicial = 0 if agregado==False else len(self.todas)
        lista = []
        lista = leer_imagenes_etiquetadas(
            rutas_imagen,
            ancho    = estilo.width,
            alto     = estilo.height, 
            redondeo = estilo.border_radius,
            nro_inicial=nro_inicial
            )
        if agregado:
            # modo agregado
            self.todas.append(lista)
        else:
            # modo reinicio
            self.todas = lista


    # def verificar_imagenes(self):
    def verificar_imagenes(self, dimensiones: tuple[int, int, int]|None=None):
        """Marca como defectuosas aquellas imágenes que no cumplan con los requisitos."""
        # marcado de imagenes defectuosas según las dimensiones requeridas 
        if dimensiones!=None:
            self.dimensiones_elegidas = dimensiones
            
        for imagen in self.todas:
            imagen.verificar_imagen(self.dimensiones_elegidas)


    def filtrar_estados(self, estado: str | None):
        """Devuelve solamente los contenedores internos con el estado de etiquetado pedido."""
        return filtrar_estados(self.todas, estado )


    def filtrar_dimensiones(self,     
        lista_imagenes: list[Contenedor_Etiquetado], 
        dimensiones: tuple[int, int, int] | None = None):
        """Devuelve solamente los contenedores de imagen con el ancho y altura correctos.
        Si las dimensiones de entrada son 'None' devuelve todos los conteedores de entrada. 
        """
        return filtrar_dimensiones(self.todas, dimensiones)


    def clasificar_estados(self):
        """Reparte las imagenes de la estructura en base a sus banderines de estado."""

        # actualizacion de posibles imagenes defectuosas
        self.verificar_imagenes()

        # creacion de listas internas
        self.guardadas    = self.filtrar_estados(Estados.GUARDADOS   .value)
        self.modificadas  = self.filtrar_estados(Estados.MODIFICADOS .value)
        self.no_alteradas = self.filtrar_estados(Estados.NO_ALTERADOS.value)
        self.defectuosas  = self.filtrar_estados(Estados.DEFECTUOSOS .value)


    def seleccionar_estado(self, estado)->list:
        """Selecciona las imágenes de una de las categorías internas. Actualiza las listas antes de asignar"""
        self.clasificar_estados()

        if estado == Estados.MODIFICADOS.value:
            self.seleccion = self.modificadas
        elif estado == Estados.GUARDADOS.value:
            self.seleccion = self.guardadas
        elif estado == Estados.NO_ALTERADOS.value:
            self.seleccion = self.no_alteradas
        elif estado == Estados.DEFECTUOSOS.value:
            self.seleccion = self.defectuosas
        elif estado == Estados.TODOS.value:
            self.seleccion = self.todas

        return self.seleccion



# Componentes globales

# clasificador_imagenes = ClasificadorImagenes()