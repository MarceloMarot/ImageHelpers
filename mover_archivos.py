import pathlib
import os
import sys
from rich import print
import time


from clasificar_archivos import Data_Archivo, clasificar_archivos, patron_camara


def Mover_Archivo(data_origen: Data_Archivo, carpeta_destino: str, fechado = False, fechado_mes = False):

    #carga de la ruta completa del archivo
    ruta_archivo = data_origen.ruta_absoluta

    # se verifica que exista el directorio de destino
    # sino se interrumpe
    destino = pathlib.Path(carpeta_destino).absolute() 
    if not os.path.isdir(destino):
        # print("Directorio inexistente")
        return False

    # (opcional) clasificacion en carpetas por año y mes
    if fechado:
        anio = data_origen.modificacion[0]
        mes  = data_origen.modificacion[1]

        # se crean los subdirectorios de ser necesario y se actualiza la ruta destino
        destino = pathlib.PurePath(destino).joinpath(str(anio))
        if not os.path.isdir(destino):
            # print("Directorio inexistente")
            os.mkdir(destino)
        
        if fechado_mes:
            destino= pathlib.PurePath(destino).joinpath(str(mes))
            if not os.path.isdir(destino):
                # print("Directorio inexistente")
                os.mkdir(destino)

    # si existe un archivo con ese nombre en destino se interrumpe la ejecucion
    ruta_destino = f"{destino}/{data_origen.nombre}"
    ruta_destino = pathlib.Path(ruta_destino).absolute()
    if os.path.exists(ruta_destino):
        # print("Nombre de archivo ya existente")
        return False

    #mover archivo
    comando = f"mv '{ruta_archivo}' '{destino}'"
    os.system(comando)


    return True





# Función MAIN
if __name__ == "__main__" :
    try:

        ruta_origen  = os.path.abspath(sys.argv[1])
        ruta_destino = os.path.abspath(sys.argv[2])

        if not os.path.isdir(ruta_origen):
            print("[bold red]Directorio origen inexistente")

        if not os.path.isdir(ruta_destino):
            print("[bold red]Directorio destino inexistente")



    except Exception as excepcion:
        print(f"[bold red]Error: [bold blue]{excepcion}")

    else:

        patron_camara = r"^[0-9]+_[0-9]+\.[0-9A-Za-z]+$"


        patron = patron_camara

        # anulacion de la busqueda con patrones regex
        patron = None

        extension = "*.JPEG"
        # extension = "*.png"
        # extension = "*.avi"

        fechar_archivos = True

        fechar_archivos_mes = False


        print(f"[bold green]Directorio origen: [bold yellow]{ruta_origen} [bold green]")
        print(f"[bold green]Directorio destino: [bold yellow]{ruta_destino} [bold green]")
    

        inicio  = time.time()

        # archivos_origen = clasificar_archivos(ruta_origen, extension)
        archivos_origen = clasificar_archivos(ruta_origen, extension,patron)

        movidos = 0
        repetidos = 0
        total = len(archivos_origen)
        for archivo in archivos_origen:
            retorno = Mover_Archivo(archivo, ruta_destino, fechar_archivos, fechar_archivos_mes)
            if retorno:
                movidos += 1
            else:
                repetidos += 1

        fin  = time.time()
        print(f"[bold yellow]Archivos movidos   : [bold blue]{movidos} de {total}")
        print(f"[bold orange]Archivos repetidos : [bold blue]{repetidos} de {total}")
        print(f'[bold magenta]Tiempo de rutina  : {fin-inicio} segundos')


