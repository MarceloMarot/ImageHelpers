from rich import print 
import pathlib 

class Etiquetas:
    """
    Clase auxiliar para manejar y clasificar etiquetas
    'ruta' es el nombre de cualquier archivo a describir
    las etiquetas se guardan/leen de un archivo de igual nombre pero con extension '.txt' 
    """
    # def __init__(self, tags: list, grupo: list, ruta: str):	
    def __init__(self, ruta: str="", tags=[], grupo=[] ):	
        self.ruta : str    = ruta      # ruta archivo
        self.datos : dict   = dict()      # etiquetas y grupos en formato diccionario
        # lectura automatica
        try:
            self.leer_archivo()
        except:
            self.datos = dict([]) 


    @property
    def tags(self)->list:
        """Devuelve la lista de etiquetas encontradas. Puede estar vacía."""
        if self.datos != None:
            return list( self.datos.keys() )
        else:
            return []


    @property
    def grupos(self)->list:
        """Devuelve la lista con todos los grupos asignados a las etiquetas. Puede estar vacía."""
        if self.datos != None:
            listas  = list(self.datos.values() )
            valores = set()
            for lista in listas:
                for valor in lista:
                    valores.add(valor)
            return  list(valores)
        else:
            return []


    #lectura desde disco
    def leer_archivo(self, etiquetas_repetidas=True) -> None:
        """Lee las etiquetas desde archivo de texto. Si éste no existe la data interna queda vacía """
        renglones_listas = lectura_archivo(self.ruta)
        self.datos = separar_etiquetas(renglones_listas, etiquetas_repetidas)


    # escritura en disco
    def guardar(self, etiquetas=[], modo: str="w", encoding='utf-8'):
        """Conversion de lista de etiquetas a texto (añade comas y respeta saltos de renglón)"""
        texto = etiquetas2texto(etiquetas)
        # guardado, actualizacion del objeto e indicacion de exito
        guardado_exitoso = guardar_archivo(self.ruta, texto, modo, encoding)
        if guardado_exitoso:
            self.leer_archivo()
        return guardado_exitoso


    def agregar_tags(self, tags: list[str], nro_grupo: int|None = None, sobreescribir:bool=False):
        """Agrega etiquetas al objeto desde el programa. Asigna tambien un numero de grupo."""

        if sobreescribir:
            self.datos=dict()

        # nuevo grupo de etiquetas si no se indica a la entrada
        if nro_grupo == None:
            nro_grupo= len(self.grupos)

        for tag in tags:
            if tag in set(self.tags): 
                self.datos[tag].append(nro_grupo)
            else:
                self.datos[tag]=[nro_grupo]



#FUNCIONES

def etiquetas2texto(lista_renglones: list) -> str:
    """Hace la conversion de lista de etiquetas a texto.
    Asigna una etiqueta por indice de la lista y las separa poor comas."""
    texto = ""
    for renglon in  lista_renglones:
        texto += str(renglon) + ", "
    return texto


def guardar_archivo(ruta: str, texto:str, modo: str="w", encoding='utf-8') -> bool:
    """ Funcion de guardado en archivo TXT. 
    Modos:
    - "w": sobreescritura (por defecto)
    - "a": agregado al final 
    Codificacion UTF-8 por defecto
    """
    path = pathlib.Path(ruta).with_suffix('.txt')
    try:
        with open(path,modo,encoding=encoding) as archivo:
            archivo.writelines(texto)
        return True
    except:
        return False   


def lectura_archivo(entrada: str = "") -> list: 
    """Funcion de lectura de un archivo de texto. Devuelve una lista con los renglones de texto leidos"""
    try:
        path = pathlib.Path(entrada).with_suffix('.txt')
        with open(path,"r") as archivo:
            # se lee TODO como LISTA de renglones
            return archivo.readlines()
    # except FileNotFoundError: 
    except: 
        return []   # lista vacía si hay error


def separar_etiquetas(renglones_entrada: list[str], repetidas=True):
    """
    Funcion que separa etiquetas en base a comas y puntos aparte. 
    Descarta etiquetas repetidas.
    Asigna numero de grupo a los tags en base al primer renglon de aparicion
    """
    # diccionario auxiliar para contener los datos
    dicc_etiquetas = dict([])
    # conjunto auxiliar: se filtrarán las etiquetas repetidas 
    set_etiquetas=set([])
    # auxiliar: numero de grupo 
    n = 0
    for i in range(0,len(renglones_entrada)):
        nuevo_tag = False
        # Eliminacion de renglones vacios
        if len(renglones_entrada[i].strip()) > 0:
            # separacion de etiquetas mediante comas (estas se eliminan)
            etiquetas_renglon = renglones_entrada[i].split(',')
            # quita de espacios vacios y guardado en lista
            for etiqueta in etiquetas_renglon :
                etiqueta = etiqueta.strip()
                # Filtrado de etiquetas no nulas
                if len(etiqueta)>0:
                    # caso nueva etiqueta
                    if not (etiqueta in set_etiquetas):
                        dicc_etiquetas[etiqueta] = [n]
                        set_etiquetas.add(etiqueta) 
                        nuevo_tag=True
                    # agregado de elementos repetidos (opcional)
                    elif repetidas:
                        dicc_etiquetas[etiqueta].append(n)
                    
            # Nuevo renglon con tags añadidas --> nuevo grupo
            if nuevo_tag :
                n += 1
                nuevo_tag = False
    # Retorno de una clase con las etiquetas y el numero de renglón (grupo)
    return dicc_etiquetas


if __name__ == "__main__":


    archivo = "demo/dataset.txt"

    # lectura de etiquetas desde archivo
    etiqueta = Etiquetas(archivo) 
    etiqueta.leer_archivo()

    # agregado de etiquetas desde programa
    tags_nuevos = [ "diamante", "cuarzo", "esmeralda", "amatista", '1', '5', '7']
    etiqueta.agregar_tags(tags_nuevos)      # default: (numero grupo + 1)
    etiqueta.agregar_tags(tags_nuevos, 999) # nro grupo arbitrario
    # etiqueta.agregar_tags(tags_nuevos, sobreescribir=True) # borrado data

    # # Muestra de resultados
    tags  = etiqueta.tags
    grupos = etiqueta.grupos 

    print(f'[bold green] {tags }')
    print(f'[bold yellow] {grupos}')

    print(f'[bold green]Longitud etiquetas: {len(tags)}')
    print(f'[bold yellow]Longitud grupos: {len(grupos)}')

    # Guardado en archivo aparte
    etiqueta.ruta = "demo/etiquetas_salida.txt"
    if etiqueta.guardar(tags):
        print("[green]Guardado exitoso")
    else:
        print("[bold red]ERROR: [green]guardado fallido")


