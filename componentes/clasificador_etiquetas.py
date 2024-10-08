from manejo_texto.procesar_etiquetas import Etiquetas

from componentes.contenedor_estados import ContenedorEstados
from componentes.contenedor_etiquetado import ContenedorEtiquetado
from componentes.clasificador_estados import ClasificadorEstados


# Clases


class ClasificadorEtiquetas(ClasificadorEstados):
    """Clase pensada para gestionar las listas de imágenes de forma centralizada y ordenada."""
    def __init__(self):
        # self.todas          : list = [ContenedorEstados]
        # self.seleccion      : list = [ContenedorEstados]
        ClasificadorEstados.__init__(self)
        self.tags : list[str]|None = None
        # self.seleccion_backup: list = [ContenedorEstados]


    @property 
    def seleccion_estado(self):
        return self.seleccion



    def filtrar_etiquetas(self, etiquetas: list[str] | None = None):
        """
        Selecciona las imagenes que tengan al menos una etiqueta de entrada. 
        Si no hay etiquetas de entrada se selecciona toda la lista de entrada.
        """ 

        self.seleccionar_estado()

        if etiquetas == None:
            self.seleccion = filtrar_etiquetas(self.seleccion_estado, self.tags)
        else:    
            self.tags = etiquetas
            self.seleccion = filtrar_etiquetas(self.seleccion_estado , etiquetas)
        
        print(f"imagenes estado: {len(self.seleccion) }")
        # print(f"imagenes backup: {len(self.seleccion_backup) }")



# Funciones

def filtrar_etiquetas(
    lista_imagenes: list[ContenedorEtiquetado], 
    etiquetas: list[str] | None = None,
    )->list[ContenedorEtiquetado]:
    """
    Devuelve las imagenes que tengan al menos una etiqueta de entrada. 
    Si no hay etiquetas de entrada se devuelve toda la lista de entrada.
    """
    imagenes_filtradas = []
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