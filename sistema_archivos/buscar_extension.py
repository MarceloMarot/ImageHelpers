#Esta rutina busca seleccionar todos los archivos con una extensón particular dentro de un directorio

# from pathlib import Path
import pathlib
import os
import sys

from rich import print

# Formatos de texto reconocidos por OpenCV (casi todos)
# NO se incluyen GIF y SVG
extensiones_OpenCV = ["*.bmp", "*.dib", "*.jpeg", "*.jpg", "*.jpe", "*.jp2", "*.png", "*.webp", "*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pxm", "*.pnm", "*.pfm", "*.sr", "*.ras", "*.tiff", "*.tif", "*.exr", "*.hdr", "*.pic"]


# Busqueda de archivos por extensión en una carpeta 
# (por defecto incluye subdirectorios)
def buscar_extension(ruta: str, extension: str, recursivo=True):
    """Busca archivos con la extensión especificada dentro del directorio indicado.
    Por defecto la búsqueda es recursiva (busca también en subdirectorios)."""
    #se buscan todos los elementos con la terminacion indicada
    lista_rutas_archivo = []
    if recursivo: 
        direcciones = pathlib.Path(ruta).rglob(extension)
    else:
        direcciones = pathlib.Path(ruta).glob(extension)
 
    for direccion in direcciones:
        direccion_actual = str(direccion.absolute())
        lista_rutas_archivo.append ( direccion_actual )
    return lista_rutas_archivo



def buscar_extensiones(ruta: str, extensiones: list[str] , recursivo=True):
    """Busca archivos con cualquiera de las extensiones especificadas dentro del directorio indicado.
    Por defecto la búsqueda es recursiva (busca también en subdirectorios).""" 
    lista_rutas_imagen = []
    # se busca cada extensión, una por una
    for extension in extensiones:
        lista_rutas_imagen = lista_rutas_imagen + buscar_extension(ruta, extension, recursivo) #Concatenacion de listas
    # numero_imagenes = len(lista_rutas)
    return lista_rutas_imagen

# Busqueda de imágenes en una carpeta (incluye subdirectorios)
def buscar_imagenes(ruta: str, extensiones = extensiones_OpenCV, recursivo=True):
    """Busca archivos de imagen compatibles con la biblioteca OpenCV (puede modificarse).
    Por defecto la búsqueda es recursiva (busca también en subdirectorios)."""
    return buscar_extensiones(ruta, extensiones, recursivo)

# Lista TODOS los archivos y subcarpetas del directorio
def listar_directorios(ruta: str, recursivo = False):
    """Devuelve la lista con los subdirectorios de la carpeta de entrada.
    También permite búsquedas recursivas."""
    directorios= []
    # Busqueda de elementos en el directorio de entrada
    resultado = pathlib.Path(ruta).iterdir()
    # filtrado: sólo se dejan los directorios
    objeto = filter(lambda path: path.is_dir(), resultado )
    directorios += list(objeto)
    if recursivo:
        subdirectorios = []
        for directorio in directorios:
            subdirectorios += listar_directorios(directorio , True)
        resultado =  directorios + subdirectorios
    else:   
        resultado =  directorios 
    resultado.sort()
    return resultado
    

# Interfaz usuario: elegir un archivo de la lista por indice
def elegir_ruta(lista_rutas_archivo):
    i=0
    for direccion in lista_rutas_archivo:
        archivo = pathlib.Path(direccion).name
        print(f"[bold bright_blue] [{i}]:[/bold bright_blue] [yellow]{archivo}[/yellow] [green] --> {direccion}[/green]")
        i += 1
    indice_elegido = False
    while indice_elegido == False :
        try:
            print(f"[bold green]Elegir opción por su índice:[/bold green]")
            eleccion = int(input())
            direccion_elegida = lista_rutas_archivo[eleccion]
        except ValueError:
            print("[bold red]ValueError: el índice debe ser un número.")
        except IndexError:
            print("[bold red]IndexError: indice fuera de rango.")
        else:    
            total = len(lista_rutas_archivo) - 1
            if eleccion <= total :
                direccion_elegida = lista_rutas_archivo[eleccion]
                # archivo_elegido = pathlib.Path(direccion_elegida).name
                # print(archivo_elegido, direccion_elegida)
            indice_elegido = True
            # print(f"[bold bright_blue]Ruta elegida:[/bold bright_blue] [yellow]{archivo_elegido}[/yellow] [green], ruta: {direccion_elegida}[/green]")
            return direccion_elegida



# Función MAIN
if __name__ == "__main__" :
    try:
        ruta = os.path.abspath(sys.argv[1])

        # print(extensiones_imagen)
        # print(len(sys.argv))

        # extension = sys.argv[2].strip() 
    except IndexError:
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError:
        print("Error: Tipo de datos de entrada erróneo")

    else:

        print(f"[bold green]Directorio: [bold yellow]{ruta} [bold green]")
        # Lista de archivos de imagen editables con OpenCV
        rutas_imagen = buscar_imagenes(ruta)
        # rutas_imagen = buscar_imagenes(ruta, recursivo=False)
    
        numero_imagenes = len(rutas_imagen)
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        if numero_imagenes > 0 :
            direccion_elegida = elegir_ruta(rutas_imagen)
            archivo_elegido = pathlib.Path(direccion_elegida).name
            print(archivo_elegido, direccion_elegida)
        else:
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")



    
