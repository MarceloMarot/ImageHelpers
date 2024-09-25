import flet as ft
import re
from componentes.etiquetador_botones import FilasBotonesEtiquetas

from vistas.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags
from manejo_texto.procesar_etiquetas import Etiquetas

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

from vistas.clasificador_etiquetador import clasificador_imagenes


lista_imagenes = clasificador_imagenes


# Entradas de texto
entrada_tags_buscar = ft.TextField(
    label="Buscar coincidencias",
    # on_change=textbox_changed,
    # on_submit=agregar_tags_seleccion,
    height=60,
    width=400
)


entrada_tags_agregar = ft.TextField(
    label="Agregar tags a las imágenes - pulsar 'ENTER' para confirmar",
    # on_change=textbox_changed,
    # on_submit=agregar_tags_seleccion,
    height=60,
    width=400
)

entrada_tags_quitar = ft.TextField(
    label="Quitar tags a las imágenes - pulsar 'ENTER' para confirmar",
    # on_change=textbox_changed,
    # on_submit=quitar_tags_seleccion,
    height=60,
    width=400
)

filas_filtrado = FilasBotonesEtiquetas()
# filas_filtrado.altura = pagina.height - 200
# filas_filtrado.altura = pagina.height - 330     #FIX

filas_filtrado.lista_colores_activo=[
    ft.colors.BLUE_800,
    ft.colors.GREEN_800,
    ft.colors.YELLOW_800,
    ft.colors.ORANGE_800,
    ft.colors.RED_800,
    ]

filas_filtrado.lista_colores_pasivo=[
    ft.colors.BLUE_100,
    ft.colors.GREEN_100,
    ft.colors.YELLOW_100,
    ft.colors.ORANGE_100,
    ft.colors.RED_100,
    ]


boton_reordenar_tags = ft.ElevatedButton(
    text = f"Orden alfabético",
    bgcolor = ft.colors.GREEN_800,
    color = ft.colors.WHITE,
    icon = ft.icons.SORT_ROUNDED
    # tooltip="Reinicia la selección de etiquetas encontradas."
    )

boton_reordenar_tags.valor = True


boton_guardar_dataset = ft.ElevatedButton(
    # text = f"Guardar como dataset",
    text = f"Guardar tags",
    bgcolor = ft.colors.AMBER_800,
    icon=ft.icons.SAVE,
    color = ft.colors.WHITE,
    ## manejador
    on_click=lambda _: dialogo_guardado_tags.save_file(
        dialog_title = "Guardar archivo de dataset (formato .txt)",
        allowed_extensions=["txt"],
        ),
    tooltip="Guarda en archivo de texto las etiquetas encontradas. Si el archivo ya existe lo sobreescribe.",
    )

boton_reset_tags = ft.ElevatedButton(
    text = f"Deseleccionar",
    bgcolor = ft.colors.BLUE_800,
    color = ft.colors.WHITE,
    icon=ft.icons.UNDO_ROUNDED, 
    tooltip="Reinicia la selección de etiquetas encontradas."
    )

texto_contador_tags= ft.Text(
    "Tags encontados:",
    size=15,
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.START,
    )

columna_etiquetas = ft.Column(
    controls=[    
        ft.Row(
            [ texto_contador_tags],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),  
        ft.Row(
            # [boton_reset_tags, 
            [boton_reordenar_tags,
            boton_reset_tags, 
            boton_guardar_dataset],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),  
        ft.Divider(height=7, thickness=1) ,
        entrada_tags_buscar,
        ft.Divider(height=7, thickness=1) ,
        filas_filtrado,
        ft.Divider(height=7, thickness=1) ,
        entrada_tags_agregar, #FIX
        entrada_tags_quitar,
    ],
    # visible=False,      # FIX
    visible=True,
    expand=1,
    # scroll=ft.ScrollMode.HIDDEN, 
    scroll=ft.ScrollMode.AUTO, 
    # height=pagina.height - 330     #FIX
    )


def estadisticas()->dict:
    """Detecta todas las etiquetas usadas en las imagenes y cuenta cuantas repeticiones tiene cada una.
    Crea tambien los botones de filtrado correspondientes a cada una."""

    conteo_etiquetas = dict()

    # lectura de patron de busqueda
    secuencia = entrada_tags_buscar.value
    # descarte de espacios en blanco
    secuencia = secuencia.strip()

    # busqueda y conteo de etiquetas
    for imagen in lista_imagenes.seleccion:  
        for tag in imagen.tags:
            retorno = re.search(secuencia, tag, re.I)
            if retorno !=None:
                conteo_etiquetas[tag] = 1 if tag not in conteo_etiquetas else conteo_etiquetas[tag]+1


    # etiquetas ordenadas de más repetidas a menos usadas
    conteo_etiquetas = dict(sorted(conteo_etiquetas.items(), key=lambda item:item[1], reverse=True))

    nro_tags = len(conteo_etiquetas.keys()) 
    lista_tags = list(conteo_etiquetas.keys()) 

    texto_contador_tags.value = f"Etiquetas encontadas: {nro_tags}"

    boton_reset_tags.text = f"Deseleccionar tags"
    # boton_reset_tags.text = f"Deseleccionar etiquetas ({nro_tags} en total)"

    # etiquetas con numero de repeticiones agregado
    tags_contadas = []
    for tag in lista_tags:
        tags_contadas.append(f"{tag}  ({conteo_etiquetas[tag]})")

    # objeto auxiliar vacio para almacenar etiquetas    
    etiquetas_marcadas = Etiquetas()

    tags_grupo = []


    if boton_reordenar_tags.valor == True:
        
        # ordenamiento por orden alfabetico, un grupo por letra

        letras = []
        set_letras = set()
        for tag in tags_contadas:
            set_letras.add(tag[0])

        letras = list(set_letras)
        letras.sort()

        for tag in tags_contadas:
            n = letras.index(tag[0])
            etiquetas_marcadas.agregar_tags([tag], n)


    else:

        # reparto en grupos y coloreo de botones en base a percentiles del 20%
        umbral_1 = int(nro_tags * Percentil.UMBRAL_1.value)
        umbral_2 = int(nro_tags * Percentil.UMBRAL_2.value)
        umbral_3 = int(nro_tags * Percentil.UMBRAL_3.value)
        umbral_4 = int(nro_tags * Percentil.UMBRAL_4.value)
        umbral_5 = int(nro_tags * Percentil.UMBRAL_5.value)

        for i in range(0, umbral_1):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_1, umbral_2):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_2, umbral_3):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_3, umbral_4):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)

        tags_grupo = []
        for i in range(umbral_4, umbral_5):
            tags_grupo.append(tags_contadas[i])
        etiquetas_marcadas.agregar_tags(tags_grupo)


    filas_filtrado.leer_dataset(etiquetas_marcadas, False)
    filas_filtrado.agregar_tags([], True)
    # filas_filtrado.evento_click(filtrar_todas_etiquetas)

    # columna_etiquetas.update()

    return conteo_etiquetas


# Demo
if __name__=="__main__":

    def main(pagina: ft.Page):
        pagina.add(columna_etiquetas)

        # Añadido de diálogos a la página
        pagina.overlay.extend([
                dialogo_directorio, dialogo_dataset, dialogo_guardado_tags
            ])

        pagina.update()


    ft.app(target=main)       