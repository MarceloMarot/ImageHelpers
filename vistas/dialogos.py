import flet as ft



# Clase para manejar dialogos de archivo y de carpeta
dialogo_directorio      = ft.FilePicker()
dialogo_dataset         = ft.FilePicker()
dialogo_guardado_tags   = ft.FilePicker()










class AlertasDialogo:

    def __init__(self, pagina:ft.Page|None=None, alerta: ft.AlertDialog|None = None, lista_funciones: list =[]):
        self.pagina = pagina
        self.alerta = alerta
        self.lista_funciones = lista_funciones


    def abrir_dialogo(self):

        self.pagina.dialog = self.alerta 

        # mantener dialogo abierto
        self.pagina.dialog.open = True
        self.pagina.update()



    def cerrar_dialogo(self):
        self.pagina.dialog.open = False
        self.pagina.update()


    # def cerrar_programa(self):
    #     self.pagina.window_destroy()


alerta_cierre = AlertasDialogo()


alerta = ft.AlertDialog(
    modal=False,
    title=ft.Text("¿Descartar cambios y salir?"),
    content=ft.Text(f"Hay imágenes con modificaciones sin guardar."),
    actions=[
        ft.ElevatedButton(
            "Sí", 
            # on_click=cerrar_programa,
            # on_click=alerta_cierre.cerrar_programa,
            autofocus=False,
            ),
        ft.OutlinedButton(
            "No", 
            # on_click=cerrar_dialogo,
            # on_click=alerta_cierre.cerrar_dialogo,
            autofocus=True 
            ),
        ],
    actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    )


