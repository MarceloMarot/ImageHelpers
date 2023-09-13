import flet as ft

# Clase para generar "contadores": boton + caja texto
class Counter(ft.UserControl):

    # manejador ("handler") para cada boton
    def add_click(self, e):
        self.counter += 1
        self.text.value = str(self.counter)
        # self.boton.bgcolor="yellow" if self.boton.bgcolor != "yellow" else "orange"
        self.boton.bgcolor="yellow" if self.counter%2 != 0 else "orange"    # color segun valor par o impar
        self.update()

    # Crear instancia --> "Construir" (build)
    def build(self):
        self.counter = 0
        self.text = ft.Text(str(self.counter))
        self.boton = ft.ElevatedButton("Sumar", on_click=self.add_click, bgcolor="red")
        return ft.Row(controls=[self.text, self.boton])

    # Para leer o afectar parametros internos hay que usar metodos dedicados
    # Metodo lectura
    def getCounter(self):
        return self.counter

    # Metodo escritura
    def setCounter(self, valor:int):
        self.counter = valor
        self.text.value = str(self.counter)
        self.boton.bgcolor="yellow" if self.counter%2 != 0 else "orange"    # color segun valor par o impar
        self.update()


def main(page):
    page.title = "Botones Contadores"
    page.window_width  = 500
    page.window_height = 500
 
    controles=[]

    numero_botones = 5

    # Creacion de contadores
    for i in range(0,numero_botones):
        control = Counter()
        controles.append(control)

    # Lectura de contadores
    def handler_lectura(e):
        t = ""
        for i in range(0, len(controles)):
            t += f" {controles[i].getCounter()} "

        texto_lectura.value = t
        page.update()


    # Elementos de lectura de estados
    boton_lectura = ft.ElevatedButton("Leer", on_click=handler_lectura, bgcolor="blue", color="white", width=200)
    texto_lectura = ft.Text()

    fila_lectura = ft.Row([boton_lectura, texto_lectura])

    #Columna botones
    columna= ft.Column(
        wrap=False,
        spacing=10,       # espaciado horizontal entre contenedores
        run_spacing=50,     # espaciado vertical entre filas
        controls = controles, 
        # controls = controles_todos, 
        scroll=ft.ScrollMode.ALWAYS,
    )
    
    # Añadido de los elementos a la pagina
    page.add(columna)
    page.add(fila_lectura)

    # Valor de arranque no nulo para un contador particular
    # Debe hacerse DESPUES de añadir los elementos a la pagina
    controles[1].setCounter(19)
    controles[2].setCounter(8)




ft.app(target=main)