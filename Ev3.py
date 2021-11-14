# Evidencia 3, Estructura de datos y su procesamiento.

from collections import namedtuple
#import os
import sys
import sqlite3
from sqlite3 import Error

Venta = namedtuple('Ventas', ('descripcion', 'cantidadVenta', 'precioVenta', 'fechaVenta'))
DiccionarioVentas = {}
ListaVentas = []
separador = ('-' * 45)
subtotal = 0
# numFila = 1

print('Bienvenido(a) al negocio de ventas de cosméticos')
print(separador)

def Menu():
    opcion = int(input('Menú de opciones:\n[1] Registrar una venta\n[2] Consultar una venta\n[3] Reporte de ventas de fecha\n[4] Salir y guardar en base de datos (.db)\n» '))
    return opcion

def RegistrarVenta():
    ListaVentas=[] # Limpieza de la lista
    print('\n--------- Registro de venta ---------')

    fecha = input('Introduzca la fecha de venta (ej. 10/10/2021)\n» ')
    while True:
        folio = int(input(f'Introduzca folio de venta de Cosmetico(s)\n» '))

        if folio in DiccionarioVentas.keys():
            print('Error, ya existe una venta con ese folio de venta')
        else:
            break

    while True:
        descripcion = input('Introduzca descripción del tipo de Cosmetico\n» ')
        cantidadVenta = int(input('Introduzca cantidad a vender del tipo de Cosmetico mencionado\n» '))
        precioVenta = float(input('Introduzca precio (sin iva) del tipo de Cosmetico (por unidad)\n» $'))
        print(separador)
        subtotal = (cantidadVenta * precioVenta)
        print(f'Subtotal (sin iva) de las Cosmetico tipo {descripcion}:','${:.2f}'.format(subtotal))
        print(separador)
        organizacionVenta = Venta(descripcion,cantidadVenta, precioVenta, fecha)
        ListaVentas.append(organizacionVenta)
        DiccionarioVentas[folio] = ListaVentas
        agregaOtroCosmeticoMismaVenta = int(input('¿Desea agregar otra(s) venta(s) de Cosmetico(s) a la misma venta?\n[1] Si \n[2] No\n» '))

        if agregaOtroCosmeticoMismaVenta == 2:
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

def ConsultarVenta():
    consulta = int(input('Folio a consultar: '))
    dimension, totalVentas = 0 , 0

    if consulta in DiccionarioVentas.keys():

        while dimension < len(DiccionarioVentas[consulta]):
            print(separador)
            print(f'Descripción del tipo de Cosmetico: {DiccionarioVentas[consulta][dimension].descripcion}')
            print(f'Cantidad de llantas: {DiccionarioVentas[consulta][dimension].cantidadVenta}')
            print('Precio: ${:.2f}'.format(DiccionarioVentas[consulta][dimension].precioVenta, 2))
            print(f'Fecha: {DiccionarioVentas[consulta][dimension].fechaVenta}')
            totalVentas = (float(DiccionarioVentas[consulta][dimension].precioVenta) * float(DiccionarioVentas[consulta][dimension].cantidadVenta)) + totalVentas
            dimension += 1
        print(separador)
        print('Subtotal: ${:.2f}'.format(totalVentas),'\nIVA:','${:.2f}'.format(totalVentas * .16))
        print('-' * 16,'\n\nTotal: ${:.2f}\n'.format(totalVentas + totalVentas * .16, 2))
        print(separador)

    else:
        print('La clave no esta registrada')

def ReporteVentas():
    fechaBusqueda = input("Ingrese la fecha para encontrar las ventas de ese día (ej: dd/mm/yyyy)\n» ")
    encontroAlMenosUnDato = False
    Subtotal = 0
    GranTotalVenta = 0
    GranTotalVentasDiaSinIva = 0
    GranTotalVentasDiaConIva = 0

    for key, valor in DiccionarioVentas.items() :
        diferentesllantasDentroMismaVenta = len(valor)
        contador = 0
        while contador < diferentesllantasDentroMismaVenta:
            fechaExtraida = valor[contador].fechaVenta # Se evitó el [:-15] en "fechaVenta"

            if fechaBusqueda == fechaExtraida:

                if encontroAlMenosUnDato == False:
                    print("\nSe ha encontrado ventas del día",fechaBusqueda)
                    print("      Folio    |   Descripcion   |  Cantidad  |  Precio c/u  |    Fecha   |  Subtotal    |   IVA      |  Total")
                    encontroAlMenosUnDato = True # Temporal

            if fechaBusqueda == fechaExtraida:
                Subtotal = valor[contador].precioVenta*valor[contador].cantidadVenta
                IVA = (valor[contador].precioVenta*valor[contador].cantidadVenta)*.16
                GranTotalVenta = IVA + (valor[contador].precioVenta*valor[contador].cantidadVenta)
                print(f'\t{key:<6} | {valor[contador].descripcion:^15} | {valor[contador].cantidadVenta:^10} |   ${valor[contador].precioVenta:<9} | {valor[contador].fechaVenta[-10:]:<8} |   ${Subtotal:<9} |   ${IVA:<7} |  ${GranTotalVenta:<10}')
                GranTotalVentasDiaSinIva = GranTotalVentasDiaSinIva + (valor[contador].precioVenta*valor[contador].cantidadVenta)
                GranTotalVentasDiaConIva = GranTotalVentasDiaConIva + GranTotalVenta
            contador+= 1

    if encontroAlMenosUnDato == True:
        print("\nEl día", fechaBusqueda, " se vendió en total:",'${:.2f}'.format(GranTotalVentasDiaSinIva),"con iva:",'${:.2f}'.format(GranTotalVentasDiaConIva))    
    print("")

    if encontroAlMenosUnDato == False:
        print("Error, no se encuentra datos de esa fecha")

def GuardarSQL_Lite3():

    # Creación de Base de datos
    try:
        with sqlite3.connect("RegistroTiendallantas.db") as conn: #1 Establezco conexion
            c = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
            c.execute("CREATE TABLE IF NOT EXISTS Folios (folio INTEGER PRIMARY KEY NOT NULL, fecha TEXT NOT NULL);") #3 Envio instrucciones mediante el curosr
            c.execute("CREATE TABLE IF NOT EXISTS DescVentas (numDescripcion INTEGER PRIMARY KEY NOT NULL, descripcion TEXT NOT NULL, cantidad INTEGER NOT NULL, precio REAL NOT NULL, folio INTEGER NOT NULL, FOREIGN KEY (folio) REFERENCES Folios (folio));") #3 Envio instrucciones mediante el cursor
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()

    folioIndependiente = 0
    cuantosElementosTieneElFolio = 0
    numDescripcion = 0

    for key, valor in DiccionarioVentas.items():
        cuantosElementosTieneElFolio = len(valor)
        folio = key
        contador2 = 0
        fecha = valor[contador2].fechaVenta
        contador2 += 1

        # Guardado de folios y fechas de ventas
        try:
            with sqlite3.connect("RegistroTiendallantas.db") as conn: #1 Establezco conexion
                c = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
                c.execute("INSERT INTO Folios VALUES(?, ?)", (folio,fecha))
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()

        contador = 0
        while contador < cuantosElementosTieneElFolio:

            numDescripcion += 1
            descripcion = valor[contador].descripcion
            cantidad = valor[contador].cantidadVenta
            precio = valor[contador].precioVenta
            contador += 1 # Contador funcional para el while

            # Guardado de descripciones de ventas independientes
            try:
                with sqlite3.connect("RegistroTiendallantas.db") as conn: #1 Establezco conexion
                    c = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
                    c.execute("INSERT INTO DescVentas VALUES(?, ?, ?, ?, ?)", (numDescripcion,descripcion,cantidad,precio,folio))
            except Error as e:
                print(e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                if conn:
                    conn.close()
    print("---\nGracias por usar este programa, buen día.")

while True:
    opcionElegida = Menu()
    if opcionElegida == 1:
        RegistrarVenta()
    if opcionElegida == 2:
        ConsultarVenta()
    if opcionElegida == 3:
        ReporteVentas()
    if opcionElegida == 4:
        GuardarSQL_Lite3()
        break