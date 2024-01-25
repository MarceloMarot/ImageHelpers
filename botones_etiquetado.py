
import flet as ft

from componentes.procesar_etiquetas import  Etiquetas
from boton_color import BotonColor , BotonGrupo


lista_colores_oscuros = [
    # ft.colors.DEEP_PURPLE_800,
    ft.colors.RED_800,
    ft.colors.ORANGE_800,
    # ft.colors.AMBER_800, 
    ft.colors.YELLOW_800,
    ft.colors.LIME_800,
    ft.colors.GREEN_800,
    ft.colors.GREEN_ACCENT_700,
    ft.colors.PINK_800,
    ft.colors.PURPLE_800,
    # ft.colors.INDIGO_800,        
    ft.colors.CYAN_800,        
    ft.colors.BLUE_800,        
    # ft.colors.GREY_800,        
    ]


class EtiquetadorBotones(ft.Column):
    def __init__(self):
        self.dataset: Etiquetas
        self.etiquetas: Etiquetas
        self.botones_etiquetas = []
        self.__botones_grupo = []
        self.__filas_botones = []
        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            controls =  [], 
            # width= 600, # anchura de columna   
            # height=500,
            scroll=ft.ScrollMode.AUTO,
        )
       

    def leer_dataset(self, ruta: str):
        self.dataset = Etiquetas(ruta) 
        self.dataset.leer()
        tags = self.dataset.tags
        grupo = self.dataset.grupo
        data = self.dataset.data
        # conteo grupos
        grupos = list(set(grupo))
        n = len(grupos)

        m = len(lista_colores_oscuros)  
        # maquetado
        self.__filas_botones = []
        self.__botones_grupo = []
        for i in range(n):
            g = BotonGrupo()
            g.data = i          # indice grupo
            g.on_click = self.conmutar_grupo
            self.__botones_grupo.append(g)
            self.__filas_botones.append( ft.Row(
                controls = [g],
                # controls = [],
                width = 400,
                wrap = True,
                ))
            i = i % m
            g.bgcolor=lista_colores_oscuros[i],

        # lista completa de botones
        self.botones_etiquetas = []
        
        # crear botones y repartirlos
        for tag in tags:
            b = BotonColor(
                tag,
                # ft.colors.GREEN_200 ,
                # ft.colors.GREEN_700
            )
            self.botones_etiquetas.append(b)
            # reparto grafico de botones
            i = data[tag]
            self.__filas_botones[i].controls.append(b)
            # se pone un tope a los grupos posibles
            # m = len(lista_colores_oscuros)
            i = i % m
            # asignacion color
            # b.color_false=lista_colores_claros[i]
            b.color_false=ft.colors.INDIGO_50
            b.color_true=lista_colores_oscuros[i]
        

        self.controls = self.__filas_botones
        self.update()


    def leer_etiquetas(self, ruta: str):
        self.etiquetas = Etiquetas(ruta) 
        self.etiquetas.leer()
        self.actualizar()


    def actualizar(self):
        for boton in self.botones_etiquetas:
            tag = boton.text
            if tag in self.etiquetas.tags:
                # boton.valor = True
                # boton.estado(True)
                boton.estado = True
            else:
                # boton.value = False
                # boton.estado(False)
                boton.estado = False
        self.update()


    def guardar_etiquetas(self):
        etiquetas=[]

        for boton in self.botones_etiquetas:
            etiqueta = boton.text
            valor    = boton.estado
            if valor:
                etiquetas.append(etiqueta)
        # relectura de etiquetas para prevenir relecturas inutiles
        self.etiquetas.leer()    
        # print("postlectura: ", self.etiquetas_imagen.ruta)
        if set(self.etiquetas.tags) != set(etiquetas): 
            # self.texto.value = "Cambios guardados"
            print("cambios guardados")
            # guardado de etiquetas y reporte
            if self.etiquetas.guardar(etiquetas)==False:
                # self.texto.value = " Error: guardado fallido"
                print("guardado fallido")
        else:
            # self.texto.value = "Sin cambios"
            print("sin cambios")
        self.update()


    def conmutar_grupo(self, e: ft.ControlEvent ):
        # estado = e.control.estado
        # grupo = e.control.data 
        boton_grupo = e.control
        grupo = boton_grupo.data

        # Se corrige el estado del grupo de modo que el click sea lo mas notorio posible
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



def main(page: ft.Page):

    # Recordar: se ignora la extension del archivo de etiqueta
    # éste siempre es TXT
    archivo_dataset = "demo_etiquetas.png"
    archivo_etiquetas = "etiquetas_salida.jpg"

    etiquetador = EtiquetadorBotones()
    etiquetador.height=700
    page.add( etiquetador)

    etiquetador.leer_dataset(archivo_dataset)
    etiquetador.leer_etiquetas(archivo_etiquetas)

    def funcion_guardar(e):
        etiquetador.guardar_etiquetas()

    b = ft.ElevatedButton(
        text="guardar",
        width =500,
        bgcolor= ft.colors.GREY_900,
        color= ft.colors.WHITE,
        on_click= funcion_guardar
        )
    page.add(b)

    page.title = "Botones etiquetado"
    page.window_height      = 900
    page.window_min_height  = 900
    page.window_width       = 600
    page.update()


ft.app(target=main)