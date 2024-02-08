from rich import print 
import pathlib 


# Clase auxiliar para manejar y clasificar etiquetas
# 'ruta' es el nombre de cualquier archivo a describir
# las etiquetas se guardan/leen de un archivo de igual nombre pero con extension '.txt'
class Etiquetas:
    # def __init__(self, tags: list, grupo: list, ruta: str):	
    def __init__(self, ruta: str, tags=[], grupo=[] ):	
        self.tags   = tags	    # lista etiquetas
        self.grupo  = grupo     # numeros de grupo de las etiquetas
        self.ruta   = ruta      # ruta archivo
        self.data = dict()
        # lectura automatica
        try:
            # self.ruta = pathlib.Path(ruta).with_suffix('.txt')
            self.leer()
        except:
            self.tags  = []
            self.grupo = []


    #lectura desde disco
    def leer(self):
        renglones_listas = lectura_archivo(self.ruta)
        self.data = filtrado_etiquetas(renglones_listas)
        self.tags  = list( self.data.keys()   )
        self.grupo = list( self.data.values() )

    # escritura en disco
    def guardar(self, etiquetas= []):
        # Si no hay lista de entrada se lee desde el objeto
        if len(etiquetas) == 0:
            texto = etiquetas2texto(self.tags)
        else:
            texto = etiquetas2texto(etiquetas)
        # guardado, actualizacion del objeto e indicacion de exito
        guardado_exitoso = guardar_archivo(self.ruta, texto)
        if guardado_exitoso:
            self.leer()
        return guardado_exitoso



#FUNCIONES

# Conversion de lista de etiquetas a texto
# una etiqueta por indice de la lista
# Separacion por comas
def etiquetas2texto(lista_renglones: list):
    texto = ""
    for renglon in  lista_renglones:
        texto += str(renglon) + ", "
    return texto





# Guardado en archivo (modo SOBREESCRITURA)
def guardar_archivo(ruta: str, texto:str):
    print(ruta)
    path = pathlib.Path(ruta).with_suffix('.txt')
    try:
        with open(path,"w") as archivo:
            archivo.writelines(texto)
        return True
    except:
        return False        


#lectura de un archivo de texto 
#devuelve una lista de los renglones leidos
def lectura_archivo(entrada: str): 
    path = pathlib.Path(entrada).with_suffix('.txt')
    try:
        with open(path,"r") as archivo:
            # se lee TODO como LISTA de renglones
            return archivo.readlines()
    except FileNotFoundError: 
        return []   # lista vacía si hay error



# Funcion que separa etiquetas en base a comas y puntos aparte
# Descarta etiquetas repetidas
# Asigna numero de grupo alos tags en base al  primer renglon de aparicion
def filtrado_etiquetas(lista_entrada: list):
    # diccionario auxiliar para contener los datos
    dicc_etiquetas = {}
    # conjunto auxiliar: se filtrarán las etiquetas repetidas 
    set_etiquetas=set([])
    # auxiliar: numero de grupo 
    n = 0

    for i in range(0,len(lista_entrada)):
        nuevo_tag = False
        # Eliminacion de renglones vacios
        if len(lista_entrada[i].strip()) > 0:
            etiquetas_renglon = lista_entrada[i].split(',')
            # quita de espacios vacios y guardado en lista
            for etiqueta in etiquetas_renglon :
                etiqueta = etiqueta.strip()
                # Filtrado de etiquetas no nulas
                if len(etiqueta)>0:
                    # sólo se añaden elementos no repetidos
                    if not (etiqueta in set_etiquetas):
                        # lista_etiquetas.append(etiqueta)
                        # grupo_etiquetas.append(n)
                        # salida en pares clave -valor 
                        dicc_etiquetas[etiqueta] = n
                        set_etiquetas.add(etiqueta) 
                        nuevo_tag=True
            # Nuevo renglon con tags añadidas --> nuevo grupo
            if nuevo_tag :
                n += 1
                nuevo_tag = False
    # Retorno de una clase con las etiquetas y el numero de renglón (grupo)
    # return [lista_etiquetas, grupo_etiquetas]
    return dicc_etiquetas


if __name__ == "__main__":


    archivo = "demo_etiquetas.txt"

    # lectura de etiquetas desde archivo
    etiqueta = Etiquetas(archivo) 
    etiqueta.leer()

    tags  = etiqueta.tags
    grupo = etiqueta.grupo 
    # tags = etiqueta.keys()
    # grupo = etiqueta.values()


    # Muestra de resultados
    print(f'[bold green]Etiquetas y Nº grupos:')
    for i in range(0,len(tags) ):
        print(f'[bold yellow] {grupo[i]} , {tags[i] }')

    print(f'[bold red]Longitud total: {len(tags)}')


    # Guardado en archivo aparte
    etiqueta.ruta = "etiquetas_salida.txt"
    if etiqueta.guardar():
        print("[green]Guardado exitoso")
    else:
        print("[bold red]ERROR: [green]guardado fallido")


