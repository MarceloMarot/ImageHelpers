
# Eventos y funciones del recortador de imagenes 

**(PSEUDOCODIGO ORIENTATIVO)**
```
resultado_directorio_origen(e):
    cargar_imagenes_galeria
    (configurar galeria)
    buscar_archivos_recortes

resultado_directorio_destino(e):

    buscar_imagenes
    galeria.ruta_recortes           (reasigna rutas de recorte)
    buscar_archivos_recortes

buscar_archivos_recortes
    (asignar recortes a galeria)
    galeria.actualizar_estilos


click_galeria(e):
    galeria -> imagen
    cargar_selector(imagen)
    imagen -> scroll


teclado_galeria(e):
    opcion cambiar imagenes:
        galeria -> imagen
        cargar_selector()
    opciones zoom:
        selector_recorte.ampliar


cargar_selector:
    selector <- data imagen
    (asignar imagen al selector)
    galeria.actualizar_estilos
    (marcar imagen actual en galeria)
    (actualizar textos)

    actualizar zoom   ??


actualizar_barra_zoom(e |None):
    (actualizar barra)
    (actualizar textos)

escalar_imagen(e):
    selector_recorte.ampliar
    actualizar_barra_zoom()


cambio_dimensiones_recorte(e):
    (cambios )


marcar_recorte(guardar)
    (cambiar propiedades imagen actual)
    imagen actual <- data selector_recorte
    si guardar:
        selector_recorte.temporal.guardar_recorte_archivo
    galeria.actualizar_estilos

click_izquierdo_selector(e):
    marcar_recorte( guardar=NO )

click_derecho_selector(e):
    marcar_recorte( guardar=SI )
```