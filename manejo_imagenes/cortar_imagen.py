# Importamos OpenCV
from types import NoneType
import cv2
import sys
import numpy as np
from rich import print as print

from  threading import Thread
from multiprocessing import Lock, freeze_support, Pipe


def nada( a ):
    pass


class ParametrosVentana:
    def __init__(
        self, 
        ruta_origen: str = "", 
        ruta_recorte: str = "recorte.jpg",
        clave: str = "---",
        dimensiones_ventana: list[int] = [768, 768],
        dimensiones_recorte: list[int] = [512, 512],
        coordenadas_ventana: list[int] = [0, 0],
        ):
        """Este objeto a pasar todos los parametros de interes para realizar los recortes de imagen.
        Por defecto se elije un tamaño de recorte de 512 x 512, que es el exigido por Stable Diffusion"""
        self.ruta_origen = ruta_origen
        self.ruta_recorte = ruta_recorte
        self.clave = clave
        self.dimensiones_ventana = dimensiones_ventana
        self.dimensiones_recorte = dimensiones_recorte
        self.coordenadas_ventana = coordenadas_ventana
        self.dimensiones_original = [0,0]   # solo anchura y altura
        self.coordenadas_recorte = [0,0,0,0]
        self.coordenadas_actuales = [0,0,0,0]
        self.coordenadas_guardado = [0,0,0,0]     
        self.escala_actual = 100
        self.escala_recorte  = 0
        self.escala_guardado = 0
        self.recorte_guardado = False
        self.recorte_marcado  = False


class ImagenOpenCV:
    def __init__(
        self,
        nombre_ventana="Ventana Recorte", 
        nombre_trackbar='Escala', 
        candado = None,
        canal_recepcion: list | None = None,   # tuberia (pipe)
        canal_transmision: list | None = None,   # tuberia (pipe)
        ):
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

        self.dimensiones_recorte: list[int]
        self.dimensiones_original : list[int]

        self.__imagen_original = None | np.ndarray
        self.__imagen_escalada = None | np.ndarray
        self.__imagen_recorte = None | np.ndarray
        self.__imagen_seleccion = None | np.ndarray

        self.__nombre_ventana = nombre_ventana
        self.__nombre_trackbar = nombre_trackbar

        self.BGR_seleccion = (200,0,150)  # magenta
        self.BGR_recorte   = (0,200,200)  # amarillo
        self.BGR_guardado  = (100,150,0)  # verde oscuro
        self.BGR_error     = (0,50,200)  # vermellon
        # flags de estado 
        self.__recorte_guardado : bool = False
        self.__recorte_marcado  : bool = False
        # auxiliares
        self.coordenadas_ventana: list[int] 
        # self.dimensiones_ventana = [768, 768]
        self.texto_consola = True
        # teclas para salida del bucle infinito
        self.teclas_escape = {"a" , "s", "d" ," " }  
        # teclas para guardado de imagen desde teclado
        self.teclas_guardado = {"s"}  

        self.brillo_ventana: int = 100
        self.contraste_ventana: float = 0.5 

        self.funcion_mouse = nada
        self.funcion_trackbar = nada

        parametros = ParametrosVentana()
        self.__ventana_creada = False
        self.leer_estados(parametros)

        cv2.namedWindow(self.__nombre_ventana, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL )
        self.dimensiones_ventana = [100,100]
        self.coordenadas_ventana = [2000, 500]
        cv2.resizeWindow(self.__nombre_ventana, self.dimensiones_ventana[0] , self.dimensiones_ventana[1]) 
        cv2.moveWindow( self.__nombre_ventana, self.coordenadas_ventana[0], self.coordenadas_ventana[1])
        cv2.setMouseCallback(self.__nombre_ventana, self.__marcar_recorte)
        cv2.createTrackbar(self.__nombre_trackbar, self.__nombre_ventana, self.__escala_actual , self.__escala_maxima , self.actualizar_proporcion)
        # bloqueo - usado para proteger la lectura y escritura de archivos
        if candado != None:
            self.candado_archivos  = candado
        else:
            self.candado_archivos = Lock()
        # tuberia (pipe) para recibir parametros de imagenes
        if canal_recepcion != None:
            self.__extremo_recepcion_interno = canal_recepcion[0]
            self.__extremo_recepcion_externo = canal_recepcion[1]
        else:
            extremo_interno, extremo_externo = Pipe()
            self.__extremo_recepcion_interno = extremo_interno
            self.__extremo_recepcion_externo = extremo_externo 
        # tuberia (pipe) para enviar parametros de imagenes
        if canal_transmision != None:
            self.__extremo_transmision_interno = canal_transmision[0]
            self.__extremo_transmision_externo = canal_transmision[1]
        else:
            extremo_interno, extremo_externo = Pipe()
            self.__extremo_transmision_interno = extremo_interno
            self.__extremo_transmision_externo = extremo_externo 


    @property
    def canal_recepcion(self):
        """Esta property permite acceder al pipe interno para enviar los parametros de la imagen a la ventana
        Uso: 
        ventana = ImagenOpenCV( ...)
        tuberia_enviar = canal_recepcion
        tuberia_enviar.send([ parametros_imagen ])
        """
        return self.__extremo_recepcion_externo

    
    def ingresar_parametros(self, parametros: ParametrosVentana):
        """Este metodo permite enviar los parametros de imagen a la ventana desde otro hilo del proceso actual."""
        self.__extremo_recepcion_externo.send([parametros])


    @property
    def canal_transmision(self):
        """Esta property permite acceder al pipe interno para enviar los parametros de la imagen a la ventana
        Uso: 
        ventana = ImagenOpenCV( ...)
        tuberia_recibir = canal_tranmsision
        [ parametros_imagen ] = tuberia_recibir.recv()
        """
        return self.__extremo_transmision_externo


    def extraer_parametros(self):
        """Este metodo permite recibir los parametros del recorte de imagen desde otro hilo del proceso actual."""
        [parametros] = self.__extremo_transmision_externo.recv()
        return parametros


    def copiar_estados(self):
        """Metodo auxiliar para hacer un backup externo de las escalas y las coordenadas guardadas"""
        param = ParametrosVentana()
        param.ruta_origen   = self.ruta_imagen_original    
        param.ruta_recorte  = self.ruta_imagen_recorte
        param.clave         = self.clave 
        param.dimensiones_ventana = self.dimensiones_ventana           
        param.dimensiones_recorte = self.dimensiones_recorte 
        param.coordenadas_ventana = self.coordenadas_ventana 
        param.dimensiones_original = self.dimensiones_original           
        param.coordenadas_recorte  = self.__coordenadas_recorte  
        param.coordenadas_guardado = self.__coordenadas_guardado 
        param.escala_actual     = self.__escala_actual   
        param.escala_recorte    = self.__escala_recorte   
        param.escala_guardado   = self.__escala_guardado
        param.recorte_guardado  = self.__recorte_guardado 
        param.recorte_marcado   = self.__recorte_marcado  
        return param


    def leer_estados(self, param: ParametrosVentana):
        """Metodo auxiliar para recupera los valores de las últimas escalas y coordenadas asignadas.
        También actualiza la imagen"""
        #inicializacion valores
        self.__escala_minima = 33     
        self.__escala_maxima = 200    
        # ingreso de valores externos 
        self.ruta_imagen_original   = param.ruta_origen
        self.ruta_imagen_recorte    = param.ruta_recorte
        self.clave                  = param.clave
        self.dimensiones_ventana = param.dimensiones_ventana
        self.dimensiones_recorte = param.dimensiones_recorte
        self.coordenadas_ventana = param.coordenadas_ventana 
        self.dimensiones_original = param.dimensiones_original 
        self.__coordenadas_recorte  = param.coordenadas_recorte
        # self.__coordenadas_actuales = param.coordenadas_actuales
        self.__coordenadas_guardado = param.coordenadas_guardado
        self.__escala_actual    = param.escala_actual
        self.__escala_recorte   = param.escala_recorte
        self.__escala_guardado  = param.escala_guardado
        self.__recorte_guardado = param.recorte_guardado
        self.__recorte_marcado  = param.recorte_marcado
        # creacion recorte vacio para prevenir errores de apertura 
        self.__recorte_vacio()


    def apertura_imagenes(self):
        """Este método relee las imagenes y permite actualizar las rutas de entrada y de salida"""
        # lectura desde archivo
        self.candado_archivos.acquire()
        self.__imagen_original = cv2.imread(self.ruta_imagen_original)
        self.candado_archivos.release()
        # configuracion del trackbar de escala
        # se verifica que el recorte se pueda hacer
        ancho_imagen    = self.__imagen_original.shape[1]
        alto_imagen     = self.__imagen_original.shape[0]
        ancho_recorte = self.dimensiones_recorte[0]
        alto_recorte = self.dimensiones_recorte[1]
        if self.texto_consola == True: 
            print(f'Dimensiones de la imagen original  : base {ancho_imagen}, altura {alto_imagen}')
            print(f'Dimensiones de la imagen recortada : base {ancho_recorte}, altura {alto_recorte}')
        #se calcula la escala minima que puede tener la imagen de modo de permitir el recorte
        if alto_imagen / alto_recorte > ancho_imagen / ancho_recorte : proporcion =  ancho_recorte / ancho_imagen 
        else : proporcion =  alto_recorte / alto_imagen 
        # se acomodan los niveles de escalado posbiles
        self.__escala_minima = int( proporcion * 100 ) #porcentaje minimo de escalado (normalmente es menor al 100%)
        self.__escala_minima += 1  # excedente del 1% para prevencion de imagenes demasiado chicas
        # Si la imagen es demasiado chica se acomoda el cursor y se advierte
        if proporcion > 1:
            self.__escala_actual = self.__escala_minima 
            if self.texto_consola == True: print("WARNING: imagen original muy pequeña") 
        # Relación fija entre escala mínima y máxima
        self.__escala_maxima = self.__escala_minima * 6
        # actualizacion grafica
        self.__actualizar_trackbar_escala()

        # Caso de reapertura de imagenes --> reestablecer escalas        
        if self.__recorte_guardado :
            self.__escala_actual = self.__escala_guardado
        elif self.__recorte_marcado :
            self.__escala_actual = self.__escala_recorte
        self.__actualizar_trackbar_escala()
        # redimensionar imagen
        porcentaje = cv2.getTrackbarPos(self.__nombre_trackbar, self.__nombre_ventana)
        # actualizacion imagen
        cv2.moveWindow( self.__nombre_ventana, self.coordenadas_ventana[0], self.coordenadas_ventana[1])
        cv2.resizeWindow(self.__nombre_ventana, self.dimensiones_ventana )
        self.actualizar_proporcion(porcentaje)


    def actualizar_proporcion(self, porcentaje: int):
        """Esta funcion / manejador actualiza el tamaño de imagen y su ventana gráfica con los cambios de la barra deslizante."""
        # porcentaje = cv2.getTrackbarPos(self.__nombre_trackbar, self.__nombre_ventana) # innecesario
        self.__escala_actual = int(porcentaje)
        # Forzar posicion de la barra de escala
        # (si fue llamada por su handler no cambia nada)
        self.__actualizar_trackbar_escala()  
        proporcion = porcentaje / 100
        # redimensionar imagen
        if type(self.__imagen_original) == NoneType:
            [anchura, altura] = self.dimensiones_original 
            self.dimensiones_escalada = self.dimensiones_original 
            # Imagen vacia
            self.__imagen_escalada = np.zeros((altura, altura,3), np.uint8)
        else:
            anchura = self.__imagen_original.shape[1] 
            altura  = self.__imagen_original.shape[0] 
            self.dimensiones_original = [anchura, altura]
            # Prevencion de errores por entrada de numeros flotantes
            anchura = int( anchura * proporcion )
            altura  = int( altura * proporcion  )
            self.dimensiones_escalada = [anchura, altura]
            # Se usa la interpolacion más lenta pero de mejor calidad
            self.__imagen_escalada = cv2.resize(self.__imagen_original, self.dimensiones_escalada , interpolation = cv2.INTER_LANCZOS4) 
        # descarta la representacion de la actual posicion del mouse
        self.__coordenadas_actuales = [0,0,0,0]
        # actualizacion grafica
        self.ventana_imagen()
        #funcionalidad opcional
        self.funcion_trackbar(porcentaje)


    def __marcar_recorte(self, evento,x_mouse,y_mouse,flags,param):
        """Este handler recibe los eventos del mouse y se encarga de marcar el recorte y guardarlo de ser requerido. 
        #en esta funcion se usan solo los primeros tres parametros:
        # - evento del mouse
        # - posicion x del mouse
        # - posicion y del mouse
        """
        # guardado de la posicion del cursor en la ventana
        self.__x_mouse = x_mouse
        self.__y_mouse = y_mouse
        # reestablecimiento de escala
        # self.__actualizar_trackbar_escala()
        # dibujar rectangulos
        self.__calcular_rectangulo( )
        # evento movimiento cursor --> actualizar seleccion
        if evento == cv2.EVENT_MOUSEMOVE:
            # Actualizacion de graficas y retorno de coordenadas de seleccion
            self.ventana_imagen() 
            #funcion usuario (opcional) 
            self.funcion_mouse(evento)
        # evento click izquierdo --> crear recorte
        if evento == cv2.EVENT_LBUTTONDOWN:
            # marcado de archivo
            self.copiar_recorte()
            # Actualizacion de graficas y retorno del recorte y sus coordenadas
            self.ventana_imagen() 
            #funcion usuario (opcional) 
            self.funcion_mouse(evento)
        # evento click derecho --> crear recorte y guardarlo en archivo
        if evento == cv2.EVENT_RBUTTONDOWN:
            # guardado de archivo
            self.copiar_recorte(guardado=True)
            # Actualizacion de graficas y retorno del recorte y sus coordenadas
            self.ventana_imagen() 
            #funcion usuario (opcional) 
            self.funcion_mouse(evento)


    def ventana_imagen(self, error=False):
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
        if self.__coordenadas_recorte != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_recorte
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_escalada[yi:yf, xi:xf]
        if self.__coordenadas_guardado != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_guardado 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.__imagen_escalada[yi:yf, xi:xf]
        # Rectángulos color
        if self.__coordenadas_actuales != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_actuales
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        if self.__coordenadas_recorte != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_recorte
            color_rectangulo = self.BGR_recorte if  self.__escala_actual== self.__escala_recorte else self.BGR_error 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        if self.__coordenadas_guardado != [0,0,0,0]:
            coordenadas_rectangulo = self.__coordenadas_guardado
            color_rectangulo = self.BGR_guardado if  self.__escala_actual == self.__escala_guardado else self.BGR_error
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        # si se indica el error de entrada se recuadra toda la imagen
        if error:
            color_rectangulo = self.BGR_error
            (xi,yi) = (0, 0)
            (yf,xf,_) = copia.shape
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_8 )
        # actualizacion grafica
        cv2.imshow(self.__nombre_ventana, copia) 


    def __calcular_rectangulo(self):  
        """Funcion creada para calcular el rectángulo de seleccion de modo de evitar desbordes"""
        # lectura de dimensiones
        [base_recorte, altura_recorte] = self.dimensiones_recorte
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
        self.__imagen_seleccion = recorte_imagen 
        self.__coordenadas_actuales = coordenadas
        # retorno resultado (opcional)
        return [recorte_imagen , coordenadas]


    def __actualizar_trackbar_escala(self):
        cv2.setTrackbarPos(self.__nombre_trackbar, self.__nombre_ventana, self.__escala_actual) 
        cv2.setTrackbarMin(self.__nombre_trackbar, self.__nombre_ventana, self.__escala_minima) 
        cv2.setTrackbarMax(self.__nombre_trackbar, self.__nombre_ventana, self.__escala_maxima) 


    def __recorte_vacio(self, dimensiones: list[int]|None = None):
        """Inicializa en negro las imagenes auxiliares de la clase"""
        if dimensiones == None:
            dimensiones = self.dimensiones_recorte
        else:
            self.dimensiones_recorte = dimensiones
        ancho_recorte = dimensiones[0]
        alto_recorte  = dimensiones[1]
        # relleno preliminar con imagen en negro
        self.__imagen_recorte = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
        self.__imagen_seleccion = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
        self.__imagen_escalada = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
        self.__imagen_original = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)


    def interfaz_edicion(
        self,  
        texto_consola=False,
        escape_teclado=False,
        funcion_mouse=nada,
        funcion_trackbar=nada,
        ):
        """Funcion para abrir la ventana de edición. La ventana se cierra presionando alguna de las teclas indicadas.
        Debe ser llamada desde el thread principal para funcionar correctamente."""
        self.funcion_mouse = funcion_mouse
        self.funcion_trackbar = funcion_trackbar
        self.texto_consola = texto_consola

        def bucle_teclado():
            """Bucle para mantener abeirto el objeto de ventana.
            Debe ser llamado desde el thread principal para funcionar correctamente."""
            # Conjunto de teclas de escape
            exito_guardado = False
            if escape_teclado:
                teclas_escape = self.teclas_escape 
            else:
                teclas_escape = {}
            tecla = "-"  # Caracter no implementado
            if texto_consola: print("Teclas implementadas: ", teclas_escape )
            # self.ventana_imagen()
            while tecla not in teclas_escape:
                # espera en reposo a que se pulse una tecla del teclado
                # k = cv2.waitKey(0)
                k = cv2.waitKeyEx(0)
                if k >= 0:
                    tecla = chr(k)  # Conversion de numero a caracter ASCII
                    if texto_consola: print("Tecla ingresada: ", tecla)
                    # se guarda una copia del recorte si la tecla es correcta
                    if tecla  in self.teclas_guardado:
                        exito_guardado = self.__guardado_recorte() 
                        # reapertura imagen
                # self.ventana_imagen()

            # self.cerrar_ventana()
            # cv2.destroyWindow(self.__nombre_ventana)
            return tecla, exito_guardado

        def bucle_espera_parametros():
            """Rutina de recepcion de datos"""
            while True:
                [parametros] = self.__extremo_recepcion_interno.recv()  
                self.leer_estados(parametros)
                # print(parametros.dimensiones_ventana)
                # cv2.resizeWindow(self.__nombre_ventana, 400, 400)
                self.apertura_imagenes()

        # Creacion del subhilo para la rutina de espera y apertura del bucle infinito
        if self.__ventana_creada == False:
            hilo_espera = Thread(target=bucle_espera_parametros)
            hilo_espera.daemon = True
            hilo_espera.start()
            self.__ventana_creada = True
            bucle_teclado() #bucle condicional
            # cv2.waitKey(0)


    def __guardado_recorte(self):
        # proteccion del guardado ante otros procesos
        self.candado_archivos.acquire()
        guardado_correcto = cv2.imwrite(self.ruta_imagen_recorte, self.__imagen_recorte)
        self.candado_archivos.release()

        if guardado_correcto:
            if self.texto_consola: 
                print("¡Recorte guardado!")
        else:
            if self.texto_consola: 
                print("WARNING: Guardado fallido")
        return guardado_correcto

    
    def copiar_recorte(self, guardado = False):
        self.__coordenadas_recorte = self.__coordenadas_actuales
        self.__imagen_recorte = self.__imagen_seleccion.copy()
        self.__escala_recorte = self.__escala_actual
        self.__recorte_marcado = True
        guardado_correcto = False
        if guardado: 
            self.__coordenadas_guardado = self.__coordenadas_actuales
            self.__escala_guardado = self.__escala_actual
            guardado_correcto = self.__guardado_recorte()   # creacion archivo
            self.__recorte_guardado = guardado_correcto
        # envio de datos al exterior por tuberia
        parametros = self.copiar_estados()
        self.__extremo_transmision_interno.send([parametros])
        # retorno con indicacion del guardado
        return guardado_correcto



# Rutina de prueba: Apertura de imagenes
# Uso:
# python cortar_imagen.py <ruta_imagen_original> <ruta_imagen_salida>
# Si faltan parámetros estos se sustituyen por valores predefinidos
if __name__ == "__main__" :

    #(requerido para los  subprocesos en Windows)
    freeze_support() # requerido para crear ejecutables en Windows

    ## APERTURA IMAGEN
    if len(sys.argv) == 1 :
        #imagen por defecto 
        ruta_archivo_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
        print("Apertura de archivo de ejemplo:", ruta_archivo_imagen)
    else :
        ruta_archivo_imagen = str(sys.argv[1])
        print("Apertura de archivo indicado:", ruta_archivo_imagen)

    if len(sys.argv) < 3 :
        ruta_archivo_recorte = 'recorte.jpg'
        print("Guardado de archivo por defecto:", ruta_archivo_recorte)
    else :
        ruta_archivo_recorte = str(sys.argv[2])
        print("Nombre de recorte:", ruta_archivo_recorte)

    ## PROCESAMIENTO
    ventana = ImagenOpenCV()
    # uso pipeline interno
    tuberia_enviar = ventana.canal_recepcion
    tuberia_recibir = ventana.canal_transmision

    def mouse(x):
        if x==cv2.EVENT_LBUTTONDOWN:
            # marcado de archivo
            print(f"Marcado recorte, codigo {x}")
        elif x==cv2.EVENT_RBUTTONDOWN:
            # guardado de archivo
            print(f"Guardado recorte, codigo {x}")

    # estructura con datos de imagen
    parametros_imagen = ParametrosVentana(
        ruta_archivo_imagen, 
        ruta_archivo_recorte,
        dimensiones_recorte=[256, 354],
        dimensiones_ventana=[512, 512],
        )
    
    
    # hilo y rutina auxiliares para actualizar imagen
    import time
    def envio_imagen():
        """Envia data de la imagen a mostrar"""
        # tuberia_enviar.send([parametros_imagen]) # correcto
        ventana.ingresar_parametros(parametros_imagen) # correcto)
        demora = 3
        while demora >= 0:
            print(f"cuenta atrás: {demora}")
            demora -= 1
            time.sleep(1)
        # marcar un recorte
        parametros_imagen.coordenadas_recorte = [100,100,300,400]
        # tuberia_enviar.send([parametros_imagen]) # correcto
        ventana.ingresar_parametros(parametros_imagen) # correcto


    hilo_mensajes = Thread(target=envio_imagen)
    hilo_mensajes.daemon = True
    hilo_mensajes.start()

    # hilo y rutina auxiliares para registrar coordenadas del recorte
    def recibir_logs():
        while True:
            # [datos] = tuberia_recibir.recv() # correcto
            datos = ventana.extraer_parametros() # correcto
            print("coord. recorte :",datos.coordenadas_recorte)
            # print("dimensiones (imagen ampliada) :",datos.dimensiones_ventana)


    hilo_logs = Thread(target=recibir_logs)
    hilo_logs.daemon = True
    hilo_logs.start()

    # llamado a la ventana grafica (bucle condicional, se sale por teclado)
    ventana.interfaz_edicion( texto_consola=True, escape_teclado=True, funcion_mouse=mouse)    # Tamaño predefinido

