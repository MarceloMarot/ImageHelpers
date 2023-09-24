
import flet as ft
from functools import partial
from contenedor import Contenedor ,crear_imagen


from buscar import buscar_imagenes

# Funciones para crear galerías de imagenes y definir eventos y propiedades
# - crear_galeria()
# - imagenes_galeria()
# - estilo_galeria()
# - eventos_galeria()


def crear_galeria(numero: int, cuadricula = False ):

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


def estilo_galeria(galeria: ft.Row, base=200, altura=200, redondeo=10, color=ft.colors.WHITE):
    #alias para los controles del elemento Row
    contenedor_fila = galeria.controls  
    numero_imagenes=len(contenedor_fila)
    # Edicion propiedades (post añadido)
    for i in range(0, numero_imagenes):
        # asignacion elemento a elemento
        c = contenedor_fila[i]    
        c.setID(i)              
        c.setDimensiones(base, altura)
        c.setBGColor(color)


def imagenes_galeria(galeria: ft.Row, lista_rutas=[], base=200, altura=200, redondeo=10):
    #alias para los controles del elemento Row
    contenedor_fila = galeria.controls  
    numero_imagenes=len(contenedor_fila)

    numero_rutas= len(lista_rutas) 
    if numero_rutas == 0 :
        print("ejemplo: imagenes desde PicSum")
        # Ejemplo:  relleno con imagenes online
        for i in range(0, numero_imagenes):
            ruta = f"https://picsum.photos/200/200?{i}"
            imagen = crear_imagen(ruta, base, altura, redondeo)
            contenedor_fila[i].setContenido(imagen)

    else:
        numero = numero_rutas if numero_rutas <= numero_imagenes else  numero_imagenes

        for i in range(numero):
        # for ruta in lista_rutas:
            imagen = crear_imagen(lista_rutas[i], base, altura, redondeo)
            contenedor_fila[i].setContenido(imagen)
 


def eventos_galeria(galeria: ft.Row, funcclick=None, funchover=None ,funclongpress=None ):
    #alias para los controles del elemento Row
    contenedor_fila = galeria.controls  
    numero_imagenes=len(contenedor_fila)

    # Edicion propiedades (post añadido)
    for i in range(0, numero_imagenes):
        c = contenedor_fila[i]    
        # funcion de click con argumento ID precargado
        if funcclick != None:
            fclick = partial(funcclick , c)
            c.setClick(fclick)      
        if funchover != None:
            fhover = partial(funchover, c)
            c.setHover(fhover) 
        if funclongpress != None:
            flongp = partial(funclongpress, c)
            c.setLongpress(flongp)  


# Rutinas Ejemplo: galería de imagenes online con interaccion con el mouse

def funcion_click(cont):
    # cambiar estilo
    cont.setRedondeo(20)
    cont.valor=True if cont.valor!=True else False
    color1=ft.colors.INDIGO
    color2=ft.colors.GREEN
    cont.setBGColor(color1) if cont.valor else cont.setBGColor(color2)
    # mostrar numero
    print(cont.getID())


def funcion_hover(cont):
    # cambiar estilo
    cont.setRedondeo(100)
    # mostrar numero
    # print(cont.getID())


def funcion_longpress(cont):
    # cambiar estilo
    cont.setRedondeo(10)
    cont.setBGColor(ft.colors.AMBER) 
    # mostrar numero
    print("Restaurado!")


def pagina_galeria(page: ft.Page):
    
    numero_imagenes = 30
    lista_imagenes = []

    ruta_imagenes="D:\Proyectos_Programacion\cartoons"
    lista_imagenes = buscar_imagenes(ruta_imagenes)
    numero_imagenes = len(lista_imagenes)
    
    # Maquetado
    # componente galeria
    galeria = crear_galeria(numero_imagenes, True)
    page.add(galeria)
    estilo_galeria(galeria,color=ft.colors.AMBER,base=200, altura=200)
    imagenes_galeria(galeria,lista_rutas=lista_imagenes ,base=200, altura=200)
    eventos_galeria(galeria, funcion_click,funcion_hover, funcion_longpress)

    # Elementos generales de la pagina
    page.title = "Galería Imágenes"
    page.window_width=1200
    page.window_height=900
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    # tema_pagina(page)
    page.update()


# creacion de ventana
if __name__ == "__main__":
    ft.app(target = pagina_galeria)