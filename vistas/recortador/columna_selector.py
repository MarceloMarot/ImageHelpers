import flet as ft

from componentes.selector_recortes import SelectorRecorte

from constantes.rutas import PREFIJO_DIRECTORIO_TEMPORAL

# textos
texto_imagen = ft.Text(
    "(Titulo)",
    size=20,
    # height=30, 
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )

texto_zoom = ft.Text("", width=300)

# Componentes especiales
selector_recorte = SelectorRecorte(PREFIJO_DIRECTORIO_TEMPORAL)
selector_recorte.height = 768
selector_recorte.width  = 768

barra_escala = ft.Slider(
    min=30, 
    max=330, 
    divisions=300,
    value=100, 
    label="{value}", 
    width=700,
    round=0,
    )

texto_zoom.value = f"Zoom: {int(barra_escala.value) } %"

# maquetado

fila_zoom = ft.Row(
    [texto_zoom, barra_escala],
    width=768,
    wrap=True,
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

columna_selector = ft.Column(
    [
    texto_imagen,
    selector_recorte,
    fila_zoom
    ],
    width  = 768,
    # height = altura_pagina,
    expand = True ,
    visible= False,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )