import sys
from rich import print 
from buscar_extension import buscar_imagenes, elegir_ruta
from cortar_imagen import Interfaz_Edicion

# Función MAIN
if __name__ == "__main__" :
    try:
        ruta = sys.argv[1]

    except IndexError():
        print("Error: faltan argumentos  ") 
        print("     Ejemplo uso: python buscar_extension.py <drectorio> *.<extension>  ") 

    except TypeError():
        print("Error: Tipo de datos de entrada erróneo")

    else:
        print(f"[bold green]Directorio: [bold yellow]{ruta} [bold green]")
        # Lista de archivos de imagen editables con OpenCV
        rutas_imagen = buscar_imagenes(ruta)
        # Conteo imagenes
        numero_imagenes = len(rutas_imagen)
        print(f"[bold green]Nº archivos encontrados: [/bold green][bold yellow] {numero_imagenes}") 
        if numero_imagenes > 0 :
            #Lista imagenes
            # print("Imagenes encontradas: ", rutas_imagen)
            archivo_recorte = '../Recortes/recorte.jpg'
            # Apertura de todas las imagenes en orden de aparicion
            # for direccion in rutas_imagen:
            #     archivo_imagen = direccion
            #     tecla, guardado = Interfaz_Edicion(archivo_imagen , archivo_recorte, True, 256, 256)
            #     print(tecla ,guardado, direccion)

            # Se abren las imagenes una a una 
            print("[bold yellow] Recorte de imagenes")
            print("[bold blue]La ventana de recorte se elige haciendo click izquierdo")
            print("[bold green]Teclas usadas")
            print(" [bold green] A : [bold blue] Retroceder") 
            print(" [bold green] D : [bold blue] Avanzar")
            print(" [bold green] S : [bold blue] Guardar (y avanzar)")
            print(" [bold green] ESPACIO : [bold blue] Interumpir")     
            indice = 0
            while indice < numero_imagenes: 
                archivo_imagen = rutas_imagen[indice]
                tecla, guardado = Interfaz_Edicion(archivo_imagen , archivo_recorte, ancho_recorte=256, alto_recorte=256)
                print(indice, tecla ,guardado, archivo_imagen)

                # la tecla 'A' permite volver a la imagen anterior 
                if tecla == 'a':
                    indice -= 1
                # la tecla SPACE interrumpe el bucle
                elif tecla == ' ' :
                    break
                # las teclas 'S' y 'D' permiten avanzar 
                else :
                    indice += 1
                

        else:
            # Mensajes de error y salida del programa
            print("[bold red]No hay imagenes disponibles en el directorio")
            print("[bold red]Cancelado")



    
