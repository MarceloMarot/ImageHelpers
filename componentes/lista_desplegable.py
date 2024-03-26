import flet as ft


tupla_resoluciones = (
    "---------",
    "512 x 512",
    "512 x 768",
    "768 x 512",
    "768 x 768",
    "1024 x 1024",
)


def extraer_numeros(texto_entrada: str)->list[int]:
    """Extrae una lista de numeros a partir de un texto.
    Presupone que los numeros estan separados por espacios vacios"""
    numeros = []
    for texto in texto_entrada.split():
        if texto.isnumeric():
            numeros.append(int(texto)) 
    return numeros 


def convertir_dimensiones_opencv(texto_entrada: str)-> tuple[int, int, int]|None:
    """Convierte el texto en una tupla numerica con las dimensiones de imagen.
    El orden es : altura, base, nº canales.
    Si hay algun error se devuelve None."""
    numeros = extraer_numeros(texto_entrada)
    if len(numeros) == 2:
        ancho = numeros[0]
        alto = numeros[1]
        numeros = [alto, ancho]     # orden de dimensiones segun OpenCV
        numeros.append(3)   # asumimos imagenes color (tres canales)
        return tuple(numeros)

    elif len(numeros) == 0:
        return None


def crear_lista_desplegable( opciones: tuple | list, ancho = 150, alto = 50):
    """Esta función crea el componente gráfico con las opciones seleccinadas"""
    lista_desplegable = ft.Dropdown(
        width=ancho,
        height=alto,
        # text_size=12,
    )
    # asignacion de opciones internas
    opciones_lista_desplegable(lista_desplegable, opciones)

    return lista_desplegable


def opciones_lista_desplegable(componente: ft.Dropdown, opciones: tuple | list):
    opciones_desplegables = []
    for opcion in opciones:
        valor = opcion
        opciones_desplegables.append( ft.dropdown.Option(valor) )

    # asignacion lista
    componente.options = opciones_desplegables



def main(page: ft.Page):

    def cambio_opcion(e):
        numeros = extraer_numeros( str(lista_desplegable.value) )
        if len(numeros)==2:
            [ancho, alto ] = numeros
            print(f"Base: {ancho}; Altura: {alto}")
            caja_texto.value = f"Base: {ancho}; Altura: {alto}"
        else: 
            print("---------")
            caja_texto.value = "---------"
        caja_texto.update()


    caja_texto = ft.Text()

    lista_desplegable = crear_lista_desplegable(tupla_resoluciones)
    lista_desplegable.on_change = cambio_opcion


    page.add(lista_desplegable,  caja_texto)
    # lista_desplegable.focus()
    lista_desplegable.update()



if __name__=="__main__":
    ft.app(target=main)
