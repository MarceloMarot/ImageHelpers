import flet as ft




class DialogoAlerta:

    def __init__(
        self, 
        pagina: ft.Page,
        titulo:     str="",
        contenido:  str="",
        ):
        self.pagina:  ft.Page = pagina
        self.titulo:    str = titulo
        self.contenido: str = contenido
        self.funcion_confirmacion = None
        self.dialogo = ft.AlertDialog(
            modal=False,
            title=ft.Text(self.titulo),
            content=ft.Text(self.contenido),
            actions=[
                ft.ElevatedButton(
                    "Sí", 
                    on_click=self.accion_confirmar,
                    autofocus=False,
                    ),
                ft.OutlinedButton(
                    "No", 
                    on_click  = self.cerrar_dialogo,
                    autofocus = True 
                    ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )

    def abrir_alerta(self, e:ft.ControlEvent|None=None):
        self.pagina.dialog = self.dialogo
        self.pagina.dialog.open = True
        self.pagina.update()

    def cerrar_dialogo(self, e:ft.ControlEvent|None=None):
        self.pagina.dialog.open = False
        self.pagina.update()

    
    def accion_confirmar(self, e:ft.ControlEvent|None=None):
        if self.funcion_confirmacion !=None:
            self.funcion_confirmacion()
        self.cerrar_dialogo(e)