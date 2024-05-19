
# Eventos y funciones del etiquetador de imagenes 

**(PSEUDOCODIGO ORIENTATIVO)**
```
resultado_directorio:                   VER DETALLES
    cargar_imagenes
    (backup)
    actualizar_lista_dimensiones    # revisar ante galeria vacia
    cargar_galeria_componentes

abrir dataset archivo: 
    cargar_galeria_componentes

filtrar por estado/dimensiones:
    cargar_galeria_componentes

click_imagen_seleccion:
    apuntar_galeria


click_imagen_galeria:
    actualizar_componentes


cargar_galeria_componentes(e| None):
    (relectura dataset archivo)
    filtrar_dimensiones_estados       
    crear_botones_etiquetador            VER AQUI
    actualizar_estilo_estado
    (borrar datos)
    actualizar_componentes 


actualizar_componentes(e | None):               
    (elige img[0] si hace falta)
    -> galeria 
    imagen -> etiquetador_imagen
    imagen_seleccion
    (ocultamiento de galeria vacia)


click_botones_etiquetador:
    actualizar bordes selector
    cargar tags a la imagen


click_botones_ {tags_encontrados}
    filtrar_todas_etiquetas



filtrar_dimensiones_estados(e|None):     CORREGIR
    filtrar_dimensiones         
    filtrar_estados            
    estadisticas
    <!-- actualizar_componentes -->


<!-- handler -->
filtrar_todas_etiquetas:        
    (correccion tags)
    filtrar_etiquetas
    actualizar_componentes


estadisticas:
    (backup)
```