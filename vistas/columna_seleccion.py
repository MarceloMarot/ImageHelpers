import flet as ft


from componentes.galeria_imagenes import  Contenedor_Imagen
from componentes.estilos_contenedores import estilos_seleccion, estilos_galeria, Estilos



texto_imagen= ft.Text(
    "(Titulo)",
    size=20,
    # height=30, 
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_ruta_titulo = ft.Text(
    "(ruta))",
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_ruta_data = ft.Text(
    "(ruta_completa))",
    weight=ft.FontWeight.NORMAL,
    text_align=ft.TextAlign.CENTER,
    )
texto_tags_titulo = ft.Text(
    "(nro tags)",
    weight=ft.FontWeight.BOLD,
    text_align=ft.TextAlign.CENTER,
    )
texto_tags_data = ft.Text(
    "(tags)",
    weight=ft.FontWeight.NORMAL,
    text_align=ft.TextAlign.CENTER,
    )


# contenedor visualizador de la imagen actual
contenedor_seleccion = Contenedor_Imagen("",512,512)
contenedor_seleccion.estilo(estilos_seleccion[Estilos.DEFAULT.value])
# contenedor_seleccion.estilo(estilos_seleccion[Estilos.ACTUAL.value])          # FIX
contenedor_seleccion.bgcolor = ft.colors.LIGHT_BLUE



columna_seleccion = ft.Column(
    [
        texto_imagen, 
        contenedor_seleccion, 
        texto_ruta_titulo, 
        texto_ruta_data, 
        texto_tags_titulo,
        texto_tags_data,
    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    expand=True,
    # expand=1,
    visible=True,
    )



# Demo
if __name__=="__main__":

    def main(pagina: ft.Page):
        pagina.add(columna_seleccion)


        pagina.update()


    ft.app(target=main)       