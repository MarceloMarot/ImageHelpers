#! /bin/bash

# creacion directorio para entorno virtual
py -m venv virtual_env/

# activacion entorno virtual
source virtual_env/bin/activate 

# actualizar PIP
pip install --upgrade pip

# instalacion desde archivo
pip  install -r requirements.txt
 

# crear ejecutables
# flet pack ImageTagger.py
# flet pack FileMover.py --add-data ./local:./local  # Importacion de traducciones fallida
# Running PyInstaller: ['ImageTagger.py', '--noconfirm', '--noconsole', '--onefile']

pyinstaller etiquetador_imagenes.py --distpath dist/ --noconfirm --noconsole --onefile --add-data traducciones/:dist/traducciones
pyinstaller recortador_imagenes.py --distpath dist/ --noconfirm --noconsole --onefile --add-data traducciones/:dist/traducciones
pyinstaller convertidor_imagenes.py --distpath dist/ --noconfirm --noconsole --onefile --add-data traducciones/:dist/traducciones
pyinstaller organizador_archivos.py --distpath dist/ --noconfirm --noconsole --onefile --add-data traducciones/:dist/traducciones



