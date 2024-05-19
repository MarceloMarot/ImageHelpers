

# Pendientes y Bugs - Etiquetador Imágenes

- Usar el "cupertino context menu" para gestionar imagenes, por ejemplo descartarlas
  https://flet.dev/docs/controls/cupertinocontextmenu



## Pendientes:

- listas de dimensiones en archivo JSON
- edicion de listas en JSON
- traduccion i18n
- rutina compilacion (todos programas)
- dividir codigo en varias partes - modularizar
- crear más constantes de diseño (refactorizar)


## Hecho / corregido:

- Mover archivos temporales a carpetas RAM reales:
  - /dev/shm (Linux) 
  - R:\\ (Windows)
- BUG: la navegacion por teclado puede afectar el guardado grupal al apretar ENTER (no así si se guarda clickeando boton flotante)
- agregar menu de confirmacion para guardado global
- agregar menu de confirmacion para descartar cambios y salir
- Habilitar guardado y restauracion por teclado
- BUG: si la ventana es demasiado estrecha varios controles quedan tapados
- BUG: al filtrar puede cambiar el estado de alguna imagen, particularmente la primera.
- BUG: si al filtrar por estados la lista queda vacía se siguen mostrando las imagenes, tags, etc
- BUG: se requiere al menos UNA etiqueta por imagen (no deja borrar etiquetado)
- BUG: marca las imagenes con etiquetas deseleccionadas como 'no etiquetada'
- prevenir relecturas frecuentes de los archivos de etiquetado
- corregir handler  para listas y 'boton_filtrar_dimensiones'  (handler 'cargar_galeria_componentes')
- eliminar 'imagenes_galeria_filtradas_backup'
- INFO emergente: TUTORIAL
- corregir colores etiquetas
- Corregir: guardar dataset en varios renglones
- INFO de texto de la imagen actual: numero, ruta, etc
- agregar botones para modificar y guardar nuevo dataset
- filtrado por tags: que el etiquetador se mueva al boton del tag filtrado (DESHABILITADO)
- activacion/desactivado simultaneo de botones con igual tag
- reconfigurar handler teclado
- revisar el uso de 'actualizar_componentes'
- BUG: "clave" vacía al cargar la galeria por primera vez
- BUG : el boton "guardar cambios" ya no anda -  CRUSH de la terminal
- BUG: no se muestra la edicion de tags existentes antes de cargar dataset (se puede guardar pero no cambian los colores)
- BUG: al haacer click en galeria si la imagene esta "modificada" se desmarcan los tags(no se ven)
- los tags se rehabilitan al cambiar de imagen (previo cargar dataset archivo). 
- reconstruir bordes del selector de imagen
- asegurar la gestion de galerias vacias
- anular el descarte recurrente de tamaños seleccionables
- boton guardado global: actualizar bordes de imagen seleccion

