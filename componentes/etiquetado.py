from copy import copy
import flet as ft

from . procesar_etiquetas import Etiquetas 
# from componentes.procesar_etiquetas import Etiquetas 

# class Columna_Etiquetas(ft.UserControl):
class Columna_Etiquetas(ft.Column):
    # def build(self):
    def __init__(self):
        
        self.checkboxes = []
        self.checkboxes_grafica= []

        self.etiquetas_dataset = Etiquetas("")
        self.etiquetas_imagen  = Etiquetas("")

        self.color_separador = ft.colors.INDIGO_200
        self.color_borde = ft.colors.INDIGO_400

        self.ancho = 450
        self.ancho_boton=130

        # cuadro de texto de salida
        self.texto = ft.Text(
            size=15,
            width=self.ancho, 
            height=100, 
            bgcolor=ft.colors.AMBER_100, 
            value="", 
            expand = False 
            )

        self.fila_texto=ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [self.texto] ,
            width=self.ancho, # anchura de columna   
            alignment= ft.MainAxisAlignment.CENTER, 
            )
        # botones de comando
        self.boton_guardado = ft.ElevatedButton(
            text = "Guardar", 
            on_click = self.guardar_opciones, 
            bgcolor="red",color="white", width=self.ancho_boton,
            )
        self.boton_todos = ft.ElevatedButton(
            text = "Todos", 
            on_click = self.checkboxes_todos,
            width=self.ancho_boton,
            )
        self.boton_ninguno = ft.ElevatedButton(
            text = "Ninguno", 
            on_click = self.checkboxes_ninguno,
            width=self.ancho_boton,
            )
        self.boton_restablecer = ft.ElevatedButton(
            text = "Restablecer", 
            on_click = self.restablecer_opciones, 
            bgcolor="blue",color="white", width=self.ancho_boton,
            )

        self.fila_botones_checkboxes = ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [ self.boton_todos, self.boton_ninguno],
            width=self.ancho, # anchura de columna   
            alignment= ft.MainAxisAlignment.CENTER,
            )

        self.fila_boton_restablecer = ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [self.boton_restablecer, self.boton_guardado],
            width=self.ancho, # anchura de columna   
            alignment= ft.MainAxisAlignment.CENTER,
            )

        # Columna de checkboxes
        self.columna_checkboxes = ft.Column(
            wrap=False,
            spacing=10,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            # controls=self.checkboxes_grafica,
            controls=self.checkboxes,
            height=600,         # altura de columna
            width=self.ancho,
            scroll=ft.ScrollMode.AUTO,
            )

        #contenedor de checkboxes (decorativo)
        self.contenedor_checkboxes = ft.Container(
            margin=10,
            padding=10,
            width   = self.ancho,
            height  = 600,
            content = self.columna_checkboxes,
            alignment=ft.alignment.center,
            # bgcolor=ft.colors.AMBER,
            border_radius=20,           # redondeo
            animate=ft.animation.Animation(
                200, 
                "bounceOut"
                ),
            border = ft.border.all(5, self.color_borde)
            )

        elementos_etiquetado=[]

        elementos_etiquetado.append(self.fila_texto)
        elementos_etiquetado.append(self.contenedor_checkboxes)
        elementos_etiquetado.append(self.fila_botones_checkboxes)
        elementos_etiquetado.append(self.fila_boton_restablecer)

        super().__init__(
            wrap=False,
            spacing=10,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = elementos_etiquetado, 
            width=self.ancho # anchura de columna   
        )



    def guardar_opciones(self, e):
        etiquetas_checkboxes=[]
        lista_checkboxes = self.checkboxes
        for checkbox  in lista_checkboxes:
            etiqueta = checkbox.label
            valor    = checkbox.value
            if valor:
                etiquetas_checkboxes.append(etiqueta)
        # relectura de etiquetas para prevenir relecturas inutiles
        self.etiquetas_imagen.leer()    
        # print("postlectura: ", self.etiquetas_imagen.ruta)
        if set(self.etiquetas_imagen.tags) != set(etiquetas_checkboxes): 
            self.texto.value = "Cambios guardados"
            # archivo creado / reescrito
            self.etiquetas_imagen.tags = etiquetas_checkboxes
            if self.etiquetas_imagen.guardar()==False:
                self.texto.value = " Error: guardado fallido"
        else:
            self.texto.value = "Sin cambios"
        self.update()

    def checkboxes_ninguno(self, e):
        # lista_checkboxes = self.checkboxes
        for checkbox  in self.checkboxes:
            checkbox.value = False
        self.texto.value = "Nada"
        self.update()

    def checkboxes_todos(self, e):
        for checkbox  in self.checkboxes:
            checkbox.value = True
            checkbox.update()
        self.texto.value = "Todo"
        self.update()

    def restablecer_opciones(self, e):
        # lista_checkboxes = self.checkboxes
        for checkbox  in self.checkboxes:
            etiqueta = checkbox.label
            if  etiqueta in self.etiquetas_imagen.tags :
                checkbox.value = True
            else:
                checkbox.value = False
        self.texto.value = "Valores reestablecidos"
        self.update()


    def crearCheckboxes(self):
        for etiqueta  in self.etiquetas_dataset.tags:
            selector = ft.Switch(label=f"{etiqueta}",value=False)
            if  etiqueta in self.etiquetas_imagen.tags:
                selector.value=True  
            self.checkboxes.append(selector) 

        # self.checkboxes_grafica= lista_checkboxes_grafica
        self.update()


    # def setDataset(self, etiquetas_dataset):
    def setEtiquetas(self, etiquetas_imagen, etiquetas_dataset=None):
        if type(etiquetas_dataset) == Etiquetas:
            self.etiquetas_dataset = etiquetas_dataset
            self.crearCheckboxes()
            
        mensaje="Etiquetado:\n" if len(self.checkboxes) > 0 else "Sin Dataset"
        self.texto.value = mensaje

        self.etiquetas_imagen = etiquetas_imagen
        ruta  = self.etiquetas_imagen.ruta
        # valor = self.texto.value 
        self.texto.value =f"{mensaje}{ruta}"
        # self.texto.value = f"ruta: {ruta}"  
        # print("SET - imagen: ",self.etiquetas_imagen.tags)    
        # print("ACTUALIZAR AQUI -->setImagen")
        self.actualizar()

    def actualizar(self):
        for checkbox in self.checkboxes:
            tag = checkbox.label
            if tag in self.etiquetas_imagen.tags:
                checkbox.value = True
            else:
                checkbox.value = False
        self.update()


# Tema aplicado globalmente
def tema_pagina(pagina: ft.Page):
    pagina.theme = ft.Theme(
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
        )
    )


def pagina_etiquetado(page: ft.Page ):

    # Procesado de archivos
    archivo_dataset = "demo_etiquetas.txt"
    archivo_salida = "etiquetas_salida.txt"      
    etiquetas_dataset = Etiquetas(archivo_dataset)
    etiquetas_imagen = Etiquetas(archivo_salida)


    # print("dataset: ",etiquetas_dataset.tags)
    # print("imagen: ",etiquetas_imagen.tags)

    ## Maquetado
    columna_tageo = Columna_Etiquetas( )
    page.add(columna_tageo)


    # columna_tageo.setDataset(etiquetas_dataset)
    # columna_tageo.setImagen(  etiquetas_imagen)
    columna_tageo.setEtiquetas(etiquetas_imagen, etiquetas_dataset)


    # columna_tageo.actualizar()
    # columna_tageo.crearCheckboxes()


    # page.add(columna_tageo.columna_checkboxes)
    page.update()



    # Estilos 
    tema_pagina(page)
    # Propiedades pagina 
    page.title = "Ventana Etiquetado Imágenes"
    page.window_width=450
    page.window_height = 1000
    page.window_maximizable=True
    page.window_minimizable=True
    page.window_maximized=False
    
    page.update()



# Llamado al programa y su frontend
if __name__ == "__main__":
    mensaje = ft.app(target=pagina_etiquetado)



