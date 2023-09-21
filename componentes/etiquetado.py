from copy import copy
import flet as ft

from procesar_etiquetas import Etiquetas 


def Columna_Etiquetas(etiquetas_dataset: Etiquetas, etiquetas_imagen: Etiquetas ):

    def guardar_opciones(e):
        etiquetas_checkboxes=[]
        for checkbox  in lista_checkboxes:
            etiqueta = checkbox.label
            valor    = checkbox.value
            if valor:
                etiquetas_checkboxes.append(etiqueta)
        if set(etiquetas_imagen.tags) != set(etiquetas_checkboxes):
            texto.value = "Cambios guardados"
            # archivo creado / reescrito
            etiquetas_imagen.tags = etiquetas_checkboxes
            etiquetas_imagen.guardar()
        else:
            texto.value = "Sin cambios"
        columna_etiquetado.update()


    def checkboxes_ninguno(e):
        for checkbox  in lista_checkboxes:
            checkbox.value = False
        texto.value = "Nada"
        columna_etiquetado.update()


    def checkboxes_todos(e):
        for checkbox  in lista_checkboxes:
            checkbox.value = True
        texto.value = "Todo"
        columna_etiquetado.update()



    def restablecer_opciones(e):
        for checkbox  in lista_checkboxes:
            etiqueta = checkbox.label
            if  etiqueta in etiquetas_imagen.tags :
                checkbox.value = True
            else:
                checkbox.value = False
        texto.value = "Valores reestablecidos"
        columna_etiquetado.update()


    numero_checkboxes = len(etiquetas_dataset.tags)
    lista_checkboxes = []
    for etiqueta  in etiquetas_dataset.tags:
        selector = ft.Switch(label=f"{etiqueta}",value=False)
        if  etiqueta in etiquetas_imagen.tags:
            selector.value=True  
        lista_checkboxes.append(selector) 

    # cuadro de texto de salida
    texto = ft.Text(size=30 ,width=400, height=100, bgcolor=ft.colors.AMBER_200, )
    # botones de comando
    boton_guardado = ft.ElevatedButton(text="Guardar", on_click=guardar_opciones, bgcolor="red",color="white", width=150)
    boton_todos = ft.ElevatedButton(text="Todos", on_click=checkboxes_todos   ,width=150)
    boton_ninguno = ft.ElevatedButton(text="Ninguno", on_click=checkboxes_ninguno ,width=150)
    boton_restablecer = ft.ElevatedButton(text="Restablecer", on_click=restablecer_opciones, bgcolor="blue",color="white", width=150)

    fila_botones_checkboxes = ft.Row(
        wrap=False,
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [ boton_todos, boton_ninguno],
        width=400, # anchura de columna   
        scroll=ft.ScrollMode.ALWAYS,
    )

    fila_boton_restablecer = ft.Row(
        wrap=False,
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [boton_restablecer, boton_guardado],
        width=400, # anchura de columna   
        scroll=ft.ScrollMode.ALWAYS,
    )

    # Columna de checkboxes
    columna_checkboxes = ft.Column(
        wrap=False,
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=lista_checkboxes,
        height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )

    elementos_etiquetado=[]
    elementos_etiquetado.append(texto)
    elementos_etiquetado.append(columna_checkboxes)
    elementos_etiquetado.append(fila_botones_checkboxes)
    elementos_etiquetado.append(fila_boton_restablecer)

    columna_etiquetado = ft.Column(
        wrap=False,
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = elementos_etiquetado, 
        width=500, # anchura de columna   
    )
    return columna_etiquetado



# Tema aplicado globalmente
def tema_pagina(pagina: ft.Page):
    pagina.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.AMBER,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.RED,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )


def pagina_etiquetado(page: ft.Page ):

    # Procesado de archivos
    archivo_dataset = "demo_etiquetas.txt"
    archivo_salida = "etiquetas_salida.txt"
    etiquetas_dataset = Etiquetas(archivo_dataset)
    etiquetas_imagen = Etiquetas(archivo_salida)


    ## Aglutinado columnas
    columna_etiquetado = Columna_Etiquetas ( etiquetas_dataset, etiquetas_imagen )
    page.add(columna_etiquetado)

    # Estilos 
    tema_pagina(page)
    # Propiedades pagina 
    page.title = "Ventana Etiquetado Imágenes"
    page.window_width=450
    page.window_height=900
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False


# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)



