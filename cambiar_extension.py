
from rich import print

from pathlib import Path

# rutas de ejemplo
filename = Path('/carpeta/mitexto.txt')
# filename = Path('micomprimido.tar.gz')
print("Nombre: ",filename.name)        #nombre (con extension)
print("Extension: ",filename.suffix)      #extension de archivo

filename_wo_ext = filename.with_suffix('')  # extension eliminada

filename_replace_ext = filename.with_suffix('.txd')     # nueva extension asignada

print(filename)

print(filename_wo_ext)

print(filename_replace_ext)

