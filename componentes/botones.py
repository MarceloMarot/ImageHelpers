from rich import print as print
import flet as ft



def nada( e ):
    pass



class BotonBiestable(ft.ElevatedButton):
# class BotonBiestable(ft.CupertinoButton):
    # def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.BLUE_50 ):
    def __init__(self, 
        texto_false: str, 
        color_false = ft.colors.BLUE_50, 
        color_true  = ft.colors.RED_800,
        texto_true: str|None = None,
        color_texto = None,
        ):
        self.__valor = False
        self.color_true  = color_true
        self.color_false = color_false
        self.texto_false = texto_false.strip()
        self.texto_true  = texto_true.strip() if (texto_true is not None ) else self.texto_false
        self.color_texto = color_texto
        super().__init__(
            text = texto_false,
            key=texto_false.split("(")[0].strip(), # (acomoda la clave a ciertas entradas )
            bgcolor= self.color_false,
            on_click=self.click,
            )
        # manejador opcional para el click 
        self.click_boton = nada
        # eleccion de color de texto
        if self.color_texto !=None:
            self.color = color_texto 


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
            self.text  = self.texto_true
            if self.color_texto != None:
                self.color = self.color_texto 
        else:
            self.__valor = False
            self.bgcolor = self.color_false
            self.color   = ft.colors.BLUE_800
            self.text  = self.texto_false
            if self.color_texto != None:
                self.color = self.color_texto 
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
