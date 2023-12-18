import flet as ft
# https://flet.dev/docs/controls/switch

def main(page: ft.Page):

    # Estilos 
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.AMBER,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: ft.colors.RED,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
            # interactive=False,
        )
    )


    page.title = "Lista CheckBoxes Variable"
    page.window_width=700
    page.window_height=1000
    # page.bgcolor=ft.colors.LIME_ACCENT_100
    # page.bgcolor=ft.color.INDIGO_100
    def submit_opciones(e):
        valores=""
        for i in range(0,len(checkboxes)):
            if  checkboxes[i].value:
                valores += " " + checkboxes[i].label   
                # reinicio de switches
                checkboxes[i].value = False
        t.value = (
            f"Switch values are:  {valores}."
        )
        page.update()


    def checkboxes_ninguno(e):
        for i in range(0,len(checkboxes)):
            # resetear de switches
            checkboxes[i].value = False
        page.update()


    def checkboxes_todos(e):
        for i in range(0,len(checkboxes)):
            # setear de switches
            checkboxes[i].value = True
        page.update()
        



    t = ft.Text(size=30 ,width=400, height=200, bgcolor=ft.colors.AMBER_200, )

    checkboxes=[]
    for i  in range(0,20):
        ccc = ft.Switch(label=f"{i}", value=False)
        checkboxes.append(ccc) 
        # ft.Switch(label=f"{i}", value=False)

    boton_submit = ft.ElevatedButton(text="Submit", on_click=submit_opciones, bgcolor="red",color="white")
    b2 = ft.ElevatedButton(text="Todo", on_click=checkboxes_todos   ,width=150)
    b3 = ft.ElevatedButton(text="Nada", on_click=checkboxes_ninguno ,width=150)


    fila_botones = ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=50,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = [ b2, b3],
        # width=page.window_width,
        # width=float("inf"), # anchura de columna    
        width=400, # anchura de columna   
        # height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )


    page.add(t,  fila_botones)
    # Columna de checkboxes
    columna = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=checkboxes,
        # width=page.window_width,
        # width=float("inf"), # anchura de columna    
        width=400, # anchura de columna   
        height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )
    page.add(columna)
    page.add(boton_submit)


#   b = ft.ElevatedButton("Click HIER!", on_click=boton_clickeado, data=0, bgcolor="green", width=150)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)

