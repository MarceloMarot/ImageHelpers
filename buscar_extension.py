#Esta rutina busca seleccionar todos los archivos con una extensón particular dentro de un directorio

# from pathlib import Path
import pathlib
import os
import sys

from rich import print

# # ruta        = '.'
# ruta        = 'D:\Proyectos_Programacion'           #ruta absoluta
# # ruta        = 'Backend'          #ruta relativa
# # ruta        = '.'          #ruta relativa
# extension   = '*.py'

# mostrar_diccionarios = False

# print("Ruta de búsqueda: ", ruta)  

archivo    = []
direccion_absoluta = []

# from rich import print
# from rich.text import Text
# from rich.tree import Tree
# from rich.filesize import decimal
# from rich.markup import escape

# arbol=Tree(
#     f"[bold orange]:open_file_folder: [link file://{ruta}]{ruta}",
#     guide_style="bold bright_blue"
# )

def buscar_extension(ruta: pathlib.Path, extension: str):
    #se buscan todos los elementos con la terminacion indicada
    # direcciones = []
    for direccion in pathlib.Path(ruta).rglob(extension):
        # print(direccion)
        # archivo_actual = str(direccion.name   )
        direccion_actual = str(direccion.absolute())

        direccion_absoluta.append ( direccion_actual )
    return direccion_absoluta


def listar_directorios(ruta: pathlib.Path()):
    direcciones = sorted(
        pathlib.Path(ruta).iterdir(),
        key = lambda path: (path.is_dir(), path.name.lower())
        )
    return direcciones
    

def elegir_ruta(direccion_absoluta):
    i=0
    for direccion in direccion_absoluta:
        archivo = pathlib.Path(direccion).name
        print(f"[bold bright_blue] [{i}]:[/bold bright_blue] [yellow]{archivo}[/yellow] [green] --> {direccion}[/green]")
        i += 1
    indice_elegido = False
    while indice_elegido == False :
        try:
            print(f"[bold green]Elegir opción por su índice:[/bold green]")
            eleccion = int(input())
            direccion_elegida = direccion_absoluta[eleccion]
        except ValueError:
            print("[bold red]ValueError: el índice debe ser un número.")
        except IndexError:
            print("[bold red]IndexError: indice fuera de rango.")
        else:    
            total = len(direccion_absoluta) - 1
            if eleccion <= total :
                direccion_elegida = direccion_absoluta[eleccion]
                archivo_elegido = pathlib.Path(direccion_elegida).name
                # print(archivo_elegido, direccion_elegida)
            indice_elegido = True
            # print(f"[bold bright_blue]Ruta elegida:[/bold bright_blue] [yellow]{archivo_elegido}[/yellow] [green], ruta: {direccion_elegida}[/green]")
            return direccion_elegida



# Función MAIN
if __name__ == "__main__" :
    try:
        ruta = os.path.abspath(sys.argv[1])
        extension = sys.argv[2].strip() 
    except IndexError():
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 
    except TypeError():
        print("Error: Tipo de datos de entrada erróneo")
    else:

        print(f"[bold yellow]Directorio: {ruta} ; extension: {extension}")
        direccion_absoluta = buscar_extension(ruta, extension)


        direccion_elegida = elegir_ruta(direccion_absoluta)


        archivo_elegido = pathlib.Path(direccion_elegida).name
        print(archivo_elegido, direccion_elegida)
    
