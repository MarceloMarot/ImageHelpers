# Importamos OpenCV
import cv2
import sys
import numpy as np


class ImagenOpenCV:
    def __init__(self, ruta_original: str = "",ruta_recorte: str = "recorte.jpg"):
        self.ruta_imagen_original = ruta_original
        self.ruta_imagen_recorte  = ruta_recorte
        # # variables globales 
        self.coordenadas_recorte = [0,0,0,0]
        self.coordenadas_seleccion = [0,0,0,0]
        self.escala_minima = 100     #inicializacion por defecto 
        self.escala_maxima = 200     #inicializacion por defecto 
        self.x_mouse = 0
        self.y_mouse = 0
        self.dimensiones_recorte = [0, 0]
        self.imagen_original = cv2.imread(ruta_original)
        self.imagen_escalada = self.imagen_original.copy()
        self.imagen_recorte = None
        self.nombre_ventana = "Ventana"
        self.color_seleccion = (200,0,150)  # magenta
        self.color_recorte   = (100,150,0)  # verde oscuro


    # Manejador para controlar el tamaño de la imagen
    def actualizar_proporcion(self, x):
        """Este manejador actualiza el tamaño de imagen y su ventana gráfica con los cambios de la barra deslizante."""
        global imagen_original, imagen_escalada
        # global x_mouse, y_mouse 
        porcentaje = cv2.getTrackbarPos('Escala', self.nombre_ventana)
        proporcion = porcentaje / 100
        # print("Escala: ",proporcion," ; Porcentaje : ",porcentaje )
        # self.imagen_escalada = redimensionar_imagen(self.imagen_original, proporcion)
        # self.imagen_escalada = self.redimensionar_imagen(proporcion)
        self.redimensionar_imagen(proporcion)
        # Actualizacion gráfica
        evento = cv2.EVENT_MOUSEMOVE
        # [x_mouse, y_mouse] = self.coordenadas_mouse
        self.marcar_recorte(evento, self.x_mouse, self.y_mouse,None,None)


    # funcion para ubicar y mostrar el recorte de imagen deseado
    def marcar_recorte(self, evento,x_mouse,y_mouse,flags,param):
        """Este handler recibe los eventos del mouse y se encarga de marcar el recorte y guardarlo de ser requerido. """
        #en esta funcion se usan solo los primeros tres parametros:
        # - evento del mouse
        # - posicion x del mouse
        # - posicion y del mouse
        # global imagen_escalada, recorte
        # global coordenadas_recorte, coordenadas_seleccion
        # global dimensiones_recorte
        # global x_mouse, y_mouse
        self.x_mouse = x_mouse
        self.y_mouse = y_mouse
        # mouse = [x_mouse, y_mouse]

        # dim_recorte = [self.imagen_recorte.shape[1], self.imagen_recorte.shape[0]]

        # Colores rectangulo
        # BGR_seleccion = (200,0,150)              #magenta
        # BGR_recorte   = (100,150,0)              #verde oscuro
        BGR_seleccion = self.color_seleccion
        BGR_recorte   = self.color_recorte
        # evento click izquierdo --> actualizar seleccion
        if evento == cv2.EVENT_MOUSEMOVE:
            # Actualizacion de graficas y retorno de coordenadas de seleccion
            # Si la posicion de la seleccion es la misma del recorte no se cambia de color
            if self.coordenadas_recorte == self.coordenadas_seleccion: 
                [imagen , coordenadas] = self.calcular_rectangulo( ) 
                self.ventana_imagen(coordenadas, BGR_recorte )  
            else:
                [imagen , coordenadas] = self.calcular_rectangulo( )
                self.ventana_imagen(coordenadas, BGR_seleccion )  
            # Sólo se registran las coordenadas del recorte 
            self.coordenadas_seleccion = coordenadas
        # evento click izquierdo --> crear recorte
        if evento == cv2.EVENT_LBUTTONDOWN:
            # Actualizacion de graficas y retorno del recorte y sus coordenadas
            [self.imagen_recorte, self.coordenadas_recorte] = self.calcular_rectangulo( )
            self.ventana_imagen(self.coordenadas_recorte, BGR_recorte )   


    # Funcion para redimencionar la imagen  de entrada sin alterar las proporciones
    # def redimensionar_imagen(imagen, escala):
    def redimensionar_imagen(self, escala):
        """Esta funcion crea una copia de la imagen de entrada ampliada o reducida en el factor de escala ingresado."""
        # la escala es relativa a las dimensiones de la imagen
        # escala > 1 : ampliacion
        # escala < 1 : reduccion 
        anchura = self.imagen_original.shape[1] * escala
        altura  = self.imagen_original.shape[0] * escala

        # Prevencion de errores por entrada de numeros flotantes
        anchura = int( anchura )
        altura  = int( altura  )
        # Se usa la interpolacion más lenta pero de mejor calidad
        dimensiones = (anchura, altura)
        # imagen_ampliada = cv2.resize(self.imagen_original, dimensiones , interpolation = cv2.INTER_LANCZOS4) 
        self.imagen_escalada = cv2.resize(self.imagen_original, dimensiones , interpolation = cv2.INTER_LANCZOS4) 
        # imagen_ampliada = cv2.resize(imagen,dimensiones , interpolation = cv2.INTER_AREA) 
        # return imagen_ampliada



    def ventana_imagen(self,
        # imagen, 
        coordenadas_rectangulo: list[int]|tuple[int], 
        color_rectangulo: list[int,int,int]|tuple[int,int,int], 
        # nombre_ventana: str 
        ):
        """función grafica: actualiza la ventana de imagen y le dibuja un rectángulo encima con las coordenadas indicadas"""
        # marcado del rectangulo sobre una copia de la imagen para no dañar la original
        # copia = imagen.copy()
        copia = self.imagen_escalada.copy()
        (xi,yi) = coordenadas_rectangulo[0:2]
        (xf,yf) = coordenadas_rectangulo[2:4]

        cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        # cv2.namedWindow(self.nombre_ventana, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL )
        cv2.imshow(self.nombre_ventana, copia) 
        # cv2.resizeWindow(self.nombre_ventana, 768,1024) 
        # cv2.resizeWindow(	winname, size	) 





    def calcular_rectangulo(self):  
        """Funcion creada para calcular el rectángulo de seleccion de modo de evitar desbordes"""
        # x_mouse, y_mouse = pos_mouse
        # [x_mouse, y_mouse] = self.coordenadas_mouse
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
        return [recorte_imagen , coordenadas]


    def interfaz_edicion(self, ancho_recorte=512, alto_recorte=512, texto_consola=True ):
        """Funcion para abrir la ventana de edición. La ventana se cierra presionando alguna de las teclas indicadas. 
        Por defecto se elije un tamaño de recorte de 512 x 512, que es el exigido por Stable Diffusion"""""
        # valores retorno
        exito = False
        tecla = "-"  # Caracter no implementado
        # Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
        # global escala_minima,escala_maxima
        # global imagen_original,imagen_escalada, recorte

        self.dimensiones_recorte = [ancho_recorte, alto_recorte]

        self.imagen_original = cv2.imread(self.ruta_imagen_original)    
        # se leen las dimensiones de imagen y de recorte

        # asignacion por defecto: NO ampliar ni reducir imagen de entrada
        # self.imagen_ampliada
        imagen_escalada = self.imagen_original
        #creacion recorte vacio
        self.imagen_recorte = np.zeros((alto_recorte,ancho_recorte,3), np.uint8)


        # cv2.namedWindow(self.nombre_ventana, cv2.WINDOW_NORMAL )
        # cv2.namedWindow(self.nombre_ventana, cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow(self.nombre_ventana, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL )
        cv2.resizeWindow(self.nombre_ventana, 768,768) 
        # k = cv2.waitKey(0)


        # se verifica que el recorte se pueda hacer
        ancho_imagen    = imagen_escalada.shape[1]
        alto_imagen     = imagen_escalada.shape[0]
        if texto_consola == True: 
            print(f'Dimensiones de la imagen original  : base {ancho_imagen}, altura {alto_imagen}')
            print(f'Dimensiones de la imagen recortada : base {ancho_recorte}, altura {alto_recorte}')
        #se calcula la esala minima que puede tener la imagen de modo de permitir el recorte
        if alto_imagen / alto_recorte > ancho_imagen / ancho_recorte : proporcion =  ancho_recorte / ancho_imagen 
        else : proporcion =  alto_recorte / alto_imagen 
        escala_minima = int( proporcion * 100 ) #porcentaje minimo de escalado (normalmente es menor al 100%)
        escala_minima += 1  # excedente del 1% para prevencion de imagenes demasiado chicas
        # Si la imagen es demasiado chica se amplía, sustituyendo a la original
        # if alto_imagen < alto_recorte or ancho_imagen < ancho_recorte:
        if proporcion > 1:
            if texto_consola == True: print("WARNING: imagen original muy pequeña") 
            # escala_minima = int( proporcion * 100) #porcentaje minimo de escalado
            # escala_minima += 1  # excedente del 1% para prevencion de imagenes demasiado chicas
            self.escala_maxima = int( proporcion * 200) #porcentaje maximo de escalado
            self.redimensionar_imagen( proporcion)
            # imagen_escalada = self.redimensionar_imagen( proporcion)
            if texto_consola == True: 
                print("Proporción de reescalado: ", proporcion) 
                print(f'Dimensiones de la imagen ampliada  : base {ancho_imagen}, altura {alto_imagen}')
            #Vieja rutina: fin del programa
            # if texto_consola == True: print("Operación interrumpida") 
            # exito = False
            # tecla = "-"  # Caracter no implementado
            # return tecla , exito
        #Recorte por defecto: arriba a la izquierda
        # x_mouse=y_mouse=0


        #Manejador de eventos del mouse sobre la imagen: movimiento cursor y click izquierdo
        evento = cv2.EVENT_LBUTTONDOWN
        self.marcar_recorte(evento, self.x_mouse, self.y_mouse, None, None)
        cv2.setMouseCallback(self.nombre_ventana, self.marcar_recorte)


        # Barra de reescalado de imagen
        if escala_minima > 100: escala_defecto = escala_minima
        else: escala_defecto = 100
        cv2.createTrackbar('Escala', self.nombre_ventana, escala_defecto , self.escala_maxima , self.actualizar_proporcion)
        cv2.setTrackbarMin('Escala', self.nombre_ventana, escala_minima	) 
        # Conjunto de teclas permitidas
        teclas_programadas = {"a" , "s", "d" ," " }  # Teclas 'A', 'S', 'D', 'SPACE' 
        tecla = "-"  # Caracter no implementado
        if texto_consola: print("Teclas implementadas: ", teclas_programadas )
        while tecla not in teclas_programadas:
            # espera en reposo a que se pulse una tecla del teclado
            k = cv2.waitKey(0)
            tecla = chr(k)  # Conversion de numero a caracter ASCII
            if texto_consola: print("Tecla ingresada: ",tecla)

        #### CORREGIR INDENTADO
        #si la tecla pulsada es 's' se guarda una copia del recorte
        if k == ord("s"):
            guardado_correcto = cv2.imwrite(self.ruta_imagen_recorte, self.imagen_recorte)
            if guardado_correcto == True :
                if texto_consola: print("¡Recorte guardado!")
                exito = True
                return tecla, exito
            else:
                if texto_consola: print("WARNING: Guardado fallido")
                exito = False
                return tecla, exito
        else: 
            # Retorno de tecla ingresada
            # exito = True
            return tecla, exito





    
        


# Rutina de prueba: Apertura de imagenes
# Uso:
# python cortar_imagen.py <ruta_imagen_original> <ruta_imagen_salida>
# Si faltan parámetros estos se sustituyen por valores predefinidos
if __name__ == "__main__" :

    ## APERTURA IMAGEN
    if len(sys.argv) == 1 :
        #imagenes por defecto 
        # archivo_imagen = '../Imagenes/at nite.webp'
        # archivo_imagen = '../Imagenes/saber in lake.webp'
        # archivo_imagen = '../Imagenes/2P.jpg'
        ruta_archivo_imagen = '00be5530-746a-42ad-a68a-9a40d6dda951.webp'
        # archivo_imagen = [
        #     '00be5530-746a-42ad-a68a-9a40d6dda951.webp',
        #     '468e6eb8-7668-4fd2-9a7d-c6021c7e690e.webp',
        #     '5d6bfe83-57b4-4934-bc5e-ef92034d4f1d.webp'
        #     ]


        print("Apertura de archivo de ejemplo:", ruta_archivo_imagen)
    else :
        ruta_archivo_imagen = str(sys.argv[1])
        print("Apertura de archivo indicado:", ruta_archivo_imagen)

    if len(sys.argv) < 3 :
        # ruta de destino (el directorio debe ser preexistente)
        ruta_archivo_recorte = 'recorte.webp'
        # archivo_recorte = '../Imagenes/HOLAH/recorte.jpg'
        print("Guardado de archivo por defecto:", ruta_archivo_recorte)
    else :
        ruta_archivo_recorte = str(sys.argv[2])
        print("Nombre de recorte:", ruta_archivo_recorte)

    ## PROCESAMIENTO
    ventana = ImagenOpenCV(ruta_archivo_imagen, ruta_archivo_recorte)
    ventana.interfaz_edicion( 512 ,512, True)    # Recorte pequeño
    # interfaz_edicion(ruta_archivo_imagen , archivo_recorte, False , 512,512)    # Recorte pequeño
    # interfaz_edicion(ruta_archivo_imagen , archivo_recorte, True, 800,800)       # Recorte demasiado grande
    # interfaz_edicion(ruta_archivo_imagen , archivo_recorte, True)              # Tamaño predefinido
    # interfaz_edicion(ruta_archivo_imagen , archivo_recorte)             # Tamaño predefinido, sin mensajes extra

    # # Cierre de ventanas
    cv2.destroyAllWindows()
    
    # interfaz_edicion(ruta_archivo_imagen , archivo_recorte, True, 512,512)    # Recorte pequeño
    # cv2.destroyAllWindows()

