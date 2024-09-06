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
    "Eumeracion de estados de las imagenes"
    TODOS = "todas"
    GUARDADOS = "guardadas"
    MODIFICADOS = "modificadas"
    NO_ALTERADOS = "no alteradas" 
    DEFECTUOSOS = "defectuosas"


tupla_estados = (
    Estados.TODOS.value,
    Estados.GUARDADOS.value,
    Estados.MODIFICADOS.value,
    Estados.NO_ALTERADOS.value,
    Estados.DEFECTUOSOS.value,
)
