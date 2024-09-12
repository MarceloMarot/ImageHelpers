from rich import print as print
import flet as ft



def nada( e ):
    pass



class BotonBiestable(ft.ElevatedButton):
# class BotonBiestable(ft.CupertinoButton):
    # def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.BLUE_50 ):
    def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.RED_800 ):
        self.__valor = False
        self.color_true  = color_true
        self.color_false = color_false
        super().__init__(
            text = texto,
            # key=texto,          # asignacion automatica
            key=texto.split("(")[0].strip(), # (acomoda la clave a ciertas entradas )
            bgcolor= self.color_false,
            on_click=self.click,

            # border_radius=ft.border_radius.all(15),
            # height=40,
            # padding=5,
            # width=150,

            )
        # manejador opcional para el click 
        self.click_boton = nada


    # implementacion del biestable
    def click(self,e: ft.ControlEvent):
        valor = True if self.__valor==False else False
        self.estado = valor
        # print(self.estado)      # FIX
        # print(self.bgcolor)      # FIX
        # print(self.color)      # FIX
        self.click_boton(e)     # (no hace nada a menos que se programe)

    @property
    def estado(self):
        return self.__valor

    # actualizacion del booleano y de colores
    @estado.setter
    def estado(self, valor: bool):
        if valor:
            self.__valor = True
            self.bgcolor = self.color_true
            self.color = ft.colors.WHITE 
        else:
            self.__valor = False
            self.bgcolor = self.color_false
            self.color   = ft.colors.BLUE_800
        self.update()

    @property
    def clave(self):
        return self.key

    @clave.setter
    def clave(self, valor: str):
        self.key = valor




class BotonGrupo(ft.IconButton):
    def __init__(self):
        self.estado = False
        super().__init__(
            icon=ft.icons.SELECT_ALL_ROUNDED ,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_800,
            )
        # manejador opcional para el click 
        self.click_boton = nada
