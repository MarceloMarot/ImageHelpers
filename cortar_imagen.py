# Importamos OpenCV
import cv2
import sys


# Clase para guardar las dimensiones de la imagen
class Dimensiones2D:
    def __init__(self, ancho, alto):
	    self.alto  = alto		
	    self.ancho = ancho


# variables globales 
dimensiones_imagen  = Dimensiones2D(0, 0)    #inicializacion por defecto
dimensiones_recorte = Dimensiones2D(512, 512)    #inicializacion por defecto , apto Stable Diffusion
coordenadas_recorte = [0,0,0,0]
coordenadas_seleccion = [0,0,0,0]


# funcion para abrir la ventana de edición
# la ventana se cierra presionando alguna de las teclas indicadas
def  Interfaz_Edicion(archivo_imagen_original, archivo_imagen_recorte, texto_consola):
    # valores retorno
    exito = False
    tecla = "-"  # Caracter no implementado

    # Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
    global imagen, recorte
    imagen = cv2.imread(archivo_imagen_original)     

    global coordenadas_recorte, coordenadas_seleccion

    # se leen las dimensiones de imagen
    dimensiones_imagen.ancho = imagen.shape[1]
    dimensiones_imagen.alto = imagen.shape[0]

    # se verifica que el recorte se pueda hacer
    ancho_recorte   = dimensiones_recorte.ancho
    alto_recorte    = dimensiones_recorte.alto
    ancho_imagen    = dimensiones_imagen.ancho
    alto_imagen     = dimensiones_imagen.alto
    if texto_consola == True: 
        print(f'Dimensiones de la imagen original  : base {ancho_imagen}, altura {alto_imagen}')
        print(f'Dimensiones de la imagen recortada : base {ancho_recorte}, altura {alto_recorte}')
    if alto_imagen < alto_recorte or ancho_imagen < ancho_recorte:
        if texto_consola == True: print("WARNING: imagen original muy pequeña") 
        exito = False
        tecla = "-"  # Caracter no implementado
        return tecla , exito
    #Recorte por defecto: arriba a la izquierda
    x_mouse=y_mouse=0
    param=flags=[]
    evento=cv2.EVENT_LBUTTONDOWN
    Marcar_Recorte(evento, x_mouse, y_mouse, flags, param)
    #Manejador de eventos del mouse sobre la imagen: movimiento cursor y click izquierdo
    cv2.setMouseCallback('Original',Marcar_Recorte)
    # Conjunto de teclas permitidas
    teclas_programadas = {"a" , "s", "d" ," " }  # Teclas 'A', 'S', 'D', 'SPACE' 
    tecla = "-"  # Caracter no implementado
    if texto_consola: print("Teclas implementadas: ", teclas_programadas )
    while tecla not in teclas_programadas:
        # espera en reposo a que se pulse una tecla del teclado
        k = cv2.waitKey(0)
        tecla = chr(k)  # Conversion de numero a caracter ASCII
        if texto_consola: print("Tecla ingresada: ",tecla)
    #si la tecla pulsada es 's' se guarda una copia del recorte
    if k == ord("s"):
        guardado_correcto = cv2.imwrite(archivo_imagen_recorte, recorte)
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


def Marcar_Rectangulo(x_mouse, y_mouse ):

    x_recorte = dimensiones_recorte.ancho
    y_recorte = dimensiones_recorte.alto

    x_max = dimensiones_imagen.ancho
    y_max = dimensiones_imagen.alto

    #Se previenen errores por recortes mayores a la imagen de origen
    if x_recorte > x_max : x_recorte = x_max
    if y_recorte > y_max : y_recorte  = y_max  
    # El puntero del mouse quedará centrado dentro del rectángulo
    xi = x_mouse - x_recorte // 2
    yi = y_mouse - y_recorte // 2
    # Se confina al rectángulo adentro de la imagen
    if xi < 0: 
        xi = 0
    if yi < 0: 
        yi = 0
    xf = xi + x_recorte
    yf = yi + y_recorte
    if xf >= x_max :
        xf = x_max
        xi = x_max - x_recorte
    if yf >= y_max :
        yf = y_max 
        yi = y_max - y_recorte
    #retorno de cooordenadas para recortar, en una lista
    return [xi, yi, xf, yf]


# funcion para ubicar el recorte de imagen deseado
def Marcar_Recorte(evento,x_mouse,y_mouse,flags,param):
    #en esta funcion se usan solo los primeros tres parametros:
    # - evento del mouse
    # - posicion x del mouse
    # - posicion y del mouse
    global imagen, recorte
    global coordenadas_recorte, coordenadas_seleccion
    # Colores rectangulo
    BGR_seleccion = (200,0,150)              #magenta
    BGR_recorte   = (100,150,0)              #verde oscuro
    # evento click izquierdo --> actualizar seleccion
    if evento == cv2.EVENT_MOUSEMOVE:
        # actualizacion de graficas y retorno de coordenadas de seleccion
        coordenadas_seleccion = Marcar_Rectangulo(x_mouse, y_mouse) 
        xi = coordenadas_seleccion[0]  
        xf = coordenadas_seleccion[2]  
        yi = coordenadas_seleccion[1] 
        yf = coordenadas_seleccion[3]  
        # Actualizacion de la gráfica  
        copia_imagen = imagen.copy()
        #color del rectángulo
        color_rectangulo = BGR_seleccion
        if coordenadas_seleccion == coordenadas_recorte :
            color_rectangulo = BGR_recorte
        cv2.rectangle(copia_imagen,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
        cv2.imshow('Original', copia_imagen)                
    # evento click izquierdo --> crear recorte
    if evento == cv2.EVENT_LBUTTONDOWN:
        # actualizacion de graficas y retorno de coordenadas ya recortadas
        coordenadas_recorte = Marcar_Rectangulo(x_mouse, y_mouse) 
        xi = coordenadas_recorte[0]  
        xf = coordenadas_recorte[2]  
        yi = coordenadas_recorte[1] 
        yf = coordenadas_recorte[3] 
        # Actualizacion de la gráfica
        copia_imagen = imagen.copy()
        #color del rectángulo
        color_rectangulo = BGR_recorte
        cv2.rectangle(copia_imagen,(xi,yi),(xf,yf),color_rectangulo,cv2.LINE_4 )
        recorte = imagen[yi:yf, xi:xf]
        # cv2.imshow('Recorte', recorte)            # imagen adicional
        cv2.imshow('Original', copia_imagen)                
        

# Rutina de prueba: Apertura de imagenes
# Uso:
# python cortar_imagen.py <ruta_imagen_original> <ruta_imagen_salida>
# Si faltan parámetros estos se sustituyen por valores predefinidos
if __name__ == "__main__" :

    ## APERTURA IMAGEN
    if len(sys.argv) == 1 :
        #imagenes por defecto 
        archivo_imagen = '../Imagenes/at nite.webp'
        archivo_imagen = '../Imagenes/2P.jpg'
        print("Apertura de archivo de ejemplo:", archivo_imagen)
    else :
        archivo_imagen = str(sys.argv[1])
        print("Apertura de archivo indicado:", archivo_imagen)

    if len(sys.argv) < 3 :
        # ruta de destino (el directorio debe ser preexistente)
        archivo_recorte = '../Imagenes/recortes/recorte.jpg'
        # archivo_recorte = '../Imagenes/HOLAH/recorte.jpg'
        print("Guardado de archivo por defecto:", archivo_recorte)
    else :
        archivo_recorte = str(sys.argv[2])
        print("Nombre de recorte:", archivo_recorte)

    # Ventana de recorte fija
    dimensiones_recorte.ancho = 256 
    dimensiones_recorte.alto  = 256 

    ## PROCESAMIENTO
    Interfaz_Edicion(archivo_imagen , archivo_recorte, True)
    # Interfaz_Edicion(archivo_imagen , archivo_recorte, False)

    # # Limpiamos y cerramos
    cv2.destroyAllWindows()

