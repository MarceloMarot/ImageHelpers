from pathlib import Path


def ruta_relativa_usuario(ruta: str):
    """Extrae la ruta personal de usuario de la ruta de entrada."""
    ruta_entrada = Path(ruta)
    carpeta_home = Path().home() 

    relativos = Path(ruta_entrada).is_relative_to(carpeta_home)
    if relativos:
        n = len(str(carpeta_home))
        ruta_salida = ruta[n:]

        # print(str(carpeta_home))
        # print(ruta_salida)
        return ruta_salida
    else:
        return ruta
