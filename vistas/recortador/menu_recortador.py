import flet as ft

# from componentes.dialogo_alerta
from componentes.lista_desplegable import crear_lista_desplegable, tupla_resoluciones

from vistas.recortador.dialogos import dialogo_directorio_origen, dialogo_directorio_destino


ancho_botones = 200
altura_botones = 40



texto_ayuda = """
Bordes de Imagen:
Cada color de borde da informacion sobre el estado del recorte de cada imagen.
Opciones:
- Celeste: no recortado
- Verde: archivo de recorte guardado
- Amarillo: recorte marcado pero sin guardar en disco

Galería de imágenes:
- Click izquierdo sobre cualquier imagen para seleccionarla.
  Se abrirá el selector de recortes a la derecha.

Selector de recortes:
- Click derecho sobre la imagen ampliada para guardar el recorte marcado;
- Click izquierdo para marcado provisional (no se guarda);
- Rueda del mouse: cambio del zoom de imagen.

Barra de zoom:
- Deslizar la barra para ajustar el zoom de imagen.

Teclas rápidas:
- Home:  primera imagen;
- RePag | A: imagen anterior;
- AvPag | D: imagen siguiente;
- End:   última imagen;
- Flechas: cambia zoom
"""

ayuda_emergente = ft.Tooltip(
        message=texto_ayuda,
        content=ft.Text("Ayuda emergente",size=20, width=200),
        padding=20,
        border_radius=10,
        text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
    )


# Botones apertura de ventana emergente
boton_carpeta_origen = ft.ElevatedButton(
    text = "Carpeta capturas",
    icon=ft.icons.FOLDER_OPEN,
    bgcolor=ft.colors.BLUE_900,
    color= ft.colors.WHITE,
    height = altura_botones,
    width  = ancho_botones,
    ## manejador
    on_click=lambda _: dialogo_directorio_origen.get_directory_path(
        dialog_title="Elegir carpeta con las capturas de imagen"
    ),
    tooltip="Elegir carpeta con las capturas de imagen",
)

boton_carpeta_destino = ft.ElevatedButton(
    text = "Carpeta recortes",
    icon=ft.icons.FOLDER_OPEN,
    ## manejador: leer sólo directorios
    on_click=lambda _: dialogo_directorio_destino.get_directory_path(
        dialog_title="Elegir carpeta para los recortes creados",
        ),
    tooltip = "Elegir carpeta para los recortes creados",
    disabled = True,       
    height = altura_botones,
    width  = ancho_botones,
    bgcolor = ft.colors.RED_900,
    color = ft.colors.WHITE,
)



texto_dimensiones = ft.Text("Dimensiones\nrecorte:", tooltip="512x512 por defecto")


# lista desplegable para elegir opciones de imagen 
lista_dimensiones_desplegable = crear_lista_desplegable(tupla_resoluciones[1:], ancho=120)


# componentes repartidos en segmentos horizontales
fila_controles_apertura = ft.Row(
    [boton_carpeta_origen, boton_carpeta_destino],
    width = 500,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    wrap = True
    )

fila_controles_dimensiones = ft.Row(
    [texto_dimensiones, lista_dimensiones_desplegable],
    width = 400,
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    wrap = False
    )

fila_controles = ft.Row([
    # boton_carpeta_origen, boton_carpeta_destino, 
    fila_controles_apertura,
    fila_controles_dimensiones,
    ayuda_emergente
    ],
    wrap = True,
    # alignment=ft.MainAxisAlignment.END,
    )
