import flet as ft
# https://flet.dev/docs/controls/switch

def main(page: ft.Page):


    page.title = "Lista CheckBoxes Variable"
    page.window_width=600
    page.window_height=1000
    page.bgcolor=ft.colors.LIME_ACCENT_100
    # page.bgcolor=ft.color.INDIGO_100
    def button_clicked(e):
        valores=""
        for i in range(0,len(c)):
            if  c[i].value:
                valores += " " + c[i].label   

            
        t.value = (
            f"Switch values are:  {valores}."
        )
        page.update()

    t = ft.Text(size=30 ,width=400, height=200, bgcolor=ft.colors.AMBER_200,)

    c=[]
    for i  in range(0,5):
        ccc = ft.Switch(label=f"{i}", value=False)
        c.append(ccc) 
        # ft.Switch(label=f"{i}", value=False)

    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(t,  b)
    for i in range(0, len(c)):
        page.add(c[i])


#   b = ft.ElevatedButton("Click HIER!", on_click=boton_clickeado, data=0, bgcolor="green", width=150)

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)