# Producto Integrador de Aprendizaje, Estructura de datos y su procesamiento.

from collections import namedtuple
import sys
import sqlite3
from sqlite3 import Error
from datetime import date, datetime

# Declaraciones iniciales
separador = ('-' * 45)

print('Bienvenido(a) al negocio de venta de llantas')
print(separador)

def Menu():
    opcion = int(input('Menú de opciones:\n[1] Registrar una venta\n[2] Consultar una venta\n[3] Reporte de ventas de fecha\n[4] Salir y guardar en base de datos (.db)\n» '))
    return opcion