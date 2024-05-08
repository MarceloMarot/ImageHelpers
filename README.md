

# Image Helpers

## Introducción

Este repositorio incluye varios utilitarios desarrollados en Python para trabajar con imágenes. La interfaz gráfica usa Flet (Flutter para Python) y se usa OpenCV para el procesamiento de imágenes. Los programas se compilan con ayuda de PyInstaller y pueden usarse tanto en Windows como en GNU/Linux.

El código fuente de los programas está escrito casi totalmente en español y se distribuye con la licencia MIT. 

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
    Un convertidor de imágenes que convierte las imagenes de un formato a otro en grupo, respetando las dimensiones originales. Formatos de salida disponibles:
    -  jpg;
    -  jpeg;
    -  png;
    -  webp;
    -  bmp;


- ### Organizador de Archivos
    Un asistente para mover archivos en masa según su extensión al directorio destino, con opción de ordenar por año y mes de creación o modificación. 

    Pensado para uso general.



## Instalación

### Requisitos del sistema

El proyecto requiere que el sistema disponga de Python3 y GIT. Se recomienda asimismo el uso de la terminal Bash por ser ejecutable tanto en Windows como en GNU/Linux.

Para comenzar la instalacion el repositorio se descarga desde GitHub:
```bash
# descarga del repositorio
git clone https://github.com/MarceloMarot/ImageHelpers.git
# entrada a la carpeta principal
cd ImageHelpers/
```

El proyecto en sí mismo requiere un espacio en disco de alrededor de casi **1GB** para la instalación (sin incluir las dependencias previas).
Este espacio puede reducirse a alrededor de **300 MB** al eliminar los archivos auxiliares (ver más adelante).

### Instalacion de paquetes

Los paquetes de Python necesarios se instalan automáticamente ejecutando una simple rutina:
```bash
chmod +x instalar.sh    # permiso ejecucion asignado
./instalar.sh           # descarga e instalacion paquetes
```
Esta rutina crea un *entorno virtual* dentro de la subcaroeta llamada *'virtual_env'* donde se descargan todos los paquetes de Python requeridos. 


### Creación de ejecutables

Los ejecutables de cada programa se pueden construir automáticamente ejecutando la rutina *'compilar.sh'*:

```bash
chmod +x compilar.sh    # permiso ejecucion asignado
./compilar.sh           # creacion de ejecutables
```
Esta rutina crea la carpeta ***'dist'*** donde aloja juntos a todos los ejecutables de los programas creados y sus dependencias. Esta carpeta puede reubicarse para su uso.

También crea la carpeta *'build'* donde se crean archivos auxiliares para la construccion de los ejecutables.


### Actualización 

El software se puede actualizar fácilmente con la rutina:
```bash
git pull        # descarga de actualizaciones desde GitHub
./instalar.sh   # actualizacion paquetes
./compilar.sh   # creacion ejecutables
```
En la carpeta ***'dist'*** se encontrarn los programas al terminar.

### Borrado de archivos

La rutina *'vaciar.sh'* elimina las carpetas *'build'* y *'virtual_env'* juntas:

```bash
chmod +x vaciar.sh    # permiso ejecucion asignado
./vaciar.sh           # eliminacion carpetas auxiliares
```
Esto ahorra de espacio en disco alrededor de 600MB; sin embargo también obliga a descargar y reinstalar los paquetes en caso de requerirse la reconstrucción o actualización de los ejecutables.


### Problemas conocidos

#### Windows

-  El recortador de imágenes en Windows carga la carpeta TEMP (carpeta oculta) con recortes e imagenes temporales que usa el programa, los cuales deben ser eliminados temporalmente.

    La carpeta TEMP en Windoows 10 se encuentra habitualmente en:
    ```bash
    C:\Users\USUARIO_ACTUAL\AppData\Local\Temp
    ``` 

- Los antivirus (particularmente: Windows Defender) pueden dar alerta de troyanos y hacer fracasar la compilación. Esto se debe al acceso del programa  'recortador_imagenes' a la carpeta de archivos temporales, lo cual es un mecanismo habitual de los troyanos.

#### Gestores de entorno

- Los gestores de entornos de ejecución como Conda pueden interferir con la instalación debido a que este proyecto usa por defecto el entorno virtual VENV.
