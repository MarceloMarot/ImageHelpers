# test:
# py -m sistema_archivos.imagen_temporal
import cv2
import tempfile
import flet as ft
import pathlib
import time

from . archivos_temporales import crear_directorio_temporal


def crear_imagen_temporal(
    ruta_archivo_disco: str, 
    directorio_virtual: tempfile.TemporaryDirectory | None = None,
    extension: str = ".bmp"
    ):
    """Esta funcion crea una imagen temporal con la extensión indicada. 
    Opcionalmente se puede alojar en un subdirectorio temporal preexistente.
    Por defecto la funcion creada será BMP por tener la conversión más rápida (aunque es el formato mas pesado).   
    """
    # nombre archivo temporal (prefijo)
    nombre = pathlib.Path(ruta_archivo_disco).stem
    nombre = str(nombre)

    dir = None if directorio_virtual == None else directorio_virtual.name
    archivo_temporal = tempfile.NamedTemporaryFile( 
            prefix = nombre,    # parte del nombre de archivo
            suffix = extension,    # extensión añadida de archivo
            dir = dir,
            # configuracion recomendada Windows (en POSIX no molesta)
            delete = True,
            delete_on_close= False,
            )

    # # apertura archivo en modo lectura binaria
    img = cv2.imread(ruta_archivo_disco)
    # # Asignacion de data al archivo
    cv2.imwrite(archivo_temporal.name, img)
    del img
    # retorno del descriptor del archivo temporal
    return archivo_temporal


if __name__ == "__main__":

    ruta_archivo = "manejo_imagenes/ejemplo2.jpg"
    ruta_archivo = "manejo_imagenes/ejemplo.jpg"
    
    extensiones = [
        ".jpg",
        ".png",
        ".webp", # extremadamente lento
        ".bmp", # el más veloz y el más pesado
        ]

    carpeta_temporal = crear_directorio_temporal("ensayo")
    print("carpeta temporal: ", carpeta_temporal.name)
    archivos = []

    for ext in extensiones:
        inicio = time.time()
        archivo_temporal = crear_imagen_temporal(ruta_archivo, carpeta_temporal, ext) #imagenes en carpeta
        # archivo_temporal = crear_imagen_temporal(ruta_archivo, extension=ext) # imagenes sueltas
        archivos.append(archivo_temporal)
        fin = time.time()

        print("archivo temporal: ",archivo_temporal.name)
        print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")


    # apertura de una imagen temporal y espera
    ventana = "imagenes temporales"
    cv2.namedWindow(ventana)
    img = cv2.imread(archivo_temporal.name)
    cv2.imshow(ventana, img)
    cv2.waitKey(0)

    # elimina archivos temporales sueltos
    for archivo in archivos:
         archivo.close()

    # elimina la carpeta temporal y sus archivos internos
    carpeta_temporal.cleanup()


