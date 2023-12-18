class MiClase:
    def __init__(self, nombre, numero) :
        self.nombre = nombre
        self.numero= numero

# Creamos el arreglo 
arreglo = []

# Agregamos instancias a voluntad 
arreglo.append(MiClase("Objeto 1"))  
arreglo.append(MiClase("Objeto 2"))
arreglo.append(MiClase("Objeto 3"))

# Podemos acceder a las instancias
print(arreglo[0].nombre) # Imprime Objeto 1
print(arreglo[1].nombre) # Imprime Objeto 2 
print(arreglo[2].nombre) # Imprime Objeto 3