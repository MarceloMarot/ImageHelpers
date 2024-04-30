from rich import print as print
import flet as ft
from manejo_texto.procesar_etiquetas import  Etiquetas


def nada( e ):
    pass


class BotonBiestable(ft.ElevatedButton):
    def __init__(self, texto: str, color_false=ft.colors.BLUE_50, color_true=ft.colors.BLUE_50 ):
        self.__valor = False
        self.color_true  = color_true
        self.color_false = color_false
        super().__init__(
            text = texto,
            key=texto,          # asignacion automatica
            bgcolor= self.color_false,
            on_click=self.click
            )
        # manejador opcional para el click 
        self.click_boton = nada

    # implementacion del biestable
    def click(self,e: ft.ControlEvent):
        valor = True if self.__valor==False else False
        self.estado = valor
        self.click_boton(e)     # (no hace nada a menos que se programe)

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

    @property
    def clave(self):
        return self.key

    @clave.setter
    def clave(self, valor: str):
        self.key = valor


class BotonGrupo(ft.IconButton):
    def __init__(self):
        self.estado = False
        super().__init__(
            icon=ft.icons.SELECT_ALL_ROUNDED ,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_800,
            )
        # manejador opcional para el click 
        self.click_boton = nada


class FilasBotonesEtiquetas(ft.Column):
    """Este componente crea botones de activacion para cada etiqueta (descripcion) detectada en un archivo de texto"""
    def __init__(self):
        self.dataset: Etiquetas =  Etiquetas()
        self.etiquetas: Etiquetas =  Etiquetas()
        self.botones_etiquetas = []
        self.botones_grupo = []
        self.__filas_botones = []
        self.__numero_grupos = 0
        self.__numero_colores = 0
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
        self.funcion_etiquetas = nada
        self.funcion_grupo = nada
        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal 
            run_spacing=50,     # espaciado vertical entre filas
            controls =  [], 
            scroll=ft.ScrollMode.AUTO,
            )

       
    def leer_dataset(self, dataset: Etiquetas):
        """Lee TODAS las etiquetas (el 'dataset') desde un archivo de texto y crea los botones de activacion de la interfaz gráfica.
        El componente clasifica las etiquetas en distintos 'grupos' en base al renglón del archivo en que se encuentran.
        """
        self.dataset = dataset
        tags = self.dataset.tags
        grupo = self.dataset.grupos
        data = self.dataset.datos
        # conteo grupos de etiquetas
        grupos = list(set(grupo))
        self.__numero_grupos = len(grupos)
        self.__numero_colores = len(self.lista_colores)  
        # maquetado
        self.__filas_botones = []
        self.botones_grupo = []
        for i in range(self.__numero_grupos):
            g = BotonGrupo()
            g.data = i          # indice grupo
            g.on_click = self.conmutar_grupo    # evento
            # lista para acceso
            self.botones_grupo.append(g)
            # colocacion al comienzo de cada fila de botones
            self.__filas_botones.append( ft.Row(
                controls = [g],
                wrap = True,
                ))  
        # lista completa de botones
        self.botones_etiquetas = []
        # crear botones y repartirlos
        for tag in tags:
            # reparto grafico de botones
            grupos_tag = data[tag]
            for grupo in grupos_tag:
                # creacion de boton (puede estar repetido)
                b = BotonBiestable(tag)
                self.botones_etiquetas.append(b)
                self.__filas_botones[grupo].controls.append(b)
                # asignacion color
                b.color_false = ft.colors.INDIGO_50
                # se pone un tope a los grupos posibles
                b.color_true = self.lista_colores[grupo % self.__numero_colores ]
                self.botones_grupo[grupo].bgcolor = self.lista_colores[grupo % self.__numero_colores ]
        self.controls = self.__filas_botones
        self.update()
        self.evento_click()

    def deshabilitar_botones(self, valor: bool):
        for boton in self.botones_grupo:
            boton.disabled = valor

        for boton in self.botones_etiquetas:
            boton.disabled = valor

    def setear_salida(self, etiquetas :Etiquetas):
        """Carga el archivo de etiquetas de salida y actualiza el etiquetador grafico"""
        self.etiquetas = etiquetas
        self.actualizar_botones()


    def agregar_tags(self, tags: list[str], sobreescribir:bool=False):
        """Ingresa las etiquetas desde una lista y actualiza los botones."""
        self.etiquetas.agregar_tags(tags,  sobreescribir=sobreescribir)
        self.actualizar_botones()


    def actualizar_botones(self):
        """Lee los estados de los botones en base a las etiquetas ingresadas al componente"""
        for boton in self.botones_etiquetas:
            tag = boton.text
            if tag in self.etiquetas.tags:
                boton.estado = True
            else:
                boton.estado = False
        self.update()



    def leer_botones(self, filtrar_repetidos=True)->list[str]:
        """Lee todas las etiquetas habilitadas mediante los botones. Por defecto filtra los repetidos."""
        etiquetas = []
        for boton in self.botones_etiquetas:
            if boton.estado:
                tag = boton.text
                etiquetas.append(tag)
        if filtrar_repetidos:
            set_etiquetas = set(etiquetas)
            return list(set_etiquetas)
        else:
            return etiquetas


    def leer_etiquetas_archivo(self):
        """Lee y carga las etiquetas ya guardadas en el archivo de salida"""
        self.etiquetas.leer_archivo()  
        

    def conmutar_grupo(self, e: ft.ControlEvent ):
        """Esta funcion habilita o deshabilita un grupo completo de etiquetas"""
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
        # funcion opcional
        boton_grupo.click_boton(e)



    def evento_click(self, funcion_etiquetas=None, funcion_grupo=None):
        """Asigna una funcion para el click de todos los botones según sean de etiquetas o de grupos"""
        if funcion_etiquetas != None:
            self.funcion_etiquetas = funcion_etiquetas 
        if funcion_grupo != None:
            self.funcion_grupo = funcion_grupo
        # asignacion de funciones a cada boton  
        for boton in self.botones_etiquetas:
            boton.click_boton =  self.funcion_etiquetas
        for boton in self.botones_grupo:
            boton.click_boton =  self.funcion_grupo

    def mostrar_tag(self, clave: str, duracion = 1000):
        """Mueve el scroll para mostrar el primer boton con la clave indicada."""
        self.scroll_to(key=clave, duration=duracion)
        self.update()


    @property
    def base(self):
        """Devuelve el ancho total del componente grafico"""
        return self.width

    @base.setter
    def base(self, valor):
        """Define el ancho total del componente grafico"""
        self.width = valor
        for fila in self.__filas_botones:
            fila.width = valor

    @property
    def altura(self):
        """Devuelve la altura total del componente grafico"""
        return self.height

    @altura.setter
    def altura(self, valor):
        """Define la altura total del componente grafico"""
        self.height = valor



class EtiquetadorBotones(ft.Column):
    def __init__(self):
        """Inicializa un componente etiquuetador, agregando a los botones de etiquetas los botones de guardado, descarte de cambios, etc """
        self.__filas_botones = FilasBotonesEtiquetas()   # componente interno --> composicion
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
            wrap = True,    
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            height = self.__altura_filas,
            )
        self.__f2 = ft.Row(
            controls= [ self.__boton_descartar, self.__boton_guardar],
            wrap = True,
            alignment = ft.MainAxisAlignment.CENTER,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 100,
            height = self.__altura_filas,
            )  
        self.controls=[self.__filas_botones, self.__divisor, self.__f1, self.__f2]
        self.click_botones = nada


    def todas_etiquetas(self, e):
        """Activa todas las etiquetas del dataset"""
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = True
        self.click_botones(e)


    def ninguna_etiqueta(self, e):
        """Descarta todas las etiquetas del dataset"""
        for boton in self.__filas_botones.botones_etiquetas:
            boton.estado = False
        self.click_botones(e)


    def restablecer_etiquetas(self, e):
        """Actualiza los botones de etiquetas a sus valores guardados en archivo"""
        self.__filas_botones.leer_etiquetas_archivo()
        self.__filas_botones.actualizar_botones()
        self.click_botones(e)


    def guardar_etiquetas(self, e):
        """Guarda todas las etiquetas seleccionadas en el archivo de texto asignado al componente. Se filtran las etiquetas repetidas."""
        # lectura de etiquetas (elementos repetidos flitrados)
        etiquetas = self.__filas_botones.leer_botones()
        set_etiquetas = set(etiquetas) 
        lista_etiquetas = list(set_etiquetas)
        # relectura de etiquetas para prevenir relecturas inutiles
        self.__filas_botones.leer_etiquetas_archivo()  
        # se intenta el guardado sólo si se detectan cambios de etiquetado 
        if set(self.__filas_botones.etiquetas.tags) != set_etiquetas: 
            # guardado de etiquetas 
            self.__filas_botones.etiquetas.guardar(lista_etiquetas)
        #funcionalidad opcional
        self.click_botones(e)
        # actualizacion grafica y salida
        self.update()
        # return retorno_guardado 


    @property
    def base(self):
        """Devuelve el ancho total del componente grafico"""
        return self.width

    @base.setter
    def base(self, valor):
        """Define el ancho total del componente grafico"""
        self.width = valor
        self.__f1.width = valor
        self.__f2.width = valor
        self.__filas_botones.width = valor

    @property
    def altura(self):
        """Devuelve la altura total del componente grafico"""
        return self.height

    @altura.setter
    def altura(self, valor):
        """Define la altura total del componente grafico"""
        self.height = valor
        resta = self.__altura_filas * 3 
        resta = resta + int(self.__divisor.height) *3
        self.__filas_botones.height = valor - resta


    def leer_dataset(self, etiquetas: Etiquetas):
        """Lee las etiquetas del dataset y actualiza etiquetas de salida si corresponde"""
        self.__filas_botones.leer_dataset( etiquetas )
        self.__dataset_seteado = True
        self.habilitado = True if self.__salida_seteada else False
        # actualiza aspecto grafico para prevenir errores
        if self.__salida_seteada : 
            self.restablecer_etiquetas( "e")


    def setear_salida(self, etiquetas: Etiquetas):
        """Elige el archivo de salida de etiquetas y establece qué botones se activan """
        self.__filas_botones.setear_salida( etiquetas )
        self.__salida_seteada = True
        self.habilitado = True if self.__dataset_seteado else False
            

    def agregar_tags(self, tags: list[str],  sobreescribir:bool=False):
        """Ingresa las etiquetas desde una lista y actualiza los botones."""
        self.__filas_botones.agregar_tags(tags, sobreescribir)
        self.habilitado = True if self.__dataset_seteado else False
        self.actualizar_botones()


    
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
            self.__filas_botones.deshabilitar_botones(False)
            # flag de estado
            self.__habilitado = True
        else: 
            self.__boton_descartar.disabled = True
            self.__boton_nada     .disabled = True
            self.__boton_todos    .disabled = True
            self.__boton_guardar  .disabled = True
            self.__filas_botones.deshabilitar_botones(True)
            # flag de estado
            self.__habilitado = False

    def leer_botones(self, filtrar_repetidos=True)->list[str]:
        """Lee todas las etiquetas habilitadas mediante los botones. Por defecto filtra los repetidos."""
        etiquetas = self.__filas_botones.leer_botones(filtrar_repetidos)
        return etiquetas

    def actualizar_botones(self):
        self.__filas_botones.actualizar_botones()

    def evento_click(self, funcion_etiquetas=None, funcion_grupo=None, funcion_comando=None):
        """Asigna una funcion para el click de todos los botones, segun sean de etiquetas o de grupos"""
        # self.funcion_comando = funcion_comando if funcion_comando!=None e
        self.__filas_botones.evento_click(funcion_etiquetas, funcion_grupo)
        if funcion_comando!=None:
            self.click_botones = funcion_comando


    def mostrar_tag(self, clave: str, duracion = 1000):
        """Mueve el scroll para mostrar el primer boton de etiquetado con la clave indicada."""
        self.__filas_botones.mostrar_tag(clave, duracion)
        self.__filas_botones.update()
        # self.scroll_to(key=clave)


########### FUNCIONES TEST #####################

def funcion_etiqueta(e: ft.ControlEvent):
    boton = e.control
    valor = boton.text
    print( "[bold green]Etiqueta afectada!")
    print(f"[bold blue]Valor etiqueta: [bold yellow]{valor}")


def funcion_comando(e: ft.ControlEvent):
    boton = e.control
    valor = boton.text
    print( "[bold magenta]Comando activado!")
    print(f"[bold blue]Comando: [bold yellow]{valor} [bold blue]activado!")


def funcion_grupos(e: ft.ControlEvent):
    boton = e.control
    valor = boton.data
    print( "[bold cyan]Grupo afectado!")
    print(f"[bold blue]Indice grupo: [bold yellow]{valor}")


################## FUNCION PRINCIPAL ####################

def main(page: ft.Page):

    archivo_dataset = "demo/dataset.png"
    archivo_etiquetas = "demo/etiquetas_imagen.jpg"


    print( "[bold green]        DEMO ETIQUETADOR        ")
    print()
    print("[bold blue]Este archivo simula las operaciones de etiquetado de una imagen.")
    print("[bold blue]Los archivos del demo están incluidos en la carpeta 'demo'.")
    print(f"[bold cyan] Archivo dataset: [bold yellow]{archivo_dataset} ")
    print(f"[bold cyan] Archivo salida : [bold yellow]{archivo_etiquetas} ")

    # Recordar: se ignora la extension del archivo de etiqueta
    # éste siempre es TXT

    # componente etiquetador
    etiquetador = EtiquetadorBotones()

    page.add( etiquetador)

    dataset     = Etiquetas(archivo_dataset) 
    etiquetas   = Etiquetas(archivo_etiquetas) 

    # dataset = Etiquetas()   # borrado forzoso

    etiquetador.altura = 800
    etiquetador.base = 700
    # carga de archivos (sentido inverso)
    etiquetador.setear_salida( etiquetas )      # carga el estado de los botones desde archivo
    etiquetador.leer_dataset(   dataset   )     # crea los botones de etiquetado

    # configuracion de eventos ante el click sobre los botones
    etiquetador.evento_click(funcion_etiqueta, funcion_grupos, funcion_comando)

    # reporte de etiquetas almacenadas
    leido = etiquetador.leer_botones()
    print("[cyan]Etiquetas leidas")
    print(leido)


    page.title = "Botones etiquetado"
    page.window_height      = 800
    page.window_min_height  = 800
    page.window_width       = 650
    page.update()


    # cambios con delay
    import time 
    time.sleep(2)
    # etiquetas agregadas desde el programa
    nuevos_tags = ["3","4","5","6", "Aquiles Brinco"] 
    etiquetador.agregar_tags(nuevos_tags, False)

    # reporte de etiquetas almacenadas
    leido = etiquetador.leer_botones()
    print("[cyan]Tags agregados - etiquetas leidas")
    print(leido)
    etiquetador.mostrar_tag("6")


    time.sleep(2)
    # etiquetas agregadas desde el programa
    nuevos_tags = ["3","4","5","6", "15","Aquiles Brinco"] 
    etiquetador.agregar_tags(nuevos_tags, True)


    # reporte de etiquetas almacenadas
    leido = etiquetador.leer_botones()
    print("[cyan]Sobreescritura de tags - etiquetas leidas")
    print(leido)
    etiquetador.mostrar_tag("fuente")

    time.sleep(2)
    etiquetador.mostrar_tag("6")

    def redimensionar_botonera(e):

        etiquetador.base   = page.width
        etiquetador.altura = page.height
        etiquetador.update()

    page.on_resize = redimensionar_botonera


    page.title = "Botones etiquetado"
    page.window_height      = 800
    page.window_min_height  = 800
    page.window_width       = 650
    page.update()


################## EJECUCION ###################

if __name__ == "__main__":
    ft.app(target=main)