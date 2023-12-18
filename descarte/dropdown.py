

# LISTA DESPLEGABLE ('DROP - DOWN')

# https://flet.dev/docs/controls/dropdown/


import flet as ft

def main(page: ft.Page):
    # def button_clicked(e):
    #     t.value = f"Dropdown value is:  {dd.value}"
    #     page.update()

    def cambio_opcion(e):
        t.value = f"Dropdown value is:  {dd.value}"
        page.update()

    t = ft.Text()
    # b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    dd = ft.Dropdown(
        width=100,
        on_change = cambio_opcion
        # options=[
        #     ft.dropdown.Option("Red"),
        #     ft.dropdown.Option("Green"),
        #     ft.dropdown.Option("Blue"),
        # ],
    )


    opciones = [] 
    for i in range(0,10):
        opciones.append( ft.dropdown.Option(f"{i}") )


    dd.options = opciones



    def buscar_opcion(valor):
        for opcion in dd.options:
             if valor == opcion.key:
                return opcion
        return None


    def agregar_opcion(e):
        # Si la opcion no existe se añade
        if option_textbox.value == "":
            return
        opcion = buscar_opcion(option_textbox.value) 
        if opcion == None:
            # creacion y agregado opcion
            nuevo = ft.dropdown.Option(option_textbox.value)
            dd.options.append(nuevo)
            dd.update()
        #borrado caja texto
        option_textbox.value=""
        option_textbox.update()


    def eliminar_opcion(e):
        # Si la opcion existe se elimina
        opcion = buscar_opcion(dd.value) 
        if opcion != None:
            dd.options.remove(opcion)
            dd.update()
            # return



    # page.add(dd, b, t)
    page.add(dd,  t)


    # d = ft.Dropdown()
    option_textbox = ft.TextField(hint_text="Agregar valor")
    boton_agregar = ft.ElevatedButton("Agregar", on_click=agregar_opcion)
    boton_quitar = ft.OutlinedButton("Quitar seleccionado", on_click=eliminar_opcion)
    page.add( ft.Row(
        controls=[
            option_textbox,
            boton_agregar, 
            boton_quitar
            ]))



ft.app(target=main) 