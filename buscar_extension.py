#Esta rutina busca seleccionar todos los archivos con una extensón particular dentro de un directorio

# from pathlib import Path
import pathlib
import os
import sys

from rich import print

# Formatos de texto reconocidos por OpenCV (casi todos)
extensiones_imagen=["*.bmp", "*.dib", "*.jpeg", "*.jpg", "*.jpe", "*.jp2", "*.png", "*.webp", "*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pxm", "*.pnm", "*.pfm", "*.sr", "*.ras", "*.tiff", "*.tif", "*.exr", "*.hdr", "*.pic"]

# Busqueda de archivos , (incluye subdirectorios)
def buscar_extension(ruta: pathlib.Path, extension: str):
    #se buscan todos los elementos con la terminacion indicada
    lista_rutas_archivo = []
    for direccion in pathlib.Path(ruta).rglob(extension):
        direccion_actual = str(direccion.absolute())
        lista_rutas_archivo.append ( direccion_actual )
    return lista_rutas_archivo


# Lista TODOS los archivos y subcarpetas del directorio
# CUIDADO con el tipo de salida
def listar_directorios(ruta: pathlib.Path()):
    direcciones = sorted(
        pathlib.Path(ruta).iterdir(),
        key = lambda path: (path.is_dir(), path.name.lower())
        )
    return direcciones
    

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
                archivo_elegido = pathlib.Path(direccion_elegida).name
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

        extension = sys.argv[2].strip() 
    except IndexError():
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError():
        print("Error: Tipo de datos de entrada erróneo")

    else:

        print(f"[bold green]Directorio: [bold yellow]{ruta} [bold green]; extension: [bold yellow]{extension}")
        # Lista de archivos cn la extension pedida
        lista_rutas_archivo = buscar_extension(ruta, extension)



        # TODAS las extensionesde imagen
        # lista_rutas_archivo = []
        for extension in extensiones_imagen:
            # print(extension)
            # lista_rutas_archivo = buscar_extension(ruta, extension)
            lista_rutas_archivo = lista_rutas_archivo + buscar_extension(ruta, extension) #Concatenacion de listas

        # print(type(lista_rutas_archivo), lista_rutas_archivo)

        # print(listar_directorios(ruta))

        # print("[bold green]Nº archivos encontrados: ", len(lista_rutas_archivo))
        numero_imagenes = len(lista_rutas_archivo)
        



        # numero_imagenes = 0
        
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        if numero_imagenes > 0 :

            direccion_elegida = elegir_ruta(lista_rutas_archivo)


            archivo_elegido = pathlib.Path(direccion_elegida).name
            print(archivo_elegido, direccion_elegida)

        else:
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")



    
