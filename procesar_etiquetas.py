from rich import print 
import sys
import pathlib 


# Clase auxiliar para manejar y clasigficar etiquetas
class Etiquetas:
    def __init__(self, etiquetas: list, grupo: list):	
        self.etiquetas = etiquetas	
        self.grupo     = grupo

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
def GuardadoTexto(ruta: str, texto:str):
    path = pathlib.Path(ruta)
    try:
        with open(path,"w") as archivo:
            archivo.writelines(texto)
            # print("Guardado exitoso")
        return True
    except:
        return False        

# Guardado en archivo (modo AÑADIDO)
# def AgregadoTexto(ruta: str, texto:str):
#     path = pathlib.Path(ruta)
#     try:
#         with open(path,"a+") as archivo:
#             archivo.writelines(texto)
#             # print("Guardado exitoso")
#         return True
#     except:
#         return False    

#lectura de un archivo de texto 
#devuelve una lista de los renglones leidos
def LecturaLista(entrada: str): 
    path = pathlib.Path(entrada)
    try:
        with open(path,"r") as archivo:
            # se lee TODO como LISTA de renglones
            return archivo.readlines()
    except FileNotFoundError: 
        return []   # lista vacía si hay error



# Funcion que separa etiquetas en base a comas y puntos aparte
# Descarta etiquetas repetidas
# Asigna numero de grupo segun ubicación de etiqueta 
def FiltradoEtiquetas(lista_entrada: list):
    # listas auxiliares para contener los datos
    lineas=[]
    lista_etiquetas = []
    grupo_etiquetas = []
    # conjunto auxiliar: se filtrarán las etiquetas repetidas 
    set_etiquetas=set([])
    for i in range(0,len(lista_entrada)):
        # Eliminacion de renglones vacios
        if len(lista_entrada[i].strip()) > 0:
            lineas.append(lista_entrada[i])
            etiquetas_renglon = lista_entrada[i].split(',')
            # quita de espacios vacios y guardado en lista
            for j in range(0, len(etiquetas_renglon)):
                etiqueta = etiquetas_renglon[j] 
                etiqueta = etiqueta.strip()
                # Filtrado de etiquetas no nulas
                if len(etiqueta)>0:
                    # sólo se añaden elementos no repetidos
                    if not (etiqueta in set_etiquetas):
                        lista_etiquetas.append(etiqueta)
                        grupo_etiquetas.append(i) 
                        set_etiquetas.add(etiqueta)

    # Retorno de una clase con las etiquetas y el numero de renglón (grupo)
    return Etiquetas(lista_etiquetas, grupo_etiquetas)


if __name__ == "__main__":

    lineas_archivo = LecturaLista("demo_etiquetas.txt")
    # lineas_archivo = Lectura_Renglones("demo_.txt")
    tags = FiltradoEtiquetas( lineas_archivo )

    # set_etiquetas = set(tags.etiquetas)

    print(f'[bold green]Etiquetas y Nº grupos:')
    for i in range(0,len(tags.etiquetas) ):
        print(f'[bold yellow] {tags.grupo[i]} , {tags.etiquetas[i] }')

    print(f'[bold red]Longitud total: {len(tags.etiquetas)}')


    # Conversion de las etiquetas a texto , separadas por comas
    tags_filtrados = etiquetas2texto(tags.etiquetas)
    # Guardado en archivo (modo ESCRITURA)
    if GuardadoTexto("etiquetas_salida.txt", tags_filtrados):
        print("[green]Guardado exitoso")
    else:
        print("[bold red]ERROR: [green]guardado fallido")

    # # Añadido de una etiqueta arbitraria 
    # if AgregadoTexto("etiqusalida.txt", "\nSimona la cacarisa"):
    #     print("[green]Añadido exitoso")
    # else:
    #     print("[bold red]ERROR: [green]Añadido fallido")
