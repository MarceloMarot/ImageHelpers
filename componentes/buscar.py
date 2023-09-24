import pathlib



# Busqueda de archivos por extensión en una carpeta (incluye subdirectorios)
def buscar_extension(ruta: pathlib.Path, extension: str):
    #se buscan todos los elementos con la terminacion indicada
    lista_rutas_archivo = []
    for direccion in pathlib.Path(ruta).rglob(extension):
        direccion_actual = str(direccion.absolute())
        lista_rutas_archivo.append ( direccion_actual )
    return lista_rutas_archivo


# Busqueda de imágenes en una carpeta (incluye subdirectorios)
def buscar_imagenes(ruta: pathlib.Path):
    lista_rutas_imagen = []
    # Formatos de texto reconocidos por OpenCV (casi todos)
    # NO se incluyen GIF y SVG
    extensiones_OpenCV = ["*.bmp", "*.dib", "*.jpeg", "*.jpg", "*.jpe", "*.jp2", "*.png", "*.webp", "*.pbm", "*.pgm", "*.ppm", "*.pxm", "*.pxm", "*.pnm", "*.pfm", "*.sr", "*.ras", "*.tiff", "*.tif", "*.exr", "*.hdr", "*.pic"]
    # se busca cada extensión, una por una
    for extension in extensiones_OpenCV:
        lista_rutas_imagen = lista_rutas_imagen + buscar_extension(ruta, extension) #Concatenacion de listas
    # numero_imagenes = len(lista_rutas)
    return lista_rutas_imagen