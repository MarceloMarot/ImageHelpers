
from componentes.galeria_imagenes import Galeria, ContenedorImagen, EstiloContenedor, ContImag
from componentes.contenedor_estados import ContenedorEstados



def nada( e ):
    pass





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
        # self.actualizar_estilos( )  
        self.estilo_estados( )  



    def estilo_estados(self):
        """Actualiza el estilo de cada imagen en base a sus flags internos de estado."""
        actualizar_estilo_estado( self.imagenes, self.estilos)    




def actualizar_estilo_estado( contenedores: list[ContenedorEstados], estilos : dict ):
    """Cambia colores y espesor de bordes de imagen según los flags de estado internos."""
    objeto = map(lambda c : c.estilo_estado(), contenedores)
    contenedores = list(objeto)

