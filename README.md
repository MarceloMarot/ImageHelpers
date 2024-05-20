

# Image Helpers

## Introducción

Este repositorio incluye varios utilitarios desarrollados en Python para trabajar con imágenes. La interfaz gráfica usa Flet (Flutter para Python) y se usa OpenCV para el procesamiento de imágenes. Los programas se compilan con ayuda de PyInstaller y **pueden usarse tanto en Windows como en GNU/Linux**.

El código fuente de los programas está escrito casi totalmente **en español** y se distribuye con la **licencia MIT**. 

## Utilitarios desarrollados:


- ### Etiquetador Imágenes

    Un etiquetador manual de imágenes que crea archivos TXT con ciertas palabras clave para describir imágenes. Pensado para preparar sets de imágenes para el entrenamiento de modelos, LoRAs, etc. para IAs de imagen.

    Incluye: 
    - detección de etiquetas presentes; 
    - filtrado de imágenes por etiquetas;
    - importación de dataset desde archivo TXT;
    - marcado gráfico de cambios;
    - activacion de etiquetas mediante botones gráficos;
    - ordenamiento y activación de etiquetas en grupos.


- ### Recortador Imágenes
    Un recortador de imágenes con tamaño de salida seleccionable, con opciones de dimensiones fijas. Dispone de zoom de imagen por interpolación y ventana de selección.

    Útil para seleccionar recortes de personajes, posturas corporales, etc.


- ### Convertidor Imágenes
    Un convertidor de imágenes que convierte las imagenes de un formato a otro en grupo, respetando las dimensiones originales. 
    
    Formatos de salida disponibles:
    -  jpg;
    -  jpeg;
    -  png;
    -  webp;
    -  bmp;

    No reescribe imágenes en el lugar de destino.


- ### Organizador de Archivos
    Un asistente para mover archivos en masa según su extensión al directorio destino, con opción de ordenar por año y mes de creación o modificación. 

    Si hay un archivo en destino con igual nombre y extensión no lo reescribe.

    Pensado para uso general.



## Instalación

### Requisitos del sistema

#### Software

El proyecto requiere que el sistema disponga de Python3 y GIT. Se recomienda asimismo el uso de la terminal Bash por ser ejecutable tanto en Windows como en GNU/Linux.

[Descargar Python](https://www.python.org/downloads/)

[Descargar Git+Bash](https://git-scm.com/downloads)


#### Espacio en disco

El proyecto en sí mismo requiere un espacio en disco de alrededor de casi **1GB** para la instalación (sin incluir las dependencias previas). Este espacio puede reducirse poco más de **300 MB** luego de eliminar los archivos auxiliares (ver más adelante).


#### Ramdisk (sólo Windows)

El recortador de imagenes funciona creando archivos temporales de las imágenes cada vez que se selecciona un recorte de imagen. Por ello el programa funciona mejor si el equipo dispone de algun directorio en memoria RAM donde alojarlos, esto le permite editar los recortes mucho más rápido y minimizar las escrituras en disco.

Para ello en **equipos Windows** es recomendable instalar un creador de discos RAM (*ramdisk*) como por ejemplo **ImDisk**.

[Descargar ImDisk Toolkit para Windows](https://sourceforge.net/projects/imdisk-toolkit/)

Instrucciones de uso:
- Instalar el toolkit.
- Crear una unidad RAM con letra R y espacio de al menos 256MB. Ruta equivalente: **'R:\\'**
- Montar la unidad R **antes** de iniciar el recortador de imágenes.

Si el programa recortador no puede acceder a la ruta RAM especificada usará la carpeta TEMP del usuario actual (carpeta oculta, disco SDD o HDD) con recortes e imagenes temporales que usa el programa y que elimina al cerrarse. 

La carpeta TEMP del usuario actual en Windows 10 se encuentra habitualmente en:
```bash
C:\Users\USUARIO_ACTUAL\AppData\Local\Temp
``` 

Como contrapartida, en **equipos GNU/Linux** se usa directamente la ruta RAM ubicada en ***'/dev/shm'***, presente en las distribuciones más habituales. Por ello normalmente **no se requiere software adicional.** Si */dev/shm* no existe entonces los archivos temporales se cargarán a la *carpeta TMP* del sistema, la cual es análoga a TEMP.

### Clonar repositorio

Para comenzar la instalacion del software hay que descargar el repositorio. Para ello abrir una terminal de Bash y copiar en ella los comandos:
```bash
# descarga del repositorio
git clone https://github.com/MarceloMarot/ImageHelpers.git
# entrada a la carpeta principal
cd ImageHelpers/
```
Los comandos se ejecutan al **pulsar** **ENTER**.

### Instalacion de paquetes

Los paquetes de Python necesarios se instalan automáticamente ejecutando una simple rutina en Bash:
```bash
chmod +x instalar.sh    # permiso ejecucion asignado
./instalar.sh           # descarga e instalacion paquetes
```
Esta rutina crea un *entorno virtual* dentro de la subcarpeta llamada *'virtual_env'* donde se descargan todos los paquetes de Python requeridos. 

La alternativa al copy-paste sobre la terminal es seleccionar al archivo ***instalar.sh*** con el mouse, hacer click derecho y seleccionar la opción de ejecutar como programa.

### Interpretado (opcional)

Los programas se pueden interpretar con ayuda del intérprete de Python. Esto permite probar y usar los programas sin necesidad de compilarlos; no obstante el funcionamiento de los mismos será más lento.

El primer paso para el interpretado es activar el entorno virtual:

```bash
# activacion entorno virtual
source virtual_env/Scripts/activate  # sistema Windows
source virtual_env/bin/activate      # sistema GNU/Linux
```

Luego se llama al intérprete de Python con el nombre del programa indicado :

```bash
py etiquetador_imagenes.py  
py recortador_imagenes.py
py convertidor_imagenes.py
py organizador_archivos.py  
```

En algunos sistemas el intérprete de Python tiene el alias *'py3'*, en tal caso usar estas instrucciones:

```bash
py3 etiquetador_imagenes.py  
py3 recortador_imagenes.py
py3 convertidor_imagenes.py
py3 organizador_archivos.py  
```
**Importante:**: es posible que estos programas se ***"tilden"*** al intentar ejecutarlos por primera vez. En tal caso conviene forzar la detención y llamar de nuevo al intérprete.


### Creación de ejecutables

Los programas se pueden construir por compilación, lo cual permite crear ejecutables que se abrirán con un simple doble click del mouse y que funcionarán más rápidamente.

Los ejecutables de cada programa se pueden construir automáticamente ejecutando la rutina *'compilar.sh'*:

```bash
chmod +x compilar.sh    # permiso ejecucion asignado
./compilar.sh           # creacion de ejecutables
```
Esta rutina crea la carpeta ***'distribuibles'*** donde aloja juntos a todos los ejecutables de los programas creados y sus dependencias. Esta carpeta puede reubicarse para su uso.

También crea la carpeta auxiliar *'build'* donde se crean archivos auxiliares para la construccion de los ejecutables.

La compilación puede tardar en completarse varios minutos, pero sólo se requiere hacerla una vez.

### Actualización de software

El software se puede actualizar fácilmente con la rutina:

```bash
git pull        # descarga de actualizaciones desde GitHub
./instalar.sh   # actualizacion paquetes de Python
./compilar.sh   # creacion ejecutables actualizados
```
En la carpeta ***'distribuibles'*** se encontrarán los programas actualizados al terminar.

### Borrado de archivos auxiliares

La rutina *'vaciar.sh'* elimina las carpetas *'build'* y *'virtual_env'* juntas:

```bash
chmod +x vaciar.sh    # permiso ejecucion asignado
./vaciar.sh           # eliminacion carpetas auxiliares
```
Esto ahorra de espacio en disco alrededor de 600MB; sin embargo también obliga a descargar y reinstalar los paquetes en caso de requerirse la reconstrucción o actualización de los ejecutables.


### Problemas conocidos

#### Windows Defender

- Los antivirus (particularmente: Windows Defender),al intentar construir los ejecutables, pueden dar alerta de troyanos  y hacer fracasar la compilación. Esto se debe al acceso del programa recortador de imagenes a la carpeta de archivos temporales, lo cual es un mecanismo habitual de los troyanos. 

    Este problema puede solucionarse eligiendo la opción "Permitir" de Windows Defender cuando el aviso emergente aparezca y repetir la compilación. También puede ayudar el intentar ejecutar los otros programas del pack.


#### Gestores de entorno

- Los gestores de entornos de ejecución como Conda pueden interferir con la instalación debido a que este proyecto usa por defecto el entorno virtual VENV.
