
# Pendientes y Bugs - Recortador Imágenes

## Pendientes:

-  evento del click mouse anulado tras click en galeria por varios segundos (parece ser propiedad de la animacion 'scroll_to()')
- refactorizar y modularizar codigo
- reordenar y compactar código 
- traduccion i18n
- agregar filtrado de imagenes por estado actual: marcada, guardada, etc.
- pasar las dimensiones de recorte a un archivo de configuración
- BUG: cargar una carpeta de imágenes reestablece la carpeta de salida
- BUG: Si el zoom de la imagen actual es muy bajo el recorte será de dimensiones incorrectas.


## Hecho / corregido:

- boton de guardado global
- crear miniaturas temporales para imagenes cargadas
- cargar miniaturas desde el comienzo
- crear carpeta por defecto para los recortes 
- asignar nombre para recortes desde el comienzo
- BUG: corregir numero zoom al cambiar de imagen
- BUG : barra de zoom rota / inutilizada
- archivos temporales dentro de "/dev/shm" siempre que exista
- eliminacion de archivos temporales al cerrar programa