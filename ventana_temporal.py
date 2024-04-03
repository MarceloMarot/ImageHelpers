


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


class ImagenTemporal:
    def __init__( self, nombre_directorio="recortador" ):
        # self.ruta_imagen_original : str = ""    # valor provisional
        # self.ruta_imagen_recorte  : str = ""    # valor provisional
        self.clave : str = "---"
        # self.__coordenadas_recorte: list[int]
        self.__coordenadas_recorte_actuales:    list[int]
        self.__coordenadas_recorte_relativas:   list[float]
        # self.__coordenadas_guardado: list[int]
        # porcentajes de ampliacion entre grafica y archivo
        # self.__escala_minima: int  
        # self.__escala_maxima: int 
        # self.__escala_actual: int 
        # self.__escala_recorte : int 
        # self.__escala_guardado: int 
        # self.__x_mouse : int = 0
        # self.__y_mouse : int = 0
        # self.__xr_mouse : float = 0
        # self.__yr_mouse : float = 0

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
        self.BGR_recorte   = (0,200,200)  # amarillo
        self.BGR_guardado  = (100,150,0)  # verde oscuro
        self.BGR_error     = (0,50,200)  # vermellon
        # flags de estado 
        self.__recorte_guardado : bool = False
        self.__recorte_marcado  : bool = False
        # auxiliares
        # self.coordenadas_ventana: list[int] 

        self.brillo_ventana: int = 100
        self.contraste_ventana: float = 0.5 

        # self.dimensiones_ventana = [100,100]
        # self.coordenadas_ventana = [2000, 500]

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
        # [altura, base, _] = self.__imagen_original.shape

        [altura, base] = self.dimensiones_original
        if escala == None:
            proporcion = self.__escala_actual/100
        else:
            self.__escala_actual = escala
            proporcion = escala/100
        altura = int(altura * proporcion)
        base = int(base * proporcion)
        print(base, altura)
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
        # print(self.dimensiones_escalada())


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
        # [base_recorte, altura_recorte] = self.dimensiones_recorte
        [x_max, y_max] = self.dimensiones_escalada
        [x, y]= self.xy_escalada
        # print("escalada",x,y)
        #Se previenen errores por recortes mayores a la imagen de origen
        if base_recorte > x_max : base_recorte = x_max
        if altura_recorte > y_max : altura_recorte  = y_max  
        # El puntero del mouse quedará centrado dentro del rectángulo
        xi = x - base_recorte // 2
        yi = y - altura_recorte // 2
        # xi = self.__x_mouse - base_recorte // 2
        # yi = self.__y_mouse - altura_recorte // 2
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
        self.__imagen_recorte  = self.__imagen_escalada[yi:yf, xi:xf]
        # recorte_imagen = imagen[yi:yf, xi:xf]
        #retorno del recorte y sus coordenadas en una lista
        coordenadas = [xi, yi, xf, yf]
        self.__coordenadas_recorte_actuales = coordenadas

        print(self.__coordenadas_recorte_actuales )

        self.__coordenadas_recorte_relativas = [xi/x_max, y/y_max, xf/x_max, yf/y_max]
        print(self.__coordenadas_recorte_relativas )

        # self.__imagen_recorte = recorte_imagen 
        # archivo sustituto   
        if pathlib.Path(self.ruta_recorte).exists():
            self.temporal_recorte.close()
        self.temporal_recorte  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_recorte, self.__imagen_recorte)
        # retorno resultado (opcional)
        # return [self.__imagen_recorte  , coordenadas]


    def marcado_seleccion(self, error=False):
        """función grafica: actualiza la ventana de imagen y le dibuja un rectángulo encima con las coordenadas indicadas"""
        # marcado del rectangulo sobre una copia de la imagen para no dañar la original
        brillo = self.brillo_ventana
        contraste = self.contraste_ventana 
        # copia de salida con brillo y contraste cambiados
        copia = cv2.convertScaleAbs(self.__imagen_miniatura, alpha=contraste, beta=brillo)
        
        [b, h] = self.dimensiones_miniatura

        # coordenadas = self.__coordenadas_recorte_actuales

        # [xi, yi, xf, yf] = coordenadas

        [xif, yif, xff, yff] = self.__coordenadas_recorte_relativas  
        # print([xif, yif, xff, yff])
        
        coordenadas =  [int(xif*b), int(yif*h), int(xff*b), int(yff*h)]

        # Rectángulos color
        if coordenadas != [0,0,0,0]:
            coordenadas_rectangulo = coordenadas
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            # ¶ectangulo color
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
            # region brillo original
            copia[yi:yf, xi:xf] = self.__imagen_miniatura[yi:yf, xi:xf]

        # print(coordenadas)
        # print("imagen:      ",self.dimensiones_miniatura)
        # print("seleccion:   ",self.dimensiones_seleccion)


        # Regiones seleccionadas : brillo original
        # if self.__coordenadas_recorte_actuales != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_recorte_actuales

        #     # FIX IT

        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     copia[yi:yf, xi:xf] = self.__imagen_miniatura[yi:yf, xi:xf]
        # if self.__coordenadas_recorte != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_recorte
        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     copia[yi:yf, xi:xf] = self.__imagen_escalada[yi:yf, xi:xf]
        # if self.__coordenadas_guardado != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_guardado 
        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     copia[yi:yf, xi:xf] = self.__imagen_escalada[yi:yf, xi:xf]
        # Rectángulos color
        # if self.__coordenadas_recorte_actuales != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_recorte_actuales
        #     color_rectangulo = self.BGR_seleccion 
        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        # if self.__coordenadas_recorte != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_recorte
        #     color_rectangulo = self.BGR_recorte if  self.__escala_actual== self.__escala_recorte else self.BGR_error 
        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        # if self.__coordenadas_guardado != [0,0,0,0]:
        #     coordenadas_rectangulo = self.__coordenadas_guardado
        #     color_rectangulo = self.BGR_guardado if  self.__escala_actual == self.__escala_guardado else self.BGR_error
        #     (xi,yi) = coordenadas_rectangulo[0:2]
        #     (xf,yf) = coordenadas_rectangulo[2:4]
        #     cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        # si se indica el error de entrada se recuadra toda la imagen
        # if error:
        #     color_rectangulo = self.BGR_error
        #     (xi,yi) = (0, 0)
        #     (yf,xf,_) = copia.shape
        #     cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_8 )
        # actualizacion grafica
        # cv2.imshow(self.__nombre_ventana, copia) 
        self.__imagen_seleccion = copia
                # archivo sustituto   
        if pathlib.Path(self.ruta_seleccion).exists():
            self.temporal_seleccion.close()
        self.temporal_seleccion  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_seleccion, self.__imagen_seleccion)



    def calcular_dimensiones(self, proporcion: float, base_max: int = 512 , altura_max: int = 512):
        """Esta funcion calcula las dimensiones para """
        # lectura de parametros entrada
        p = proporcion
        (b, h) = imagen_temporal.dimensiones_original
        # limitacion de dimensiones maximas
        if base_max < int(b*p):
            p = base_max / b 
        if altura_max < int(h*p):
            p = altura_max / h 
        # print("dimensiones entrada:", b, h)
        # print("dimensiones finales:", b*p, h*p)
        base = int(h * p)
        altura = int(b * p)
        escala = float(p)
        return [base, altura, escala]



    def crear_miniatura(self, base: int, altura: int):
        """Crea la imagen miniatura que servira de referencia a la imagen de seleccion."""
        # [altura, base] = self.dimensiones_original
        # if escala == None:
        #     proporcion = self.__escala_actual/100
        # else:
        #     self.__escala_actual = escala
        #     proporcion = escala/100
        # altura = int(altura * proporcion)
        # base = int(base * proporcion)
        # print(base, altura)
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
        # print("miniatura creada, ", self.dimensiones_miniatura)








def principal(page: ft.Page):

    global imagen_temporal

    def cambiar_brillo(e):
        """MERO EJEMPLO --> ES PARA DESCARTE"""
        global imagen_temporal
        inicio = time.time()
        brillo = float(barra_brillo.value)
        contraste = float(barra_contraste.value/100)

        # # copia de salida con brillo y contraste cambiados
        imagen_temporal.cambiar_brillo(brillo, contraste)
        imagen.src = imagen_temporal.ruta_seleccion
        imagen.update()

        contenedor.update()
        fin = time.time()
        print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")


    def coordenadas(e):
        # coordenadas relativas al contenedor
        base   = int(contenedor.width)
        altura = int(contenedor.height)

        # confinamiento de las coordenadas obtenidas
        x = e.local_x if e.local_x < base else base
        y = e.local_y if e.local_y < altura else altura
        x = 0 if x <= 0 else x
        y = 0 if y <= 0 else y
        # conversion a valor relativo
        x = x / base
        y = y / altura
        # imagen_temporal.xr_mouse = x 
        # imagen_temporal.yr_mouse = y 
        imagen_temporal.xy_relativo = [x, y]
        # print("coordenadas:",x,y)
        # inicio = time.time()
        imagen_temporal.calcular_recorte([256,256])
        [b, h ,p] = imagen_temporal.calcular_dimensiones(1, base, altura)
        imagen_temporal.crear_miniatura(b, h)
        # print( "proporcion:", p)
        imagen_temporal.marcado_seleccion()
        # fin = time.time()
        # print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")
        imagen.src = imagen_temporal.ruta_seleccion
        imagen.update()

 
    def escalar(e):
        valor = e.control.value
        # print(valor)
        imagen_temporal.ampliar(valor)
        imagen.src = imagen_temporal.ruta_recorte
        imagen.update()


    def dimensiones( proporcion: float, base_max: int = 512 , altura_max: int = 512):
        # lectura de parametros entrada
        p = proporcion
        (b, h) = imagen_temporal.dimensiones_original
        # limitacion de dimensiones maximas
        if base_max < int(b*p):
            p = base_max / b 
        if altura_max < int(h*p):
            p = altura_max / h 
        # print("dimensiones entrada:", b, h)
        # print("dimensiones finales:", b*p, h*p)
        # correcion
        imagen.height = int(h * p)
        imagen.width = int(b * p)
        imagen.update()
        contenedor.height = int(h * p)
        contenedor.width = int(b * p)
        contenedor.update()
        detector_gestos.height = int(h * p)
        detector_gestos.width = int(b * p)
        detector_gestos.update()





    # Componentes graficos
    imagen = ft.Image(
        src = imagen_temporal.ruta_seleccion,
        # height = 512,
        # width  = 512, 
        fit = ft.ImageFit.CONTAIN,
        gapless_playback = True,        # transicion suave entre imagenes (retiene la version anterior hasta poder cambiar)
        )

    contenedor = ft.Container(
        content = imagen,
        # height = 512,
        # width  = 512, 
        padding=0,
        image_fit = ft.ImageFit.CONTAIN,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
        )



    detector_gestos = ft.GestureDetector(
        # height = 512,
        # width  = 512,
        content= contenedor,
        # on_pan_start=coordenadas,
        # on_pan_update=coordenadas,
        # on_pan_end=fin_seleccion,
        on_hover=coordenadas,
        )   



    # barra_escala = ft.Slider(min=30, max=330, divisions=300,value=100, label="{value}")
    # barra_escala.on_change = escalar

    page.add(detector_gestos)
    # page.add(barra_escala)

    dimensiones(0.5)

    # page.add(barra_brillo)
    # page.add(barra_contraste)
    # page.window_height = 700
    # page.window_width  = 600

    page.theme_mode = ft.ThemeMode.DARK

    page.update()










if __name__ == "__main__":


    ruta_archivo = "manejo_imagenes/ejemplo2.jpg"
    # ruta_archivo = "manejo_imagenes/ejemplo.jpg"

    # inicio = time.time()
    imagen_temporal = ImagenTemporal("ensayus_")
    imagen_temporal.abrir_imagen(ruta_archivo)
    # fin = time.time()
    # print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")

    ft.app(target=principal)

    # elimina la carpeta temporal y sus archivos internos al salir
    imagen_temporal.cerrar()