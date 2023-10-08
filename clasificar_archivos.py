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
            data = [
                ruta_archivo,
                creacion,
                modificado,
                peso
                ]
            data_archivos.append(data)          
        

        ## Filtrado por año modificacion

        def anio_modificacion( anio, data):
            # print(f"año: {anio}; data[2][0]: {data[2][0]}")
            return data[2][0] == anio   

        def anio_creacion( anio, data):
            return data[1][0] == anio   



        # funcion de mapeo : solo ruta archivo
        def solo_path( data):
            return data[0]

        def solo_peso(data):
            return data[3]


        anio_inicial = 2007     # caso personal
        anio_final = datetime.fromtimestamp(inicio).year

        # lista con archivos y datos clasificados por año
        contenidos_anio = []

        for anio in range(anio_inicial, anio_final + 1):
            # Se filtran los archivos por año de modificacion
            # los errores de lectura ('err') quedan afuera
            filtro_anio = partial(anio_modificacion, anio )

            lista_rutas = list(filter(filtro_anio, data_archivos))

            lista_pesos = list(  map(  solo_peso , lista_rutas))
            lista_rutas = list(  map(  solo_path , lista_rutas))
            
            # procesamiento de data
            numero_archivos = len(lista_rutas)

            peso_archivos = 0

            for peso in lista_pesos:
                # filtrado de los valores errones (por las dudas)
                if peso != 'err':
                    peso_archivos += peso
 

            peso_archivos = int( peso_archivos/(1024*1024))   # peso en MB 
            contenidos_anio.append([
                anio,
                numero_archivos,
                peso_archivos,
                lista_rutas   
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


        # print(contenidos_anio[5][3])

