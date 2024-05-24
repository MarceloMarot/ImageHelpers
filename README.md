

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
    -  jpg: recomendado para fotos, dibujos, etc;
    -  jpeg;
    -  png: recomendado para diagramas de bloques, capturas de ventanas, etc;
    -  webp;
    -  bmp;

    Este programa no reescribe imágenes preexistentes en la carpeta de destino.


- ### Organizador de Archivos
    Un asistente para mover archivos en masa según su extensión al directorio destino, con opción de ordenar por año y mes de creación o modificación. 

    Si hay un archivo en destino con igual nombre y extensión no lo reescribe.

    Pensado para uso general.


### Requisitos del sistema

#### Software

El proyecto requiere que el sistema disponga de Python3 y GIT. Se recomienda asimismo el uso de la terminal Bash por ser ejecutable tanto en Windows como en GNU/Linux.

[Descargar Python](https://www.python.org/downloads/)

[Descargar Git+Bash](https://git-scm.com/downloads)



#### Ramdisk (sólo en sistemas Windows)

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

#### Espacio en disco

El proyecto en sí mismo requiere un espacio en disco de alrededor de casi **1GB** para la instalación (sin incluir las dependencias previas). Este espacio puede reducirse poco más de **300 MB** luego de eliminar los archivos auxiliares (ver más adelante).



## Instalación

### Instrucciones:

#### 1 - Clonar repositorio

Para comenzar la instalacion del software hay que descargar el repositorio. Para ello abrir una terminal de Bash, copiar en ella esta rutina :
```bash
# descarga del repositorio
git clone https://github.com/MarceloMarot/ImageHelpers.git
# entrada a la carpeta principal
cd ImageHelpers/
```
y presionar ENTER.

#### 2 - Instalar paquetes y compilar

ara ello 

Abrir una terminal de Bash dentro de la carpeta del proyecto, copiar en ella esta rutina:

```bash
chmod +x instalar.sh  compilar.sh  vaciar.sh # permiso ejecucion asignado
git pull                # descarga de actualizaciones desde GitHub
./instalar.sh           # descarga e instalacion paquetes --> crea entorno virtual interno
./compilar.sh           # creacion de ejecutables
```
y presionar ENTER.

Esta rutina crea la carpeta ***'distribuibles'*** donde aloja juntos a todos los ejecutables de los programas creados y sus dependencias. Esta carpeta puede reubicarse en otra carpeta para su uso.

La compilación puede tardar en completarse varios minutos, pero sólo se requiere hacerla una vez.


#### 3 - Borrado de archivos auxiliares (opcional)

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
