import flet as ft
# https://flet.dev/docs/controls/switch

# from functools import partial       # usado para los handlers

from procesar_etiquetas import FiltradoEtiquetas, LecturaLista, Etiquetas, etiquetas2texto, GuardadoTexto

from buscar_extension import buscar_imagenes


lista_imagenes = []     # se carga de direcciones en 'main'

indice_imagen=0


etiquetas_dataset = []

etiquetas_imagen = []


archivo_dataset = ""
archivo_salida  = ""



def Columna_Etiquetas(pagina: ft.Page ):

    def guardar_opciones(e):
        # valores=""
        # for i in range(0,len(lista_checkboxes)):
        #     if  lista_checkboxes[i].value:
        #         valores += " " + lista_checkboxes[i].label   
        #         # reinicio de switches
        #         # lista_checkboxes[i].value = False
        global etiquetas_imagen
        # reasignacion de etiquetas para la imagen


        etiquetas_checkboxes=[]
        for checkbox  in lista_checkboxes:
            etiqueta = checkbox.label
            valor    = checkbox.value
            if valor:
                etiquetas_checkboxes.append(etiqueta)

        if set(etiquetas_imagen) != set(etiquetas_checkboxes):
            texto.value = "Cambios guardados"
            # archivo creado / reescrito
            etiquetas_imagen = etiquetas_checkboxes
            labels = etiquetas2texto(etiquetas_imagen)
            GuardadoTexto(archivo_salida, labels )
        else:
            texto.value = "Sin cambios"

        pagina.update()


    def checkboxes_ninguno(e):
        for checkbox  in lista_checkboxes:
            checkbox.value = False
        pagina.update()


    def checkboxes_todos(e):
        for checkbox  in lista_checkboxes:
            checkbox.value = True
        pagina.update()


    def restablecer_opciones(e):
        for checkbox  in lista_checkboxes:
            etiqueta = checkbox.label
            if  etiqueta in etiquetas_imagen :
                checkbox.value = True
            else:
                checkbox.value = False
        # texto.value = etiquetas2texto(etiquetas_imagen)
        texto.value = "Valores reestablecidos"
        pagina.update()


    # global lista_checkboxes
    numero_checkboxes = len(etiquetas_dataset)
    lista_checkboxes = []
    # for i  in range(0,numero_checkboxes):
    for etiqueta  in etiquetas_dataset:
        selector = ft.Switch(label=f"{etiqueta}",value=False)
        if  etiqueta in etiquetas_imagen:
            selector.value=True  
        # else: 
        #     selector.value=False
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
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [ boton_todos, boton_ninguno],
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        width=400, # anchura de columna   
        # height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )


    fila_boton_restablecer = ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [boton_restablecer, boton_guardado],
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        width=400, # anchura de columna   
        # height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )

    # Columna de checkboxes
    columna_checkboxes = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=lista_checkboxes,
        # controls=contenido,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        # width=400, # anchura de columna   
        height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    
    )

    elementos_etiquetado=[]
    elementos_etiquetado.append(texto)
    elementos_etiquetado.append(columna_checkboxes)
    elementos_etiquetado.append(fila_botones_checkboxes)
    elementos_etiquetado.append(fila_boton_restablecer)
    # elementos_etiquetado.append(boton_guardado)

    columna_etiquetado = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        # controls=lista_checkboxes,
        controls = elementos_etiquetado, 
        # controls=contenido,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        width=500, # anchura de columna   
        # height=900,         # altura de columna
        # scroll=ft.ScrollMode.ALWAYS,
    )

    return columna_etiquetado




def Columna_Imagen(pagina: ft.Page):
    ## COLUMNA IMAGEN

    # ruta_imagen = imagenes[0]
    ruta_imagen = lista_imagenes[0]

    dim_imagen = 512
    borde = 5

    #lectura imagen
    imagen_actual = ft.Image(
        src = ruta_imagen,
        width = dim_imagen,
        height = dim_imagen ,
        # fit=ft.ImageFit.NONE,
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(10),
    )

    def container_click(e):
        global indice_imagen, container_imagen
        print(indice_imagen)
        # container_imagen.content=lista_imagenes[indice_imagen]
        # imagen_actual.src = lista_imagenes[indice_imagen]
        pagina.update()
        return indice_imagen

    # Inclusion de la imagen dentro de un contenedor
    # Esto habilita bordes, eventos con el mouse, etc 
    # global container_imagen
    container_imagen = ft.Container(
        # content=ft.Text("Non clickable"),
        content = imagen_actual,      
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.AMBER,
        width=dim_imagen + borde,
        height=dim_imagen + borde,
        border_radius=10,           # redondeo
        on_click=container_click, 
    )

    texto_imagen= ft.Text(size=20 ,width=500, height=50, bgcolor=ft.colors.AMBER_200 )
    texto_imagen.value=f"{indice_imagen} - {ruta_imagen}"


    def adelantar(e):
        global indice_imagen, lista_imagenes, ruta_imagen
        indice_imagen += 1
        if indice_imagen >= len(lista_imagenes): 
            indice_imagen = len(lista_imagenes)-1
        ruta_imagen = lista_imagenes[indice_imagen]
        imagen_actual.src = lista_imagenes[indice_imagen]
        texto_imagen.value=f"{indice_imagen} - {ruta_imagen}"
        # print("+1")
        pagina.update()

    def adelantar_fast(e):
        global indice_imagen, lista_imagenes, ruta_imagen
        indice_imagen += 10
        if indice_imagen >= len(lista_imagenes): 
            indice_imagen = len(lista_imagenes)-1
        ruta_imagen = lista_imagenes[indice_imagen]
        imagen_actual.src = lista_imagenes[indice_imagen]
        texto_imagen.value=f"{indice_imagen} - {ruta_imagen}"
        # print("+10")
        pagina.update()

    def retroceder(e):
        global indice_imagen, lista_imagenes, ruta_imagen
        indice_imagen -= 1
        if indice_imagen < 0: 
            indice_imagen = 0
        ruta_imagen = lista_imagenes[indice_imagen]
        imagen_actual.src = lista_imagenes[indice_imagen]
        texto_imagen.value=f"{indice_imagen} - {ruta_imagen}"
        # print("-1")
        pagina.update()


    def retroceder_fast(e):
        global indice_imagen, lista_imagenes, ruta_imagen
        indice_imagen -= 10
        if indice_imagen < 0: 
            indice_imagen = 0
        ruta_imagen = lista_imagenes[indice_imagen]
        imagen_actual.src = lista_imagenes[indice_imagen]
        texto_imagen.value=f"{indice_imagen} - {ruta_imagen}"
        # print("-10")
        pagina.update()


    ancho_boton = 200

    boton_next      = ft.ElevatedButton(text="Siguiente",     on_click=adelantar ,width=ancho_boton)
    boton_prev      = ft.ElevatedButton(text="Anterior" ,     on_click=retroceder ,width=ancho_boton)
    boton_next_fast = ft.ElevatedButton(text="Siguiente +10", on_click=adelantar_fast ,width=ancho_boton)
    boton_prev_fast = ft.ElevatedButton(text="Anterior  -10", on_click=retroceder_fast ,width=ancho_boton)

    # lista_botones_navegacion =[boton_prev_fast, boton_prev,boton_next, boton_next_fast]
    lista_botones_navegacion_1 =[boton_prev     , boton_next    ]
    lista_botones_navegacion_2 =[boton_prev_fast, boton_next_fast]

    fila_botones_navegacion_1 = ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = lista_botones_navegacion_1,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        # width=400, # anchura de columna   
        # height=600,         # altura de columna
        alignment=ft.MainAxisAlignment.CENTER,
        # scroll=ft.ScrollMode.ALWAYS,
    )

    fila_botones_navegacion_2 = ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = lista_botones_navegacion_2,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        # width=400, # anchura de columna   
        # height=600,         # altura de columna
        alignment=ft.MainAxisAlignment.CENTER,
        # scroll=ft.ScrollMode.ALWAYS,
    )

    elementos_imagen=[]
    elementos_imagen.append(container_imagen)
    elementos_imagen.append(texto_imagen)
    elementos_imagen.append(fila_botones_navegacion_1)
    elementos_imagen.append(fila_botones_navegacion_2)
    # elementos_imagen.append(boton_guardado)

    columna_imagen = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        # controls=lista_checkboxes,
        controls = elementos_imagen, 
        # controls=contenido,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        # width=500, # anchura de columna   
        # height=900,         # altura de columna
        # alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ALWAYS,
    )

    ## FIN COLUMNA IMAGEN
    return columna_imagen







def Contenedor_Todo( pagina: ft.Page  ):
  

    ## Aglutinado columnas
    columna_etiquetado = Columna_Etiquetas(pagina)
    columna_navegacion = Columna_Imagen(pagina)

    lista_columnas =[columna_etiquetado, columna_navegacion]

    todas_columnas = ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = lista_columnas,
        # width=pagina.window_width,
        # width=float("inf"), # anchura de columna    
        # width=400, # anchura de columna   
        # height=600,         # altura de columna
        # scroll=ft.ScrollMode.ALWAYS,
    )

    ## Fin aglutinado columnas
    return todas_columnas
    # pagina.add(todas_columnas)





# ancho_boton = 200

def pagina_etiquetado(page: ft.Page ):
# def main(page: ft.Page):
    page.title = "Ventana Etiquetado Imágenes"
    page.window_width=1200
    page.window_height=900
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False

    todalapagina = Contenedor_Todo(page)

    page.add(todalapagina)
    # page.add(todas_columnas)

    # Estilos 
    page.theme = ft.Theme(
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
            # interactive=False,
        )
    )

    # Elementos generales de la pagina
    page.title = "Lista CheckBoxes Variable"
    # page.window_width=1500
    # page.window_height=1100
    page.window_maximizable=True
    page.window_minimizable=True
    # page.window_maximized=True

    # Uso de los elementos
    # page.add(texto,  fila_botones)
    # page.add(columna_checkboxes)
    # page.add(boton_submit)
    # page.add(columna_etiquetado)
    # page.add(columna_imagen)
    # page.add(todas_columnas)







# Función MAIN: demo
if __name__ == "__main__" :

    numero_imagenes=50
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    # ft.app(target=main)
    for i in range(0, numero_imagenes):
        lista_imagenes.append( f"https://picsum.photos/200/200?{i}" )   # imagenes online


    archivo_dataset = "demo_etiquetas.txt"

    lineas_dataset = LecturaLista(archivo_dataset )
    tags_dataset = FiltradoEtiquetas( lineas_dataset )

    etiquetas_dataset = tags_dataset.etiquetas


    archivo_salida="etiquetas_salida.txt"

    lineas_imagen = LecturaLista(archivo_salida)
    tags_imagen = FiltradoEtiquetas( lineas_imagen )

    etiquetas_imagen = tags_imagen.etiquetas

    mensaje = ft.app(target=pagina_etiquetado)
