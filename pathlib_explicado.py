
## PATHLIB.PATH EXPLICADO

from rich import print

from pathlib import Path

# rutas de ejemplo
filename = Path('/carpeta/carpetazo/mitexto.txt')
# filename = Path('micomprimido.tar.gz')
print("Nombre: ",filename.name)        #nombre (con extension)
print("Extension: ",filename.suffix)      #extension de archivo

filename_wo_ext = filename.with_suffix('')  # extension eliminada

filename_replace_ext = filename.with_suffix('.txd')     # nueva extension asignada

print(filename)

print(filename_wo_ext)

print(filename_replace_ext)




print("carpeta:",filename.parent)

print("carpeta superior:",filename.parent.parent)

nueva_carpeta = "/personal"
nueva_ruta = Path(nueva_carpeta, filename.name) 


print("nueva carpeta:", nueva_carpeta)
print("nueva ruta:", nueva_ruta)

# PATH EXPLICADO
# https://www.digitalocean.com/community/tutorials/how-to-use-the-pathlib-module-to-manipulate-filesystem-paths-in-python-3-es