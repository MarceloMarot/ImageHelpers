#! /bin/bash

# configuraciones
carpeta_destino='distribuibles'
carpeta_union='temporal'
carpeta_traducciones='traducciones'



carpeta_dependencias='_internal' # valor por defecto




# activacion entorno virtual
directorio_virtual='virtual_env' # carpeta entorno virtual creado
sistema=`uname`
sistema=${sistema,,} # conversion a minusculas
# echo "$sistema"

if [ $sistema = "linux" ]    # conversion a minusculas y comparacion
then    
    echo "Sistema GNU/Linux detectado"
    source $directorio_virtual/bin/activate
    if `source "$directorio_virtual"/bin/activate`   # caso Linux
    then
        echo "entorno virtual activado"
    else 
        echo "ERROR: no se pudo activar el entorno virtual"
    fi
else    
    echo "Sistema Windows detectado"
    source "$directorio_virtual"/Scripts/activate
    if `source "$directorio_virtual"/Scripts/activate`   # caso Windows
    then
        echo "entorno virtual activado"
    else 
        echo "ERROR: no se pudo activar el entorno virtual"
    fi
fi



# Busqueda de rutinas principales Python
lista_archivos=`ls` 

lista_python=()
lista_programas=()

for elemento in ${lista_archivos[*]}
do 
    extension_archivo="${elemento##*.}" # elimina todo hasta el último punto
    nombre_archivo="${elemento%.*}"     # elimina todo desde el último punto
    # echo "$elemento , $extension_archivo"    
    if [ "$extension_archivo" = "py" ]
    then
        # echo "$elemento , $extension_archivo"    
        lista_python+=("$elemento") 
        lista_programas+=("$nombre_archivo") 
    fi
done
echo ""

# lectura de lista completa
echo "Rutinas Python encontradas:"
echo "${lista_python[*]}"
echo "Programas a compilar:"

for nombre in ${lista_programas[*]}
do
    echo "  - $nombre"
done





echo ""
if `test -d "$carpeta_destino/$carpeta_union"`
then
    echo "Directorio temporal '$carpeta_destino/$carpeta_union' preexistente"
else
    mkdir "$carpeta_destino/$carpeta_union"
    echo "Directorio temporal '$carpeta_destino/$carpeta_union' creado"
fi
echo ""
echo ""
echo "Creación y compilacion de programas"
echo ""

for elemento in ${lista_programas[*]}
do 
    # compilacion ejecutable
    echo "Compilando $elemento..."
    pyinstaller $elemento.py --distpath $carpeta_destino --noconfirm --noconsole --add-data $carpeta_traducciones/:$carpeta_destino/$carpeta_traducciones
    # compactado en directorio unico
    cd $carpeta_destino
    if `test -f "$elemento/$elemento"`
    then
        # actualizacion de objetos creados
        cp -u $elemento/$elemento  _$elemento
        cp -r -u  $elemento/$carpeta_dependencias/  .
        # eliminacion de elementos originales
        rm -r $elemento
        # renombrado de ejecutable salida
        mv  _$elemento $elemento
    fi
    cd ..
done

echo ""
echo "Programas creados y compactados"
echo ""


# borrado de carpeta temporal
rm -r $carpeta_destino/$carpeta_union
echo "Directorio temporal '$carpeta_destino/$carpeta_union' eliminado"

# copia archivos traduccion
echo "Copiando archivos de traducciones"
cp -r  $carpeta_traducciones/  $carpeta_destino/$carpeta_traducciones
echo "Hecho!"


# fin rutina

deactivate # cerrado del entorno virtual

echo ""
echo ""
echo "Compilacion completada"

