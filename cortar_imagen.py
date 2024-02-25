# Importamos OpenCV
from types import NoneType
import cv2
import sys
import numpy as np



class ImagenOpenCV:
    # def __init__(self, ruta_original: str = "",ruta_recorte: str = "recorte.jpg"):
        # self.ruta_imagen_original = ruta_original
        # self.ruta_imagen_recorte  = ruta_recorte
    def __init__(self):
        self.ruta_imagen_original = ""
        self.ruta_imagen_recorte  = ""
        self.coordenadas_recorte = [0,0,0,0]
        self.coordenadas_seleccion = [0,0,0,0]
        self.coordenadas_guardado = [0,0,0,0]
        # porcentajes de ampliacion entre grafica y archivo
        self.escala_minima: int = 33     #inicializacion por defecto 
        self.escala_maxima: int = 200     #inicializacion por defecto 
        self.escala_actual: int = 100
        self.escala_recorte: int = 0
        self.escala_guardado: int = 0

        self.x_mouse = 0
        self.y_mouse = 0
        self.dimensiones_recorte = [256, 256]
        self.dimensiones_original = [512, 512]

        # self.imagen_original = cv2.imread(ruta_original)
        # self.imagen_escalada = self.imagen_original.copy()
        self.imagen_original = None | np.ndarray
        self.imagen_escalada = None | np.ndarray
        self.imagen_recorte = None | np.ndarray
        self.imagen_seleccion = None | np.ndarray

        self.imagen_grafica = None | np.ndarray

        self.nombre_ventana = "Ventana Recorte"
        self.nombre_trackbar = 'Escala' 
        self.BGR_seleccion = (200,0,150)  # magenta
        self.BGR_recorte   = (0,200,200)  # amarillo
        self.BGR_guardado  = (100,150,0)  # verde oscuro

        self.BGR_error = (0,50,200)  # vermellon

        # self.__nro_aperturas_ventana = 0

        self.__recorte_guardado = False
        self.__recorte_marcado  = False

        self.coordenadas_ventana = [900, 100]
        self.dimensiones_ventana = [768, 768]
        self.texto_consola = True


        self.configurar_ventana()
        self.crear_trackbar()
        # self.ventana_imagen()




    def crear_trackbar(self):
        # creacion de la barra de escala
        cv2.createTrackbar(self.nombre_trackbar, self.nombre_ventana, self.escala_actual , self.escala_maxima , self.actualizar_proporcion) 
        #seteo del handler de escala
        # cv2.setMouseCallback(self.nombre_ventana, self.marcar_recorte)  



    # Manejador para controlar el tamaño de la imagen
    def actualizar_proporcion(self, x):
        """Este manejador actualiza el tamaño de imagen y su ventana gráfica con los cambios de la barra deslizante."""
        porcentaje = cv2.getTrackbarPos(self.nombre_trackbar, self.nombre_ventana)
        self.escala_actual = int(porcentaje)
        proporcion = porcentaje / 100
        self.redimensionar_imagen(proporcion)
        # descarta la representacion de la actual posicion del mouse
        self.coordenadas_seleccion = [0,0,0,0]
        # actualizacion grafica
        self.ventana_imagen()



    # funcion para ubicar y mostrar el recorte de imagen deseado
    def marcar_recorte(self, evento,x_mouse,y_mouse,flags,param):
        """Este handler recibe los eventos del mouse y se encarga de marcar el recorte y guardarlo de ser requerido. """
        #en esta funcion se usan solo los primeros tres parametros:
        # - evento del mouse
        # - posicion x del mouse
        # - posicion y del mouse
        self.x_mouse = x_mouse
        self.y_mouse = y_mouse

        # reestablecimiento de escala
        self.actualizar_trackbar_escala()
        # dibujar rectangulos
        self.calcular_rectangulo( )
        # evento movimiento cursor --> actualizar seleccion
        if evento == cv2.EVENT_MOUSEMOVE:
            # Actualizacion de graficas y retorno de coordenadas de seleccion
            self.ventana_imagen() 
        # evento click izquierdo --> crear recorte
        if evento == cv2.EVENT_LBUTTONDOWN:
            # Actualizacion de graficas y retorno del recorte y sus coordenadas
            self.copiar_recorte()
            self.ventana_imagen() 
        # evento click derecho --> crear recorte y guardarlo en archivo
        if evento == cv2.EVENT_RBUTTONDOWN:
            # Actualizacion de graficas y retorno del recorte y sus coordenadas
            self.copiar_recorte(guardado=True)
            self.ventana_imagen() 



    # Funcion para redimencionar la imagen  de entrada sin alterar las proporciones
    def redimensionar_imagen(self, proporcion ):
        """Esta funcion crea una copia de la imagen de entrada ampliada o reducida en el factor de escala ingresado."""
        # print("TIPO:",type(self.imagen_original))
        if type(self.imagen_original) == NoneType:

            [anchura, altura] = self.dimensiones_original 
            self.dimensiones_escalada = self.dimensiones_original 
            # Imagen vacia
            self.imagen_escalada = np.zeros((altura, altura,3), np.uint8)

        else:
            anchura = self.imagen_original.shape[1] 
            altura  = self.imagen_original.shape[0] 
            self.dimensiones_original = [anchura, altura]

            # Prevencion de errores por entrada de numeros flotantes
            anchura = int( anchura * proporcion )
            altura  = int( altura * proporcion  )
            self.dimensiones_escalada = [anchura, altura]

            # Se usa la interpolacion más lenta pero de mejor calidad
            self.imagen_escalada = cv2.resize(self.imagen_original, self.dimensiones_escalada , interpolation = cv2.INTER_LANCZOS4) 



    def ventana_imagen(self, error=False):
        """función grafica: actualiza la ventana de imagen y le dibuja un rectángulo encima con las coordenadas indicadas"""
        # marcado del rectangulo sobre una copia de la imagen para no dañar la original

        brillo = 100
        contraste = 0.5 
        # brillo = 150
        # contraste = 0.33
        copia = cv2.convertScaleAbs(self.imagen_escalada, alpha=contraste, beta=brillo)

        # reestablecimiento de escala
        # self.actualizar_trackbar_escala()

        # Regiones seleccionadas : brillo original
        if self.coordenadas_seleccion != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_seleccion
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.imagen_escalada[yi:yf, xi:xf]
        if self.coordenadas_recorte != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_recorte
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.imagen_escalada[yi:yf, xi:xf]
        if self.coordenadas_guardado != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_guardado 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            copia[yi:yf, xi:xf] = self.imagen_escalada[yi:yf, xi:xf]
            
        # Rectángulos color
        if self.coordenadas_seleccion != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_seleccion
            color_rectangulo = self.BGR_seleccion 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        if self.coordenadas_recorte != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_recorte
            color_rectangulo = self.BGR_recorte if  self.escala_actual== self.escala_recorte else self.BGR_error 
            (xi,yi) = coordenadas_rectangulo[0:2]
            (xf,yf) = coordenadas_rectangulo[2:4]
            cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        if self.coordenadas_guardado != [0,0,0,0]:
            coordenadas_rectangulo = self.coordenadas_guardado
            color_rectangulo = self.BGR_guardado if  self.escala_actual == self.escala_guardado else self.BGR_error
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
        cv2.imshow(self.nombre_ventana, copia) 


    def calcular_rectangulo(self):  
        """Funcion creada para calcular el rectángulo de seleccion de modo de evitar desbordes"""
        # lectura de dimensiones
        [base_recorte, altura_recorte] = self.dimensiones_recorte
        imagen = self.imagen_escalada
        x_max = imagen.shape[1]
        y_max = imagen.shape[0]
        #Se previenen errores por recortes mayores a la imagen de origen
        if base_recorte > x_max : base_recorte = x_max
        if altura_recorte > y_max : altura_recorte  = y_max  
        # El puntero del mouse quedará centrado dentro del rectángulo
        xi = self.x_mouse - base_recorte // 2
        yi = self.y_mouse - altura_recorte // 2
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
        self.imagen_seleccion = recorte_imagen 
        self.coordenadas_seleccion = coordenadas
        # retorno resultado (opcional)
        return [recorte_imagen , coordenadas]


    def configurar_ventana(self):
        cv2.namedWindow(self.nombre_ventana, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL )
        ancho_ventana = self.dimensiones_ventana[0]
        alto_ventana  = self.dimensiones_ventana[1]
        cv2.resizeWindow(self.nombre_ventana, ancho_ventana , alto_ventana ) 
        b = self.coordenadas_ventana[0]
        h = self.coordenadas_ventana[1]
        cv2.moveWindow(self.nombre_ventana, b, h)
        cv2.setMouseCallback(self.nombre_ventana, self.marcar_recorte) 





    def configurar_trackbar_escala(self):

        # se verifica que el recorte se pueda hacer
        ancho_imagen    = self.imagen_original.shape[1]
        alto_imagen     = self.imagen_original.shape[0]

        ancho_recorte = self.dimensiones_recorte[0]
        alto_recorte = self.dimensiones_recorte[1]

        if self.texto_consola == True: 
            print(f'Dimensiones de la imagen original  : base {ancho_imagen}, altura {alto_imagen}')
            print(f'Dimensiones de la imagen recortada : base {ancho_recorte}, altura {alto_recorte}')
        #se calcula la escala minima que puede tener la imagen de modo de permitir el recorte
        if alto_imagen / alto_recorte > ancho_imagen / ancho_recorte : proporcion =  ancho_recorte / ancho_imagen 
        else : proporcion =  alto_recorte / alto_imagen 
        # se acomodan los niveles de escalado posbiles
        self.escala_minima = int( proporcion * 100 ) #porcentaje minimo de escalado (normalmente es menor al 100%)
        self.escala_minima += 1  # excedente del 1% para prevencion de imagenes demasiado chicas

        # Si la imagen es demasiado chica se acomoda el cursor y se advierte
        if proporcion > 1:
            self.escala_actual = self.escala_minima 
            if self.texto_consola == True: print("WARNING: imagen original muy pequeña") 

        # Relación fija entre escala mínima y máxima
        self.escala_maxima = self.escala_minima * 6
        # actualizacion grafica
        self.actualizar_trackbar_escala()


    def actualizar_trackbar_escala(self):
        # Caso de reapertura de imagenes --> reestablecer escalas        
        # if self.__recorte_guardado :
        #     self.escala_actual = self.escala_guardado
        # elif self.__recorte_marcado :
        #     self.escala_actual = self.escala_recorte
        cv2.setTrackbarPos(self.nombre_trackbar, self.nombre_ventana, self.escala_actual) 
        cv2.setTrackbarMin(self.nombre_trackbar, self.nombre_ventana, self.escala_minima) 
        cv2.setTrackbarMax(self.nombre_trackbar, self.nombre_ventana, self.escala_maxima) 


    def apertura_imagen(self, ruta: str|None = None):
        if ruta != None:
            # actualizacion de ruta de imagen 
            self.ruta_imagen_original = ruta
            # borrado de flags auxiliares
            self.__recorte_guardado = False
            self.__recorte_marcado  = False
            self.recorte_vacio()

        # lectura desde archivo
        self.imagen_original = cv2.imread(self.ruta_imagen_original)

        self.configurar_trackbar_escala()

        # # Caso de reapertura de imagenes --> reestablecer escalas        
        if self.__recorte_guardado :
            self.escala_actual = self.escala_guardado
        elif self.__recorte_marcado :
            self.escala_actual = self.escala_recorte

        self.actualizar_trackbar_escala()
        self.redimensionar_imagen(self.escala_actual/100 )

        self.ventana_imagen()


    def recorte_vacio(self, dimensiones: list[int]|None = None):
        #creacion recorte vacio
        if dimensiones == None:
            dimensiones = self.dimensiones_recorte
        else:
            self.dimensiones_recorte = dimensiones
        ancho_recorte = dimensiones[0]
        alto_recorte  = dimensiones[1]
        # relleno preliminar con imagen en negro
        self.imagen_recorte = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
        self.imagen_seleccion = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)




    def interfaz_edicion(
        self,  
        ruta_original: str = "",
        ruta_recorte: str = "recorte.jpg",
        dimensiones_recorte=[512, 512], 
        dimensiones_ventana=[768, 768], 
        texto_consola=True,
        escape_teclado=True
        ):
        """Funcion para abrir la ventana de edición. La ventana se cierra presionando alguna de las teclas indicadas. 
        Por defecto se elije un tamaño de recorte de 512 x 512, que es el exigido por Stable Diffusion"""
        self.ruta_imagen_original = ruta_original
        self.ruta_imagen_recorte  = ruta_recorte
        self.texto_consola = texto_consola

        self.dimensiones_ventana = dimensiones_ventana
        # valores retorno
        exito = False
        tecla = "-"  # Caracter no implementado
        # Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
        # self.imagen_original = cv2.imread(self.ruta_imagen_original)    
        # se leen las dimensiones de imagen y de recorte
        # asignacion por defecto: NO ampliar ni reducir imagen de entrada
        # imagen_escalada = self.imagen_original.copy()
        # #creacion recorte vacio
        # self.dimensiones_recorte = dimensiones_recorte
        # ancho_recorte = dimensiones_recorte[0]
        # alto_recorte  = dimensiones_recorte[1]
        # # relleno preliminar con imagen en negro
        # self.imagen_recorte = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
        # self.imagen_seleccion = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)

        self.recorte_vacio(dimensiones_recorte)
        self.apertura_imagen()

        # self.configurar_trackbar_escala()

        # # # Caso de reapertura de imagenes --> reestablecer escalas        
        # if self.__recorte_guardado :
        #     self.escala_actual = self.escala_guardado
        # elif self.__recorte_marcado :
        #     self.escala_actual = self.escala_recorte

        # self.actualizar_trackbar_escala()
        # self.redimensionar_imagen(self.escala_actual/100 )
        # self.ventana_imagen()


        # Conjunto de teclas de escape
        exito_guardado = False
        if escape_teclado:
            teclas_escape = {"a" , "s", "d" ," " }  # Teclas 'A', 'S', 'D', 'SPACE' 
        else:
            teclas_escape = {}
        tecla = "-"  # Caracter no implementado
        if texto_consola: print("Teclas implementadas: ", teclas_escape )
        while tecla not in teclas_escape:
            # espera en reposo a que se pulse una tecla del teclado
            # k = cv2.waitKey(0)
            k = cv2.waitKeyEx(0)
            tecla = chr(k)  # Conversion de numero a caracter ASCII

            print(k, tecla )
            if texto_consola: print("Tecla ingresada: ", tecla)
            #si la tecla pulsada es 's' se guarda una copia del recorte
            if k == ord("s"):
                exito_guardado = self.guardado_recorte() 

        # self.cerrar_ventana()
        return tecla, exito_guardado


    def guardado_recorte(self):
        guardado_correcto = cv2.imwrite(self.ruta_imagen_recorte, self.imagen_recorte)
        if guardado_correcto == True :
            if self.texto_consola: 
                print("¡Recorte guardado!")
        else:
            if self.texto_consola: 
                print("WARNING: Guardado fallido")
        return guardado_correcto

    
    def copiar_recorte(self, guardado = False):
        self.coordenadas_recorte = self.coordenadas_seleccion
        self.imagen_recorte = self.imagen_seleccion.copy()
        self.escala_recorte = self.escala_actual
        self.__recorte_marcado = True
        if guardado: 
            self.coordenadas_guardado = self.coordenadas_seleccion
            self.escala_guardado = self.escala_actual
            guardado_correcto = self.guardado_recorte()
            self.__recorte_guardado = guardado
            return guardado_correcto


    def cerrar_ventana(self):
        cv2.destroyWindow(self.nombre_ventana)


# Rutina de prueba: Apertura de imagenes
# Uso:
# python cortar_imagen.py <ruta_imagen_original> <ruta_imagen_salida>
# Si faltan parámetros estos se sustituyen por valores predefinidos
if __name__ == "__main__" :

    ## APERTURA IMAGEN
    if len(sys.argv) == 1 :
        #imagen por defecto 
        ruta_archivo_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
        print("Apertura de archivo de ejemplo:", ruta_archivo_imagen)
    else :
        ruta_archivo_imagen = str(sys.argv[1])
        print("Apertura de archivo indicado:", ruta_archivo_imagen)

    if len(sys.argv) < 3 :
        ruta_archivo_recorte = 'recorte.webp'
        print("Guardado de archivo por defecto:", ruta_archivo_recorte)
    else :
        ruta_archivo_recorte = str(sys.argv[2])
        print("Nombre de recorte:", ruta_archivo_recorte)

    ## PROCESAMIENTO
    ventana = ImagenOpenCV()
    # ventana = ImagenOpenCV(ruta_archivo_imagen, ruta_archivo_recorte)

    
    # ventana.interfaz_edicion(dimensiones_recorte=[256, 256],escape_teclado=True) # Recorte pequeño
    ventana.interfaz_edicion( ruta_archivo_imagen, ruta_archivo_recorte, escape_teclado=True)    # Tamaño predefinido
    # ventana.interfaz_edicion(dimensiones_recorte=[900, 900],escape_teclado=True) # Recorte demasiado grande


    # # Cierre de ventanas
    # cv2.destroyAllWindows()
    # cv2.destroyWindow(ventana.nombre_ventana)
    ventana.cerrar_ventana()