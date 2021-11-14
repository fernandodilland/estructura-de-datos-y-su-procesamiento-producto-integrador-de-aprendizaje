# Producto Integrador de Aprendizaje, Estructura de datos y su procesamiento.

from collections import namedtuple
import sys
import sqlite3
from sqlite3 import Error
from datetime import date, datetime
import os.path
from os import path

# Declaraciones iniciales
separador = ('-' * 45)

print('Bienvenido(a) al negocio de venta de llantas')
print(separador)

def creacionBD_PIA():
    if path.exists("BD_PIA.db") == False:
        # Creación de Base de datos con el Folio y Descripcion Ventas
        try:
            with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
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
    
    
    
    
    
    
    try:
        with sqlite3.connect("BD_PIA.db") as conn: #1 Establezco conexion
            c = conn.cursor() #2 Creo cursor que viajara por la conexion llevando instrucciones
            c.execute("SELECT * FROM Cliente")
            registros = c.fetchall()
            
            if registros:
                print("Clientes\n")
                print("id \t Nombre \t Apellidos")
                print("*" * 40)
                for id_cliente, nombre, apellidos in registros:
                    print(f"{id_cliente}\t{nombre}\t{apellidos}")
                print()
                print("*" * 40)
                    
            c.execute("SELECT * FROM Vendedor")
            registros = c.fetchall()
            if registros:
                print("Vendedores\n")
                print("id \t Nombre \t Apellidos")
                print("*" * 40)
                for id_vendedor, nombre, apellidos in registros:
                    print(f"{id_vendedor}\t{nombre}\t{apellidos}")
                print()
                print("*" * 40)
                
            while True:
                
                folio = int(input("Inserte el folio de la venta: "))
                print("*" * 50)
                
                while True:
                    fecha = input("Fecha de la venta: ")
                    fecha_capturada = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
                    fecha_actual = datetime.date.today()
                    
                    if fecha_capturada > fecha_actual:
                        print("La fecha capturada no es válida. Ingrese una fecha menor o igual a la fecha actual.")
                        print("*" * 50)
                    else:
                        print("*" * 50)
                        break
                        
                        
                    
                while True:
                    cliente = int(input("Ingrese el id del cliente: "))
                    valor_cliente = {"id_cliente":cliente} #Diccionario para evitar inyeccion de sql
                    c.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = :id_cliente", valor_cliente)
                    registro = c.fetchall()
                    if registro:
                        print("*" * 50)
                        break
                    else:
                        print("El id del cliente no existe. Ingresar un id válido.")
                        print("*" * 50)
                    
                
                while True:
                    vendedor = int(input("Ingrese id del vendedor: "))
                    valor_vendedor = {"id_vendedor":vendedor}
                    c.execute("SELECT id_vendedor FROM Vendedor WHERE id_vendedor = :id_vendedor", valor_vendedor)
                    registro = c.fetchall()
                    if registro:
                        print("*" * 50)
                        break
                    else:
                        print("El id del vendedor no existe. Ingresar un id válido.")
                        print("*" * 50)
                    
                    
                valores_venta = {"folio":folio, "fecha":fecha, "id_cliente":cliente, "id_vendedor":vendedor}
                
                c.execute(f"INSERT INTO Venta VALUES(:folio, :fecha, :id_cliente, :id_vendedor);", valores_venta)
                
                print("*" * 50)
                print("Venta inicializada.")
                print("*" * 50)
                    
                while True:
                    descripcion = input("Ingrese una descripción para el artículo: ")
                    print("*" * 50)
                    
                    while True:
                        cant_pzs = int(input("Ingrese la cantidad de piezas: "))
                        if cant_pzs > 0:
                            print("*" * 50)
                            break
                        else:
                            print("Ingresa una cantidad de piezas mayor a cero para continuar.")
                            print("*" * 50)
                    
                    while True:
                        precio_unitario = float(input("Ingrese el precio unitario: "))
                        if precio_unitario > 0:
                            print("*" * 50)
                            break
                        else:
                            print("Ingresa un precio unitario mayor a cero para continuar.")
                            print("*" * 50)
                            
                    valores_articulo = {"descripcion":descripcion, "cant_pzs":cant_pzs, "precio_unitario":precio_unitario, "folio":folio}
                    
                    c.execute("INSERT INTO Venta_detalles VALUES(:descripcion, :cant_pzs, :precio_unitario, :folio);", valores_articulo)
                    
                    print("*" * 50)
                    pregunta = input("¿Quiere seguir registrando? (S/N): ").upper()
                    
                    if pregunta == 'S':
                        print("*" * 50)
                    else:
                        break
                break
                        
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if conn:
            conn.close()
    
    
    
    
    
def ConsultarVenta():
    pass
    
    
    """ListaVentas=[]
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
        organizacionVenta = Venta(descripcion,cantidadVenta, precioVenta, fecha)
        ListaVentas.append(organizacionVenta)
        DiccionarioVentas[folio] = ListaVentas
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
            break"""

while True:
    creacionBD_PIA()
    opcionElegida = Menu() # Manda a ejecutar menú y trae elección
    if int(opcionElegida) == 1:
        RegistrarVenta()
    if int(opcionElegida) == 2:
        ConsultarVenta()
    if int(opcionElegida) == 3:
        break