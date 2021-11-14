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
    while True:
        opcion = input('Menú de opciones:\n[1] Registrar una venta\n[2] Consultar venta(s) de un día específico\n[3] Salir\n» ')
        try:
            int(opcion)
            if 1 <= int(opcion) <= 3:
                break # La validación es correcta
            else:
                print("\nError #2: Introduzca un número de entre 1 y 3")
                print(separador)
        except ValueError:
            try:
                float(opcion)
                print("test")
            except ValueError:
                print("\nError #1: Introduzca un número")
                print(separador)
    return opcion

def RegistrarVenta():
    ListaVentas=[]
    print('\n--------- Registro de venta ---------')

    fecha = input('Introduzca la fecha de venta (ej. 10/10/2021)\n» ')
    while True:
        folio = int(input(f'Introduzca folio de venta de Llanta(s)\n» '))

        if folio in DiccionarioVentas.keys():
            print('Error, ya existe una venta con ese folio de venta')
        else:
            break

    while True:
        descripcion = input('Introduzca descripción del tipo de Llanta\n» ')
        cantidadVenta = int(input('Introduzca cantidad a vender del tipo de Llanta mencionado\n» '))
        precioVenta = float(input('Introduzca precio (sin iva) del tipo de Llanta (por unidad)\n» $'))
        print(separador)
        subtotal = (cantidadVenta * precioVenta)
        print(f'Subtotal (sin iva) de las Llanta tipo {descripcion}:','${:.2f}'.format(subtotal))
        print(separador)
        """organizacionVenta = Venta(descripcion,cantidadVenta, precioVenta, fecha)
        ListaVentas.append(organizacionVenta)
        DiccionarioVentas[folio] = ListaVentas"""
        agregaOtroLlantaMismaVenta = int(input('¿Desea agregar otra(s) venta(s) de Llanta(s) a la misma venta?\n[1] Si \n[2] No\n» '))

        if agregaOtroLlantaMismaVenta == 2:
            dimensionVentas, acumuladoVentas = 0 , 0
            while dimensionVentas < len(DiccionarioVentas[folio]):
                aculumador = (float(DiccionarioVentas[folio][dimensionVentas].precioVenta) * int(DiccionarioVentas[folio][dimensionVentas].cantidadVenta))
                acumuladoVentas =  aculumador + acumuladoVentas
                dimensionVentas += 1
            print(separador)
            print('Subtotal: ${:.2f}'.format(acumuladoVentas),'\nIVA:','${:.2f}'.format(acumuladoVentas * .16))
            print('-' * 16,'\n\nTotal: ${:.2f}'.format(acumuladoVentas*1.16, 2),f'\nVenta realizada el: {fecha}\n')
            print(separador)
            break

while True:
    opcionElegida = Menu() # Manda a ejecutar menú y trae elección
    if int(opcionElegida) == 1:
        RegistrarVenta()
    """if int(opcionElegida) == 2:
        ConsultarVenta()"""
    if int(opcionElegida) == 3:
        break