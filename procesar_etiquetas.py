from rich import print 




class Etiquetas:
    def __init__(self, etiquetas: list, grupo: list):	
        self.etiquetas = etiquetas	
        self.grupo     = grupo
	# def <metodo1>(self):
	# 	#código 1
	# def <metodo2>(self):
	# 	#código 2





#FUNCIONES

# Conversion de lista a texto
def renglones2texto(lista_renglones: list):
    texto = ""
    for renglon in  lista_renglones:
        texto += str(renglon) + ", "
    return texto



# Funcion que separa etiquetas en base a comas y puntos aparte
# Descarta etiquetas negativas
def FiltradoEtiquetas(linea_archivos: list):
    # listas auxiliares para contener los datos
    lista_etiquetas = []
    grupo_etiquetas = []
    # conjunto auxiliar: se filtrarán las etiquetas repetidas 
    set_etiquetas=set([])
    for i in range(0,len(lineas_archivo)):
        # Eliminacion de renglones vacios
        if len(lineas_archivo[i].strip()) > 0:
            lineas.append(lineas_archivo[i])
            etiquetas_renglon = lineas_archivo[i].split(',')
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
                        # set_etiquetas.add(etiqueta)

    # Retorno de una clase con las etiquetas y el numero de renglón (grupo)
    return Etiquetas(lista_etiquetas, grupo_etiquetas)


# Lectura de la lista de etiquetas desde archivo
# def Leer_Etiquetas(archivo: str):
#     with open(archivo,"r") as archivo:
#         # se lee TODO como LISTA de renglones
#         lineas_archivo = archivo.readlines()
#     return FiltradoEtiquetas(lineas_archivo)





#lista vacía
lineas=[]

with open("etiquetas.txt","r") as archivo:
    # se lee TODO como LISTA de renglones
    lineas_archivo = archivo.readlines()





# Procesamiento linea a linea
# lista_etiquetas = []
# set_etiquetas = {}

# print(type(lista_etiquetas), type(set_etiquetas))

# lista_etiquetas = FiltradoEtiquetas( lineas_archivo )


tags = FiltradoEtiquetas( lineas_archivo )

set_etiquetas = set(tags.etiquetas)

print(f'[bold yellow] {tags.grupo} , {tags.etiquetas}')
print(f'[bold red]{len(tags.etiquetas)}')
# print(f'[bold green]{set_etiquetas}')
# print(f'[bold magenta]{len(set_etiquetas)}')


# lista_etiquetas = list(set_etiquetas)
# print(tags.etiquetas)
# tag ='feather-trimmed sleeves'
# tag ='blue eyes'
# index_tag = lista_etiquetas.index(tag)
# print(f"Ubicacion {tag}: {index_tag}")





tags_filtrados = renglones2texto(tags.etiquetas)


with open("etiquetas_salida.txt","w") as archivo:
    # se lee TODO como LISTA de renglones
    # lineas_archivo = archivo.readlines()
    archivo.writelines(tags_filtrados)
    print("Guardado exitoso")



with open("etiquetas_salida.txt","a") as archivo:
    archivo.write("Simona la Cacarisa") #ELIMINAR
    print("Añadido exitoso")





# nums = {6, 4, 5, 9, 8}
# item = 17

# isPresent = item in nums
# print(isPresent)            # True
 

# print(f"[bold red] Juego con SETs:")

# print(set_etiquetas)

# etiqueta='white blindfold'

# print(etiqueta in set_etiquetas)

