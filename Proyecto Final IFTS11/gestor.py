import sys
import os
from db import DB 
from registro import Cliente 
from turno import Turno 
from datetime import datetime, date, time 



def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_hora(hora_str):
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False


class GestorTurnos(object):

    def __init__(self):
        self.db_clientes = DB.crear_db_clientes()
        self.db_turnos = DB.crear_db_turnos()

        try:
            self.clientes = self.db_clientes.read()
            self.turnos = self.db_turnos.read()
            self.turnos.sort() 
            print(f"Sistema iniciado. {len(self.clientes)} clientes y {len(self.turnos)} turnos cargados desde CSV.")
        except Exception as e:
            print(f" Error al cargar datos: {e}. Iniciando con listas vacías.")
            self.clientes = []
            self.turnos = []



    def buscar_cliente(self, dni):
        for c in self.clientes:
            if hasattr(c, 'dni') and c.dni == dni:
                return c
        return None

    def existe_turno_en(self, fecha, hora, turno_excluir=None):
        for t in self.turnos:
            if t.fecha == fecha and t.hora == hora and t != turno_excluir:
                return True
        return False


    def registrar_cliente(self):
        print("\n--- 1. Registrar nuevo cliente ---")

        dni = input("DNI: ").strip()
        
        if self.buscar_cliente(dni):
            print(" Error: Ya existe un cliente con ese DNI.")
            return

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()

        nuevo_cliente = Cliente(dni=dni, nombre=nombre, apellido=apellido)

        if not nuevo_cliente.validar():
            print(" Error: Datos de cliente inválidos (ej. DNI no tiene 8 dígitos o falta el nombre).")
            return
            
        self.clientes.append(nuevo_cliente)
        print(" Cliente registrado.")
        
        self.guardar_datos()
        
    def listar_clientes(self):
        print("\n--- 2. Lista de clientes ---")
        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for i, c in enumerate(self.clientes):
            print(f"{i + 1}) DNI: {getattr(c, 'dni', 'N/A')} - {c.nombre_completo()}")


    # TURNOS 
    def solicitar_turno(self):
        print("\n--- 3. Solicitar turno ---")

        dni = input("DNI del cliente: ").strip()
        cliente = self.buscar_cliente(dni)

        if not cliente:
            print(" Error: El cliente no existe.")
            return
            
        fecha = input("Fecha (DD/MM/AAAA): ").strip()
        if not validar_fecha(fecha):
            print(" Fecha inválida (formato DD/MM/AAAA).")
            return

        hora = input("Hora (HH:MM): ").strip()
        if not validar_hora(hora):
            print(" Hora inválida (formato HH:MM).")
            return

        if self.existe_turno_en(fecha, hora):
            print(" Ya existe un turno en esa fecha y horario. Pruebe otra hora.")
            return

        nuevo_turno = Turno(dni=dni, fecha=fecha, hora=hora, servicio='Corte') 
        
        if not nuevo_turno.validar():
             print(" Error interno de validación de turno.")
             return

        self.turnos.append(nuevo_turno)
        self.turnos.sort() 
        print(f"Turno registrado para {cliente.nombre_completo()} el {fecha} a las {hora}.")
        
        self.guardar_datos()


    def listar_turnos(self):
        print("\n--- 4. Lista de turnos ---")

        if not self.turnos:
            print("No hay turnos cargados.")
            return
        
        for i, t in enumerate(self.turnos):
            cliente = self.buscar_cliente(getattr(t, 'dni', ''))
            nombre = cliente.nombre_completo() if cliente else "CLIENTE NO REGISTRADO"
            
            print(f"{i + 1}) Fecha: {t.fecha} | Hora: {t.hora} | Cliente: {nombre} (DNI: {getattr(t, 'dni', 'N/A')})")


    # MODIFICAR Y CANCELAR 
    def modificar_turno(self):
        print("\n--- 5. Modificar turno ---")

        if not self.turnos:
            print("No hay turnos registrados.")
            return

        self.listar_turnos()

        try:
            opcion = int(input("Seleccione número de turno: "))
            if opcion < 1 or opcion > len(self.turnos):
                print(" Opción inválida.")
                return
        except ValueError:
            print(" Debe ingresar un número.")
            return

        turno = self.turnos[opcion - 1]
        modificado = False

        print("\nTurno seleccionado:", turno) 
        print("\n¿Qué desea modificar?")
        print("1) Fecha")
        print("2) Hora")
        print("3) DNI del Cliente")
        print("0) Cancelar")

        eleccion = input("Opción: ")

        if eleccion == "1":
            nueva_fecha = input("Nueva fecha (DD/MM/AAAA): ").strip()
            if validar_fecha(nueva_fecha) and not self.existe_turno_en(nueva_fecha, turno.hora, turno):
                turno.fecha = nueva_fecha
                turno.validar() 
                self.turnos.sort() 
                print(" Fecha modificada.")
                modificado = True
            else:
                print(" Fecha inválida o ya existe un turno a esa hora.")

        elif eleccion == "2":
            nueva_hora = input("Nueva hora (HH:MM): ").strip()
            if validar_hora(nueva_hora) and not self.existe_turno_en(turno.fecha, nueva_hora, turno):
                turno.hora = nueva_hora
                turno.validar() 
                self.turnos.sort() 
                print(" Hora modificada.")
                modificado = True
            else:
                print(" Hora inválida o ya existe un turno en esa fecha.")

        elif eleccion == "3":
            nuevo_dni = input("Nuevo DNI: ").strip()
            if self.buscar_cliente(nuevo_dni):
                turno.dni = nuevo_dni
                print("DNI modificado.")
                modificado = True
            else:
                print("DNI inválido. El cliente debe estar registrado.")
        
        elif eleccion == "0":
            print("Modificación cancelada.")

        else:
            print(" Opción inválida.")
        
        if modificado:
            self.guardar_datos()


    def cancelar_turno(self):
        print("\n--- 6. Cancelar turno ---")

        if not self.turnos:
            print("No hay turnos registrados.")
            return

        self.listar_turnos()

        try:
            opcion = int(input("Seleccione número de turno a cancelar: "))
            if opcion < 1 or opcion > len(self.turnos):
                print(" Opción inválida.")
                return
        except ValueError:
            print(" Debe ingresar un número.")
            return

        eliminado = self.turnos.pop(opcion - 1)
        print(f"Turno eliminado: {eliminado.fecha} {eliminado.hora} - {getattr(eliminado, 'dni', 'N/A')}")
        
        self.guardar_datos()


    # GUARDAR 


    def guardar_datos(self):
        
        try:
            self.db_clientes.write(self.clientes)
            self.db_turnos.write(self.turnos)

            self.clientes = self.db_clientes.read()
            self.turnos = self.db_turnos.read()
            self.turnos.sort() 

            print(" Datos guardados correctamente.")
        except Exception as e:
            print(f" Error al guardar/sincronizar datos: {e}")
            


    # MENU PRINCIPAL
    def mostrar_menu(self):
        while True:
            print("\n========== SISTEMA DE TURNOS ==========")
            print("1. Registrar cliente")
            print("2. Listar clientes")
            print("3. Solicitar turno")
            print("4. Listar turnos")
            print("5. Modificar turno")
            print("6. Cancelar turno")
            print("7. Guardar datos ")
            print("8. Salir")

            op = input("Opción: ")

            if op == "1": self.registrar_cliente()
            elif op == "2": self.listar_clientes()
            elif op == "3": self.solicitar_turno()
            elif op == "4": self.listar_turnos()
            elif op == "5": self.modificar_turno()
            elif op == "6": self.cancelar_turno()
            elif op == "7": self.guardar_datos()
            elif op == "8":
                print("Cerrando")
                self.guardar_datos() 
                break
            else:
                print(" Opción no válida muñeco.")
