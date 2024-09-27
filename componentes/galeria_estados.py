from manejo_texto.procesar_etiquetas import Etiquetas
from componentes.galeria_imagenes import Galeria, ContenedorImagen, EstiloContenedor, ContImag
from estilos.estilos_contenedores import  estilos_seleccion, estilos_galeria, Estilos

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from constantes.constantes import Tab, Percentil, Estados

from sistema_archivos.rutas import ruta_relativa_usuario


from componentes.contenedor_estados import ContenedorEstados



def nada( e ):
    pass



class Contenedor_Etiquetado( Etiquetas, ContenedorEstados):
    """Clase usada para manejar imágenes etiquetables."""
    def __init__(
        self, 
        ruta: str, 
        ancho:int=768, 
        alto:int=768, 
        redondeo:int=0 , 
        estilos: dict[str, EstiloContenedor] = estilos_galeria,
        ):
        Etiquetas.__init__(self, ruta)
        ContenedorEstados.__init__(self,ruta, ancho, alto, redondeo)

 
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


# REDEFINICION  de componente
class GaleriaEstados(Galeria):
    """Clase usada para manejar galerías de imágenes con estados.
    Acepta objetos de la clase ContenedorEstados y sus derivados."""
    def __init__(self, estilos: dict):
        super().__init__()
        self.estilos = estilos


    def cargar_imagenes(self, 
        imagenes: list[ContImag ], 
        cuadricula=True):
        """Lee objetos de imagen Flet del tipo ContenedorImagen previamente creados."""
        super().cargar_imagenes(imagenes, cuadricula)
        self.imagenes = imagenes
        self.actualizar_estilos( )  



    def estilo_estados(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    



    # metodo obsoleto
    def actualizar_estilos(self):
        actualizar_estilo_estado( self.imagenes, self.estilos)    





def actualizar_estilo_estado( contenedores: list[ContenedorEstados], estilos : dict ):
    """Cambia colores y espesor de bordes de imagen según los flags de estado internos."""
    objeto = map(lambda c : c.estilo_estado(), contenedores)
    contenedores = list(objeto)
