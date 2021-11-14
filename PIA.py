# Producto Integrador de Aprendizaje, Estructura de datos y su procesamiento.

from collections import namedtuple
import sys
import sqlite3
from sqlite3 import Error
from datetime import date, datetime
import os.path
from os import path
import datetime

# Declaraciones iniciales
separador = ('-' * 45)

print('Bienvenido(a) al negocio de venta de llantas')
print(separador)

def creacionBD_PIA():
    if path.exists("BD_PIA.db") == False:
        # Creación de Base de datos con el Folio y Descripcion Ventas
        try:
            with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
                cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
                cursorPIA.execute("CREATE TABLE IF NOT EXISTS Folios (folio INTEGER PRIMARY KEY NOT NULL, fecha TEXT NOT NULL);") #3 Envio instrucciones mediante el curosr
                cursorPIA.execute("CREATE TABLE IF NOT EXISTS DescVentas (descripcion TEXT NOT NULL, cantidad INTEGER NOT NULL, precio REAL NOT NULL, folio INTEGER NOT NULL, FOREIGN KEY (folio) REFERENCES Folios (folio));") #3 Envio instrucciones mediante el cursor
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
                conn.close()
        print("No se identificó una base de datos, se creó (BD_PIA.db)")
        print(separador)
    else:
        print("Se identificó una base de datos (BD_PIA.db)")
        
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

    totalFinalUnitario = 0

    try:
        with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
            cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones

            while True:

                error3 = "Error #3 El folio ya existe"
                error4 = "Error #4 Introduzca un número mayor a 0"
                error5 = "Error #5 Lo introducido está vacío o contiene sólo espacios."
                error6 = "Error #6 intente con un número"

                # Sistema de obtención de fecha actual en sistema
                fecha = datetime.datetime.now()
                year = '{:02d}'.format(fecha.year)
                month = '{:02d}'.format(fecha.month)
                day = '{:02d}'.format(fecha.day)
                fecha = '{}/{}/{}'.format(day, month, year)
                print("Confirmación de fecha:",fecha)
                print(separador)

                # Sistema de validación de existencia de Folio de Venta (en BD)
                while True:
                    folioVenta = input("Ingrese el folio de la venta\n» ")
                    try:
                        int(folioVenta)
                        folioVenta = int(folioVenta)
                        if folioVenta > 0:
                            valor_folio = {"Folio":folioVenta} #Diccionario para evitar inyeccion de sql
                            cursorPIA.execute("SELECT folio FROM Folios WHERE folio = :Folio", valor_folio)
                            registro = cursorPIA.fetchall()
                            if registro:
                                print(error3)
                            else:
                                break
                        else:
                            print(error4)
                    except:
                        print(error6)

                # Mecanismo de inyección de datos a SQL en Folios
                folioVentaInt = int(folioVenta)
                valores_venta = {"folio":folioVentaInt, "fecha":fecha}
                #valores_articulo = {"descripcion":descripcion, "cant_pzs":cantidadVenta, "precio_unitario":precioVenta, "folio":Folio}
                cursorPIA.execute("INSERT INTO Folios VALUES(:folio, :fecha);", valores_venta)
                print(separador)

                while True: # While para varios productos en misma venta

                    # Sistema de obtención de descripción del producto
                    while True:
                        descripcion = input('Introduzca descripción del tipo de Llanta (Ej: Michelin)\n» ')
                        if descripcion and descripcion.strip():
                            break
                        else:
                            print(error5)

                    while True:
                        # Sistema de obtención de cantidad del producto
                        cantidadVenta = input('Introduzca cantidad a vender del tipo de llanta\n» ')
                        try:
                            int(cantidadVenta) # Validación TRY
                            if cantidadVenta and cantidadVenta.strip():
                                if int(cantidadVenta) > 0:
                                    break
                                else:
                                    print(error4)
                            else:
                                print(error5)
                        except:
                            print(error6)

                    # Sistema de obtención del precio del producto
                    while True:
                        precioVenta = input('Introduzca precio (sin iva) del tipo de llanta (por unidad)\n» $')
                        try:
                            int(precioVenta) # Validación TRY
                            if precioVenta and precioVenta.strip():
                                if int(precioVenta) > 0:
                                    break
                                else:
                                    print(error4)
                            else:
                                print(error5)
                        except:
                            print(error6)
                    
                    # Sistema temporal de almacenamiento de total
                    totalFinalUnitario = totalFinalUnitario + ( int(precioVenta) * int(cantidadVenta) )

                    # Mecanismo de inyección de datos a SQL en DescVentas
                    folioVentaInt = int(folioVenta)
                    valores_articulo = {"descripcion":descripcion, "cantidad":cantidadVenta, "precio":precioVenta, "folio":folioVentaInt}
                    cursorPIA.execute("INSERT INTO DescVentas VALUES(:descripcion, :cantidad, :precio, :folio);", valores_articulo)
                    print(separador)
                    pregunta = input("¿Quiere seguir registrando? (S/N)\n» ")
                    if pregunta == 'S':
                        print(separador)
                    else:
                        break
                print(separador)
                print('\nEl subtotal a pagar es » ${:.2f}'.format(totalFinalUnitario))
                print('El total a pagar es » ${:.2f}'.format(totalFinalUnitario+totalFinalUnitario*.16))

                break
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()


def ConsultarVenta():
    try:
        # original 2 >>>> with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
        with sqlite3.connect("BD_PIA.db",detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursorPIA = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
            while True:
                fechaAConsultar = input("Ingrese la fecha a buscar (ej: 14/11/2021)\n» ")
                fecha = datetime.datetime.now()
                year = '{:02d}'.format(fecha.year)
                month = '{:02d}'.format(fecha.month)
                day = '{:02d}'.format(fecha.day)
                fecha = '{}/{}/{}'.format(day, month, year)
                print("Confirmación de fecha actual del sistema:",fecha)

                if fechaAConsultar > fecha:
                    print("Error: La fecha no es valida, ingrese otra")
                else:
                    print("La fecha si fue valida")
                    
                    
                    
                    
                    
                    #try:
                    #with sqlite3.connect("ConFechas_timestamp.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                        # >>>>>>> original with sqlite3.connect("BD_PIA.db",detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("SELECT folio, fecha FROM Folios")
                    registros = mi_cursor.fetchall()
            
                    for folio, fecha in registros:
                        print(f"Clave = {folio}, tipo de dato {type(folio)}")
                        print(f"Fecha de registro = {fecha}, tipo de dato {type(fecha)}\n")
                        
                    """except sqlite3.Error as e:
                        print (e)
                    except Exception:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    finally:
                        if (conn):
                            conn.close()
                            print("Se ha cerrado la conexión")"""
                    
                    
                    
                    
                    
                    
                    #fecha_a_consultar = {"Fecha":fechaAConsultar}
                    #print("gg1")
                    #cursorPIA.execute("SELECT descripcion, cantidad, precio, folio FROM DescVentas WHERE folio = 1")
                    #cursorPIA.execute("SELECT descripcion, cantidad, precio, folio FROM DescVentas WHERE folio IN(SELECT folio FROM Folios WHERE fecha=:fechaAConsultar)","14/11/2021")
                    #cursorPIA.execute("SELECT folio FROM Folios WHERE folio = :Folio", valor_folio)
                    #valores_articulo = {"descripcion":descripcion, "cantidad":cantidadVenta, "precio":precioVenta, "folio":folioVentaInt}
                    #consulta = cursorPIA.fetchall()
                    #print(consulta)
                    break

    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()


while True:
    creacionBD_PIA()
    opcionElegida = Menu() # Manda a ejecutar menú y trae elección
    if int(opcionElegida) == 1:
        RegistrarVenta()
    if int(opcionElegida) == 2:
        ConsultarVenta()
    if int(opcionElegida) == 3:
        break