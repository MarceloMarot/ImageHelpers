from enum import Enum


class Tab(Enum):
    TAB_GALERIA = 0
    TAB_SELECCION = 1
    TAB_GLOBAL = 2

class Percentil(Enum):
    UMBRAL_1 = 0.2
    UMBRAL_2 = 0.4
    UMBRAL_3 = 0.6
    UMBRAL_4 = 0.8
    UMBRAL_5 = 1

class Estados(Enum):
    "Enumeracion de estados de las imagenes"
    TODOS = "todas"
    GUARDADO = "guardadas"
    MODIFICADO = "modificadas"
    NO_ALTERADO = "no alteradas" 
    DEFECTUOSO = "defectuosas"


tupla_estados = (
    Estados.TODOS.value,
    Estados.GUARDADO.value,
    Estados.MODIFICADO.value,
    Estados.NO_ALTERADO.value,
    Estados.DEFECTUOSO.value,
)
