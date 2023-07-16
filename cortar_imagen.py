# Importamos OpenCV
import cv2


# funcion auxiliar: no hace nada
def nothing(x):
    pass


def Redibujar_Imagen(x,y):
    global imagen, copia_imagen,recorte,ancho_recorte,alto_recorte
    # global titulo_imagen
    (alto_imagen, ancho_imagen) = imagen.shape[:2]
    xmax, ymax = ancho_imagen, alto_imagen

    #Se previenen errores por recortes mayores a la imagen de origen
    if ancho_recorte > ancho_imagen : ancho_recorte = ancho_imagen
    if alto_recorte  > alto_imagen  : alto_recorte  = alto_imagen  
    
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
        xf = xmax
        xi = xmax - ancho_recorte
    if yf >= ymax :
        yf = ymax 
        yi = ymax - alto_recorte
    # Actualizacion de la gráfica
    # print(xi,yi,xf,yf)   
    copia_imagen = imagen.copy()
    cv2.rectangle(copia_imagen,(xi,yi),(xf,yf),BGR_marcador,cv2.LINE_4 )
    cv2.imshow(titulo_imagen, copia_imagen)
    # recorte = imagen[yi:yf, xi:xf]
    # cv2.imshow('Recorte', recorte)
    #retorno de cooordenadas para recortar
    return xi, yi, xf, yf


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
        # print(xi, yi, xf, yf )
        cv2.imshow('Recorte', recorte)
        print(f'Dimensiones del recorte: base {recorte.shape[1]}, altura {recorte.shape[0]}')
        # print(xi,yi,xf,yf)        


archivo_imagen = '../Imagenes/at nite.webp'
archivo_imagen = '../Imagenes/2P.jpg'

# ruta de destino (el directorio debe ser preexistente)
archivo_recorte = '../Imagenes/recorte.jpg'

# Título de ventana: nombre del archivo imagen
titulo_imagen = f'Original: {archivo_imagen}'
#color del rectángulo
BGR_marcador=(255,0,200)

# Variables Globales: posición del mouse
x_mouse = y_mouse = 0

# Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
imagen = cv2.imread(archivo_imagen)
copia_imagen = imagen.copy()        #se hace una copia descartable de la imagen
cv2.imshow(titulo_imagen, copia_imagen)

#medidas del recorte (por defecto)
ancho_defecto = 512
alto_defecto  = 512

ancho_recorte = ancho_defecto
alto_recorte = alto_defecto

# se leen las dimensiones de imagen
(alto_imagen, ancho_imagen) = imagen.shape[:2]
if alto_imagen < alto_defecto or ancho_imagen < ancho_defecto:
    print("Cuidado: imagen original muy pequeña") 
print(f'Dimensiones de la imagen original: base {ancho_imagen}, altura {alto_imagen}')

#Manejador del mouse sobre la imagen --> llama a la imagen de dibujar circulos
cv2.setMouseCallback(titulo_imagen,marcar_recorte)

# espera en reposo a que se pulse una tecla del teclado
k = cv2.waitKey(0)

#si la tecla pulsada es 's' se guarda una copia del recorte
if k == ord("s"):
    cv2.imwrite(archivo_recorte, recorte)

# Limpiamos y cerramos
cv2.destroyAllWindows()