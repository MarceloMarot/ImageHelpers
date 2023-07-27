import sys
from rich import print 
from buscar_extension import buscar_imagenes, elegir_ruta
from cortar_imagen import Interfaz_Edicion

import os
import pathlib

# Función MAIN
if __name__ == "__main__" :

    # carpetas por defecto
    ruta_entrada = "../Imagenes" 
    ruta_salida = "../Recortes"
    # ruta_salida = "../Imagenes"
    modo_test = True

    # print(len(sys.argv))
    if len(sys.argv) >= 2 :
        ruta_entrada = sys.argv[1]
        modo_test = True

    if len(sys.argv) >= 3 :
        ruta_salida = sys.argv[2]
        modo_test = False

    # Conversion de rutas a ruta absoluta
    ruta_entrada = os.path.abspath(ruta_entrada)
    ruta_salida = os.path.abspath(ruta_salida)

    print("[bold yellow] --- RECORTE DE IMAGENES POR CONSOLA ---")
    print("[bold blue]La ventana de recorte se elige haciendo click izquierdosobre la imagen.")
    print("[bold blue]El rectangulo seleccionado para guardar se vuelve verde.")
    print("[bold blue]Comandos desde la terminal:")
    print("[bold blue] python <nombre_rutina> <carpeta_entrada> <carpeta_salida>") 

    print(f"[bold green]Directorio de origen: [bold yellow]{ruta_entrada}")
    # Lista de archivos de imagen editables con OpenCV
    rutas_imagen = buscar_imagenes(ruta_entrada)
    # Conteo imagenes
    numero_imagenes = len(rutas_imagen)
    print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
    print(f"[bold green]Directorio de destino: [bold yellow]{ruta_salida}")

    # # Si los directorios coinciden se lanza una advertencia
    # if  os.path.samefile(ruta_entrada, ruta_salida) :
    #     print("[bold yellow]WARNING: [bold red] ORIGEN Y DESTINO COINCIDENTES.")

    if numero_imagenes > 0 :
 
        # Se abren las imagenes una a una 

        print("[bold green]Teclas usadas")
        print(" [bold green] A : [bold blue] Retroceder") 
        print(" [bold green] D : [bold blue] Avanzar")
        print(" [bold green] S : [bold blue] Guardar (y avanzar)")
        print(" [bold green] ESPACIO : [bold blue] Interumpir")     

        if modo_test :
            print("[bold magenta]Modo TEST: recorte reducido a 256 x 256.")
        else:
            print("[bold green]Modo STANDARD: recorte de 512 x 512.")

        # Si los directorios coinciden se lanza una advertencia
        if  os.path.samefile(ruta_entrada, ruta_salida) :
            print("[bold yellow]WARNING: [bold red] ORIGEN Y DESTINO COINCIDENTES.")

        print("[bold blue]Archivos leidos:")

        indice = 0
        while indice < numero_imagenes: 
            archivo_imagen = rutas_imagen[indice]

            archivo_elegido = pathlib.Path(archivo_imagen).name #NOMBRE ARCHIVO
            # directorio_nuevo = pathlib.Path(archivo_imagen).mkdir #  CREAR carpeta
            # directorio_nuevo = pathlib.Path(archivo_imagen). #  CREAR carpeta

            archivo_recorte = pathlib.Path(ruta_salida).joinpath(archivo_elegido)
            # conversion a ruta absoluta
            archivo_recorte = str(archivo_recorte.absolute())

            if modo_test :
                tecla, guardado = Interfaz_Edicion(archivo_imagen , archivo_recorte, ancho_recorte=256, alto_recorte=256)
            else:
                tecla, guardado = Interfaz_Edicion(archivo_imagen , archivo_recorte)

            print(f"{indice}[green] tecla: [bold blue]'{tecla}' [green], guardado: [yellow]{guardado}[green], archivo: [yellow]{archivo_elegido}")

            # la tecla 'a' permite volver a la imagen anterior 
            if tecla == 'a':
                indice -= 1
            # la tecla SPACE interrumpe el bucle
            elif tecla == ' ' :
                break
            # las teclas 's' y 'd' permiten avanzar 
            else :
                indice += 1
            
    else:
        # Mensajes de error y salida del programa
        print("[bold red]No hay imagenes disponibles en el directorio")
        print("[bold red]Cancelado")



    
