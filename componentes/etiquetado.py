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


    # numero_checkboxes = len(etiquetas_dataset.tags)
    lista_checkboxes = []       # lista para lógica
    j=0
    for etiqueta  in etiquetas_dataset.tags:
        j += 1
        selector = ft.Switch(label=f"{etiqueta}",value=False)
        if  etiqueta in etiquetas_imagen.tags:
            selector.value=True  
        lista_checkboxes.append(selector) 
    
   
    divisor = ft.Divider(height=9, thickness=3, color=ft.colors.INDIGO_100)

    # version grafica con divisores
    lista_checkboxes_grafica=[] # lista para grafica
    lista_checkboxes_grafica=lista_checkboxes.copy()
    grupo = etiquetas_dataset.grupo
    conjunto_grupos = set( etiquetas_dataset.grupo )
    lista_grupos = list(conjunto_grupos)





    # msg_separador = f"Grupo {k}" 
    # separador = ft.Text(size=20 ,width=100, height=30,  value=msg_separador, color=ft.colors.INDIGO_100 )

    # Se añaden separadores de grupo de ultimp a primero
    for i in range(len(grupo)-1, 0 , -1):
        if grupo[i-1] != grupo[i]:
            k = lista_grupos.pop()   
            msg_separador = f"Grupo {k}" 
            separador = ft.Text(size=20 ,width=100, height=30,  value=msg_separador, color=ft.colors.INDIGO_100 )
            lista_checkboxes_grafica.insert(i, separador )


    if len(lista_grupos)>0:
        k = lista_grupos.pop()  
        msg_separador = f"Grupo {k}" 
        separador = ft.Text(size=20 ,width=100, height=30,  value=msg_separador, color=ft.colors.INDIGO_100 )
        lista_checkboxes_grafica.insert(0, separador )



    ancho = 500
    mensaje="Etiquetado" if len(lista_checkboxes) > 0 else "Sin Dataset"

    # cuadro de texto de salida
    texto = ft.Text(size=20 ,width=300, height=30, bgcolor=ft.colors.AMBER_100, value=mensaje, expand = False )
    fila_texto=ft.Row(
        wrap=False,
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [texto] ,
        width=ancho, # anchura de columna   
        alignment= ft.MainAxisAlignment.CENTER, 
    )
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
        width=ancho, # anchura de columna   
        alignment= ft.MainAxisAlignment.CENTER,
    )

    fila_boton_restablecer = ft.Row(
        wrap=False,
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [boton_restablecer, boton_guardado],
        width=ancho, # anchura de columna   
        alignment= ft.MainAxisAlignment.CENTER,
    )

    # Columna de checkboxes
    columna_checkboxes = ft.Column(
        wrap=False,
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=lista_checkboxes_grafica,
        height=600,         # altura de columna
        width=ancho,
        scroll=ft.ScrollMode.AUTO,
    )

    #contenedor de checkboxes (decorativo)
    contenedor_checkboxes = ft.Container(
                margin=10,
                padding=10,
                width   = ancho,
                height  = 600,
                content = columna_checkboxes,
                alignment=ft.alignment.center,
                # bgcolor=ft.colors.AMBER,
                border_radius=20,           # redondeo
                animate=ft.animation.Animation(200, "bounceOut"),
            )
    contenedor_checkboxes.border = ft.border.all(5, ft.colors.INDIGO_400)



    elementos_etiquetado=[]
    # elementos_etiquetado.append(texto)
    elementos_etiquetado.append(fila_texto)
    # elementos_etiquetado.append(columna_checkboxes)
    elementos_etiquetado.append(contenedor_checkboxes)
    elementos_etiquetado.append(fila_botones_checkboxes)
    elementos_etiquetado.append(fila_boton_restablecer)
    # elementos_etiquetado.append(ft.Divider(height=9, thickness=3))

    columna_etiquetado = ft.Column(
        wrap=False,
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = elementos_etiquetado, 
        width=ancho # anchura de columna   
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
    page.window_height = 1000
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False
    
    page.update()



# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)



