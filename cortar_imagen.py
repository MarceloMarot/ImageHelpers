# Importamos OpenCV
import cv2
import sys

# funcion auxiliar: no hace nada
def nothing(x):
    pass


def Marcar_Rectangulo(x_mouse, y_mouse ,ancho_recorte, alto_recorte):
    # global ancho_recorte,alto_recorte
    (alto_imagen, ancho_imagen) = imagen.shape[:2]           # FIX
    xmax, ymax = ancho_imagen, alto_imagen
    #Se previenen errores por recortes mayores a la imagen de origen
    if ancho_recorte > ancho_imagen : ancho_recorte = ancho_imagen
    if alto_recorte  > alto_imagen  : alto_recorte  = alto_imagen  
    # El puntero del mouse quedará centrado dentro del rectángulo
    xi = x_mouse - ancho_recorte // 2
    yi = y_mouse - alto_recorte // 2
    # Se confina al rectángulo adentro de la imagen
    if xi < 0: 
        xi = 0
    if yi < 0: 
        yi = 0
    xf = xi + ancho_recorte
    yf = yi + alto_recorte
    if xf >= xmax :
        xf = xmax
        xi = xmax - ancho_recorte
    if yf >= ymax :
        yf = ymax 
        yi = ymax - alto_recorte
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
        # actualizacion de graficas y retorno de coordenadas para recortar
        coordenadas_seleccion = Marcar_Rectangulo(x_mouse, y_mouse, ancho_recorte, alto_recorte) 
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
        cv2.imshow(titulo_imagen, copia_imagen)
    # evento click izquierdo --> crear recorte
    if evento == cv2.EVENT_LBUTTONDOWN:
        # actualizacion de graficas y retorno de coordenadas para recortar
        coordenadas_recorte = Marcar_Rectangulo(x_mouse, y_mouse, ancho_recorte, alto_recorte)  
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
        cv2.imshow('Recorte', recorte)
        cv2.imshow(titulo_imagen, copia_imagen)
        



# sys.argv


## APERTURA IMAGEN

archivo_imagen = '../Imagenes/at nite.webp'
archivo_imagen = '../Imagenes/2P.jpg'

# ruta de destino (el directorio debe ser preexistente)
archivo_recorte = '../Imagenes/recorte.jpg'

# Título de ventana: nombre del archivo imagen
titulo_imagen = f'Original: {archivo_imagen}'

# Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
imagen = cv2.imread(archivo_imagen)
copia_imagen = imagen.copy()        #se hace una copia descartable de la imagen
cv2.imshow(titulo_imagen, copia_imagen)

#medidas del recorte (por defecto)
ancho_recorte = 256
alto_recorte = 256


coordenadas_recorte   = [0,0,0,0]
coordenadas_seleccion = [0,0,0,0]


## PROCESAMIENTO
# se leen las dimensiones de imagen
(alto_imagen, ancho_imagen) = imagen.shape[:2]
if alto_imagen < alto_recorte or ancho_imagen < ancho_recorte:
    print("Cuidado: imagen original muy pequeña") 
print(f'Dimensiones de la imagen original: base {ancho_imagen}, altura {alto_imagen}')


# INTERFAZ USUARIO

#Recorte por defecto: arriba a la izquierda
x_mouse=y_mouse=0
param=flags=[]
evento=cv2.EVENT_LBUTTONDOWN
Marcar_Recorte(evento,x_mouse,y_mouse,flags,param)

#Manejador de eventos del mouse sobre la imagen: movimiento cursor y click izquierdo
cv2.setMouseCallback(titulo_imagen,Marcar_Recorte)


# espera en reposo a que se pulse una tecla del teclado
k = cv2.waitKey(0)

#si la tecla pulsada es 's' se guarda una copia del recorte
if k == ord("s"):
    cv2.imwrite(archivo_recorte, recorte)

# Limpiamos y cerramos
cv2.destroyAllWindows()