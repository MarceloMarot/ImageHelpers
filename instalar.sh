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
flet pack ImageTagger.py
