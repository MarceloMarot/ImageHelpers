


import cv2
import numpy as np
import flet as ft
import pathlib
import time
import json

from typing import IO

from sistema_archivos.archivos_temporales import  crear_directorio_temporal
from sistema_archivos.imagen_temporal import crear_imagen_temporal
from sistema_archivos.imagen_editable import ImagenEditable

from componentes.galeria_imagenes import Contenedor , Contenedor_Imagen


def nada(x):
    pass


class DataRecorte():
    """Estructura auxiliar para los datos de recortes."""
    def __init__(self):
        self.coordenadas_absolutas: list[int] = [0,0,0,0]
        self.coordenadas_relativas: list[float] = [0,0,0,0]
        self.escala: int = 100

    def leer(self, data):
        """Lee los datos desde otra estructura 'DataRecorte' """
        self.coordenadas_absolutas  = data.coordenadas_absolutas
        self.coordenadas_relativas  = data.coordenadas_relativas
        self.escala                 = data.escala


class ImagenesTemporalesSelector:
    """Crea los archivos temporales de seleccion, recorte, etc de la imagen de entrada."""
    def __init__( self, nombre_directorio="recortador" ):
        self.clave : str = "---"

        self.data_actual = DataRecorte()
        self.data_marcado = DataRecorte()
        self.data_guardado = DataRecorte()

        self.__xy_relativo  : list[float] = [0.0, 0.0]
        self.__xy_original  : list[int] = [0, 0]
        self.__xy_escalada  : list[int] = [0, 0]
        self.__xy_seleccion : list[int] = [0, 0]

        self.__imagen_original  : None | np.ndarray
        self.__imagen_escalada  : None | np.ndarray
        self.__imagen_recorte   : None | np.ndarray
        self.__imagen_seleccion : None | np.ndarray
        self.__imagen_miniatura : None | np.ndarray

        self.__escala_actual    : int = 100
        self.incremento_escala  : int = 1

        self.BGR_seleccion = (200,0,150)  # magenta
        self.BGR_marcado   = (0,200,200)  # amarillo
        self.BGR_guardado  = (100,150,0)  # verde oscuro
        self.BGR_error     = (0,50,200)  # vermellon

        self.brillo_ventana: int = 100
        self.contraste_ventana: float = 0.5 

        # ruta RAM habitual en Linux
        ruta = "/dev/shm/"
        if pathlib.Path(ruta).exists():
            ruta_temporal = ruta
        # ruta TEMP designada por sistema operativo ( en disco rigido)
        else:
            ruta_temporal = None        

        self.carpeta_temporal = crear_directorio_temporal(nombre_directorio, ruta_temporal)

        self.temporal_original = ImagenEditable(self.carpeta_temporal.name)
        self.temporal_escalada  = ImagenEditable(self.carpeta_temporal.name)
        self.temporal_recorte   = ImagenEditable(self.carpeta_temporal.name)
        self.temporal_miniatura = ImagenEditable(self.carpeta_temporal.name)
        self.temporal_seleccion = ImagenEditable(self.carpeta_temporal.name)

    #COORDENADAS
    @property
    def xy_original(self)->list[int]:
        return self.__xy_original


    @property
    def xy_escalada(self)->list[int]:
        return self.__xy_escalada


    @property
    def xy_seleccion(self)->list[int]:
        return self.__xy_seleccion


    @property
    def xy_relativo(self)->list[float]:
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


    @property
    def ruta_original(self) -> str:
        return self.temporal_original.ruta


    @property
    def ruta_escalada(self) -> str:
        return self.temporal_escalada.ruta
    

    @property
    def ruta_recorte(self) -> str:
        return self.temporal_recorte.ruta
    

    @property
    def ruta_seleccion(self) -> str:
        return self.temporal_seleccion.ruta


    @property
    def ruta_miniatura(self) -> str:
        return self.temporal_miniatura.ruta


    def cerrar(self):
        """Elimina la carpeta temporal y sus archivos internos"""
        # borrado de todas las imagenes temporales
        self.temporal_original.cerrar()
        self.temporal_escalada.cerrar()
        self.temporal_recorte.cerrar()
        self.temporal_seleccion.cerrar()
        self.temporal_miniatura.cerrar()
        # borrado carpeta
        self.carpeta_temporal.cleanup()




    def abrir_imagen(self,ruta_archivo: str ):
        """Carga de los archivos temporales y su primera version"""
        # copia temporal desde archivo fisico
        self.temporal_original.subir(ruta_archivo)
        # # copias hechas desde el archivo temporal
        self.temporal_escalada .subir(ruta_archivo)
        self.temporal_recorte  .subir(ruta_archivo)
        self.temporal_miniatura.subir(ruta_archivo)
        self.temporal_seleccion.subir(ruta_archivo)
        # # objetos matriciales de OpenCV representando las imagenes    
        self.__imagen_original  = cv2.imread(self.ruta_original)
        self.__imagen_escalada  = cv2.imread(self.ruta_original)
        self.__imagen_recorte   = cv2.imread(self.ruta_original)
        self.__imagen_miniatura = cv2.imread(self.ruta_original)
        self.__imagen_seleccion = cv2.imread(self.ruta_original)


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


    def escalar(self, escala: int|None = None):
        """Crea una copia ampliada de la imagen de entrada en base al porcentaje indicado."""
        [base, altura] = self.dimensiones_original
        if escala == None:
            proporcion = self.__escala_actual/100
        else:
            self.__escala_actual = escala
            proporcion = escala/100
        altura = int(altura * proporcion)
        base = int(base * proporcion)

        self.__imagen_escalada = cv2.resize(
            src=self.__imagen_original, 
            dsize=(base, altura), 
            interpolation=cv2.INTER_LANCZOS4,
            ) 
        # archivo sustituto   
        self.temporal_escalada.crear(self.__imagen_escalada)
        if escala != None:
            self.data_actual.escala = escala


    @property
    def escala_actual(self)->int:
        return self.__escala_actual


    def cambiar_brillo(self, brillo, contraste):

        self.__imagen_seleccion = cv2.convertScaleAbs(self.__imagen_original, alpha=contraste, beta=brillo)
        # archivo sustituto
        # actualizacion datos
        self.temporal_seleccion.subir(self.__imagen_seleccion)


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
        self.data_marcado.leer(self.data_actual)

        [xi, yi, xf, yf] = self.data_marcado.coordenadas_absolutas
        self.__imagen_recorte  = self.__imagen_escalada[yi:yf, xi:xf]
        # archivo sustituto     
        self.temporal_recorte.crear(self.__imagen_recorte)


    def hacer_recorte_definitivo(self):
        self.data_guardado.leer(self.data_actual)

        # borrado del marcado antiguo
        self.data_marcado.coordenadas_absolutas = [0, 0, 0, 0]
        self.data_marcado.coordenadas_relativas = [0, 0, 0, 0]
        self.data_marcado.escala                = self.data_actual.escala
        [xi, yi, xf, yf] = self.data_guardado.coordenadas_absolutas
        self.__imagen_recorte  = self.__imagen_escalada[yi:yf, xi:xf]
        # archivo sustituto     
        self.temporal_recorte.crear(self.__imagen_recorte)


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
        self.temporal_seleccion.crear(self.__imagen_seleccion)


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

        dimensiones = ( altura, base)
        self.__imagen_miniatura = cv2.resize(
            self.__imagen_original, 
            dsize=dimensiones, 
            interpolation = cv2.INTER_LANCZOS4
            ) 
        # archivo sustituto   
        self.temporal_miniatura.crear(self.__imagen_miniatura)


    def guardar_recorte_archivo(self, ruta_destino: str ):
        cv2.imwrite(ruta_destino, self.__imagen_recorte)



class SelectorRecorte(ft.GestureDetector):
    def __init__(self, carpeta_temporal: str ="ensayo_"):
        # Componentes graficos
        self.imagen = ft.Image(
            height=512,
            width=512,
            fit = ft.ImageFit.CONTAIN,
            gapless_playback = True,        # transicion suave entre imagenes (retiene la version anterior hasta poder cambiar)
            )

        self.contenedor = Contenedor( ancho=512, alto=512 )
        self.contenedor.content = self.imagen
        self.contenedor.padding = 0
        self.contenedor.margin = 0
        self.contenedor.border=ft.border.all(0, ft.colors.BLACK12)
        self.contenedor.image_fit = ft.ImageFit.CONTAIN

        super().__init__(
            height=512,
            width=512,
            content = self.contenedor,
            on_tap  = self.click_izquierdo,
            on_secondary_tap = self.click_derecho,
            on_hover = self.coordenadas,
            on_scroll= self.scrollear_mouse,
            hover_interval = 100,  # retardo minimo entre eventos 
            drag_interval  = 100,  # retardo minimo entre eventos 
            ) 
        self.dimensiones_recorte = [256, 256]  
        self.temporal = ImagenesTemporalesSelector(carpeta_temporal) 
        self.funcion_click_izquierdo    = nada
        self.funcion_click_derecho      = nada
        self.funcion_scroll_mouse       = nada



    def abrir_imagen(self, ruta_archivo: str):
        self.temporal.abrir_imagen(ruta_archivo)
        self.imagen.src = self.temporal.ruta_miniatura
        self.update()


    def escalar(self, porcentaje: int):
        """Amplia o reduce el archivo de imagen en base al factor de escala indicado"""
        # copia de coordenadas relativas del punto central de seleccion actual
        xy = self.xy_relativo
        # ampliacion de imagen
        self.temporal.escalar(int(porcentaje))
        # reestablecimiento de punto central de seleccion
        self.xy_relativo = xy 
        # actualizacion grafica con la seleccion actual
        self.coordenadas()

    @property
    def escala_actual(self)->int:
        return self.temporal.escala_actual

    @property
    def incremento_escala(self)->int:
        return self.temporal.incremento_escala

    @incremento_escala.setter
    def incremento_escala(self, valor: int):
        self.temporal.incremento_escala = valor

    def scrollear_mouse(self, e: ft.ScrollEvent):
        """cambio de zoom de imagen basado en el deslizamiento de la rueda del mouse """
        # lectura de datos y conversion a diccionario
        texto_diccionario = e.data
        data = json.loads(texto_diccionario)
        # lectura de numero deslizamiento vertical
        valor = int(data["dy"])  
        escala = self.escala_actual
        if valor < 0:
            # deslizamiento abajo -> reducir
            escala -= self.incremento_escala
            self.escalar(escala)
        else:
            # deslizamiento abajo -> ampliar
            escala += self.incremento_escala
            self.escalar(escala)

        # funcion opcional externa
        self.funcion_scroll_mouse(e)


    def coordenadas(self, e: ft.ControlEvent | None = None):
        """Lee las coordenadas del puntero del mouse, calcula el rectangulo de seleccion y actualiza la miniatura de la imagen."""
        # coordenadas relativas al contenedor
        base   = int(self.contenedor.width)
        altura = int(self.contenedor.height)
        # confinamiento de las coordenadas obtenidas 
        if e!=None:
            x = e.local_x if e.local_x < base else base
            y = e.local_y if e.local_y < altura else altura
            x = 0 if x <= 0 else x
            y = 0 if y <= 0 else y
            # conversion a valor relativo
            x = x / base
            y = y / altura
            self.temporal.xy_relativo = [x, y]

        self.temporal.calcular_recorte(self.dimensiones_recorte)
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


    @property
    def ruta_recorte(self):
        return self.temporal.ruta_recorte

    def hacer_recorte_preliminar(self):
        self.temporal.hacer_recorte_preliminar()

    def hacer_recorte_definitivo(self):
        self.temporal.hacer_recorte_definitivo()


    def cerrar(self):
        """Elimina la carpeta temporal y sus archivos internos"""
        self.temporal.cerrar()
        # self.temporal.carpeta_temporal.cleanup()


    @property
    def xy_relativo(self)->list[float]:
        return self.temporal.xy_relativo


    @xy_relativo.setter
    def xy_relativo(self, xy: list[float]):
        self.temporal.xy_relativo = xy


def principal(page: ft.Page):

    def click_izquierdo(e):
        selector_recorte.hacer_recorte_preliminar()
        imagen_miniatura.src = selector_recorte.ruta_recorte
        imagen_miniatura.visible=True
        imagen_miniatura.update()
        print(f"dimensiones marcado: {selector_recorte.dimensiones_recorte}")


    def click_derecho(e):
        selector_recorte.hacer_recorte_definitivo()
        imagen_miniatura.src = selector_recorte.ruta_recorte
        imagen_miniatura.visible=True
        imagen_miniatura.update()
        print(f"dimensiones guardado: {selector_recorte.dimensiones_recorte}")
 

    def escalar(e):
        valor = e.control.value
        selector_recorte.escalar(int(valor))


    def actualizar_barra(e):
        # actualizacion grafica de la barra deslizante
        barra_escala.value = selector_recorte.escala_actual
        barra_escala.update()


    def cierre(e:ft.ControlEvent):
        if e.data=="close":
            page.window_destroy()
            time.sleep(0.5)
            selector_recorte.cerrar()



    barra_escala = ft.Slider(
        min=30, 
        max=330, 
        divisions=300,
        value=100, 
        label="{value}", 
        width=512
        )
    barra_escala.on_change = escalar

    selector_recorte = SelectorRecorte("selector_recortes__")

    imagen_miniatura = ft.Image(
        height=256,
        width=256,
        visible=False,
    )

    fila = ft.Row(
        [selector_recorte,
        imagen_miniatura,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,

    )

    page.add(fila)
    page.add(ft.Row(
        [barra_escala],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        ))

    page.window_height = 700
    fila.height = 400
    page.window_width  = 1000
    fila.width  = 1000
    page.theme_mode = ft.ThemeMode.DARK
    page.on_window_event = cierre
    page.window_prevent_close = True
    page.update()

    selector_recorte.abrir_imagen(ruta_archivo)

    selector_recorte.dimensiones_graficas(0.5)
    selector_recorte.dimensiones_recorte = [512, 512]
    selector_recorte.funcion_click_izquierdo = click_izquierdo
    selector_recorte.funcion_click_derecho = click_derecho
    selector_recorte.funcion_scroll_mouse = actualizar_barra


    time.sleep(0.5)
    selector_recorte.xy_relativo = [0.5, 0.5]
    selector_recorte.coordenadas()
    click_izquierdo("")


    page.update()


if __name__ == "__main__":

    import sys
    if len(sys.argv) == 2:
        ruta_archivo = sys.argv[1]
        ft.app(target=principal)

    else:
        print('uso programa: py -m componentes.selector_recortes  "ruta_archivo" ')

