# https://flet.dev/docs/controls/image

import flet as ft

from functools import partial

from contenedor import Contenedor 


def galeria_contenedores(numero: int, cuadricula : bool):

    contenedores = []
    for i in range(numero):
        contenedor = Contenedor()
        contenedores.append(contenedor)

    fila_imagenes = ft.Row(
        expand=1, 
        wrap = cuadricula, # version galería (si es 'False' las imagenes van en linea)
        scroll=ft.ScrollMode.ALWAYS,
        controls= contenedores,
        )    
    return fila_imagenes


# Lee una imagen y la carga en un objeto FLET 
def crear_imagen(ruta: str, base=200, altura=200,redondeo=0):
    imagen = ft.Image(
        src = ruta,
        width = base,
        height = altura ,
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(redondeo),
    )
    return imagen





def pagina_galeria(page: ft.Page):

    numero_imagenes = 8
    # lista_imagenes = [] 
    lista_contenedores = []

    # Maquetado
    # componente galeria
    imagenes_fila = galeria_contenedores(numero_imagenes, True)
    page.add(imagenes_fila)

    #alias para los controles del elemento Row
    contenedor_fila = imagenes_fila.controls  
    
    # Funcion general para manejar clickeos sobre los containers
    def funcion_click(n):
        cont = contenedor_fila[n]
        # cambiar estilo
        cont.setRedondeo(20)
        cont.valor=True if cont.valor!=True else False
        color1=ft.colors.INDIGO_400
        color2=ft.colors.GREEN_200
        cont.setBGColor(color1) if cont.valor else cont.setBGColor(color2)
        # mostrar numero
        print(cont.getID())


    # Edicion propiedades (post añadido)
    for i in range(0, numero_imagenes):


        c = contenedor_fila[i]    

        c.setID(i)
        c.setDimensiones(200,200)
        c.setBGColor(ft.colors.AMBER)

        # funcion de click con argumento ID precargado
        func = partial(funcion_click, i)
        c.setClick(func)

        # Relleno con imagenes online
        ruta = f"https://picsum.photos/200/200?{i}"
        imagen = crear_imagen(ruta, 400, 400, 50)

        c.setContenido(imagen)




    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=700
    page.window_height=900
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    page.update()


# creacion de ventana
if __name__ == "__main__":
    ft.app(target = pagina_galeria)