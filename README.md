

# Image Helpers


Contenidos:


- [Introducción](#introducción)
- [Utilitarios desarrollados](#utilitarios-desarrollados)
    - [Etiquetador Imágenes](#etiquetador-imágenes)
    - [Recortador Imágenes](#recortador-imágenes)
    - [Convertidor Imágenes](#convertidor-imágenes)
    - [Organizador de Archivos](#organizador-de-archivos)
- [Requisitos del sistema](#requisitos-del-sistema)
    - [Software básico](#software-básico)
    - [Ramdisk (sólo necesario en sistemas Windows)](#ramdisk-sólo-necesario-en-sistemas-windows)
    - [Espacio en disco](#espacio-en-disco)
- [Instrucciones de instalación](#instrucciones-de-instalación)
    - [1 - Clonar repositorio](#1---clonar-repositorio)
    - [2 - Instalar paquetes y compilar](#2---instalar-paquetes-y-compilar)
    - [3 - Borrado de archivos auxiliares (opcional)](#3---borrado-de-archivos-auxiliares-opcional)
- [Problemas conocidos](#problemas-conocidos)
    - [Windows Defender](#windows-defender)
    - [Gestores de entorno](#gestores-de-entorno)


## Introducción

Este repositorio incluye varios utilitarios desarrollados en Python para trabajar con imágenes. La interfaz gráfica usa Flet (Flutter para Python) y se usa OpenCV para el procesamiento de imágenes. Los programas se compilan con ayuda de PyInstaller y **pueden usarse tanto en Windows como en GNU/Linux**.

El código fuente de los programas está escrito casi totalmente **en español** y se distribuye con la **licencia MIT**. 



## Utilitarios desarrollados


### Etiquetador Imágenes

Un etiquetador manual de imágenes que crea archivos TXT con ciertas palabras clave para describir imágenes. Pensado para preparar sets de imágenes para el entrenamiento de modelos, LoRAs, etc. para IAs de imagen. 
Incluye: 
- detección de etiquetas presentes, con ordenamiento automático por frecuencia de uso; 
- filtrado de imágenes por etiquetas;
- importación de dataset desde archivo TXT;
- marcado gráfico de cambios;
- activacion de etiquetas mediante botones gráficos;
- ordenamiento y activación de etiquetas en grupos (cada renglón del archivo de dataset se interpreta como un "grupo" de etiquetas).

Capturas (versión 0.6.2):

- Etiquetado:

    <image src='capturas/etiquetador_v062-etiquetado.jpg' width=700em alt="Etiquetador - etiquetado manual (v0.6.2)" >

- Filtrado de imágenes por tags:

    <image src='capturas/etiquetador_v062-seleccion.jpg' width=700em alt="Etiquetador - seleccion manual (v0.6.2)" >


### Recortador Imágenes

Un recortador de imágenes con tamaño de salida seleccionable, con opciones de dimensiones fijas. Dispone de zoom de imagen por interpolación y ventana de selección.


<image src='capturas/recortador_v062.jpg' width=700em alt="Recortador - zoom y recorte (v0.6.2)" >

Útil para seleccionar recortes de personajes, posturas corporales, etc.


### Convertidor Imágenes

Un convertidor de imágenes que convierte las imagenes de un formato a otro en grupo, respetando las dimensiones originales. 

<image src='capturas/convertidor_v062.jpg' width=400em alt="Convertidor imágenes (v0.6.2)" >

Formatos de salida disponibles:
-  jpg: recomendado para fotos, dibujos, etc;
-  jpeg;
-  png: recomendado para diagramas de bloques, capturas de ventanas, etc;
-  webp;
-  bmp;

Este programa no reescribe imágenes preexistentes en la carpeta de destino.


### Organizador de Archivos

Un asistente para mover archivos en masa según su extensión al directorio destino, con opción de ordenar por año y mes de creación o modificación. 

<image src='capturas/organizador_v062.png' width=400em alt="Convertidor imágenes (v0.6.2)" >

Si hay un archivo en destino con igual nombre y extensión no lo reescribe, simplemente omite su reubicación y sigue con los siguientes.

Pensado para uso general.

**Advertencia:** este programa puede romper páginas HTML guardadas localmente (archivo texto HTML + carpeta contenidos) como también arruinar proyectos guardados que tengan archivos con la extensión elegida. 
No incluye opciones de restauración de ubicaciones; por ello **elegir las carpetas a ordenar con prudencia**.





## Requisitos del sistema

### Software básico

El proyecto requiere que el sistema disponga de Python3 y GIT. Se recomienda asimismo el uso de la terminal Bash por ser ejecutable tanto en Windows como en GNU/Linux.

[Descargar Python](https://www.python.org/downloads/)

[Descargar Git+Bash](https://git-scm.com/downloads)



### Ramdisk (sólo necesario en sistemas Windows) 

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

### Espacio en disco

El proyecto en sí mismo requiere un espacio en disco de alrededor de casi **1GB** para la instalación (sin incluir las dependencias previas). Este espacio puede reducirse poco más de **300 MB** luego de eliminar los archivos auxiliares (ver más adelante).




## Instrucciones de instalación

### 1 - Clonar repositorio

Para comenzar la instalacion del software hay que descargar el repositorio. Para ello abrir una terminal de Bash, copiar en ella esta rutina :
```bash
# descarga del repositorio
git clone https://github.com/MarceloMarot/ImageHelpers.git
# entrada a la carpeta principal
cd ImageHelpers/
```
y presionar ENTER.

### 2 - Instalar paquetes y compilar

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


### 3 - Borrado de archivos auxiliares (opcional)

La rutina *'vaciar.sh'* elimina las carpetas *'build'* y *'virtual_env'* juntas:

```bash
chmod +x vaciar.sh    # permiso ejecucion asignado
./vaciar.sh           # eliminacion carpetas auxiliares
```
Esto ahorra de espacio en disco alrededor de 600MB; sin embargo también obliga a descargar y reinstalar los paquetes en caso de requerirse la reconstrucción o actualización de los ejecutables.



## Problemas conocidos

### Windows 

#### Windows Defender

- Los antivirus (particularmente: Windows Defender),al intentar construir los ejecutables, pueden dar alerta de troyanos  y hacer fracasar la compilación. Esto se debe al acceso del programa recortador de imagenes a la carpeta de archivos temporales, lo cual es un mecanismo habitual de los troyanos. 

    Este problema puede solucionarse eligiendo la opción "Permitir" de Windows Defender cuando el aviso emergente aparezca y repetir la compilación. También puede ayudar el intentar ejecutar los otros programas del pack.


### Linux

#### libmpv.so.1 faltante 

Flet requiere la biblioteca **libmpv** en su versión `libmpv.so.1`.
La biblioteca puede instalarse con:

```bash
sudo apt install libmpv-dev mpv     # caso Ubuntu / Debian
sudo dnf mpv-devel.x86_64 mpv       # caso Fedora
```
Se necesita verificar la existencia de la biblioteca en el sistema :

```bash
# caso Ubuntu / Debian
cd /usr/lib
ls *mpv*

# caso Fedora
cd /usr/lib64
ls *mpv*
```
El resultado suele ser algo como:

```bash
libmpv.so libmpv.so.2 libmpv.so.2.1.0
```

Entonces el problema puede solucionarse creando un **enlace simbólico** llamado `libmpv.so.1` dentro de la carpeta `/usr/lib/` y/o `/usr/lib64/`, dependiendo de la distribución usada:

```bash
$ sudo ln -s    /usr/lib/libmpv.so     /usr/lib/libmpv.so.1      # caso Ubuntu / Debian
$ sudo ln -s    /usr/lib64/libmpv.so   /usr/lib64/libmpv.so.1    # Caso Fedora
```
Más información:

[GitHub - Flet 0.20.0 mpv error #2639](https://github.com/flet-dev/flet/discussions/2639)

[GitHub Gist - Installing the packages and creating a symbolic link](https://gist.github.com/luizmarinhojr/f5ede39febd53fceb757eef88618f2b8)

### Gestores de entorno

Los gestores de entornos de ejecución como Conda pueden interferir con la instalación debido a que este proyecto usa por defecto el entorno virtual VENV.
