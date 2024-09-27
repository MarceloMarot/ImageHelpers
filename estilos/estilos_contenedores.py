import flet as ft


from enum import Enum


# Clase auxiliar para configurar contenedores
class EstiloContenedor:
    """'EstiloContenedor' es una estructura de datos creada para guardar parametros de estilo de los contenedores: tamaño, colores, bordes, etc"""
    def __init__(
        self,
        width=256,
        height=256,
        border_radius=0, 
        bgcolor=ft.colors.WHITE, 
        margin=10,
        padding=10,
        border=ft.border.all(0, ft.colors.WHITE),
        ):
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.bgcolor = bgcolor
        self.margin  = margin
        self.padding = padding
        self.border = border




class Estilos(Enum):
    "Eumeracion de estilos para contenedores"
    DEFAULT     = "predefinido" 
    MODIFICADO  = "modificado" 
    GUARDADO    = "guardado" 
    ERRONEO     = "erroneo" 
    ACTUAL      = "actual"  

# estilos para contenedores 
estilo_galeria_defecto = EstiloContenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_galeria_modificado = EstiloContenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_galeria_guardado = EstiloContenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_galeria_erroneo = EstiloContenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilo_galeria_actual = EstiloContenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.PURPLE_300,
    border=ft.border.all(10, ft.colors.PURPLE_600)
    )

estilos_galeria = {
    Estilos.DEFAULT.value    : estilo_galeria_defecto,
    Estilos.MODIFICADO.value : estilo_galeria_modificado,
    Estilos.GUARDADO.value   : estilo_galeria_guardado,
    Estilos.ERRONEO.value    : estilo_galeria_erroneo,
    Estilos.ACTUAL.value     : estilo_galeria_actual,
    }


# estilos para el contenedor 
estilo_seleccion_defecto = EstiloContenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_seleccion_modificado = EstiloContenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_seleccion_guardado = EstiloContenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_seleccion_erroneo = EstiloContenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilo_seleccion_actual = EstiloContenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )


estilos_seleccion = {
    Estilos.DEFAULT.value    : estilo_seleccion_defecto,
    Estilos.MODIFICADO.value : estilo_seleccion_modificado,
    Estilos.GUARDADO.value   : estilo_seleccion_guardado,
    Estilos.ERRONEO.value    : estilo_seleccion_erroneo,
    Estilos.ACTUAL.value     : estilo_seleccion_actual,
    }