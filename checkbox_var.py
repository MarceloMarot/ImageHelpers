import flet as ft
# https://flet.dev/docs/controls/switch

def main(page: ft.Page):

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
    def button_clicked(e):
        valores=""
        # for i in range(0,len(c)):
        #     if  c[i].value:
        #         valores += " " + c[i].label   
        #         # reinicio de switches
        #         c[i].value = False
    # for i in range(0,len(columna)):
    #     if  columna[i].value:
    #         valores += " " + columna[i].label   
    #         # reinicio de switches
    #         columna[i].value = False            


        t.value = (
            f"Switch values are:  {valores}."
        )
        page.update()

    t = ft.Text(size=30 ,width=400, height=200, bgcolor=ft.colors.AMBER_200, )

    c=[]
    for i  in range(0,20):
        ccc = ft.Switch(label=f"{i}", value=False )
        c.append(ccc) 
        # ft.Switch(label=f"{i}", value=False)

    d=[]
    for i  in range(20,35):
        ddd = ft.Switch(label=f"{i}", value=False )
        d.append(ddd) 
        # ft.Switch(label=f"{i}", value=False)



    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(t,  b)
    # Columna de checkboxes
    columna=[]
    col = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=c,
        # width=page.window_width,
        # width=float("inf"), # anchura de columna    
        width=300, # anchura de columna   
        height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )
    columna.append(col)
    col = ft.Column(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=d,
        # width=page.window_width,
        # width=float("inf"), # anchura de columna    
        width=300, # anchura de columna   
        height=600,         # altura de columna
        scroll=ft.ScrollMode.ALWAYS,
    )
    columna.append(col)
    fila=ft.Row(
        wrap=False,
        # spacing=10,       # espaciado horizontal entre contenedores
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls=columna,
        # width=page.window_width,
        # width=float("inf"), # anchura de columna    
        width=700,      # anchura de fila  
        height=600,     # altura de fila
    )
    page.add(fila)






#   b = ft.ElevatedButton("Click HIER!", on_click=boton_clickeado, data=0, bgcolor="green", width=150)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)

