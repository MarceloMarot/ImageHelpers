# from copy import copy
import flet as ft
from functools import partial       # usado para los handlers

# from procesar_etiquetas import Etiquetas 
from . buscar import buscar_imagenes

from . contenedor import Contenedor, crear_imagen


from . galeria_imagenes import crear_galeria, estilo_galeria, imagenes_galeria, eventos_galeria



class MenuNavegacion(ft.UserControl):

    # Referencia a UN elemento de entrada
    # seleccion = etiqueta[0]
    def cambiar_indice(self,incrementar,e):
        index = self.indice
        index += incrementar
        self.setIndice(index)
        self.funcion_indice()
        self.actualizarImagen()

    def build(self):

        # inicializacion
        self.indice = 0
        self.maximo = 0
        self.incremento = 10
        self.ancho_boton = 200
 
        # acciones para los eventos  - Anulados por defecto
        self.funcion_indice      = lambda: nada()

        # imagenes de la galeria
        self.imagenes=[]
        # Se invoca un contenedor hijo
        self.contenedor = Contenedor()


        fila_contenedor = ft.Row(
            # wrap=False,
            # spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = [self.contenedor],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        adelantar       = partial(self.cambiar_indice, 1)
        adelantar_fast  = partial(self.cambiar_indice, self.incremento)
        retroceder      = partial(self.cambiar_indice, -1)
        retroceder_fast = partial(self.cambiar_indice, -1*self.incremento)


        # botones de navegacion
        self.boton_next      = ft.ElevatedButton(text="Siguiente",     on_click=adelantar ,width=self.ancho_boton)
        self.boton_prev      = ft.ElevatedButton(text="Anterior" ,     on_click=retroceder ,width=self.ancho_boton)
        self.boton_next_fast = ft.ElevatedButton(text=f"Siguiente + {self.incremento}", on_click=adelantar_fast ,width=self.ancho_boton)
        self.boton_prev_fast = ft.ElevatedButton(text=f"Anterior  - {self.incremento}", on_click=retroceder_fast ,width=self.ancho_boton)

        lista_botones_navegacion_1 =[self.boton_prev     , self.boton_next     ]
        lista_botones_navegacion_2 =[self.boton_prev_fast, self.boton_next_fast]

        fila_botones_navegacion_1 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = lista_botones_navegacion_1,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        fila_botones_navegacion_2 = ft.Row(
            # wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            # run_spacing=50,     # espaciado vertical entre filas
            controls = lista_botones_navegacion_2,
            alignment=ft.MainAxisAlignment.CENTER,
        )


        self.columna_navegacion = ft.Column(
            # wrap=False,
            # spacing=10,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [ fila_contenedor, fila_botones_navegacion_1, fila_botones_navegacion_2], 
            # controls = [],
            # scroll=ft.ScrollMode.ALWAYS,
        )
        return self.columna_navegacion

    # Metodo actualizacion
    def actualizarImagen(self):
        if self.maximo >0 :
            self.contenedor.setContenido(self.imagenes[self.indice])
        else:
            self.contenedor.setContenido(ft.Text(value = "(sin imágenes)"))
        self.update()

    # Metodos 'SETTERS' auxiliares para el contenedor interno
    def setImagenes(self, lista_imagenes ):
        self.imagenes = lista_imagenes
        self.maximo = len(self.imagenes)
        self.actualizarImagen()

    def setIndice(self, numero):
        if numero <0:
            self.indice = 0
        elif numero >= self.maximo:
            self.indice = self.maximo -1
        else:
            self.indice = numero
        self.actualizarImagen()
        self.update()

    def setDimensiones(self, base: int, altura: int):
        self.contenedor.setDimensiones(base, altura)

    def setBGColor(self, color: ft.colors):
        self.contenedor.setBGColor(color)

    def setRedondeo(self, radio: int):
        self.contenedor.setRedondeo(radio)

    # los eventos sobre elcontenedor de imagen se configuran aquí
    # deben asignarse funciones lambda
    def setHoverImagen(self, funcion):
        self.contenedor.setHover(funcion)

    def setClickImagen(self, funcion):
        self.contenedor.setClick(funcion) 

    def setLongpressImagen(self, funcion):
        self.contenedor.setLongpress(funcion) 

    def setFuncionIndice(self, funcion):
        self.funcion_indice = funcion


    # Metodos 'GETTERS' auxiliares
    def getIndice(self):
        return self.indice

    def getDimensiones(self):
        return self.contenedor.getDimensiones()

    def getBGColor(self):
        return self.contenedor.getBGColor()

    def getRedondeo(self, radio: int):
        return self.contenedor.getRedondeo()




# Funcion auxiliar: sirve para anular eventos
def nada():
    pass



def pagina_etiquetado(page: ft.Page ):


    # rutas_imagenes = []
    directorio="D:\Proyectos_Programacion\cartoons"
    rutas_imagenes = buscar_imagenes(directorio)
    numero_imagenes = len(rutas_imagenes)
    


    imagenes = []
    for ruta in rutas_imagenes:
        # imagenes.append(crear_imagen(ruta, 512, 512))
        imagenes.append(crear_imagen(ruta, 1024,1024))   

    
    # Elemento gráfico
    menu = MenuNavegacion()
    page.add(menu)

    menu.setBGColor(ft.colors.AMBER)
    menu.setDimensiones(512, 512)

    menu.setImagenes(imagenes)

    def click_seleccion(m:  MenuNavegacion()):
        print(m.getIndice())
        color1 = ft.colors.GREEN_400
        color2 = ft.colors.INDIGO_400 
        color = m.getBGColor()
        m.setBGColor(color1) if color != color1 else m.setBGColor(color2) 
        # print(color)

    h = partial(click_seleccion, menu)
    menu.setClickImagen(h )


    # Funcion que se ejecuta al cambiar de iamgen
    def navegando():
        print("estoy navegando, indice: ", menu.getIndice())

    menu.setFuncionIndice( navegando)



    # Estilos 
    Tema_Pagina(page)

    page.title = "Navegación Imágenes"
    page.window_width=600
    page.window_height=900
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False

    page.update()



# Tema aplicado globalmente
def Tema_Pagina(pagina: ft.Page):
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



# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)



