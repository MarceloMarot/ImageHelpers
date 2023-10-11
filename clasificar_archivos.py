# from pathlib import Path
import pathlib
import os
import sys
from rich import print

from datetime import datetime
import time
from functools import partial, reduce
import re

from  buscar_extension import  buscar_imagenes , listar_directorios, buscar_extension

from rich.progress import Progress


error = "err"

class Data_Archivo:
    def __init__(self, ruta):
        # self.ruta_absoluta = ruta
        self.ruta_absoluta = pathlib.Path(ruta).absolute()
        self.nombre = self.ruta_absoluta.name
        self.extension = self.ruta_absoluta.suffix
        self.directorio =self.ruta_absoluta.parent
        self.peso = 0
        self.creacion = []
        self.modificacion = []
    
        self.CreacionArchivo()
        self.ModificacionArchivo()
        self.PesoArchivo()


    def CreacionArchivo(self):
        # path = pathlib.Path(nombre_archivo)
        # Se evitan errores de lectura de archivos
        # Ej: archivos manipulados desde otro sistema operativo
        try:
            # current_timestamp = path.stat().st_ctime
            current_timestamp = self.ruta_absoluta.stat().st_ctime
            c_time = datetime.fromtimestamp(current_timestamp)
            year    = c_time.year
            month   = c_time.month
            day     = c_time.day
            minute  = c_time.minute
            second  = c_time.second
            self.creacion = [year, month, day, minute, second]
        except FileNotFoundError:
            self.creacion = [error , error , error, error, error ]


    def ModificacionArchivo(self):
        # path = pathlib.Path(nombre_archivo)
        # Se evitan errores de lectura de archivos
        # Ej: archivos manipulados desde otro sistema operativo
        try:
            # current_timestamp = path.stat().st_mtime
            current_timestamp = self.ruta_absoluta.stat().st_mtime
            m_time = datetime.fromtimestamp(current_timestamp)
            year    = m_time.year
            month   = m_time.month
            day     = m_time.day
            minute  = m_time.minute
            second  = m_time.second
            self.modificacion = [year, month, day, minute, second]
        except FileNotFoundError:
            self.modificacion = [error , error , error, error, error ]

    # def LeerPesoArchivo(nombre_archivo: str):
    def PesoArchivo(self):
        path = str(self.ruta_absoluta)
        try:
            sizefile = os.path.getsize(path)
            self.peso = sizefile
        except FileNotFoundError:
            self.peso = error






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
        

        # BUSQUEDA ARCHIVOS (TODOS)
        inicio  = time.time()
        # # Lista de archivos de imagen editables con OpenCV
        # rutas_archivo = buscar_imagenes(ruta)
        # rutas_archivo = []
        rutas_archivo = buscar_extension(ruta, "*.jpg") #fotos JPG
        # rutas_archivo = buscar_extension(ruta, "*.mp4")    #videos MP4
        # rutas_archivo = buscar_extension(ruta, "*.png")
        # rutas_archivo = []
        # for subdirectorio in  lista_subdirectorios :
        #     rutas_archivo += buscar_imagenes(subdirectorio)   # concatenacion rutas
        fin  = time.time()

        numero_imagenes = len(rutas_archivo)
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        print(f"[bold magenta]Tiempo de busqueda archivos: {fin - inicio}")
        if numero_imagenes == 0 :
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")

        # --------------PROCESADO DATOS -----------

        # FILTRADO POR FECHAS (incompleto)
        inicio  = time.time()

        # data_archivos = []
        # lista de ESTRUCTURAS
        archivos = []
        espacio_disco = 0

        extensiones_archivo = set([])
        directorios_archivo = set([])

        # extensiones_archivo = {}
        # directorios_archivo = {}


        for ruta_archivo in rutas_archivo:
            archivo = Data_Archivo( ruta_archivo )
            # print("")
            # print("nombre: ",archivo.nombre)
            # print("creado: ",archivo.creacion)
            # print("modif : ", archivo.modificacion)
            # print("ruta  : " , archivo.ruta_absoluta)
            # print("")


            espacio_disco += archivo.peso 
            archivos.append( archivo )


            # Estadisticas adicionales

            # todas las extensiones de archivo existentes

            # print(archivo.extension)
            # print(archivo.directorio)


            # extensiones_archivo |= {archivo.extension}        # conjunto
            # directorios_archivo |= {archivo.directorio}

            extensiones_archivo.add(archivo.extension)        # conjunto
            directorios_archivo.add(archivo.directorio)
            # if archivo.modificacion[0] <= 2010:
            #     print(archivo.nombre)




        # ----------------------------

        total_archivos = len(archivos)


        fin  = time.time()
        print(f"[bold green]Clasificacion archivos terminada[/bold green]")
        print(f'[bold magenta]Tiempo de lectura datos: {fin-inicio} segundos')

        # for contenido in contenidos_anio:
        #     print(f'[bold yellow]Año {contenido[0]}: [bold green]{contenido[1]} archivos, [bold cyan]{contenido[2]} MB')

        espacio_disco = int(espacio_disco/(1024**2))    #conversion a MB
        # print(f'[bold red]Erroneos: [bold green]{archivos_anio[error]} archivos')
        print(f"[bold green]Numero total de archivos: [bold yellow]{total_archivos}")
        print(f"[bold green]Peso total de archivos  : [bold yellow]{espacio_disco} MB")

        numero_erroneos = numero_imagenes - total_archivos

        if numero_erroneos > 0:
            print(f'[bold red]Archivos erróneos: [bold orange]{numero_erroneos} archivos')


        numero_directorios = len(directorios_archivo)
        print(f"[bold green]Numero total de carpetas: [bold yellow]{numero_directorios}")


        numero_extensiones = len(extensiones_archivo)
        print(f"[bold green]Numero total de extensiones: [bold yellow]{numero_extensiones}")


        # lectura extensiones y carpetas

        print("[bold yellow]extensiones archivo encontradas:")
        # for e in extensiones_archivo:
        #     print(e)

        print(extensiones_archivo)
        # print("[bold yellow] Directorios")
        # for r in directorios_archivo:
        #     print(str(r))

        # print(contenidos_anio[5][3])


        ## Filtrado de fotos


        patron_foto = r"^[0-9]+_[0-9]+\.[0-9A-Za-z]+$"

        fotos = []
        espacio_fotos = 0 

        for archivo in archivos:
            nombre = archivo.nombre
            foto = re.findall(patron_foto, nombre)

            if len(foto) > 0:
                fotos.append(foto)
                espacio_fotos += archivo.peso


        espacio_fotos = int(espacio_fotos/(1024**2))
        numero_fotos = len(fotos)
        print(f"[bold green]Numero total de fotos: [bold yellow]{numero_fotos}")
        print(f"[bold green]Peso total de fotos  : [bold yellow]{espacio_fotos} MB")



        # for i in range(10000,10020):
        #     print(fotos[i])