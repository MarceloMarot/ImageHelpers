


import cv2
import numpy as np
# import tempfile
import flet as ft
import pathlib
import time

from typing import IO
# from copy import deepcopy

from sistema_archivos.archivos_temporales import  crear_directorio_temporal
from sistema_archivos.imagen_temporal import crear_imagen_temporal


def nada(x):
    pass


class DataRecorte():
    def __init__(self):
        self.coordenadas_absolutas: list[int] = [0,0,0,0]
        self.coordenadas_relativas: list[float] = [0,0,0,0]
        self.escala: int = 100
        # self.dimensiones: list[int]


class ImagenTemporal:
    def __init__( self, nombre_directorio="recortador" ):
        self.clave : str = "---"

        self.data_actual = DataRecorte()
        self.data_marcado = DataRecorte()
        self.data_guardado = DataRecorte()

        self.__xy_relativo  = [0, 0]
        self.__xy_original  = [0, 0]
        self.__xy_escalada  = [0, 0]
        self.__xy_seleccion = [0, 0]

        self.__imagen_original = None | np.ndarray
        self.__imagen_escalada = None | np.ndarray
        self.__imagen_recorte = None | np.ndarray
        self.__imagen_seleccion = None | np.ndarray
        self.__imagen_miniatura = None | np.ndarray


        self.BGR_seleccion = (200,0,150)  # magenta
        self.BGR_marcado   = (0,200,200)  # amarillo
        self.BGR_guardado  = (100,150,0)  # verde oscuro
        self.BGR_error     = (0,50,200)  # vermellon
        # flags de estado 
        # self.__recorte_guardado : bool = False
        # self.__recorte_marcado  : bool = False
        # auxiliares

        self.brillo_ventana: int = 100
        self.contraste_ventana: float = 0.5 

        self.carpeta_temporal = crear_directorio_temporal(nombre_directorio)

        self.temporal_original : IO
        self.temporal_escalada : IO
        self.temporal_recorte  : IO
        self.temporal_seleccion  : IO


    #COORDENADAS
    @property
    def xy_original(self):
        return self.__xy_original

    @property
    def xy_escalada(self):
        return self.__xy_escalada

    @property
    def xy_seleccion(self):
        return self.__xy_seleccion

    @property
    def xy_relativo(self):
        return self.__xy_relativo

    @xy_relativo.setter
    def xy_relativo(self, xy: list[float]):
        """Asigna coordenadas a todas las imagenes"""
        # coordenadas relativas
        [x, y] = xy
        self.__xy_relativo = xy
        # actualizacion solidaria de las coordenadas de todas las imagenes
        (b, h) = self.dimensiones_original
        self.__xy_original = [int(b*x), int(h*y)]
        (b, h) = self.dimensiones_escalada
        self.__xy_escalada = [int(b*x), int(h*y)]
        (b, h) = self.dimensiones_seleccion
        self.__xy_seleccion = [int(b*x), int(h*y)]

    # DIMENSIONES
    @property
    def ruta_original(self) -> str:
        return self.temporal_original.name

    @property
    def ruta_escalada(self) -> str:
        return self.temporal_escalada.name
    
    @property
    def ruta_recorte(self) -> str:
        return self.temporal_recorte.name
    
    @property
    def ruta_seleccion(self) -> str:
        return self.temporal_seleccion.name

    @property
    def ruta_miniatura(self) -> str:
        return self.temporal_miniatura.name

    def cerrar(self):
        """Elimina la carpeta temporal y sus archivos internos"""
        self.carpeta_temporal.cleanup()


    def abrir_imagen(self,ruta_archivo: str ):
        """Carga de los archivos temporales y su primera version"""
        # copia temporal desde archivo fisico
        self.temporal_original = crear_imagen_temporal(ruta_archivo, self.carpeta_temporal)
        # copias hechas desde el archivo temporal
        self.temporal_escalada  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        self.temporal_recorte   = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        self.temporal_miniatura = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        self.temporal_seleccion = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        # # objetos matriciales de OpenCV representando las imagenes    
        self.__imagen_original  = cv2.imread(self.ruta_original)
        self.__imagen_escalada  = cv2.imread(self.ruta_original)
        self.__imagen_recorte   = cv2.imread(self.ruta_original)
        self.__imagen_miniatura = cv2.imread(self.ruta_original)
        self.__imagen_seleccion = cv2.imread(self.ruta_original)
        # self.__escala_actual = 100

    @property
    def dimensiones_original(self):
        (h, b, _) = self.__imagen_original.shape 
        return [b, h]

    @property
    def dimensiones_escalada(self):
        (h, b, _) = self.__imagen_escalada.shape 
        return [b, h]

    @property
    def dimensiones_recorte(self):
        (h, b, _) = self.__imagen_recorte.shape  
        return [b, h]

    @property
    def dimensiones_miniatura(self):
        (h, b, _) = self.__imagen_miniatura.shape  
        return [b, h]

    @property
    def dimensiones_seleccion(self):
        (h, b, _) = self.__imagen_seleccion.shape
        return [b, h]


    def ampliar(self, escala: int|None = None):
        """Crea una copia ampliada de la imagen de entrada en base al porcentaje indicado."""
        [base, altura] = self.dimensiones_original
        if escala == None:
            proporcion = self.__escala_actual/100
        else:
            self.__escala_actual = escala
            proporcion = escala/100
        altura = int(altura * proporcion)
        base = int(base * proporcion)
        # print(f"dimensiones ampliacion: [{base}, {altura}], escala: {escala}")
        self.__imagen_escalada = cv2.resize(
            self.__imagen_original, 
            dsize=[base, altura], 
            interpolation = cv2.INTER_LANCZOS4
            ) 
        # archivo sustituto   
        if pathlib.Path(self.ruta_escalada).exists():
            self.temporal_escalada.close()
        self.temporal_escalada = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_escalada, self.__imagen_escalada)
        if escala != None:
            self.data_actual.escala = escala


    def cambiar_brillo(self, brillo, contraste):
        # orig = cv2.imread(imagen_temporal_original.name)
        self.__imagen_seleccion = cv2.convertScaleAbs(self.__imagen_original, alpha=contraste, beta=brillo)
        # archivo sustituto
        self.temporal_seleccion = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        # actualizacion datos
        cv2.imwrite(self.ruta_seleccion, self.__imagen_seleccion)


    def calcular_recorte(self, dimensiones_recorte):  
        """Funcion creada para calcular el rectángulo de seleccion de modo de evitar desbordes"""
        # lectura de dimensiones
        [base_recorte, altura_recorte] = dimensiones_recorte
        [x_max, y_max] = self.dimensiones_escalada
        [x, y]= self.xy_escalada
        #Se previenen errores por recortes mayores a la imagen de origen
        if base_recorte > x_max : base_recorte = x_max
        if altura_recorte > y_max : altura_recorte  = y_max  
        # El puntero del mouse quedará centrado dentro del rectángulo
        xi = x - base_recorte // 2
        yi = y - altura_recorte // 2
        # Se confina al rectángulo adentro de la imagen
        xi = 0 if xi < 0 else xi 
        yi = 0 if yi < 0 else yi 
        xf = xi + base_recorte
        yf = yi + altura_recorte
        if xf >= x_max :
            xf = x_max
            xi = x_max - base_recorte
        if yf >= y_max :
            yf = y_max 
            yi = y_max - altura_recorte
        # creacion del recorte de imagen
        #retorno del recorte y sus coordenadas en una lista
        self.data_actual.coordenadas_absolutas = [xi, yi, xf, yf]
        self.data_actual.coordenadas_relativas = [xi/x_max, yi/y_max, xf/x_max, yf/y_max]


    def hacer_recorte_preliminar(self):
        self.data_marcado.coordenadas_absolutas = self.data_actual.coordenadas_absolutas
        self.data_marcado.coordenadas_relativas = self.data_actual.coordenadas_relativas
        self.data_marcado.escala                = self.data_actual.escala

        [xi, yi, xf, yf] = self.data_marcado.coordenadas_absolutas
        self.__imagen_recorte  = self.__imagen_escalada[yi:yf, xi:xf]
        # archivo sustituto   
        if pathlib.Path(self.ruta_recorte).exists():
            self.temporal_recorte.close()
        self.temporal_recorte  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_recorte, self.__imagen_recorte)


    def hacer_recorte_definitivo(self):
        self.data_guardado.coordenadas_absolutas = self.data_actual.coordenadas_absolutas
        self.data_guardado.coordenadas_relativas = self.data_actual.coordenadas_relativas
        self.data_guardado.escala                = self.data_actual.escala
        # borrado del marcado antiguo
        self.data_marcado.coordenadas_absolutas = [0, 0, 0, 0]
        self.data_marcado.coordenadas_relativas = [0, 0, 0, 0]
        self.data_marcado.escala                = self.data_actual.escala
        [xi, yi, xf, yf] = self.data_guardado.coordenadas_absolutas
        self.__imagen_recorte  = self.__imagen_escalada[yi:yf, xi:xf]
        # archivo sustituto   
        if pathlib.Path(self.ruta_recorte).exists():
            self.temporal_recorte.close()
        self.temporal_recorte  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_recorte, self.__imagen_recorte)


    def marcado_seleccion(self, error=False):
        """función grafica: actualiza la ventana de imagen y le dibuja un rectángulo encima con las coordenadas indicadas"""
        # marcado del rectangulo sobre una copia de la imagen para no dañar la original
        brillo = self.brillo_ventana
        contraste = self.contraste_ventana 
        # copia de salida con brillo y contraste cambiados
        copia = cv2.convertScaleAbs(self.__imagen_miniatura, alpha=contraste, beta=brillo)
        
        [b, h] = self.dimensiones_miniatura

        # regiones brillo original ( se superponen)
        [xif, yif, xff, yff] = self.data_actual.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_miniatura[yi:yf, xi:xf]
        [xif, yif, xff, yff] = self.data_marcado.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_marcado  
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_miniatura[yi:yf, xi:xf]
        [xif, yif, xff, yff] = self.data_guardado.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_guardado  
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_miniatura[yi:yf, xi:xf]
        # Rectángulos color
        [xif, yif, xff, yff] = self.data_actual.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        [xif, yif, xff, yff] = self.data_marcado.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_marcado if self.data_actual.escala==self.data_marcado.escala else self.BGR_error 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        [xif, yif, xff, yff] = self.data_guardado.coordenadas_relativas 
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas 
            color_rectangulo = self.BGR_guardado if self.data_actual.escala==self.data_guardado.escala else self.BGR_error
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )

        self.__imagen_seleccion = copia
        # archivo sustituto   
        if pathlib.Path(self.ruta_seleccion).exists():
            self.temporal_seleccion.close()
        self.temporal_seleccion  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_seleccion, self.__imagen_seleccion)


    def crear_miniatura(self, proporcion: float, base_max: int = 512 , altura_max: int = 512):
        """Crea la imagen miniatura que servira de referencia a la imagen de seleccion."""
        # lectura de parametros entrada
        p = proporcion
        (b, h) = self.dimensiones_original
        # limitacion de dimensiones maximas
        if base_max < int(b*p):
            p = base_max / b 
        if altura_max < int(h*p):
            p = altura_max / h 
        base = int(h * p)
        altura = int(b * p)
        # escala = float(p)

        dimensiones = ( altura, base)
        self.__imagen_miniatura = cv2.resize(
            self.__imagen_original, 
            dsize=dimensiones, 
            interpolation = cv2.INTER_LANCZOS4
            ) 
        # archivo sustituto   
        if pathlib.Path(self.ruta_escalada).exists():
            self.temporal_miniatura.close()
        self.temporal_miniatura = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_miniatura, self.__imagen_miniatura)


    def guardar_recorte_archivo(self, ruta_destino: str ):
        # ruta = pathlib.Path(ruta_destino).absolute
        cv2.imwrite(ruta_destino, self.__imagen_recorte)




class SelectorRecorte(ft.GestureDetector):
    def __init__(self):
        # Componentes graficos
        self.imagen = ft.Image(
            height=512,
            width=512,
            # src = imagen_temporal.ruta_seleccion,
            fit = ft.ImageFit.CONTAIN,
            gapless_playback = True,        # transicion suave entre imagenes (retiene la version anterior hasta poder cambiar)
            )
        self.contenedor = ft.Container(
            height=512,
            width=512,
            content = self.imagen,
            padding=0,
            image_fit = ft.ImageFit.CONTAIN,
            # animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
            )
        super().__init__(
            height=512,
            width=512,
            content = self.contenedor,
            on_tap  = self.click_izquierdo,
            on_secondary_tap = self.click_derecho,
            on_hover = self.coordenadas,
            hover_interval = 50  # retardo minimo entre eventos 
            ) 
        self.dimensiones_recorte = [256, 256]  
        self.temporal : ImagenTemporal  
        self.funcion_click_izquierdo    = nada
        self.funcion_click_derecho      = nada


    def coordenadas(self, e):
        # coordenadas relativas al contenedor
        base   = int(self.contenedor.width)
        altura = int(self.contenedor.height)
        # confinamiento de las coordenadas obtenidas
        x = e.local_x if e.local_x < base else base
        y = e.local_y if e.local_y < altura else altura
        x = 0 if x <= 0 else x
        y = 0 if y <= 0 else y
        # conversion a valor relativo
        x = x / base
        y = y / altura
        self.temporal.xy_relativo = [x, y]
        self.temporal.calcular_recorte(self.dimensiones_recorte)
        # imagen_temporal.calcular_recorte([256,256])
        self.temporal.crear_miniatura(1, base, altura)
        self.temporal.marcado_seleccion()
        self.imagen.src = self.temporal.ruta_seleccion
        self.imagen.update()


    def click_izquierdo(self, e: ft.ControlEvent):
        self.temporal.hacer_recorte_preliminar()
        self.funcion_click_izquierdo(e)


    def click_derecho(self, e: ft.ControlEvent):
        self.temporal.hacer_recorte_definitivo()
        self.funcion_click_derecho(e)


    def dimensiones_graficas(self, proporcion: float, base_max: int = 512 , altura_max: int = 512):
        # lectura de parametros entrada
        p = proporcion
        (b, h) = self.temporal.dimensiones_original
        # limitacion de dimensiones maximas
        if base_max < int(b*p):
            p = base_max / b 
        if altura_max < int(h*p):
            p = altura_max / h 
        self.imagen.height = int(h * p)
        self.imagen.width = int(b * p)
        self.contenedor.height = int(h * p)
        self.contenedor.width = int(b * p)
        self.height = int(h * p)
        self.width = int(b * p)
        self.update()


    def asignar(self, temporal: ImagenTemporal):
        self.temporal   = temporal
        self.imagen.src = temporal.ruta_miniatura



def principal(page: ft.Page):

    def click_izquierdo(e):
        # imagen_temporal.hacer_recorte_preliminar()
        imagen_miniatura.src = imagen_temporal.ruta_recorte
        imagen_miniatura.update()
        print(f"dimensiones marcado: {imagen_temporal.dimensiones_recorte}")


    def click_derecho(e):
        # imagen_temporal.hacer_recorte_definitivo()
        imagen_miniatura.src = imagen_temporal.ruta_recorte
        imagen_miniatura.update()
        print(f"dimensiones guardado: {imagen_temporal.dimensiones_recorte}")
 

    def escalar(e):
        valor = e.control.value
        imagen_temporal.ampliar(int(valor))


    global imagen_temporal
    imagen_temporal = ImagenTemporal("ensayus_")
    imagen_temporal.abrir_imagen(ruta_archivo)

    imagen_miniatura = ft.Image(
        height  = 256,
        width   = 256,
        src = imagen_temporal.ruta_recorte,
        fit = ft.ImageFit.CONTAIN,
        gapless_playback = True,        # transicion suave entre imagenes (retiene la version anterior hasta poder cambiar)
        )

    contenedor_miniatura = ft.Container(
        height = 256,
        width  = 256,
        content = imagen_miniatura,
        padding=0,
        image_fit = ft.ImageFit.CONTAIN,
        # animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
        )

    barra_escala = ft.Slider(
        min=30, 
        max=330, 
        divisions=300,
        value=100, 
        label="{value}", 
        width=512
        )
    barra_escala.on_change = escalar


    selector_recorte = SelectorRecorte()

    fila = ft.Row(
        # [detector_gestos,
        [selector_recorte,
        contenedor_miniatura,
        ]
    )

    page.add(fila)
    page.add(barra_escala)

    selector_recorte.asignar( imagen_temporal)
    # selector_recorte.temporal = imagen_temporal
    # selector_recorte.imagen.src = imagen_temporal.ruta_miniatura
    selector_recorte.dimensiones_graficas(0.5)
    selector_recorte.dimensiones_recorte = [512, 512]
    selector_recorte.funcion_click_izquierdo = click_izquierdo
    selector_recorte.funcion_click_derecho = click_derecho

    # dimensiones_graficas(0.5)
    page.window_height = 700
    page.window_width  = 1000

    page.theme_mode = ft.ThemeMode.DARK
    page.update()



if __name__ == "__main__":

    ruta_archivo = "manejo_imagenes/ejemplo2.jpg"
    # ruta_archivo = "manejo_imagenes/ejemplo.jpg"

    # inicio = time.time()
    # imagen_temporal = ImagenTemporal("ensayus_")
    # imagen_temporal.abrir_imagen(ruta_archivo)
    # fin = time.time()
    # print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")

    ft.app(target=principal)
    
    # elimina la carpeta temporal y sus archivos internos al salir
    global imagen_temporal
    imagen_temporal.cerrar()