# https://flet.dev/docs/controls/image

import flet as ft

from functools import partial

#parametros globales
lista_imagenes = []     # se carga de direcciones en 'main'
pixeles_imagen = 250
borde = 10



# def main(page: ft.Page):

#     #fila de contenedores con imagenes (comienza vacía)
#     fila_imagenes = ft.Row(expand=1, wrap=True, scroll=ft.ScrollMode.ALWAYS)    # version galería
#     # fila_imagenes = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)    # version fila
#     page.add(fila_imagenes)


# componente galeria 

def Galeria_Imagenes(imagenes: list):

    #fila de contenedores con imagenes (comienza vacía)
    fila_imagenes = ft.Row(expand=1, wrap=True, scroll=ft.ScrollMode.ALWAYS)    # version galería
    # fila_imagenes = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)    # version fila

    # lista de manejadores para los containers (vacia)
    container_click=[]
    for i in range(0, len(imagenes)):

        def click_iesimo(x, residuo):
            # print(e , i)
            # return [e, i]
            print(x , imagenes[x])
            return [x , imagenes[x]]

        # lista de handlers para los containers: uno por valor de indice
        # container_click = []
        parcial = partial( click_iesimo, i)
        container_click.append( parcial )

        #lectura imagen
        imagen_nesima= ft.Image(
            src = imagenes[i],
            width = pixeles_imagen,
            height = pixeles_imagen ,
            # fit=ft.ImageFit.NONE,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )

        # Inclusion de la imagen dentro de un contenedor
        # Esto habilita bordes, eventos con el mouse, etc 
        fila_imagenes.controls.append(
            ft.Container(
                # content=ft.Text("Non clickable"),
                content = imagen_nesima,      
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER,
                width=pixeles_imagen + borde,
                height=pixeles_imagen + borde,
                border_radius=10,           # redondeo
                # EVENTOS:
                # on_click=container_click,     
                # on_long_press = ,
                # on_hover = ,
                on_click=container_click[i], 
            )
        )

    return fila_imagenes

# fin componente galeria



def main(page: ft.Page):

    # #fila de contenedores con imagenes (comienza vacía)
    # fila_imagenes = ft.Row(expand=1, wrap=True, scroll=ft.ScrollMode.ALWAYS)    # version galería
    # # fila_imagenes = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS)    # version fila
    # page.add(fila_imagenes)

    imagenes_fila = Galeria_Imagenes(lista_imagenes)

    page.add(imagenes_fila)

    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=1500
    page.window_height=1000
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    page.update()



# Función MAIN
if __name__ == "__main__" :

    numero_imagenes=50

    # Prueba preliminar: imagenes online 
    for i in range(0, numero_imagenes):
        lista_imagenes.append( f"https://picsum.photos/200/200?{i}" )   # imagenes online


    # creacion de ventana
    ft.app(target = main)