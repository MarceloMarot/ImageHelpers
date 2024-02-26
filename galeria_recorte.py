
import flet as ft
import cv2
from cortar_imagen import ImagenOpenCV



from manejo_texto.procesar_etiquetas import Etiquetas 

from componentes.galeria_imagenes import Galeria, Contenedor, Contenedor_Imagen, Estilo_Contenedor
from componentes.menu_navegacion import  MenuNavegacion
from componentes.etiquetador_botones import EtiquetadorBotones

from componentes.lista_desplegable import crear_lista_desplegable,convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from sistema_archivos.buscar_extension import buscar_imagenes

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen




clickeos = 0

# ventana = None


def main(page: ft.Page):

    ancho_pagina = 800
    altura_pagina = 800

    base = 768
    altura = 768


    ruta_recorte = "recorte.webp"
    # ventana = ImagenOpenCV()



    # Botones apertura de ventana emergente
    boton_carpeta = ft.ElevatedButton(
        text = "Abrir carpeta",
        icon=ft.icons.FOLDER_OPEN,
        bgcolor=ft.colors.RED,
        color= ft.colors.WHITE,
        ## manejador
        on_click=lambda _: dialogo_directorio.get_directory_path(
            dialog_title="Elegir carpeta con todas las imágenes"
        ),
    )

    page.add(boton_carpeta)


    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        if e.path:

            # acceso a elementos globales
            global imagenes_etiquetadas
            global imagenes_galeria
            # busqueda 
            directorio = e.path
            rutas_imagen = buscar_imagenes(directorio)
            # Carga de imagenes del directorio
            # imagenes_etiquetadas, imagenes_galeria = cargar_imagenes(rutas_imagen)

            # Objeto galeria
            galeria.leer_imagenes(rutas_imagen, redondeo = 30)
            # galeria.cargar_imagenes( imagenes_galeria )
            galeria.eventos(click = click_galeria)
            galeria.estilo(estilo_defecto)
            galeria.update()



    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   = ft.FilePicker(on_result = resultado_directorio )
   

    # Añadido de diálogos a la página
    page.overlay.extend([
            dialogo_directorio
        ])


    def click_galeria(e):
        global clickeos
        clickeos += 1
        print(f"Nº clicks: {clickeos}")
        global ventana


        cont = e.control 
        # print("ruta: ", cont.content.src)
        ruta_imagen = cont.content.src
        print("ruta: ", ruta_imagen)
        print("click: ", cont.content.key)


        if clickeos ==1: 
            ventana = ImagenOpenCV()
            ventana.interfaz_edicion(ruta_imagen, ruta_recorte,[512,512],[768,768],texto_consola=False, escape_teclado=False)  #tamaño recorte predefinido
   

        if clickeos >1: 

            # estado = ventana.copiar_estados()
            ventana.apertura_imagenes(ruta_imagen)
            # ventana.recuperar_estados(estado)
            # ventana.apertura_imagenes()



    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   
        print(f"Tecla: {tecla}")
  

    galeria = Galeria()
    page.add(galeria)


    estilo_defecto = Estilo_Contenedor(
        width = 300,
        height = 300,
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100),
        )


    # propiedad de pagina: handler del teclado elegido
    page.on_keyboard_event = desplazamiento_teclado

    page.title="Galeria Recorte"
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = altura_pagina
    page.window_width  = ancho_pagina

    page.update()








if __name__=="__main__":
    ft.app(target=main)


