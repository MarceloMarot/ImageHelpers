# Importamos OpenCV
import cv2

import numpy as np

ruta_imagen = '../Imagenes/at nite.webp'
ruta_imagen = '../Imagenes/2P.png'

# ruta de destino (el directorio debe ser preexistente)
archivo_recorte = '../Imagenes/recorte.jpg'



def redibujar_X(a):
    global x_mouse, y_mouse
    Redibujar_Imagen(x_mouse,y_mouse)


def redibujar_Y(b):
    global x_mouse, y_mouse
    Redibujar_Imagen(x_mouse,y_mouse)


def Redibujar_Imagen(x,y):
    global imagen, copia_imagen,recorte
    # global titulo_imagen
    (alto_imagen, ancho_imagen) = imagen.shape[:2]
    (xmax, ymax) = ancho_imagen, alto_imagen
    ancho_recorte = cv2.getTrackbarPos('Ancho'  ,titulo_imagen)
    alto_recorte  = cv2.getTrackbarPos('Altura' ,titulo_imagen) 
    # El puntero del mouse quedará centrado dentro del rectángulo
    xi = x - ancho_recorte // 2
    yi = y - alto_recorte // 2
    # Se confina al rectángulo adentro de la imagen
    if xi < 0: 
        xi = 0
    if yi < 0: 
        yi = 0
    xf = xi + ancho_recorte
    yf = yi + alto_recorte
    if xf >= xmax :
        xf = xmax - 1
        xi = xf - ancho_recorte
    if yf >= ymax :
        yf = ymax - 1
        yi = yf - alto_recorte
    # Actualizacion de la gráfica
    # print(xi,yi,xf,yf)   
    copia_imagen = imagen.copy()
    cv2.rectangle(copia_imagen,(xi,yi),(xf,yf),BGR_marcador,cv2.LINE_4 )
    cv2.imshow(titulo_imagen, copia_imagen)
    # recorte = imagen[yi:yf, xi:xf]
    # cv2.imshow('Recorte', recorte)
    #retorno de cooordenadas para recortar
    return xi, yi, xf, yf


# funcion auxiliar: no hace nada
def nothing(x):
    pass


# funcion para ubicar el recorte de imagen deseado
def marcar_recorte(evento,x,y,flags,param):
    #en esta funcion se usan solo los primeros tres parametros:
    # - evento del mose
    # - posicion x del mouse
    # - posicion y del mouse
    global x_mouse, y_mouse
    x_mouse = x
    y_mouse = y
    global imagen, recorte
    # Cuando el puntero del mouse se mueve dentro de la imagen debe dibujarse el rectángulo de seleccion
    xi, yi, xf, yf = Redibujar_Imagen(x,y) 
    if evento == cv2.EVENT_MOUSEMOVE:
        # actualizacion de graficas y retorno de coordenadas para recortar
        xi, yi, xf, yf = Redibujar_Imagen(x,y)  
    # evento click izquierdo --> crear recorte
    if evento == cv2.EVENT_LBUTTONDOWN:
        recorte = imagen[yi:yf, xi:xf]
        cv2.imshow('Recorte', recorte)
        # print(xi,yi,xf,yf)        



titulo_imagen = f'Original: {ruta_imagen}'
#color del rectángulo
BGR_marcador=(255,0,200)

x_mouse = y_mouse = 0

# Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
imagen = cv2.imread(ruta_imagen)
copia_imagen = imagen.copy()        #se hace una copia descartable de la imagen
cv2.imshow(titulo_imagen, copia_imagen)

#medidas del recorte (por defecto)
ancho_defecto = 256
alto_defecto  = 256

# se leen las dimensiones de imagen
(alto_imagen, ancho_imagen) = imagen.shape[:2]
print(f'Dimensiones de la imagen original: base {ancho_imagen}, altura {alto_imagen}')

# se crean las barras deslizantes
# también se ordena la rutina de actualizacion de imagen cada vez que se deslizan la barran
cv2.createTrackbar('Altura',titulo_imagen,alto_defecto ,alto_imagen ,redibujar_Y)
cv2.createTrackbar('Ancho' ,titulo_imagen,ancho_defecto,ancho_imagen,redibujar_X)

#Manejador del mouse sobre la imagen --> llama a la imagen de dibujar circulos
cv2.setMouseCallback(titulo_imagen,marcar_recorte)

# espera en reposo a que se pulse una tecla del teclado
k = cv2.waitKey(0)

#si la tecla pulsada es 's' se guarda una copia del recorte
if k == ord("s"):
    cv2.imwrite(archivo_recorte, recorte)

# Limpiamos y cerramos
cv2.destroyAllWindows()