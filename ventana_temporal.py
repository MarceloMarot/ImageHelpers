


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
        self.ruta_imagen_original : str = ""    # valor provisional
        self.ruta_imagen_recorte  : str = ""    # valor provisional
        self.clave : str = "---"
        self.__coordenadas_recorte: list[int]
        self.__coordenadas_actuales: list[int]
        self.__coordenadas_guardado: list[int]
        # porcentajes de ampliacion entre grafica y archivo
        self.__escala_minima: int  
        self.__escala_maxima: int 
        self.__escala_actual: int 
        self.__escala_recorte : int 
        self.__escala_guardado: int 
        self.__x_mouse : int = 0
        self.__y_mouse : int = 0
        self.__xr_mouse : float = 0
        self.__yr_mouse : float = 0

        # self.dimensiones_original   : list[int]
        # self.dimensiones_original   : list[int]
        # self.dimensiones_recorte    : list[int]
        # self.dimensiones_original   : list[int]

        self.__imagen_original = None | np.ndarray
        self.__imagen_escalada = None | np.ndarray
        self.__imagen_recorte = None | np.ndarray
        self.__imagen_seleccion = None | np.ndarray


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


    @property
    def x_mouse(self):
        return self.__x_mouse

    @property
    def y_mouse(self):
        return self.__y_mouse

    @property
    def xr_mouse(self):
        return self.__xr_mouse

    @property
    def yr_mouse(self):
        return self.__yr_mouse 

    @xr_mouse.setter
    def xr_mouse(self,  valor: float):
        self.__xr_mouse = int(valor)
        (h, b , c) = self.dimensiones_escalada()
        self.__x_mouse  = int(valor*b)

    @yr_mouse.setter
    def yr_mouse(self, valor: float):
        self.__yr_mouse = int(valor)
        (h, b , c) = self.dimensiones_escalada()
        self.__y_mouse  = int(valor*h)


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

    def cerrar(self):
        """Elimina la carpeta temporal y sus archivos internos"""
        self.carpeta_temporal.cleanup()






    def abrir_imagen(self,ruta_archivo: str ):
        """Carga de los archivos temporales y su primera version"""
        # copia temporal desde archivo fisico
        self.temporal_original = crear_imagen_temporal(ruta_archivo, self.carpeta_temporal)
        # copias hechas desde el archivo temporal
        self.temporal_escalada = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        self.temporal_recorte  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        # self.temporal_seleccion  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        self.temporal_seleccion  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        # # objetos matriciales de OpenCV representando las imagenes    
        self.__imagen_original  = cv2.imread(self.ruta_original)
        self.__imagen_escalada  = cv2.imread(self.ruta_original)
        self.__imagen_recorte   = cv2.imread(self.ruta_original)
        self.__imagen_seleccion = cv2.imread(self.ruta_original)
        self.__escala_actual = 100

    def dimensiones_original(self):
        return self.__imagen_original.shape 

    def dimensiones_escalada(self):
        return self.__imagen_escalada.shape 

    def dimensiones_recorte(self):
        return self.__imagen_recorte.shape  

    def dimensiones_seleccion(self):
        return self.__imagen_seleccion.shape  


    def ampliar(self, escala: int|None = None):
        """Crea una copia ampliada de la imagen de entrada."""
        [altura, base, _] = self.__imagen_original.shape
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

        # QUITAR (FIX)
        # self.calcular_recorte([512,512])




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
        imagen = self.__imagen_escalada
        x_max = imagen.shape[1]
        y_max = imagen.shape[0]
        #Se previenen errores por recortes mayores a la imagen de origen
        if base_recorte > x_max : base_recorte = x_max
        if altura_recorte > y_max : altura_recorte  = y_max  
        # El puntero del mouse quedará centrado dentro del rectángulo
        xi = self.__x_mouse - base_recorte // 2
        yi = self.__y_mouse - altura_recorte // 2
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
        recorte_imagen = imagen[yi:yf, xi:xf]
        #retorno del recorte y sus coordenadas en una lista
        coordenadas = [xi, yi, xf, yf]
        self.__coordenadas_actuales = coordenadas
        self.__imagen_recorte = recorte_imagen 
        # archivo sustituto   
        if pathlib.Path(self.ruta_recorte).exists():
            self.temporal_recorte.close()
        self.temporal_recorte  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_recorte, self.__imagen_recorte)
        # retorno resultado (opcional)
        return [recorte_imagen , coordenadas]


    def marcado_seleccion(self, error=False):
        """función grafica: actualiza la ventana de imagen y le dibuja un rectángulo encima con las coordenadas indicadas"""
        # marcado del rectangulo sobre una copia de la imagen para no dañar la original
        brillo = self.brillo_ventana
        contraste = self.contraste_ventana 
        # copia de salida con brillo y contraste cambiados
        copia = cv2.convertScaleAbs(self.__imagen_escalada, alpha=contraste, beta=brillo)
        # Regiones seleccionadas : brillo original
        if self.__coordenadas_actuales != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_actuales
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_escalada[yi:yf, xi:xf]
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
        if self.__coordenadas_actuales != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_actuales
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
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
        if error:
            color_rectangulo = self.BGR_error
            (xi,yi) = (0, 0)
            (yf,xf,_) = copia.shape
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_8 )
        # actualizacion grafica
        # cv2.imshow(self.__nombre_ventana, copia) 
        self.__imagen_seleccion = copia
                # archivo sustituto   
        if pathlib.Path(self.ruta_seleccion).exists():
            self.temporal_seleccion.close()
        self.temporal_seleccion  = crear_imagen_temporal(self.ruta_original, self.carpeta_temporal)
        cv2.imwrite(self.ruta_seleccion, self.__imagen_seleccion)












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
        # print(f" lx: {e.local_x}, ly: {e.local_y}")

        # [altura, base, _ ] = imagen_temporal.dimensiones_escalada()


        # coordenadas relativas al contenedor
        base   = int(contenedor.width)
        altura = int(contenedor.height)
        # confinamiento de las coordenadas obtenidas
        x = e.local_x if e.local_x < base else base
        y = e.local_y if e.local_y < altura else altura
        x = 0 if x <= 0 else x
        y = 0 if y <= 0 else y

        # print("A",x,y)
        x = x / base
        y = y / altura
        # print("B",x,y)


        proporcion = barra_escala.value / 100

        imagen_temporal.xr_mouse = x * proporcion
        imagen_temporal.yr_mouse = y * proporcion


        # print("coordenadas:",x,y)
        inicio = time.time()
        imagen_temporal.calcular_recorte([256,256])
        imagen_temporal.marcado_seleccion()
        fin = time.time()
        print(f"tiempo {(fin - inicio)*1e3 :4.3} mseg.")




        imagen.src = imagen_temporal.ruta_seleccion
        imagen.update()

 




    def fin_seleccion(e):
        contenedor.update()
        imagen.update()

    def escalar(e):
        valor = e.control.value
        # print(valor)
        imagen_temporal.ampliar(valor)
        imagen.src = imagen_temporal.ruta_recorte
        imagen.update()



    def coordenadas_relativas(e):
        base   = int(contenedor.width)
        altura = int(contenedor.height)


        # confinamiento de las coordenadas obtenidas
        x = e.local_x if e.local_x < base else base
        y = e.local_y if e.local_y < altura else altura
        x = 0 if x <= 0 else x
        y = 0 if y <= 0 else y
        # conversion al valor relativo
        xr = x / base
        yr = y / altura
        # print(f" x: {x}, y: {y}")
        # print(f" xr: {xr}, yr: {yr}")
        return [xr, yr]


    # Componentes graficos

    imagen = ft.Image(
        src = imagen_temporal.ruta_seleccion,
        height = 512,
        width  = 512, 
        fit = ft.ImageFit.CONTAIN,
        gapless_playback = True,        # transicion suave entre imagenes (retiene la version anterior hasta poder cambiar)
        )

    contenedor = ft.Container(
        content = imagen,
        height = 512,
        width  = 512, 
        image_fit = ft.ImageFit.CONTAIN,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.EASE),
        )

    detector_gesto = ft.GestureDetector(
        content= contenedor,
        # on_pan_start=coordenadas,
        # on_pan_update=coordenadas,
        on_hover=coordenadas,
        # on_pan_start=coordenadas,
        # on_pan_update=coordenadas_relativas,
        # on_pan_end=fin_seleccion,
        )   

    barra_escala = ft.Slider(min=30, max=330, divisions=300,value=100, label="{value}")
    # barra_brillo = ft.Slider(min=-255, max=255, divisions=500,value=0, label="{value}")
    # barra_contraste = ft.Slider(min=0, max=300, divisions=300,value=100, label="{value}")
    # barra_brillo.   on_change = cambiar_brillo
    # barra_contraste.on_change = cambiar_brillo
    barra_escala.on_change = escalar
    # barra_brillo.   on_change_end = cambiar_brillo
    # barra_contraste.on_change_end = cambiar_brillo

    page.add(detector_gesto)
    page.add(barra_escala)
    # page.add(barra_brillo)
    # page.add(barra_contraste)
    page.window_height = 700
    page.window_width  = 600

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