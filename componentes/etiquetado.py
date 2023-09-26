from copy import copy
import flet as ft

from procesar_etiquetas import Etiquetas 
# from componentes.procesar_etiquetas import Etiquetas 

class Columna_Etiquetas(ft.UserControl):

    def build(self):
        
        self.checkboxes = []
        self.checkboxes_grafica= []

        self.etiquetas_dataset = Etiquetas("")
        self.etiquetas_imagen  = Etiquetas("")

        self.color_separador = ft.colors.INDIGO_200
        self.color_borde = ft.colors.INDIGO_400

        ancho = 450
        ancho_boton=130

        # cuadro de texto de salida
        self.texto = ft.Text(size=15,width=ancho, height=100, bgcolor=ft.colors.AMBER_100, value="", expand = False )

        fila_texto=ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [self.texto] ,
            width=ancho, # anchura de columna   
            alignment= ft.MainAxisAlignment.CENTER, 
            )
        # botones de comando
        self.boton_guardado = ft.ElevatedButton(
            text = "Guardar", 
            on_click = self.guardar_opciones, 
            bgcolor="red",color="white", width=ancho_boton,
            )
        self.boton_todos = ft.ElevatedButton(
            text = "Todos", 
            on_click = self.checkboxes_todos,
            width=ancho_boton,
            )
        self.boton_ninguno = ft.ElevatedButton(
            text = "Ninguno", 
            on_click = self.checkboxes_ninguno,
            width=ancho_boton,
            )
        self.boton_restablecer = ft.ElevatedButton(
            text = "Restablecer", 
            on_click = self.restablecer_opciones, 
            bgcolor="blue",color="white", width=ancho_boton,
            )

        fila_botones_checkboxes = ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [ self.boton_todos, self.boton_ninguno],
            width=ancho, # anchura de columna   
            alignment= ft.MainAxisAlignment.CENTER,
            )

        fila_boton_restablecer = ft.Row(
            wrap=False,
            spacing=50,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = [self.boton_restablecer, self.boton_guardado],
            width=ancho, # anchura de columna   
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
            width=ancho,
            scroll=ft.ScrollMode.AUTO,
            )

        #contenedor de checkboxes (decorativo)
        self.contenedor_checkboxes = ft.Container(
            margin=10,
            padding=10,
            width   = ancho,
            height  = 600,
            content = self.columna_checkboxes,
            alignment=ft.alignment.center,
            # bgcolor=ft.colors.AMBER,
            border_radius=20,           # redondeo
            animate=ft.animation.Animation(200, "bounceOut"),
            border = ft.border.all(5, self.color_borde)
            )

        elementos_etiquetado=[]
        # elementos_etiquetado.append(texto)
        elementos_etiquetado.append(fila_texto)
        # elementos_etiquetado.append(self.columna_checkboxes)
        # elementos_etiquetado.append(self.checkboxes_grafica)
        elementos_etiquetado.append(self.contenedor_checkboxes)
        elementos_etiquetado.append(fila_botones_checkboxes)
        elementos_etiquetado.append(fila_boton_restablecer)
        # elementos_etiquetado.append(ft.Divider(height=9, thickness=3))

        columna_etiquetado = ft.Column(
            wrap=False,
            spacing=10,       # espaciado horizontal entre contenedores
            run_spacing=50,     # espaciado vertical entre filas
            controls = elementos_etiquetado, 
            width=ancho # anchura de columna   
        )
        return columna_etiquetado


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

        
        # version grafica con divisores (COSMETICA)
        # self.checkboxes_grafica = [] # lista para grafica
        # self.checkboxess_grafica = self.checkboxes.deepcopy()
        # grupo = self.etiquetas_dataset.grupo
        # conjunto_grupos = set( self.etiquetas_dataset.grupo )
        # lista_grupos = list(conjunto_grupos)

        # # Se añaden separadores de grupo de ultimp a primero
        # for i in range(len(grupo)-1, 0 , -1):
        #     if grupo[i-1] != grupo[i]:
        #         k = lista_grupos.pop()   
        #         msg_separador = f"Grupo {k}" 
        #         separador = ft.Text(size=20 ,width=100, height=30,  value=msg_separador, color=self.color_separador )
        #         self.checkboxes_grafica.insert(i, separador )

        # if len(lista_grupos)>0:
        #     k = lista_grupos.pop()  
        #     msg_separador = f"Grupo {k}" 
        #     separador = ft.Text(size=20 ,width=100, height=30,  value=msg_separador, color=self.color_separador )
        #     self.checkboxes_grafica.insert(0, separador )

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
        valor = self.texto.value 
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
    archivo_dataset = "../demo_etiquetas.txt"
    archivo_salida = "../etiquetas_salida.png"      
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



