def carga_archivo(archivo):
        #Carga y lectura del archivo clientes
        archivo_clientes = open("clientes.csv", "rt")#lee linea 0
        llaves_clientes = archivo_clientes.readline()
        clientes = Transformador(llaves_clientes)
        lista_clientes = []
        
        line_cli = archivo_clientes.readline() #lee linea con valores
        while line.cli != "": #mientras uqe la linea no este vacia hacer lo que esta a contiunuacion 
            if line_cli = "\n": #saltar si la linea esta vacio 
                line_cli = archivo_clientes.readline()
                continue
            d = cliente.str2dict(line_cli)
            lista_clientes.append(d)
            line_cli = archivo_clientes.readline()
        archivo_clientes.close

class GestorTurnos(object):

    def __init__(self,cliente, otra, nose):
         self.cliente = carga_archivo(cliente)
         self.otra = carga_archivo(otra)
         self.nose = carga_archivo(nose)
#carga 

    def registrar_cliente(self):
         nuevo = self.cliente.ingresar_valores()
         self.lista_clientes.append(nuevo)  
         print("Cliente registrado correctamente")
    
    
    def registar_nuevo_empleado(self):
         nuevo = self.empleado.ingresar_valores()
         self.lista_empleados.append(nuevo)


    def solicitar_turno(self):
         print("Solicitando turno")

    def listar_turnos(self):
         print("Se listan turnos")

    def modificar_turno(self):
        print("Se modifica turno existente")
    
    def cancelar_turno(self):
         print("Se cancela turno")
    
    def guardar_datos(self):
        print("Se guardaron datos en archivo CSV")

    #Menú 

    def mostrar_menu(self):
        print("**********************************************")
        print("SISTEMA DE GESTIÓN DE TURNOS")
        print("**********************************************")
        print("----------------------------------------------")
        print("MENÚ PRINCIPAL")
        print("----------------------------------------------")

gt = GestorTurnos("cliente.csv", "asdsadsad", "")
