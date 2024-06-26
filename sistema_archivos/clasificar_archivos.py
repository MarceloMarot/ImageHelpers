import pathlib
import os
import sys
from rich import print

# from rich.progress import Progress

from datetime import datetime
import time
# from functools import partial, reduce
import re

# archivo "clasificar_archivos" aledaño (mismo subdirectorio)
from . buscar_extension import  buscar_extension
# from  .  import  buscar_extension
# from  sistema_archivos.buscar_extension import  buscar_extension


# expresion regular para filtrar fotos y videos de camara sin renombrar
patron_camara = r"^[0-9]+_[0-9]+\.[0-9A-Za-z]+$"



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
        self.lectura_exitosa = False
        # lectura de parámetros automática
        try:
            self.CreacionArchivo()
            self.ModificacionArchivo()
            self.PesoArchivo()
            self.lectura_exitosa = True
        except FileNotFoundError:
            self.lectura_exitosa = False

    def CreacionArchivo(self):
        # path = pathlib.Path(nombre_archivo)
        # Se evitan errores de lectura de archivos
        # Ej: archivos manipulados desde otro sistema operativo
        # try:
        # current_timestamp = path.stat().st_ctime
        current_timestamp = self.ruta_absoluta.stat().st_ctime
        c_time = datetime.fromtimestamp(current_timestamp)
        year    = c_time.year
        month   = c_time.month
        day     = c_time.day
        minute  = c_time.minute
        second  = c_time.second
        self.creacion = [year, month, day, minute, second]
        # except FileNotFoundError:
            # self.creacion = [error , error , error, error, error ]


    def ModificacionArchivo(self):
        # path = pathlib.Path(nombre_archivo)
        # Se evitan errores de lectura de archivos
        # Ej: archivos manipulados desde otro sistema operativo
        # try:
        # current_timestamp = path.stat().st_mtime
        current_timestamp = self.ruta_absoluta.stat().st_mtime
        m_time = datetime.fromtimestamp(current_timestamp)
        year    = m_time.year
        month   = m_time.month
        day     = m_time.day
        minute  = m_time.minute
        second  = m_time.second
        self.modificacion = [year, month, day, minute, second]

        # except FileNotFoundError:
        #     self.modificacion = [error , error , error, error, error ]

    # def LeerPesoArchivo(nombre_archivo: str):
    def PesoArchivo(self):
        path = str(self.ruta_absoluta)
        # try:
        self.peso = os.path.getsize(path)
        # except FileNotFoundError:
        #     self.peso = error




def clasificar_archivos(ruta: str, extension: str, patron_nombre=None):

        rutas_archivo = buscar_extension(ruta,extension.lower()) 
        #extension en mayusculas
        rutas_archivo += buscar_extension(ruta,extension.upper())   

        data_archivos = []
        archivos_ilegibles= []

        for ruta_archivo in rutas_archivo:
            # creacion de objeto de archivo
            archivo = Data_Archivo( ruta_archivo )

            #se filtran los nombres de archivo en caso de ser requerido
            if patron_nombre == None:
                if archivo.lectura_exitosa:
                    data_archivos.append( archivo )
                else:
                    archivos_ilegibles.append( archivo )
            else:
                nombre = archivo.nombre
                coincidencia = re.findall(patron_nombre, nombre)
                if len(coincidencia) > 0:
                    if archivo.lectura_exitosa:
                        data_archivos.append( archivo )
                    else:
                        archivos_ilegibles.append( archivo )


        # devolucion de ambas listas
        return [data_archivos, archivos_ilegibles]



# Función MAIN
if __name__ == "__main__" :
    try:
        ruta_entrada = os.path.abspath(sys.argv[1])
        # extension = os.path.abspath(sys.argv[2])

        # extension = "*.jpg"
        extension = "*.webp"
        patron = None

        print(f"[bold green]Directorio: [bold yellow]{ruta_entrada} [bold green]")
        print(f"[bold green]Extension : [bold yellow]{extension} [bold green]")
        ## Filtrado de fotos
        inicio  = time.time()
        fotos = []
        espacio_fotos = 0 
        fotos, ilegibles = clasificar_archivos(ruta_entrada,extension,patron)


        # Lectura despacio en disco (en MB)
        for foto in fotos: 
            espacio_fotos += foto.peso

        # espacio_fotos = int(espacio_fotos/(1024**2))
        espacio_fotos = f"{espacio_fotos/(1024**2) :.4}" #peso en MB, 4 digitos
        numero_fotos = len(fotos)
        fotos_ilegibles = len(ilegibles)

        fin  = time.time()
        print(f"[bold green]Filtrado archivos terminado[/bold green]")
        print(f'[bold magenta]Tiempo de rutina: {fin-inicio} segundos')

        print(f"[bold green]Numero de fotos: [bold yellow]{numero_fotos}")
        print(f"[bold green]Peso total de fotos: [bold yellow]{espacio_fotos} MB")
        print(f"[bold green]Fotos ilegibles: [bold yellow]{fotos_ilegibles}")
    except IndexError:
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError:
        print("Error: Tipo de datos de entrada erróneo")

    except Exception as excepcion:
        print(f"[bold red]Error: [bold blue]{excepcion}")


    else:

        print("finalizado")

        # for foto in fotos:
        #     print(foto.nombre, foto.peso)