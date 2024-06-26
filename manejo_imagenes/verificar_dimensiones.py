import cv2 as cv


def dimensiones_imagen(ruta: str)->tuple[int, ...]|None:
    """Devuelve las dimensiones de un archivo de imagen. Orden de parámetros:
    - altura
    - base
    - numero de canales: 
        -1: monocromatica
        -3: color 
        -4: color y transparencia
    Si el archivo no se pudo abrir la funcion devuelve 'None'. 
    """
    imagen = cv.imread(ruta)
    if imagen is None:
        return None
    else:
        dimensiones = imagen.shape
        del imagen
        return tuple(dimensiones)


if __name__=="__main__":
    import sys , os

    try:
        # se busca en el directorio indicado
        ruta = os.path.abspath(sys.argv[1])

        dimensiones = dimensiones_imagen(ruta)
        if dimensiones != None:
            altura, base, canales = dimensiones
            # base, altura, canales = list(dimensiones)
            print(f"Dimensiones: {base} X {altura} X {canales}")
        else: 
            print("Error de apertura")

    except:
        print("Error de ruta de archivo")


