import os 
from transforma import Transforma 
from registro import Cliente, Registro 
from turno import Turno 

class DB(object):
    
    def __init__(self, filename, tipo_registro=None):
        self.filename = os.path.join("datos", filename) 
        self.tipo_registro = tipo_registro or Registro
        self._ensure_data_dir() 

    def _ensure_data_dir(self):
        if not os.path.exists("datos"):
            os.makedirs("datos")

    def read(self):
        db = []
        try:
            file = open(self.filename, "rt", encoding="utf-8")
        except FileNotFoundError:
            return db 

        line = file.readline().strip()
        if not line:
            file.close()
            return db
            
        keys = line.split(",")
        tran = Transforma(keys, self.tipo_registro)
        
        line = file.readline()
        while line: 
            values = line.strip().split(",")
            obj = tran.toObject(values)
            
            if obj: 
                db.append(obj)
                
            line = file.readline()
            
        file.close()
        return db

    def write(self, registros):
        if not registros:
            keys = []
        else:
            keys = [k for k in registros[0].__dict__.keys() if not k.startswith('_') and k not in ['dt_fecha_hora', 'clave_unica']]

        try:
            with open(self.filename, "wt", encoding="utf-8") as file:
                file.write(",".join(keys) + "\n")

                for r in registros:
                    fila = []
                    for k in keys:
                        # Usa getattr para obtener el valor del atributo
                        valor = str(getattr(r, k, "")) 
                        fila.append(valor)
                    file.write(",".join(fila) + "\n")
        except Exception as e:
            print(f" Error al escribir el archivo {self.filename}: {e}")

    @classmethod
    def crear_db_clientes(cls, filename="clientes.csv"):
        return cls(filename, Cliente)

    @classmethod
    def crear_db_turnos(cls, filename="turnos.csv"):
        return cls(filename, Turno)