import cv2 as cv
import sys
import pathlib 

from sistema_archivos.imagen_editable import crear_directorio_RAM, ImagenEditable




from PIL import Image


def frames2gif( 
    rutas_frames: list[str],  
    ruta_gif: str, 
    intervalo_mseg: int,
    repeticiones: int = 0
    ):
    """Convierte las imágenes elegidas ('frames') en un archivo GIF."""

    imagenes = []

    for ruta in rutas_frames:
        im = Image.open(ruta)
        imagenes.append(im)

    imagenes[0].save(ruta_gif,
                save_all = True, 
                append_images = imagenes[1:], 
                optimize = True, 
                # optimize = False, 
                duration = intervalo_mseg,
                loop = repeticiones # 0: repeticiones a a perpetuidad
                )


def video2gif(
    ruta_video: str,
    ruta_gif: str, 
    intervalo_mseg: int = 25,
    factor_diezmado: int = 1,
    repeticiones: int = 0
    ):
    """Convierte el video elegido en un archivo GIF."""

    T = intervalo_mseg * factor_diezmado

    capturas = cv.VideoCapture(ruta_video)

    # carpeta temporal
    ruta_directorio_frames = "video2gif__"
    directorio_frames = crear_directorio_RAM(ruta_directorio_frames)
    imagenes = []
    i = 0
    extension_frame = ".png"

    while capturas.isOpened():

        ret, frame = capturas.read()
        # el bucle se rompe cuando no haya mas frames en archivo
        if not ret:
            break

        # diezmado de frames
        if i % factor_diezmado == 0 :
            # creacion de archivo en RAM vacio
            frame_archivo = ImagenEditable(
                directorio_frames.name,
                extension_frame,
                prefijo=f"imag{i}_"
                )
            # asignacion de frame a archivo en RAM
            frame_archivo.crear(frame)

            # conversion a datos de Pillow 
            im = Image.open(frame_archivo.ruta)
            # guardado en lista
            imagenes.append(im)
        i += 1

    capturas.release()
    # borrado de carpeta y de archivo interno
    imagenes[0].save(ruta_gif,
                save_all = True, 
                append_images = imagenes[1:], 
                optimize = True, 
                # optimize = False, 
                duration = T,
                loop = repeticiones # 0: repeticiones a a perpetuidad
                )


def video2frames(ruta_video: str,ruta_directorio: str, factor_diezmado: int ):

    capturas = cv.VideoCapture(ruta_video)
    extension = ".png"
    rutas_frames = []
    i = 0
    while capturas.isOpened():

        ret, frame = capturas.read()
        # el bucle se rompe cuando no haya mas frames en archivo
        if not ret:
            break

        nombre = f"imag_{i}" 
        ruta_imagen = pathlib.Path(ruta_directorio).joinpath(nombre).with_suffix(extension)

        ruta_imagen = str(ruta_imagen)

        # diezmado de frames
        if i % factor_diezmado == 0:
            # asignacion de frame a archivo en RAM
            cv.imwrite(ruta_imagen, frame)
            rutas_frames.append(ruta_imagen)
        i += 1
    capturas.release()

    return rutas_frames



if __name__=="__main__":

    if len(sys.argv)>=3:

        factor_diezmado = int(sys.argv[2])
        T = 25 * factor_diezmado

    else: 
        factor_diezmado = 1
        T = 25  # tiempo en ms

    if len(sys.argv)>=2:

        ruta_video = sys.argv[1]

        # carpeta temporal
        ruta_directorio = "editor_gifs__"
        directorio_frames = crear_directorio_RAM(ruta_directorio)

        rutas_frames = video2frames(
            ruta_video,
            directorio_frames.name,
            factor_diezmado
            )

        print("archivos temporales listados")
        print(f"{len(rutas_frames)} frames")

        import time

        print(f"intervalo: {T} mseg")


        i = time.time()
        frames2gif( rutas_frames, "/dev/shm/demo.gif" , T )
        f = time.time()
        print(f-i)

        print("archivo GIF creado")
        directorio_frames.cleanup()
        

        i = time.time()

        video2gif( ruta_video, 
            "/dev/shm/demo_video.gif", 
            factor_diezmado=factor_diezmado, 
            )
        f = time.time()
        print(f-i)

        print("video convertido a GIF")

    else:
        print("Modo de uso:")
        print('py video_gif.py <ruta_video> <factor diezmado [veces]>')
        
