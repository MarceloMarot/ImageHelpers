import flet as ft
from . galeria_imagenes import Estilo_Contenedor 


# estilos para contenedores 
estilo_galeria_defecto = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(5, ft.colors.INDIGO_100)
    )

estilo_galeria_modificado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(5, ft.colors.AMBER_600)
    )

estilo_galeria_guardado = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(5, ft.colors.GREEN_800)
    )

estilo_galeria_erroneo = Estilo_Contenedor(
    width = 256, 
    height = 256,
    border_radius = 10, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(5, ft.colors.BROWN_800)
    )

estilos_galeria = {
    "predefinido" : estilo_galeria_defecto,
    "modificado" : estilo_galeria_modificado,
    "guardado" : estilo_galeria_guardado,
    "erroneo" : estilo_galeria_erroneo
    }


# estilos para el contenedor 
estilo_menu_defecto = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.BLUE_100,
    border=ft.border.all(10, ft.colors.INDIGO_100)
    )

estilo_menu_modificado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.YELLOW_600,
    border=ft.border.all(10, ft.colors.AMBER_600)
    )

estilo_menu_guardado = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.LIME_800,
    border=ft.border.all(10, ft.colors.GREEN_800)
    )

estilo_menu_erroneo = Estilo_Contenedor(
    width = 512,
    height = 512,
    border_radius = 20, 
    bgcolor = ft.colors.RED_800,
    border=ft.border.all(10, ft.colors.BROWN_800)
    )

estilos_seleccion = {
    "predefinido" : estilo_menu_defecto,
    "modificado" : estilo_menu_modificado,
    "guardado" : estilo_menu_guardado,
    "erroneo" : estilo_menu_erroneo
    }