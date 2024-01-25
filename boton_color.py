
import flet as ft

class BotonColor(ft.ElevatedButton):
    def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.BLUE_50 ):
        self.__valor = False
        self.color_true  = color_true
        self.color_false = color_false
        super().__init__(
            text = texto,
            bgcolor= self.color_false,
            on_click=self.click
        )

    # implementacion del biestable
    def click(self,e: ft.ControlEvent):
        valor = True if self.__valor==False else False
        # self.estado(valor)
        self.estado = valor

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
            self.color = ft.colors.BLUE_800
        # print(self.valor)
        self.update()






class BotonGrupo(ft.IconButton):
    def __init__(self):
        # self.__valor = False
        self.estado = False
        super().__init__(
            icon=ft.icons.SELECT_ALL_ROUNDED ,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_800,
            # on_click = self.click,
            )



def main(page: ft.Page):


    boton = BotonColor(
        texto = "yo soy un boton biestable",
        color_false = ft.colors.AMBER_200 ,
        color_true = ft.colors.AMBER_700
    )
    # boton = Boton_Color(
    #     "yo soy un boton biestable",
    #     ft.colors.GREEN_200 ,
    #     ft.colors.GREEN_700
    # )

    page.add(boton)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)