#! /bin/bash

# desactivado del entorno virtual (preventivo)
deactivate 

echo "Borrado de paquetes y archivos auxiliares"

carpetas=('build' 'virtual_env') 

for carpeta in ${carpetas[*]}
do
    if existe=`test -d $carpeta`
    then
        eliminado=`rm -r  $carpeta`
        if $eliminado
        then
            echo "Carpeta $carpeta eliminada" 
        else 
            echo "Carpeta $carpeta inexistente"
        fi
    fi

done

echo "Terminado"