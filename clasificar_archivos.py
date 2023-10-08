# from pathlib import Path
import pathlib
import os
import sys
from rich import print

from datetime import datetime
import time
from functools import partial, reduce
import re

from  buscar_extension import elegir_ruta, buscar_imagenes


def LeerCreacionArchivo(nombre_archivo: str):
    path = pathlib.Path(nombre_archivo)
    # Se evitan errores de lectura de archivos
    # Ej: archivos manipulados desde otro sistema operativo
    try:
        current_timestamp = path.stat().st_ctime
        c_time = datetime.fromtimestamp(current_timestamp)
        year    = c_time.year
        month   = c_time.month
        day     = c_time.day
        return [year, month, day]
    except FileNotFoundError:
        return ["err" , "err" , "err"]



def LeerModificacionArchivo(nombre_archivo: str):
    path = pathlib.Path(nombre_archivo)
    # Se evitan errores de lectura de archivos
    # Ej: archivos manipulados desde otro sistema operativo
    try:
        current_timestamp = path.stat().st_mtime
        m_time = datetime.fromtimestamp(current_timestamp)
        year    = m_time.year
        month   = m_time.month
        day     = m_time.day
        return [year, month, day]
    except FileNotFoundError:
        return ["err" , "err" , "err"]




def LeerPesoArchivo(nombre_archivo: str):
    try:
        sizefile = os.path.getsize(nombre_archivo)
        return sizefile
    except FileNotFoundError:
        return "err"


class Data_Archivo:
    def __init__(self, ruta, creacion, modificado, peso):
        self.ruta = ruta
        self.creacion = creacion
        self.modificado = modificado
        self.peso = peso
    
                






# Función MAIN
if __name__ == "__main__" :
    try:

        ruta = os.path.abspath(sys.argv[1])

    except IndexError():
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError():
        print("Error: Tipo de datos de entrada erróneo")

    else:
        print(f"[bold green]Directorio: [bold yellow]{ruta} [bold green]")
        
        inicio  = time.time()
        # Lista de archivos de imagen editables con OpenCV
        rutas_archivo = buscar_imagenes(ruta)
        fin  = time.time()
    
        numero_imagenes = len(rutas_archivo)
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        print(f"[bold magenta]Tiempo de busqueda archivos: {fin - inicio}")
        if numero_imagenes == 0 :
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")


        # FILTRADO POR FECHAS (incompleto)
        inicio  = time.time()

        data_archivos = []

        for ruta_archivo in rutas_archivo:
            creacion     = LeerCreacionArchivo(     ruta_archivo )
            modificado  = LeerModificacionArchivo( ruta_archivo )
            peso        = LeerPesoArchivo( ruta_archivo )
            data = Data_Archivo(
                ruta_archivo,
                creacion,
                modificado,
                peso
                )
            
            data_archivos.append(data)          

        ## Filtrado por año modificacion

        def anio_modificacion( anio, data):
            return data.modificado[0] == anio   

        def anio_creacion( anio, data):
            return data.creacion[0] == anio   


        anio_inicial = 2007     # caso personal
        anio_final = datetime.fromtimestamp(inicio).year

        # lista con archivos y datos clasificados por año
        contenidos_anio = []

        for anio in range(anio_inicial, anio_final + 1):
            # Se filtran los archivos por año de modificacion
            # los errores de lectura ('err') quedan afuera

            filtro_anio = partial(anio_modificacion, anio )

            # filtro_anio = partial(anio_creacion, anio )

            lista_archivos = list(filter(filtro_anio, data_archivos))
            # procesamiento de data
            numero_archivos = len(lista_archivos)

            peso_archivos = 0

            for archivo in lista_archivos:
                valor = archivo.peso
                # filtrado de los valores errones (por las dudas)
                if valor != 'err':
                    peso_archivos += archivo.peso
 

            peso_archivos = int( peso_archivos/(1024*1024))   # peso en MB 
            contenidos_anio.append([
                anio,
                numero_archivos,
                peso_archivos,
                lista_archivos      #lista de OBJETOS 
                ])

        # Estadísticas globales
        total_archivos = 0
        espacio_disco = 0 

        for contenido in contenidos_anio:
            total_archivos += contenido[1]
            espacio_disco  += contenido[2]


        fin  = time.time()
        print(f'[bold magenta]Tiempo de lectura datos: {fin-inicio} segundos')

        for contenido in contenidos_anio:
            print(f'[bold yellow]Año {contenido[0]}: [bold green]{contenido[1]} archivos, [bold cyan]{contenido[2]} MB')


        # print(f'[bold red]Erroneos: [bold green]{archivos_anio["err"]} archivos')
        print(f"[bold green]Numero total de archivos: [bold yellow]{total_archivos}")
        print(f"[bold green]Peso total de archivos  : [bold yellow]{espacio_disco} MB")

        print(f'[bold red]Archivos erróneos: [bold green]{numero_imagenes - total_archivos} archivos')


        # print(contenidos_anio[5][3].ruta)

