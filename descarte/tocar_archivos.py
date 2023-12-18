import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
from flet_core.utils import string


# Contenedor con eventos integrados
# pensado para contener imagenes
class BotonAperturaArchivos(ft.UserControl):

    # INICIALIZACION
    def build(self ):
        # self.funcion_click = lambda: nada()
        #identificador numerico
        # self.archivos_seleccionados = []
        # self.dialogo_archivos = FilePicker(
        #     on_result=self.abrir_archivos
        #     )
        # self.dialog =  FilePicker(on_result=leer_archivos)

        self.boton = ElevatedButton(
            text="Subir Archivo(s)",
            icon=icons.UPLOAD_FILE,
            # on_click=lambda _: self.dialogo_archivos.pick_files(
            #     allow_multiple=True
            #     # allow_multiple=False
            # ),
            # on_click = self.click,

        )
        # FilePicker(on_result=pick_files_result)
        return self.boton




    # hide all dialogs in overlay
    # el añadido de los diálogos es OBLIGATORIO
    #  NO es necesario añadirlos todos juntos
    # page.overlay.extend([ mi_dialogo ])


    # Pick files dialog
    def abrir_archivos(self, e: FilePickerResultEvent):
        # self.archivos_seleccionados.value = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        # self.archivos_seleccionados = e.files
        print("Archivos :",         e.files[0] )
        print("Tipo     :", type(   e.files[0]))
        print("name     :",     e.files[0].name)
        print("path     :",     e.files[0].path)
        print("size     :",     e.files[0].size)


def main(page: Page):
    # Funcion de seleccion de archivos
    def pick_files_result(e: FilePickerResultEvent):
        # print("Archivos :",         e.files[0] )
        # print("Tipo     :", type(   e.files[0]))
        # print("name     :",     e.files[0].name)
        # print("path     :",     e.files[0].path)
        # print("size     :",     e.files[0].size)
        # selected_files.value = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        selected_files.value = str(e.files)
        selected_files.update()

    # Clase para manejar dialogos de archivo
    # pick_files_dialog = FilePicker(on_result=pick_files_result)
    pick_files_dialog = FilePicker(on_result=None)
    # Caja de texto
    selected_files = Text()

    # Funcion de guardado de archivo
    def save_file_result(e: FilePickerResultEvent):
        # save_file_path.value = e.path if e.path else "Cancelled!"
        save_file_path.value = e.path 
        save_file_path.update()

    # Clase para manejar dialogos de archivo
    save_file_dialog = FilePicker(on_result=save_file_result)
    # Caja de texto
    save_file_path = Text()

    # Funcion de apertura de directorio
    def get_directory_result(e: FilePickerResultEvent):
        # directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.value = e.path 
        directory_path.update()

    # Clase para manejar dialogos de archivo
    get_directory_dialog = FilePicker(on_result=get_directory_result)
    # Caja de texto
    directory_path = Text()

    # # hide all dialogs in overlay
    # # el añadido de los diálogos es OBLIGATORIO
    #  NO es necesario añadirlos todos juntos
    page.overlay.extend([
        pick_files_dialog, 
        save_file_dialog, 
        get_directory_dialog, 
        # mi_dialogo
        ])

    def leer_archivos(e: FilePickerResultEvent):
        print("Archivos :",         e.files[0] )
        print("Tipo     :", type(   e.files[0]))
        print("name     :",     e.files[0].name)
        print("path     :",     e.files[0].path)
        print("size     :",     e.files[0].size)


    
    mi_dialogo =  FilePicker(on_result=leer_archivos)
    # hide all dialogs in overlay
    # el añadido de los diálogos es OBLIGATORIO
    #  NO es necesario añadirlos todos juntos
    page.overlay.extend([ mi_dialogo ])
    # page.overlay.extend([ mi_dialogo ])
    # page.overlay.extend([ mi_dialogo ])



    page.add(
        Row(
            [
                ElevatedButton(
                    text="Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                        # allow_multiple=False
                    ),
                ),
                selected_files,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    text="Save file",
                    icon=icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(),
                    disabled=page.web,      # deshabiliado en modo pagina web
                ),
                save_file_path,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    text="Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,       # deshabiliado en modo pagina web
                ),
                directory_path,
            ]
        ),

    )

    miboton = BotonAperturaArchivos()     
    page.add(miboton)     

    page.overlay.extend([ mi_dialogo ])
    # miboton.extend([ mi_dialogo ])
    miboton.boton.on_click = lambda _: mi_dialogo.pick_files(
                allow_multiple=True
                # allow_multiple=False
            )
    # page.add( ft.IconButton(icon=ft.icons.ZOOM_IN))
    # page.add( ft.IconButton(icon=ft.icons.REMOVE))
    # page.add( ft.IconButton(icon=ft.icons.TERMINAL  ))
    # page.add(
    #     ft.TextField(
    #         value="0", 
    #         text_align=ft.TextAlign.LEFT, 
    #         width=300
    #         )
    #     )

    # page.add( ft.IconButton(icon=ft.icons.SQUARE  ))
    # Orden de apertura archivos
    # pick_files_dialog.pick_files()

    # page.controls.append( ft.IconButton(icon=ft.icons.ZOOM_OUT) )
    # page.update()

ft.app(target=main)



