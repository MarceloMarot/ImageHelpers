import flet as ft


class AnilloReporte(ft.Row):
    def __init__(self):
        self.altura = 150
        self.dim_anillo = 100
        self.ancho_filas = 600
        self.anillo_progreso = ft.ProgressRing(
            width = self.dim_anillo , 
            height = self.dim_anillo , 
            stroke_width = 10 ,
            color=ft.colors.GREY_300,
            value = 1,          # valor inicial
            # value = None,          # tiempo indefinido
            )
        self.reporte = []
        ancho_reporte = self.ancho_filas - self.altura*1.5
        for _ in range(5):
            self.reporte.append( 
                    ft.Text(
                    value="", 
                    # height=25, 
                    width = ancho_reporte , 
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.START,
                    )
                )
        self.columna_anillo = ft.Column(
            controls = [self.anillo_progreso],
            height = self.altura,
            width = self.altura * 1.5, 
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.columna_reporte = ft.Column(
            controls = self.reporte,
            height = self.altura,
            width = ancho_reporte, 
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(               
            controls = [self.columna_anillo, self.columna_reporte],
            expand = False,
            width  = self.ancho_filas, 
            height = self.altura,
            alignment= ft.MainAxisAlignment.CENTER, 
            )


    def borrar_reporte(self):
        for i in range(len(self.reporte)):
            self.reporte[i].value =""
        self.update()


    def texto_reporte(self, renglon1 ="", renglon2="", renglon3="", renglon4="", renglon5=""):
        self.reporte[0].value = renglon1
        self.reporte[1].value = renglon2
        self.reporte[2].value = renglon3
        self.reporte[3].value = renglon4
        self.reporte[4].value = renglon5
        self.update()

    @property
    def color_anillo(self):
        return self.anillo_progreso.color

    @color_anillo.setter
    def color_anillo(self, color):
        self.anillo_progreso.color = color
        self.anillo_progreso.update()

    @property
    def valor_anillo(self):
        return self.anillo_progreso.value

    @valor_anillo.setter
    def valor_anillo(self, valor = None):
        self.anillo_progreso.value = valor
        self.anillo_progreso.update()