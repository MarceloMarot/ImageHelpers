import flet as ft
from . galeria_imagenes import Estilo_Contenedor 


# estilos para contenedores 
estilo_galeria_defecto = Estilo_Contenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_galeria_modificado = Estilo_Contenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_galeria_guardado = Estilo_Contenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_galeria_erroneo = Estilo_Contenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilo_galeria_actual = Estilo_Contenedor(
    width = 128, 
    height = 128,
    border_radius = 10, 
    bgcolor = ft.colors.PURPLE_300,
    border=ft.border.all(10, ft.colors.PURPLE_600)
    )

estilos_galeria = {
    "predefinido" : estilo_galeria_defecto,
    "modificado" : estilo_galeria_modificado,
    "guardado" : estilo_galeria_guardado,
    "erroneo" : estilo_galeria_erroneo,
    "actual"  : estilo_galeria_actual,
    }


# estilos para el contenedor 
estilo_seleccion_defecto = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_seleccion_modificado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_seleccion_guardado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_seleccion_erroneo = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilo_seleccion_actual = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )


estilos_seleccion = {
    "predefinido" : estilo_seleccion_defecto,
    "modificado" : estilo_seleccion_modificado,
    "guardado" : estilo_seleccion_guardado,
    "erroneo" : estilo_seleccion_erroneo,
    "actual" : estilo_seleccion_actual,
    }