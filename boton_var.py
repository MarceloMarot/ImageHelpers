import flet as ft
# https://flet.dev/docs/controls/switch

def main(page):

    page.title = "Lista Botones Variable"
    page.window_width=600
    page.window_height=1000
    # page.bgcolor=ft.colors.LIME_ACCENT_100

    # Manejador botones con retencion --> evento 'click' 
    def boton_clickeado(self, e):
        e.data += 1                                    #variable entera interna del botón
        e.bgcolor="yellow" if b.bgcolor!="yellow" else "orange"
        e.text =  f"Button clicked {b.data} time(s)"  # la propiedad 'text' del boton es analoga al 'print' de consola
        page.update()


    def click_submit(e):
        # b.bgcolor="yellow" if b.bgcolor!="yellow" else "orange"
        valores=""
        for i in range(0,len(c)):
            if  c[i].data/2:
                valores += " " + c[i].label   
                # c[i].bgcolor="yellow" if c[i].bgcolor!="yellow" else "orange"
            
        t.value = (
            f"Switch values are:  {valores}."
        )
        page.update()

    t = ft.Text()

    c=[]
    for i  in range(0,5):
        ccc = ft.ElevatedButton(text=f"{i}", on_click=boton_clickeado ,data=0, bgcolor="green", width=150)
        # ccc = ft.Switch(label=f"{i}", value=False)
        c.append(ccc) 
        # ft.Switch(label=f"{i}", value=False)

    b = ft.ElevatedButton(text="Submit", on_click=click_submit, bgcolor="red",color="white",width=150)
    page.add( b, t)
    for i in range(0, len(c)):
        page.add(c[i])




# ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)