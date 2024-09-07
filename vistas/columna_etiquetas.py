import flet as ft

from componentes.etiquetador_botones import FilasBotonesEtiquetas

from vistas.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags



# Entradas de texto
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


boton_guardar_dataset = ft.ElevatedButton(
    text = f"Guardar como dataset",
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
    text = f"Deseleccionar etiquetas...",
    bgcolor = ft.colors.BLUE_800,
    color = ft.colors.WHITE,
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
            [boton_reset_tags, 
            boton_guardar_dataset],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),  
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