# https://flet.dev/docs/controls/image

import flet as ft

from functools import partial



# Contenedor con eventos integrados
# pensado para contener imagenes
class Contenedor(ft.UserControl):

    # MANEJADORES DE EVENTOS 
    # Se configuran mediante metodos dedicados
    def longpress(self, e):
        # self.funcion_longpress()
        self.update()

    def hover(self,e):
        # self.funcion_hover()
        self.update()

    def click(self, e):
        # self.funcion_click()
        self.valor=True if self.valor!=True else False
        color1=ft.colors.INDIGO_400
        color2=ft.colors.GREEN_200
        print(self.getID())
        self.setBGColor(color1) if self.valor else self.setBGColor(color2)
        self.update()

    # INICIALIZACION
    def build(self):
        self.id = 0
        self.valor = False
        self.contenedor = ft.Container(
                margin=10,
                padding=10,
                width   = 200,
                height  = 200,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,
                # border_radius=0,           # redondeo
                animate=ft.animation.Animation(200, "bounceOut"),
                # EVENTOS:  
                on_long_press = self.longpress,
                on_hover = self.hover,
                on_click = self.click, 
            )
        return self.contenedor
    
    #METODOS
    # 'setters'
    def setID(self, id: int):
        self.contenedor.id = id

    def setContenido(self, imagen: ft.Image ):
        self.contenedor.content  = imagen 
        self.update()

    def setDimensiones(self, base: int, altura: int):
        self.contenedor.height= altura
        self.contenedor.width = base
        self.update()

    def setBGColor(self, color: ft.colors):
        self.contenedor.bgcolor = color
        self.update()
        
    def setRedondeo(self, radio: int):
        self.contenedor.border_radius = radio
        self.update()

    # 'getters'
    def getID(self):
        return self.contenedor.id 

    def getContenido(self):
        return self.contenedor.content

    def getDimensiones(self):
        return [self.contenedor.width , self.contenedor.height]
    
    def getBGColor(self):
        return self.contenedor.bgcolor

    def getRedondeo(self):
        return self.contenedor.border_radius



# Funcion auxiliar: sirve para anular eventos
# def nada():
#     pass





def Galeria(elementos: list, cuadricula : bool):
    fila_imagenes = ft.Row(
        expand=1, 
        wrap = cuadricula, # version galería (si es 'False' las imagenes van en linea)
        scroll=ft.ScrollMode.ALWAYS,
        controls= elementos,
        )    
    return fila_imagenes






def pagina_galeria(page: ft.Page):

    numero_imagenes = 8
    # lista_imagenes = [] 
    lista_contenedores = []

    # Maquetado
    # Prueba preliminar: imagenes online 
    for i in range(0, numero_imagenes):
        # lista_imagenes.append( f"https://picsum.photos/200/200?{i}" )   # imagenes online
        contenedor = Contenedor()
        lista_contenedores.append(contenedor)

        # imagen = ft.Image(
        #     src = f"https://picsum.photos/200/200?{i}",
        #     width = 400,
        #     height = 400 ,
        #     fit=ft.ImageFit.CONTAIN,
        #     repeat=ft.ImageRepeat.NO_REPEAT,
        #     border_radius=ft.border_radius.all(50),
        # )
        # lista_imagenes.append(imagen)


    # componente galeria
    # imagenes_fila = Galeria_Imagenes(lista_imagenes )

    imagenes_fila = Galeria(lista_contenedores, True)
    page.add(imagenes_fila)


    # Edicion propiedades
    for i in range(0, numero_imagenes):
        lista_contenedores[i].setID(i)
        lista_contenedores[i].setDimensiones(200,200)
        lista_contenedores[i].setBGColor(ft.colors.AMBER)
        imagen = ft.Image(
            src = f"https://picsum.photos/200/200?{i}",
            width = 400,
            height = 400 ,
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(50),
        )
        lista_contenedores[i].setContenido(imagen)


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