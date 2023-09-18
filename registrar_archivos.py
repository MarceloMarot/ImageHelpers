# from pathlib import Path
import pathlib
import os
import sys
from rich import print

from datetime import datetime
import time

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

        # print(extensiones_imagen)
        # print(len(sys.argv))

        # extension = sys.argv[2].strip() 
    except IndexError():
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError():
        print("Error: Tipo de datos de entrada erróneo")

    else:
        print(f"[bold green]Directorio: [bold yellow]{ruta} [bold green]")
        
        inicio  = time.time()
        # Lista de archivos de imagen editables con OpenCV
        rutas_imagen = buscar_imagenes(ruta)
        fin  = time.time()
    
        numero_imagenes = len(rutas_imagen)
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        print(f"[bold magenta]Tiempo de busqueda archivos: {fin - inicio}")
        if numero_imagenes == 0 :
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")


        # FILTRADO POR FECHAS (incompleto)
        inicio  = time.time()
        anios=[]
        espacio_disco=0  # tamaño total de archivos
        peso=0
        for i in range(0, len(rutas_imagen)):
            # print(LeerCreacionArchivo(rutas_imagen[i]))
            ruta = str(rutas_imagen[i])
            # ruta = r'{ruta}'
            [anio, mes, dia] = LeerCreacionArchivo(ruta)
            peso = LeerPesoArchivo(ruta)
            if peso != "err":
                espacio_disco += peso
            # print(anio, mes)
            anios.append(anio)
        fin  = time.time()

        print(f'[bold magenta]Tiempo de lectura datos: {fin-inicio} segundos')

        # diccionario con archivos por año
        lista_anios = {}
        anio_inicial = 2007
        ahora = datetime.fromtimestamp(inicio)
        anio_final = ahora.year    

        for i in range(anio_inicial, anio_final+1):
            lista_anios[i] = len( re.findall(f'{i}' , str(anios)))

        lista_anios["err"] = len( re.findall('err' , str(anios)))

        print(f'[bold green] Resultados:')
        for i in range(anio_inicial, anio_final+1):
            print(f'[bold yellow]Año {i}: [bold green]{lista_anios[i]} archivos')

        print(f'[bold red]Erroneos: [bold green]{lista_anios["err"]} archivos')

        print(f"[bold green]Peso total de archivos: {int(espacio_disco/(1024*1024))} MB")