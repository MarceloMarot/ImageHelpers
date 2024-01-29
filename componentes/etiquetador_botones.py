
import flet as ft

from componentes.procesar_etiquetas import  Etiquetas


class BotonBiestable(ft.ElevatedButton):
    def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.BLUE_50 ):
        self.__valor = False
        self.color_true  = color_true
        self.color_false = color_false
        super().__init__(
            text = texto,
            bgcolor= self.color_false,
            on_click=self.click
        )

    # implementacion del biestable
    def click(self,e: ft.ControlEvent):
        valor = True if self.__valor==False else False
        self.estado = valor

    @property
    def estado(self):
        return self.__valor

    # actualizacion del booleano y de colores
    @estado.setter
    def estado(self, valor: bool):
        if valor:
            self.__valor = True
            self.bgcolor = self.color_true
            self.color = ft.colors.WHITE 
        else:
            self.__valor = False
            self.bgcolor = self.color_false
            self.color   = ft.colors.BLUE_800
        self.update()


class BotonGrupo(ft.IconButton):
    def __init__(self):
        self.estado = False
        super().__init__(
            icon=ft.icons.SELECT_ALL_ROUNDED ,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_800,
            )


class FilasBotones(ft.Column):
    def __init__(self):
        self.dataset: Etiquetas
        self.etiquetas: Etiquetas
        self.botones_etiquetas = []
        self.__botones_grupo = []
        self.__filas_botones = []
        self.__numero_grupos = 0
        self.__numero_colores = 0
        self.__ancho = 600
        self.lista_colores = [
            ft.colors.RED_800,
            ft.colors.ORANGE_800, 
            ft.colors.YELLOW_800,
            ft.colors.LIME_800,
            ft.colors.GREEN_800,
            ft.colors.GREEN_ACCENT_700,
            ft.colors.CYAN_800,        
            ft.colors.BLUE_800,           
            ft.colors.PURPLE_800,      
            ft.colors.BROWN_800,
            ]
        self.boton_guardar = ft.ElevatedButton(
            text="guardar cambios",
            # width =500,
            width = 200,
            bgcolor= ft.colors.RED_900,
            color= ft.colors.WHITE,
            # on_click= funcion_guardar
            on_click= self.guardar_etiquetas
            )

        self.boton_todos = ft.ElevatedButton(
            text="todas",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.todas_etiquetas
            )

        self.boton_nada = ft.ElevatedButton(
            text="ninguna",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.ninguna_etiqueta
            )

        self.boton_descartar = ft.ElevatedButton(
            text="descartar cambios",
            width = 200,
            bgcolor= ft.colors.GREEN_800,
            color= ft.colors.WHITE,
            on_click= self.restablecer_etiquetas
            )
        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            controls =  [], 
            width= self.__ancho, # anchura de columna   
            # height=500,
            scroll=ft.ScrollMode.AUTO,
        )

    @property
    def ancho(self):
        return self.__ancho

    @ancho.setter
    def ancho(self, valor):
        self.__ancho = valor
        for i in range(self.__numero_grupos):
            self.__filas_botones[i].width = self.__ancho
       

    def leer_dataset(self, ruta: str):
        self.dataset = Etiquetas(ruta) 
        self.dataset.leer()
        tags = self.dataset.tags
        grupo = self.dataset.grupo
        data = self.dataset.data
        # conteo grupos de etiquetas
        grupos = list(set(grupo))
        self.__numero_grupos = len(grupos)
        self.__numero_colores = len(self.lista_colores)  
        # maquetado
        self.__filas_botones = []
        self.__botones_grupo = []
        for i in range(self.__numero_grupos):
            g = BotonGrupo()
            g.data = i          # indice grupo
            g.on_click = self.conmutar_grupo
            self.__botones_grupo.append(g)
            self.__filas_botones.append( ft.Row(
                controls = [g],
                width = self.__ancho,
                wrap = True,
                ))  
        # lista completa de botones
        self.botones_etiquetas = []
        # crear botones y repartirlos
        for tag in tags:
            b = BotonBiestable(tag)
            self.botones_etiquetas.append(b)
            # reparto grafico de botones
            i = data[tag]
            self.__filas_botones[i].controls.append(b)
            # asignacion color
            b.color_false = ft.colors.INDIGO_50
            # se pone un tope a los grupos posibles
            b.color_true = self.lista_colores[i % self.__numero_colores ]
            self.__botones_grupo[i].bgcolor = self.lista_colores[i % self.__numero_colores ]
        self.controls = self.__filas_botones
        self.update()


    def leer_etiquetas(self, ruta: str):
        self.etiquetas = Etiquetas(ruta) 
        self.etiquetas.leer()
        self.actualizar_botones()


    def actualizar_botones(self):
        for boton in self.botones_etiquetas:
            tag = boton.text
            if tag in self.etiquetas.tags:
                boton.estado = True
            else:
                boton.estado = False
        self.update()

    def todas_etiquetas(self, e):
        for boton in self.botones_etiquetas:
            boton.estado = True


    def ninguna_etiqueta(self,e):
        for boton in self.botones_etiquetas:
            boton.estado = False


    def restablecer_etiquetas(self, e):
        self.etiquetas.leer()
        self.actualizar_botones()


    def guardar_etiquetas(self, e):
        etiquetas=[]

        for boton in self.botones_etiquetas:
            etiqueta = boton.text
            valor    = boton.estado
            if valor:
                etiquetas.append(etiqueta)
        # relectura de etiquetas para prevenir relecturas inutiles
        self.etiquetas.leer()    
        if set(self.etiquetas.tags) != set(etiquetas): 
            print("cambios guardados")
            # guardado de etiquetas y reporte
            if self.etiquetas.guardar(etiquetas)==False:
                print("guardado fallido")
        else:
            print("sin cambios")
        self.update()


    def conmutar_grupo(self, e: ft.ControlEvent ):
        boton_grupo = e.control
        grupo = boton_grupo.data
        # Se corrige el estado del grupo de modo que el click afecte al mayor numero de etiquetas posible
        # (mejora la respuesta al usuario)
        activados = 0
        desactivados = 0
        for boton in self.__filas_botones[grupo].controls:
            if boton.estado:
                activados += 1
            else:
                desactivados += 1
        boton_grupo.estado = True if activados >= desactivados else False
        # cambio de estado lógico de todo el grupo
        boton_grupo.estado = True if boton_grupo.estado == False else False 
        for boton in self.__filas_botones[grupo].controls:
            boton.estado = boton_grupo.estado
        # actualizacion
        self.__filas_botones[grupo].update()


class EtiquetadorBotones(ft.Column):
    def __init__(self, filas_botones: FilasBotones):
        # self.controles: FilasBotones
        self.__ancho = 600
        super().__init__(
            controls = [filas_botones],
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            scroll=ft.ScrollMode.HIDDEN, 
            )
        self.divisor = ft.Divider()
        # self.divisor = ft.Divider(height=10)
        self.controls.append(self.divisor)
        self.__f1 =ft.Row([
            filas_botones.boton_todos, filas_botones.boton_nada
            ],
            width = self.__ancho, 
            wrap = True,    
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            # run_spacing=100
            )
        self.controls.append(self.__f1)
        self.__f2 = ft.Row([
            filas_botones.boton_descartar, filas_botones.boton_guardar
            ],
            width = self.__ancho, 
            wrap = True,
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            # run_spacing=100
            )  
        self.controls.append(self.__f2)

    @property
    def ancho(self):
        return self.ancho

    @ancho.setter
    def ancho(self, valor):
        self.__ancho = valor
        self.__f1.width = valor
        self.__f2.width = valor


def main(page: ft.Page):

    # Recordar: se ignora la extension del archivo de etiqueta
    # éste siempre es TXT
    archivo_dataset = "demo_etiquetas.png"
    archivo_etiquetas = "etiquetas_salida.jpg"

    # componente etiquetador
    filas_etiquetas = FilasBotones()
    etiquetador = EtiquetadorBotones(filas_etiquetas)
    page.add( etiquetador)

    filas_etiquetas.height = 700
    filas_etiquetas.ancho         = 500
    etiquetador.ancho   = 500
    filas_etiquetas.leer_dataset(archivo_dataset)
    filas_etiquetas.leer_etiquetas(archivo_etiquetas)

    page.title = "Botones etiquetado"
    page.window_height      = 900
    page.window_min_height  = 900
    page.window_width       = 600
    page.update()



if __name__ == "__main__":
    ft.app(target=main)