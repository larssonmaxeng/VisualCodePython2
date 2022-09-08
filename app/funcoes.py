import base64
from email.encoders import encode_base64
import json
from json import *
from app import app
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