from pathlib import Path

# archivo "clasificar_archivos" aledaño (mismo subdirectorio)
from . buscar_extension import buscar_extension
# from sistema_archivos.buscar_extension import buscar_extension

from rich import print




# listar todas las extensiones de archivo de un directorio
def listar_extensiones(ruta: str, distinguir_mayusculas = False ):
    lista_archivos =  buscar_extension(ruta, "*.*")
    set_extensiones = set()
    for archivo in lista_archivos:
        if distinguir_mayusculas: 
            extension = Path(archivo).suffix
        else:
            extension = Path(archivo).suffix.lower()
        # print(extension)
        set_extensiones.add(extension)

    return list(set_extensiones)





# Función MAIN
if __name__ == "__main__" :
    try:
        # se busca en el directorio indicado
        ruta = os.path.abspath(sys.argv[1])

    except:
        # se busca en el directorio de la rutina
        ruta = "./"

    finally:

        extensiones = listar_extensiones(ruta, True)
        print("[bold yellow]Extensiones (todas):")
        print(f"[bold green] {extensiones}")
        extensiones = listar_extensiones(ruta, False)
        print("[bold yellow]Extensiones (solo minusculas):")
        print(f"[bold blue] {extensiones}")