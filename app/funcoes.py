import base64
from email.encoders import encode_base64
import json
from json import *
import matplotlib.pyplot as mlt
import numpy as np
from time import sleep
import io

def Desfuzzificar(nota):
        match nota:
            case "Ruim":
                return 2
            case "Medio":
                return 5
            case "Bom":
                return 8
def incrementarPontoDeOrigem(pontoAtual, distanciaX):
    lista = list(pontoAtual)
    lista[0] = lista[0] + distanciaX + 0.5
    return tuple(lista)
                    