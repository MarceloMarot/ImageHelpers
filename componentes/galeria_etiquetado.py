from manejo_texto.procesar_etiquetas import Etiquetas
from componentes.galeria_imagenes import Galeria, Contenedor_Imagen, Estilo_Contenedor, ContImag
from componentes.estilos_contenedores import  estilos_seleccion, estilos_galeria, Estilos

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from constantes.constantes import Tab, Percentil, Estados

from sistema_archivos.rutas import ruta_relativa_usuario




def nada( e ):
    pass



from abc import ABC, abstractclassmethod


# Clase plantilla para crear contenedores de imagenes con estados
class ContenedorEstados(ABC, Contenedor_Imagen):
    #  Inicializacion
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
        self.verificar_guardado()
        self.estilos = estilos
        self.tooltip = ruta_relativa_usuario(ruta)


    # clases a rediseñar
    def verificar_guardado(self):
        pass


    # clases prediseñadas 

    def estilo_estado(self, estilos : dict):
        if self.defectuosa :     
            estilo = estilos[Estilos.ERRONEO.value]     
        elif self.modificada :
            estilo = estilos[Estilos.MODIFICADO.value]
        elif self.guardada :
            estilo = estilos[Estilos.GUARDADO.value]
        else: 
            estilo = estilos[Estilos.DEFAULT.value]
        self.estilo( estilo )

    #  REPETIDO
    def actualizar_estilo_estado(self):
        self.estilo_estado(self.estilos)

    def leer_dimensiones(self):
        """Este método lee altura, base y numero de canales de la imagen"""
        dim = dimensiones_imagen(self.ruta)  
        self.__dimensiones = dim if dim!=None else None 
        return self.__dimensiones

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

    @property
    def guardada(self)->bool:
        return self.__guardada 

    @property
    def modificada(self)->bool:
        return self.__modificada 


class Contenedor_Etiquetado( Etiquetas, ContenedorEstados):
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, Estilo_Contenedor] = estilos_galeria,
        ):
        ContenedorEstados.__init__(self,ruta, ancho, alto, redondeo)
        Etiquetas.__init__(self, ruta)

 
    # Implementacion de metodos requeridos
    def verificar_guardado(self):
        self.verificar_guardado_tags()


    def buscar_etiqueta(self, etiqueta: str):
        """Este método busca la etiqueta en la imagen y si la encuentra devuelve 'True'."""
        return True if etiqueta in self.tags else False
            

    def verificar_guardado_tags(self ):
        """Comprueba si las etiquetas actuales son las mismas que las guardadas en archivo de texto"""
        # verificacion guardado
        tags_archivo  = self.tags_archivo 
        self.__guardada = False if len(tags_archivo)==0 else True
        # verificacion modificaciones de etiquetado
        tags_imagen =  self.tags
        self.__modificada = True if set(tags_imagen) != set(tags_archivo) else False 


    #  REPETIDOS PERO NECESARIOS 
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



def actualizar_estilo_estado( contenedores: list[Contenedor_Etiquetado], estilos : dict ):
    """Cambia colores y espesor de bordes de imagen según los flags de estado internos."""
    objeto = map(lambda c : c.estilo_estado(estilos), contenedores)
    contenedores = list(objeto)

