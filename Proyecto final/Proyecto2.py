# CLASE PRESENCIAL
class Transforma(object):
    def __init__(self, atributos):
        self.keys = atributos

    def toDict(self, values):
        # Verifica que la cantidad de valores coincida con la cantidad de claves
        if len(values) != len(self.keys):
            return None
        
        d = {}
        i = 0
        
        # Itera sobre los valores usando un índice
        while i < len(values):
            # Asigna el valor al diccionario usando la clave correspondiente
            d[self.keys[i]] = values[i]
            i = i + 1
            
        return d
    
class DB(object):
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        file = open(self.filename, "rt")
        line = file.readline() #Leo encabezado
        db = []
        if line == "":
            return []
        keys = line.split(",")
        tran = Transforma(keys)
        line = file.readline()
        while line != "":
            values = line.split(",")
            d = tran.toDict(values)
            db.append(d)
            line = file.readline()
        file.close()
        return db

    def write (self, registros):
        pass

db = DB("db.csv")  
registros = db.read()
print(registros) 

i = 0 
while i < len(registros):
    print("Nombre: ", registros[i]["nombre"])
    i = i + 1