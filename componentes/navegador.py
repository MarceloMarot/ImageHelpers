# Ejecutar demo:
# py -m componentes.contenedor

# from sys import getsizeof
import flet as ft


from . contenedor import Contenedor_Imagen, Contenedor, Estilo_Contenedor
# DOS COMPONENTES UTILES:
# - Contenedor_Compuesto() --> Clase
# - crear_imagen() --> Funcion


# Contenedor con titulo, cuadro de imagen y subtitulo internos
class Contenedor_Compuesto(ft.UserControl):
    def build(self, ancho = 256, alto = 256):
        self.id = 0
        self.__ancho = ancho
        self.__alto = alto
        self.titulo = ft.Text(
            size=30,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            )
        # self.interior= ft.Container(
        #     padding=10,
        #     alignment = ft.alignment.center,
        #     bgcolor = ft.colors.WHITE,
        #     animate=ft.animation.Animation(1000, "bounceOut")
        # ) 
        self.interior = Contenedor_Imagen()
        self.subtitulo = ft.Text(
            size=20,
            text_align=ft.TextAlign.CENTER,
            )
        self.columna= ft.Column(
            [self.titulo, self.interior, self.subtitulo],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand = True
        )
        # self.exterior= ft.Container(
        #     content = self.columna,
        #     padding = 10,
        #     alignment = ft.alignment.center,
        #     bgcolor = ft.colors.WHITE,
        #     animate=ft.animation.Animation(1000, "bounceOut"),
        #     # border=ft.border.all(5, ft.colors.INDIGO_100)
        # )
        self.exterior = Contenedor(
            content = self.columna
        )
        self.ancho = ancho 
        self.alto = alto
        return self.exterior
        # return self.columna

    @property
    def ancho(self):
        return self.__ancho

    @ancho.setter
    def ancho(self, valor):
        self.__ancho        = valor
        self.interior.width = valor
        self.exterior.width = valor + 40
        self.columna.width  = valor + 40
        self.titulo.width   = valor
        self.subtitulo.width= valor

    @property
    def alto(self):
        return self.__alto

    @alto.setter
    def alto(self, valor):
        self.__alto         = valor
        self.interior.height = valor
        self.exterior.height = valor + 120
        self.columna.height  = valor + 120
        self.titulo.height   = 40
        self.subtitulo.height= 25





# Lee una imagen y la carga en un objeto FLET 
def crear_imagen(ruta: str, base=256, altura=256,redondeo=0):
    imagen = ft.Image(
        src = ruta,
        width = base,
        height = altura ,
        fit=ft.ImageFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.border_radius.all(redondeo),
    )
    return imagen


# FUNCION MAIN

def pagina(page: ft.Page):

    contenedor = Contenedor_Compuesto()

    # fila=ft.Row()
    # fila.controls = [contenedor]

    page.add(contenedor)


    # estilos para el contenedor 
    estilo_defecto = Estilo_Contenedor(
        border_radius = 50, 
        bgcolor = ft.colors.BLUE_400,
        border=ft.border.all(20, ft.colors.INDIGO_100)
        )

    estilo_click = Estilo_Contenedor(
        border_radius = 5,
        bgcolor = ft.colors.RED_900,
        border = ft.border.all(20, ft.colors.PURPLE_900),
        )   
    
    estilo_hover = Estilo_Contenedor(
        border_radius = 50, 
        bgcolor = ft.colors.AMBER_400,
        border=ft.border.all(20, ft.colors.ORANGE_600),
        )


    # La configuracion del contenedor se puede hacer:
    # - durante inicializacion;
    # - Despues del agregado a página
    # Hacerlo en la definición de clase NO SIRVE


    def funcion_click(cont, e):
        cont.estilo(estilo_click)

    def funcion_hover(cont, e):
        cont.estilo(estilo_hover)

    def funcion_longpress(cont, e):        
        cont.estilo(estilo_defecto)



    contenedor.interior.setup(512,512)
    contenedor.interior.estilo(estilo_defecto)

    # contenedor.interior.click(funcion_click)
    # contenedor.interior.hover(funcion_hover)
    # contenedor.interior.longpress(funcion_longpress)
    contenedor.interior.crear_imagen("https://picsum.photos/200/200?0",10)

    contenedor.exterior.setup(512,512)
    contenedor.exterior.estilo(estilo_defecto)
    contenedor.exterior.click(funcion_click)
    contenedor.exterior.hover(funcion_hover)
    contenedor.exterior.longpress(funcion_longpress)


    # metodos Property
    contenedor.ancho = 512
    contenedor.alto  = 512  
    
    borde_exterior = 5

    # def funcion_click(e):
    #     contenedor.interior.bgcolor = ft.colors.RED
    #     contenedor.interior.border_radius = 200 
    #     contenedor.interior.border=ft.border.all(20, ft.colors.PURPLE_900)
    #     contenedor.exterior.border=ft.border.all(borde_exterior, ft.colors.PURPLE_900)
    #     contenedor.exterior.border_radius = 10
    #     contenedor.update()


    # def funcion_hover(e):
    #     contenedor.interior.bgcolor = ft.colors.AMBER_400
    #     contenedor.interior.border_radius = 50 
    #     contenedor.interior.border=ft.border.all(20, ft.colors.ORANGE_600)
    #     contenedor.exterior.border=ft.border.all(borde_exterior, ft.colors.ORANGE_600)
    #     contenedor.exterior.border_radius = 10
    #     contenedor.update()


    # def funcion_defecto():   
    #     contenedor.interior.bgcolor = ft.colors.BLUE_400
    #     contenedor.interior.border_radius = 0 
    #     contenedor.interior.border=ft.border.all(20, ft.colors.INDIGO_100)
    #     contenedor.exterior.border=ft.border.all(borde_exterior, ft.colors.INDIGO_100) 
    #     contenedor.exterior.border_radius = 10 
    #     contenedor.update()


    # def funcion_longpress(e):
    #     funcion_defecto()


    # contenedor.exterior.on_click = funcion_click
    # contenedor.exterior.on_hover = funcion_hover
    # contenedor.exterior.on_long_press = funcion_longpress
    
    contenedor.titulo.value = "Titulo"
    contenedor.subtitulo.value = "Subtitulo"


    # funcion_defecto()

    imagen_actual = crear_imagen(
        "https://picsum.photos/200/200?0",base=256,altura=512)
    contenedor.interior.content = imagen_actual
    contenedor.interior.content.fit=ft.ImageFit.CONTAIN
    # contenedor.interior.content.fit=ft.ImageFit.COVER
    # contenedor.interior.content.fit=ft.ImageFit.SCALE_DOWN  
    # contenedor.interior.content.fit=ft.ImageFit.NONE  
    # contenedor.interior.content.fit=ft.ImageFit.FILL  

    contenedor.update()

    page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.update()




if __name__ == "__main__":
    ft.app(target = pagina)