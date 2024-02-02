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
        self.__alto = 400
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
        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            controls =  [], 
            width= self.__ancho, # anchura de columna   
            height=self.__alto,
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

    def setear_salida(self, ruta: str):
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
    def __init__(self):
        self.__filas_botones = FilasBotones()   # componente interno --> composicion
        self.__ancho = 600
        self.__altura_filas = 40
        self.__habilitado = False
        self.__dataset_seteado = False
        self.__salida_seteada = False
        self.__boton_guardar = ft.ElevatedButton(
            text="guardar cambios",
            width = 200,
            bgcolor= ft.colors.RED_900,
            color= ft.colors.WHITE,
            on_click= self.guardar_etiquetas
            )
        self.__boton_todos = ft.ElevatedButton(
            text="todas",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.todas_etiquetas
            )
        self.__boton_nada = ft.ElevatedButton(
            text="ninguna",
            width = 200,
            bgcolor= ft.colors.INDIGO_400,
            color= ft.colors.WHITE,
            on_click= self.ninguna_etiqueta
            )
        self.__boton_descartar = ft.ElevatedButton(
            text="descartar cambios",
            width = 200,
            bgcolor= ft.colors.GREEN_800,
            color= ft.colors.WHITE,
            on_click= self.restablecer_etiquetas
            )
        super().__init__(
            controls = [],
            wrap=False,
            # spacing=10,       # espaciado horizontal 
            # run_spacing=50,     # espaciado vertical entre filas
            )
        self.__divisor = ft.Divider(height = 10)
        self.__f1 =ft.Row(
            controls= [ self.__boton_todos, self.__boton_nada ],
            width = self.__ancho, 
            wrap = True,    
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            height = self.__altura_filas,
            )
        self.__f2 = ft.Row(
            controls= [ self.__boton_descartar, self.__boton_guardar],
            width = self.__ancho, 
            wrap = True,
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            height = self.__altura_filas,
            )  
        self.controls=[self.__filas_botones, self.__divisor, self.__f1, self.__f2, self.__divisor]

    def todas_etiquetas(self, e):
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = True

    def ninguna_etiqueta(self, e):
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = False

    def restablecer_etiquetas(self, e):
        self.__filas_botones.etiquetas.leer()
        self.__filas_botones.actualizar_botones()

    def guardar_etiquetas(self, e):
        etiquetas=[]
        for boton in self.__filas_botones.botones_etiquetas:
            etiqueta = boton.text
            valor    = boton.estado
            if valor:
                etiquetas.append(etiqueta)
        # relectura de etiquetas para prevenir relecturas inutiles
        self.__filas_botones.etiquetas.leer()    
        if set(self.__filas_botones.etiquetas.tags) != set(etiquetas): 
            print("cambios guardados")
            # guardado de etiquetas y reporte
            if self.__filas_botones.etiquetas.guardar(etiquetas)==False:
                print("guardado fallido")
        else:
            print("sin cambios")
        self.update()

    @property
    def ancho(self):
        """Devuelve el ancho total del componente grafico"""
        return self.__ancho

    @ancho.setter
    def ancho(self, valor):
        """Define el ancho total del componente grafico"""
        self.__ancho = valor
        self.__f1.width = valor
        self.__f2.width = valor
        self.__filas_botones.ancho = valor

    @property
    def alto(self):
        """Devuelve el alto total del componente grafico"""
        return self.height

    @alto.setter
    def alto(self, valor):
        """Define el alto total del componente grafico"""
        self.height = valor
        resta = self.__altura_filas * 3 
        resta = resta + int(self.__divisor.height) *3
        self.__filas_botones.height = valor - resta
        self.__filas_botones.update()

    def leer_dataset(self, etiquetas: Etiquetas):
        """Lee las etiquetas del dataset y actualiza etiquetas de salida si corresponde"""
        self.__filas_botones.leer_dataset( etiquetas.ruta )
        self.__dataset_seteado = True
        self.habilitado = True if self.__salida_seteada else False
        # actualiza aspecto grafico para prevenir errores
        if self.__salida_seteada : 
            self.restablecer_etiquetas( "e")


    def setear_salida(self, etiquetas: Etiquetas):
        """Elige el archivo de salida de etiquetas y establece qué botones se activan """
        self.__filas_botones.setear_salida( etiquetas.ruta )
        self.__salida_seteada = True
        self.habilitado = True if self.__dataset_seteado else False
            
    
    @property
    def dataset_seteado(self):
        """Indica si se eligio el archivo del dataset con todas las etiquetas"""
        return self.__dataset_seteado

    @property
    def salida_seteada(self):
        """Indica si se eligio el archivo de salida para las etiquetas"""
        return self.__salida_seteada

    @property
    def habilitado(self):
        """Indica si los controles están habilitados o no"""
        return self.__habilitado

    @habilitado.setter
    def habilitado(self, booleano):
        """Habilita / deshabilita manualmente los controles del etiquetador"""
        if booleano: 
            self.__boton_descartar.disabled = False
            self.__boton_nada     .disabled = False
            self.__boton_todos    .disabled = False
            self.__boton_guardar  .disabled = False
            for boton in self.__filas_botones.botones_etiquetas:
                boton.disabled = False
            # flag de estado
            self.__habilitado = True
        else: 
            self.__boton_descartar.disabled = True
            self.__boton_nada     .disabled = True
            self.__boton_todos    .disabled = True
            self.__boton_guardar  .disabled = True
            for boton in self.__filas_botones.botones_etiquetas:
                boton.disabled = True
            # flag de estado
            self.__habilitado = False



def main(page: ft.Page):

    # Recordar: se ignora la extension del archivo de etiqueta
    # éste siempre es TXT
    archivo_dataset = "demo_etiquetas.png"
    archivo_etiquetas = "etiquetas_salida.jpg"

    # componente etiquetador
    etiquetador = EtiquetadorBotones()
    page.add( etiquetador)

    dataset     = Etiquetas(archivo_dataset) 
    etiquetas   = Etiquetas(archivo_etiquetas) 

    etiquetador.alto = 800
    etiquetador.ancho  = 500
    # carga de archivos (sentido inverso)
    etiquetador.setear_salida( etiquetas )
    etiquetador.leer_dataset(   dataset   )

    page.title = "Botones etiquetado"
    page.window_height      = 800
    page.window_min_height  = 800
    page.window_width       = 650
    page.update()



if __name__ == "__main__":
    ft.app(target=main)