# Importamos OpenCV
import cv2
import sys
import numpy as np


# # variables globales 
coordenadas_recorte = [0,0,0,0]
coordenadas_seleccion = [0,0,0,0]
escala_minima = 100     #inicializacion por defecto 
escala_maxima = 200     #inicializacion por defecto 
xmouse = ymouse =0


# Manejador para controlar el tamaño de la imagen
def Actualizar_Proporcion(x):
    global imagen_original,imagen_escalada
    global xmouse, ymouse 
    porcentaje = cv2.getTrackbarPos('Escala'  , 'Original')
    proporcion = porcentaje / 100
    # print("Escala: ",proporcion," ; Porcentaje : ",porcentaje )
    imagen_escalada = Redimensionar_Imagen(imagen_original, proporcion)
    # Actualizacion gráfica
    evento = cv2.EVENT_MOUSEMOVE
    Marcar_Recorte(evento, xmouse, ymouse, [],[] )
    return


# Funcion para redimencionar la imagen  de entrada sin alterar las proporciones
def Redimensionar_Imagen(imagen, escala):
    # la escala es relativa a las dimensiones de la imagen
    # escala > 1 : ampliacion
    # escala < 1 : reduccion 
    anchura = imagen.shape[1] * escala
    altura  = imagen.shape[0] * escala

    #     # FIX IT !!!
    # #correccion proporcional de los tamaños
    # if alto_imagen < alto_recorte:
    #     proporcion = alto_recorte / alto_imagen
    #     ancho_imagen *= proporcion
    #     ancho_imagen = int(ancho_imagen)
    #     alto_imagen = alto_recorte
    # if ancho_imagen < ancho_recorte:
    #     proporcion = ancho_recorte / ancho_imagen
    #     alto_imagen *= proporcion
    #     alto_imagen = int( alto_imagen)
    #     ancho_imagen = ancho_recorte

    # Prevencion de errores por entrada de numeros flotantes
    anchura= int(anchura )
    altura = int(altura  )

    # Se usa la interpolacion más lenta pero de mejor calidad
    dimensiones = (anchura, altura)
    imagen_ampliada = cv2.resize(imagen,dimensiones , interpolation = cv2.INTER_LANCZOS4) 
    return imagen_ampliada


# funcion para abrir la ventana de edición
# la ventana se cierra presionando alguna de las teclas indicadas
# por defecto se elije un tamaño de recorte de 512 x 512, que es el exigido por Stable Diffusion
def  Interfaz_Edicion(archivo_imagen_original, archivo_imagen_recorte, texto_consola=False , ancho_recorte=512, alto_recorte=512 ):
    # valores retorno
    exito = False
    tecla = "-"  # Caracter no implementado
    # Leemos la imagen de entrada, la mostramos e imprimimos sus dimensiones.
    global escala_minima,escala_maxima
    global imagen_original,imagen_escalada, recorte
    imagen_original = cv2.imread(archivo_imagen_original)    
    # se leen las dimensiones de imagen y de recorte

    # asignacion por defecto: NO ampliar ni reducir imagen de entrada
    imagen_escalada = imagen_original
    #creacion recorte vacio
    recorte= np.zeros((alto_recorte,ancho_recorte,3), np.uint8)
    # print(f"ALTO: {recorte.shape[0]} , ANCHO: {recorte.shape[1]}")

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
        escala_maxima = int( proporcion * 200) #porcentaje maximo de escalado
        imagen_escalada = Redimensionar_Imagen(imagen_original, proporcion)
        if texto_consola == True: print("Proporción de reescalado: ", proporcion) 
        print(f'Dimensiones de la imagen ampliada  : base {ancho_imagen}, altura {alto_imagen}')
        #Vieja rutina: fin del programa
        # if texto_consola == True: print("Operación interrumpida") 
        # exito = False
        # tecla = "-"  # Caracter no implementado
        # return tecla , exito
    #Recorte por defecto: arriba a la izquierda
    x_mouse=y_mouse=0

    param=flags=[]
    evento=cv2.EVENT_LBUTTONDOWN
    Marcar_Recorte(evento, x_mouse, y_mouse, flags, param)

    #Manejador de eventos del mouse sobre la imagen: movimiento cursor y click izquierdo
    cv2.setMouseCallback('Original', Marcar_Recorte)

    # Barra de reescalado de imagen
    if escala_minima > 100: escala_defecto = escala_minima
    else: escala_defecto = 100
    cv2.createTrackbar('Escala', 'Original', escala_defecto , escala_maxima , Actualizar_Proporcion)
    cv2.setTrackbarMin('Escala', 'Original', escala_minima	) 
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


# Funcion creada para calcular el rectángulo de seleccion de modo de evitar desbordes
def Calcular_Rectangulo(pos_mouse,dim_recorte, imagen, color_rectangulo ):

    x_mouse, y_mouse = pos_mouse
    # lectura de dimensiones
    [x_recorte, y_recorte] = dim_recorte
    x_max = imagen.shape[1]
    y_max = imagen.shape[0]
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
    # creacion del recorte de imagen
    recorte_imagen = imagen[yi:yf, xi:xf]
    # marcado del rectangulo sobre una copia de la imagen para no dañar la original
    copia = imagen.copy()
    cv2.rectangle(copia,(xi,yi),(xf,yf),color_rectangulo ,cv2.LINE_4 )
    cv2.imshow('Original',copia) 
    #retorno de cooordenadas para recortar, en una lista
    return [recorte_imagen ,[xi, yi, xf, yf]]


# funcion para ubicar y mostrar el recorte de imagen deseado
def Marcar_Recorte(evento,x_mouse,y_mouse,flags,param):
    #en esta funcion se usan solo los primeros tres parametros:
    # - evento del mouse
    # - posicion x del mouse
    # - posicion y del mouse
    mouse = [x_mouse, y_mouse]
    global imagen_escalada, recorte
    global coordenadas_recorte, coordenadas_seleccion
    # global dimensiones_recorte
    global xmouse, ymouse
    xmouse = x_mouse
    ymouse = y_mouse

    dim_recorte = [recorte.shape[1], recorte.shape[0]]

    # Colores rectangulo
    BGR_seleccion = (200,0,150)              #magenta
    BGR_recorte   = (100,150,0)              #verde oscuro
    # evento click izquierdo --> actualizar seleccion
    if evento == cv2.EVENT_MOUSEMOVE:
        # Actualizacion de graficas y retorno de coordenadas de seleccion
        # Si la posicion de la seleccion es la misma del recorte no se cambai de color
        if coordenadas_recorte == coordenadas_seleccion: 
            retorno = Calcular_Rectangulo(mouse, dim_recorte, imagen_escalada, BGR_recorte ) 
        else:
            retorno = Calcular_Rectangulo(mouse, dim_recorte, imagen_escalada, BGR_seleccion )
        # Sólo se registran las coordenadas del recorte 
        coordenadas_seleccion = retorno[1]
    # evento click izquierdo --> crear recorte
    if evento == cv2.EVENT_LBUTTONDOWN:
        # Actualizacion de graficas y retorno del recorte y sus coordenadas
        [recorte , coordenadas_recorte]= Calcular_Rectangulo(mouse, dim_recorte, imagen_escalada, BGR_recorte )   
        # print(f"flags: {flags} {type(flags)} ||| param: {param} {type(param)}")     
        


# Rutina de prueba: Apertura de imagenes
# Uso:
# python cortar_imagen.py <ruta_imagen_original> <ruta_imagen_salida>
# Si faltan parámetros estos se sustituyen por valores predefinidos
if __name__ == "__main__" :

    ## APERTURA IMAGEN
    if len(sys.argv) == 1 :
        #imagenes por defecto 
        # archivo_imagen = '../Imagenes/at nite.webp'
        archivo_imagen = '../Imagenes/saber in lake.webp'
        # archivo_imagen = '../Imagenes/2P.jpg'
        archivo_imagen = '../Imagenes/2P en bosque.webp'
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

    ## PROCESAMIENTO
    Interfaz_Edicion(archivo_imagen , archivo_recorte, True, 512,512)    # Recorte pequeño
    # Interfaz_Edicion(archivo_imagen , archivo_recorte, True, 800,800)       # Recorte demasiado grande
    # Interfaz_Edicion(archivo_imagen , archivo_recorte, True)              # Tamaño predefinido
    # Interfaz_Edicion(archivo_imagen , archivo_recorte)             # Tamaño predefinido, sin mensajes extra

    # # Cierre de ventanas
    cv2.destroyAllWindows()

