#! /bin/bash

# creacion directorio para entorno virtual
directorio_virtual='virtual_env'


if `test -d $directorio_virtual`
then
    echo "Directorio virtual preexistente"
    echo "Nombre: $directorio_virtual"

else
    mkdir $directorio_virtual
    echo "Directorio virtual creado"
    echo "Nombre: $directorio_virtual"
fi
echo ""

# creacion entorno virtual
py -m venv "$directorio_virtual"




# activacion entorno virtual
sistema=`uname`
sistema=${sistema,,} # conversion a minusculas
# echo "$sistema"

if [ $sistema = "linux" ]    # conversion a minusculas y comparacion
then    
    echo "Sistema GNU/Linux detectado"
    source $directorio_virtual/bin/activate
    # actualizar PIP
    pip install --upgrade pip
    if `source "$directorio_virtual"/bin/activate`   # caso Linux
    then
        echo "entorno virtual activado"
    else 
        echo "ERROR: no se pudo activar el entorno virtual"
    fi
else    
    echo "Sistema Windows detectado"
    source "$directorio_virtual"/Scripts/activate
    # actualizar PIP
    python.exe -m pip install --upgrade pip
    if `source "$directorio_virtual"/Scripts/activate`   # caso Windows
    then
        echo "entorno virtual activado"
    else 
        echo "ERROR: no se pudo activar el entorno virtual"
    fi
fi


# source virtual_env/bin/activate
pip list   # debe dar una lista casi vacia 

# actualizar PIP
# pip install --upgrade pip

# instalacion desde archivo
pip  install -r requirements.txt
 
pip list   


# fin rutina

deactivate # cerrado del entorno virtual

echo ""
echo ""
echo "Instalacion de entorno virtual completada"


