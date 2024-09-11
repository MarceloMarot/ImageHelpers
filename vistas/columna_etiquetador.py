
from manejo_texto.procesar_etiquetas import  Etiquetas
from componentes.etiquetador_botones import EtiquetadorBotones  
from vistas.columna_etiquetas import filas_filtrado


# Componentes globales


etiquetador_imagen = EtiquetadorBotones()




############### funciones ###################

def crear_botones_etiquetador(dataset: Etiquetas):
    """Crea los botones del etiquetador en base al archivo de texto indicado y a los tags ya presentes en las imagenes actuales"""

    # reestablecimiento de la estructura de dataset (solo deja tags procedentes de archivo)
    dataset.datos = dataset.datos_archivo 

    # lectura de todas las etiquetas encontradas en las imagenes
    tags_grupos = filas_filtrado.dataset.tags_grupos
    # borrado de numeros estadisticos
    for lista in tags_grupos:
        for tag in lista:
            i = tags_grupos.index(lista)
            j = lista.index(tag)
            tag = tag.split("(")[0].strip()
            tags_grupos[i][j] = tag

    # descarte de etiquetas ya incluidas desde archivo     
    tags_archivo = dataset.tags_archivo
    for tags_lista  in tags_grupos:
        i = tags_grupos.index(tags_lista )
        tags_faltantes = set(tags_lista).difference(tags_archivo)
        tags_faltantes = list(tags_faltantes)
        tags_grupos[i] = tags_faltantes

    # agregado de las etiquetas, un grupo por vez
    for lista in tags_grupos:
        dataset.agregar_tags(lista, sobreescribir=False)

    # crea la botonera de edicion
    etiquetador_imagen.leer_dataset(dataset)

    # # Eventos de los botones
    # etiquetador_imagen.evento_click(
    #     funcion_etiquetas   = click_botones_tags,
    #     funcion_grupo       = click_botones_etiquetador,
    #     funcion_comando     = click_botones_etiquetador
    #     )







